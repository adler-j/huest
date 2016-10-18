# huest

HoUnsfield ESTimate, a package for estimation of hounsfield values given material compositions.

Includes functionality for

* Computing HU value from a given material composition and a density
* Computing the density from a given material composition

# Installation

Simply run

    pip install huest

The library uses [xraylib](https://github.com/tschoonj/xraylib) in order to find the attenuation coefficients by the material.
This needs to be [installed separately](https://github.com/tschoonj/xraylib/wiki/Installation-instructions).

# Examples

Compute HU value of water

    >>> import huest
    >>> density = 1.0  # g / cm^3
    >>> energy = 50  # kilovolt
    >>> huest.hounsfield_value('Water, Liquid', density, energy)
    0.0

Compute the HU value of bone with a given energy spectrum

    >>> import huest
    >>> density = 1.92  # g / cm^3
    >>> energies = [40, 60, 80]  # kilovolt
    >>> spectrum = [2, 2, 1]  # relative density of each energy
    >>> huest.hounsfield_value('Bone, Cortical (ICRP)', density, energies, spectrum)
    2617.5413064730405

Can also be used to compute densities from HU values

    >>> import huest
    >>> hu_value = 2000.0
    >>> energies = [40, 60, 80]
    >>> spectrum = [2, 2, 1]
    >>> density = huest.density('Bone, Cortical (ICRP)', hu_value, energies, spectrum)
    1.5922416669281303

The full list of supported materials can be acquired from `xraylib`:

    >>> import xraylib
    >>> xraylib.GetCompoundDataNISTList()
    ['A-150 Tissue-Equivalent Plastic',
     ...,
     'Xylene']
     
Materials can also be given according to their stoichiometric composition. Note that water is not exactly `'H2O'`:

    >>> import huest
    >>> huest.hounsfield_value('H2O', 1, 50)
    0.10973551267046133
