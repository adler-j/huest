import pytest
import huest


def test_water_named():
    assert huest.hounsfield_value('Water, Liquid', 1.0, 0.05) == 0.0


def test_water_formula():
    # Slight difference in formula
    assert abs(huest.hounsfield_value('H2O', 1.0, 0.05)) < 1


def test_dense_water():
    assert huest.hounsfield_value('Water, Liquid', 1.5, 0.05) == 500.0


def test_invalid_name():
    with pytest.raises(ValueError):
        huest.hounsfield_value('SOMETHING WEIRD', 1.5, 0.05)


if __name__ == '__main__':
    pytest.main([str(__file__.replace('\\', '/')), '-v'])
