from dataclasses import dataclass

from property_utils.properties import ValidatedProperty, Property, p
from property_utils.exceptions import PropertyValidationError
from property_utils.units import *  # pylint: disable=unused-wildcard-import


class Temperature(ValidatedProperty):
    """
    Temperature property with default units of Kelvin.
    """

    generic_unit_descriptor = AbsoluteTemperatureUnit
    default_units = KELVIN

    def validate_value(self, value: float) -> None:
        if p(value, self.unit) < p(0, KELVIN):
            raise PropertyValidationError(
                "cannot create a temperature with value less than absolute 0. "
            )


class Pressure(ValidatedProperty):
    """
    Pressure property with default units of bar.
    """

    generic_unit_descriptor = PressureUnit
    default_units = BAR

    def validate_value(self, value: float) -> None:
        if not value >= 0:
            raise PropertyValidationError(
                "cannot create a pressure with value less than 0. "
            )


class MolarVolume(ValidatedProperty):
    """
    Molar volume property with default units of m^3/kmol.
    """

    generic_unit_descriptor = LengthUnit**3 / AmountUnit
    default_units = METER**3 / KILO_MOL

    def validate_value(self, value: float) -> None:
        if not value >= 0:
            raise PropertyValidationError(
                "cannot create a volume with value less than 0. "
            )


@dataclass
class CriticalProperties:
    """
    Properties at the critical point of chemical substances.
    """

    temperature: Temperature
    pressure: Pressure
    volume: MolarVolume


class MolarEnergy(Property):
    """
    Molar energy property with default units of J/kmol.
    """

    default_units = JOULE / KILO_MOL


@dataclass
class FormationProperties:
    """
    Formation properties of chemical substances.
    """

    enthalpy: MolarEnergy
    gibbs_energy: MolarEnergy


class Entropy(ValidatedProperty):
    """
    Entropy property with default units of J/kmol/K.
    """

    generic_unit_descriptor = EnergyUnit / AmountUnit / AbsoluteTemperatureUnit
    default_units = JOULE / KILO_MOL / KELVIN

    def validate_value(self, value: float) -> None:
        if not value >= 0:
            raise PropertyValidationError("entropy must be bigger than 0. ")
