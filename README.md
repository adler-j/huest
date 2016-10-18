# huest

HoUnsfield ESTimate, a package for estimation of hounsfield values given material compositions.

Includes functionality for

* Computing HU value from a given material composition and a density
* Computing the density from a given material composition

# Installation

Simply run

    pip install huest

The library uses [xraylib](https://github.com/tschoonj/xraylib) in order to find the attenuation coefficients by the material.
This needs to be installed separately.

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

    >>> hu_value = 2000.0
    >>> energies = [40, 60, 80]
    >>> spectrum = [2, 2, 1]
    >>> density = huest.density('Bone, Cortical (ICRP)', hu_value, energies, spectrum)
    1.5922416669281303
