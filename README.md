# huest

HoUnsfield ESTimate, a package for estimation of hounsfield values given material compositions.

Includes functionality for

* Computing HU value from a given material composition and a density
* Computing the density from a given material composition

# Dependencies

Uses [xraylib](https://github.com/tschoonj/xraylib) in order to find the attenuation coefficients by the material.

# Installation

Clone the repository and run (in the root folder of the repository)

    pip install -e .

# Examples

Compute HU value of water

    >>> import huest
    >>> density = 1.0  # g / cm^3
    >>> energy = 0.05  # kilovolt
    >>> huest.hounsfield_value('Water, Liquid', density, energy)
    0.0

Compute the HU value of bone with a given energy spectrum

    >>> import huest
    >>> density = 1.0  # g / cm^3
    >>> energies = [0.02, 0.04, 0.06, 0.08]  # kilovolt
    >>> spectrum = [1, 2, 2, 1]  # relative density of each energy
    >>> huest.hounsfield_value('Bone, Cortical (ICRP)', density, energies, spectrum)
    0.0