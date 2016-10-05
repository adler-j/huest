"""Create the cross-section tables needed by GPUMCI."""

import numpy as np
import xraylib as xrl

__all__ = ('hounsfield_value',)


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
        The energy or energies that should be used
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
        assert spectrum.shape == energies.shape
    spectrum /= spectrum.sum()

    attenuation = np.array([xrl.CS_Total_CP(formula, energy)
                            for energy in energies])

    if np.any(attenuation == 0):
        raise ValueError('invalid formula')

    attenuation_water = np.array([xrl.CS_Total_CP('Water, Liquid', energy)
                                  for energy in energies])

    mean_att = np.sum(attenuation * spectrum)
    mean_water_att = np.sum(attenuation_water * spectrum)

    print(attenuation)
    print(attenuation_water)

    return (density * mean_att / mean_water_att - 1.0) * 1000.0
