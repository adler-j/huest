"""Create the cross-section tables needed by GPUMCI."""

import numpy as np
import xraylib as xrl
import os
import sys

__all__ = ('hounsfield_value', 'density')


class Silence:
    """Context manager to silence C output that xraylib spams."""
    def __enter__(self):
        # save previous stdout/stderr
        self.saved_streams = sys.__stdout__, sys.__stderr__
        self.fds = fds = [s.fileno() for s in self.saved_streams]
        self.saved_fds = map(os.dup, fds)
        # flush any pending output
        for s in self.saved_streams:
            s.flush()

        # open surrogate files
        null_streams = [open(f, 'w', 0) for f in [os.devnull, os.devnull]]
        self.null_fds = [s.fileno() for s in null_streams]
        self.null_streams = null_streams

        # overwrite file objects and low-level file descriptors
        map(os.dup2, self.null_fds, fds)

    def __exit__(self, *args):
        # flush any pending output
        for s in self.saved_streams:
            s.flush()
        # restore original streams and file descriptors
        map(os.dup2, self.saved_fds, self.fds)
        sys.stdout, sys.stderr = self.saved_streams
        # clean up
        for s in self.null_streams:
            s.close()
        for fd in self.saved_fds:
            os.close(fd)
        return False


def hounsfield_value(formula, density, energies, spectrum=None):
    """Compute hounsfield value from formula and density.

    Parameters
    ----------
    formula : `str`
        Formula for the material, i.e. 'H2O' or a NIST name.
        See `xraylib.GetCompoundDataNISTList()` for a list of valid names.
    density : float
        Density of the material
    energies : float or array-like
        The energy or energies that should be used. Measured in kilo-Volt.
    spectrum : float or array-like
        Relative weights of each energy in energies.
    """
    formula = str(formula)
    density = float(density)
    energies = np.array(energies, ndmin=1, dtype='float')

    if spectrum is None:
        spectrum = np.ones_like(energies)
    else:
        spectrum = np.array(spectrum, ndmin=1, dtype='float')
        if spectrum.shape != energies.shape:
            raise ValueError('shape of `energies` and `spectrum` should match')
    spectrum /= spectrum.sum()

    with Silence():
        attenuation = np.array([xrl.CS_Total_CP(formula, energy)
                                for energy in energies])

    if np.any(attenuation == 0):
        raise ValueError('invalid formula')

    with Silence():
        attenuation_water = np.array([xrl.CS_Total_CP('Water, Liquid', energy)
                                      for energy in energies])

    mean_att = np.sum(attenuation * spectrum)
    mean_water_att = np.sum(attenuation_water * spectrum)

    return (density * mean_att / mean_water_att - 1.0) * 1000.0


def density(formula, hu_value, energies, spectrum=None):
    """Compute density value from formula and hu_value.

    Parameters
    ----------
    formula : `str`
        Formula for the material, i.e. 'H2O' or a NIST name.
        See `xraylib.GetCompoundDataNISTList()` for a list of valid names.
    hu_value : float
        HU value of the material
    energies : float or array-like
        The energy or energies that should be used. Measured in kilo-Volt.
    spectrum : float or array-like
        Relative weights of each energy in energies.
    """
    formula = str(formula)
    hu_value = float(hu_value)
    energies = np.array(energies, ndmin=1, dtype='float')

    if spectrum is None:
        spectrum = np.ones_like(energies)
    else:
        spectrum = np.array(spectrum, ndmin=1, dtype='float')
        if spectrum.shape != energies.shape:
            raise ValueError('shape of `energies` and `spectrum` should match')
    spectrum /= spectrum.sum()

    attenuation = np.array([xrl.CS_Total_CP(formula, energy)
                            for energy in energies])

    if np.any(attenuation == 0):
        raise ValueError('invalid formula')

    attenuation_water = np.array([xrl.CS_Total_CP('Water, Liquid', energy)
                                  for energy in energies])

    mean_att = np.sum(attenuation * spectrum)
    mean_water_att = np.sum(attenuation_water * spectrum)

    return (mean_water_att / mean_att) * (hu_value + 1000.0) / 1000.0
