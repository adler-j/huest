import pytest
import huest


# -- Hounsfield value --


def test_hounsfield_water_named():
    assert huest.hounsfield_value('Water, Liquid', 1.0, 50) == 0.0


def test_hounsfield_water_formula():
    # Slight difference in formula
    assert abs(huest.hounsfield_value('H2O', 1.0, 50)) < 1


def test_hounsfield_dense_water():
    assert huest.hounsfield_value('Water, Liquid', 1.5, 50) == 500.0


def test_hounsfield_invalid_name():
    with pytest.raises(ValueError):
        huest.hounsfield_value('SOMETHING WEIRD', 1.5, 50)


def test_hounsfield_spectrum():
    density = 1.92
    energies = [40, 60, 80]
    spectrum = [2, 2, 1]
    hu_value = huest.hounsfield_value('Bone, Cortical (ICRP)',
                                      density, energies, spectrum)

    # This should be large
    assert hu_value > 1000.0


def test_hounsfield_invalid_spectrum_size():
    density = 1.92
    energies = [40, 60, 80]
    spectrum = [2, 2]
    with pytest.raises(ValueError):
        huest.hounsfield_value('Bone, Cortical (ICRP)',
                               density, energies, spectrum)


def test_hounsfield_zero_density():
    assert huest.hounsfield_value('Fe', 0, 90) == -1000.0
    assert huest.hounsfield_value('Bone, Cortical (ICRP)', 0, 50) == -1000.0
    assert huest.hounsfield_value('Water, Liquid', 0, 50) == -1000.0


# -- Density --


def test_density_water_named():
    assert huest.density('Water, Liquid', 0.0, 50) == 1.0


def test_density_water_formula():
    # Slight difference in formula
    assert abs(huest.density('H2O', 1.0, 50) - 1.0) < 0.01


def test_density_dense_water():
    assert huest.density('Water, Liquid', 500.0, 50) == 1.5


def test_density_invalid_name():
    with pytest.raises(ValueError):
        huest.density('SOMETHING WEIRD', 1.5, 50)


def test_density_spectrum():
    hu_value = 2000.0
    energies = [40, 60, 80]
    spectrum = [2, 2, 1]
    density = huest.density('Bone, Cortical (ICRP)',
                            hu_value, energies, spectrum)

    # This should be large
    assert density > 1.0


def test_density_invalid_spectrum_size():
    density = 1.92
    energies = [40, 60, 80]
    spectrum = [2, 2]
    with pytest.raises(ValueError):
        huest.density('Bone, Cortical (ICRP)',
                      density, energies, spectrum)


def test_density_zero_density():
    assert huest.density('Fe', -1000.0, 90) == 0
    assert huest.density('Bone, Cortical (ICRP)', -1000.0, 50) == 0
    assert huest.density('Water, Liquid', -1000.0, 50) == 0


# -- Combinations --

def test_inverses_named():
    material = 'Water, Liquid'
    density = 1.05
    energies = [50, 60]
    spectrum = [1, 1]
    hu_value = huest.hounsfield_value(material, density, energies, spectrum)
    density_out = huest.density(material, hu_value, energies, spectrum)

    assert density_out == density


if __name__ == '__main__':
    pytest.main([str(__file__.replace('\\', '/')), '-v'])
