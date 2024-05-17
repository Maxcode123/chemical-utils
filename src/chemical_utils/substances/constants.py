from typing import Union, Optional, Iterable

from property_utils.units import *  # pylint: disable=unused-wildcard-import
from property_utils.units.descriptors import CompositeDimension

from chemical_utils.substances.substance import (
    ChemicalElement,
    ChemicalCompound,
    ChemicalCompoundComponent,
)
from chemical_utils.properties.properties import (
    Temperature,
    Pressure,
    MolarVolume,
    MolarEnergy,
    Entropy,
)
from chemical_utils.properties.registry import (
    create_critical_properties,
    create_standard_formation_properties,
    create_standard_entropy,
)

__all__ = [
    "HYDROGEN",
    "HELIUM",
    "LITHIUM",
    "BERYLLIUM",
    "BORON",
    "CARBON",
    "NITROGEN",
    "OXYGEN",
    "FLUORINE",
    "NEON",
    "SODIUM",
    "MAGNESIUM",
    "ALUMINUM",
    "SILLICON",
    "PHOSPHORUS",
    "SULFUR",
    "CHLORINE",
    "ARGON",
    "POTASSIUM",
    "CALCIUM",
    "SCANDIUM",
    "TITANIUM",
    "VANADIUM",
    "CHROMIUM",
    "MANGANESE",
    "IRON",
    "COBALT",
    "NICKEL",
    "COPPER",
    "ZINC",
    "GALLIUM",
    "GERMANIUM",
    "ARSENIC",
    "SELENIUM",
    "BROMINE",
    "KRYPTON",
    "RUBIDIUM",
    "STRONTIUM",
    "YTRIUM",
    "ZITRONIUM",
    "NIOBIUM",
    "MOLYBDENIUM",
    "TECHNETIUM",
    "RUTHENIUM",
    "RHODIUM",
    "PALLADIUM",
    "SILVER",
    "CADMIUM",
    "INDIUM",
    "TIN",
    "ANTIMONY",
    "TELLURIUM",
    "IODINE",
    "XENON",
    "CESIUM",
    "BARIUM",
    "HAFNIUM",
    "TANTALUM",
    "HYDROGEN2",
    "OXYGEN2",
    "WATER",
    "CARBON_MONOXIDE",
    "CARBON_DIOXIDE",
    "METHANE",
]


def _t(
    value: float, unit: Union[AbsoluteTemperatureUnit, RelativeTemperatureUnit] = KELVIN
) -> Temperature:
    return Temperature(value, unit)


def _p(value: float, unit: PressureUnit = BAR) -> Pressure:
    return Pressure(value, unit)


def _v(value: float, unit: CompositeDimension = METER**3 / KILO_MOL) -> MolarVolume:
    return MolarVolume(value, unit)


def _e(value: float, unit: CompositeDimension = JOULE / KILO_MOL) -> MolarEnergy:
    return MolarEnergy(value, unit)


def _s(value: float, unit: CompositeDimension = JOULE / KILO_MOL / KELVIN) -> Entropy:
    return Entropy(value, unit)


def _element(  # pylint: disable=too-many-arguments
    atomic_number: int,
    atomic_mass: float,
    symbol: str,
    critical_temperature: Optional[Temperature] = None,
    critical_pressure: Optional[Pressure] = None,
    critical_volume: Optional[MolarVolume] = None,
    standard_formation_enthalpy: MolarEnergy = _e(0),
    standard_formation_gibbs_energy: MolarEnergy = _e(0),
    standard_entropy: Optional[Entropy] = None,
) -> ChemicalElement:
    element = ChemicalElement(atomic_number, atomic_mass, symbol)

    if (
        critical_temperature is not None
        and critical_pressure is not None
        and critical_volume is not None
    ):
        create_critical_properties(
            element, critical_temperature, critical_pressure, critical_volume
        )

    create_standard_formation_properties(
        element, standard_formation_enthalpy, standard_formation_gibbs_energy
    )

    if standard_entropy is not None:
        create_standard_entropy(element, standard_entropy)

    return element


def _compound(  # pylint: disable=too-many-arguments
    components: Iterable[ChemicalCompoundComponent],
    critical_temperature: Optional[Temperature] = None,
    critical_pressure: Optional[Pressure] = None,
    critical_volume: Optional[MolarVolume] = None,
    standard_formation_enthalpy: Optional[MolarEnergy] = None,
    standard_formation_gibbs_energy: Optional[MolarEnergy] = None,
    standard_entropy: Optional[Entropy] = None,
) -> ChemicalCompound:
    compound = ChemicalCompound(*components)

    if (
        critical_temperature is not None
        and critical_pressure is not None
        and critical_volume is not None
    ):
        create_critical_properties(
            compound, critical_temperature, critical_pressure, critical_volume
        )

    if (
        standard_formation_enthalpy is not None
        and standard_formation_gibbs_energy is not None
    ):
        create_standard_formation_properties(
            compound, standard_formation_enthalpy, standard_formation_gibbs_energy
        )

    if standard_entropy is not None:
        create_standard_entropy(compound, standard_entropy)

    return compound


HYDROGEN = _element(1, 1.0080, "H")
HELIUM = _element(2, 4.00260, "He")
LITHIUM = _element(3, 7.0, "Li")
BERYLLIUM = _element(4, 9.012183, "Be")
BORON = _element(5, 10.81, "B")
CARBON = _element(6, 12.011, "C")
NITROGEN = _element(7, 14.007, "N")
OXYGEN = _element(8, 15.999, "O")
FLUORINE = _element(9, 18.99840316, "F")
NEON = _element(10, 20.180, "Ne")
SODIUM = _element(11, 22.9897693, "Na")
MAGNESIUM = _element(12, 24.305, "Mg")
ALUMINUM = _element(13, 26.981538, "Al")
SILLICON = _element(14, 28.085, "Si")
PHOSPHORUS = _element(15, 30.97376200, "P")
SULFUR = _element(16, 32.07, "S")
CHLORINE = _element(17, 35.45, "Cl")
ARGON = _element(18, 39.9, "Ar")
POTASSIUM = _element(19, 39.0983, "K")
CALCIUM = _element(20, 40.08, "Ca")
SCANDIUM = _element(21, 44.95591, "Sc")
TITANIUM = _element(22, 47.867, "Ti")
VANADIUM = _element(23, 50.9415, "V")
CHROMIUM = _element(24, 51.996, "Cr")
MANGANESE = _element(25, 54.93804, "Mn")
IRON = _element(26, 55.84, "Fe")
COBALT = _element(27, 58.93319, "Co")
NICKEL = _element(28, 58.693, "Ni")
COPPER = _element(29, 63.55, "Cu")
ZINC = _element(30, 65.4, "Zn")
GALLIUM = _element(31, 69.723, "Ga")
GERMANIUM = _element(32, 72.63, "Ge")
ARSENIC = _element(33, 74.92159, "As")
SELENIUM = _element(34, 78.97, "Se")
BROMINE = _element(35, 79.90, "Br")
KRYPTON = _element(36, 83.80, "Kr")
RUBIDIUM = _element(37, 85.468, "Rb")
STRONTIUM = _element(38, 87.62, "Sr")
YTRIUM = _element(39, 88.90584, "Y")
ZITRONIUM = _element(40, 91.22, "Zr")
NIOBIUM = _element(41, 92.90637, "Nb")
MOLYBDENIUM = _element(42, 95.95, "Mo")
TECHNETIUM = _element(43, 96.90636, "Tc")
RUTHENIUM = _element(44, 101.1, "Ru")
RHODIUM = _element(45, 102.9055, "Rh")
PALLADIUM = _element(46, 106.42, "Pd")
SILVER = _element(47, 107.868, "Ag")
CADMIUM = _element(48, 112.41, "Cd")
INDIUM = _element(49, 114.818, "In")
TIN = _element(50, 118.71, "Sn")
ANTIMONY = _element(51, 121.760, "Sb")
TELLURIUM = _element(52, 127.6, "Te")
IODINE = _element(53, 126.9045, "I")
XENON = _element(54, 131.29, "Xe")
CESIUM = _element(55, 132.9054520, "Cs")
BARIUM = _element(56, 137.33, "Ba")
HAFNIUM = _element(72, 178.49, "Hf")
TANTALUM = _element(73, 180.9479, "Ta")

HYDROGEN2 = _compound(
    [HYDROGEN * 2], _t(33.19), _p(13.13), _v(0.064147), _e(0), _e(0), _s(1.30571e5)
)
OXYGEN2 = _compound(
    [OXYGEN * 2], _t(154.58), _p(50.43), _v(0.0734), _e(0), _e(0), _s(2.05043e5)
)
WATER = _compound(
    [HYDROGEN * 2, OXYGEN],
    _t(647.096),
    _p(220.64),
    _v(0.0559472),
    _e(-24.1814e7),
    _e(-22.859e7),
    _s(1.88724e5),
)
CARBON_MONOXIDE = _compound(
    [CARBON, OXYGEN],
    _t(132.92),
    _p(34.99),
    _v(0.0944),
    _e(-11.053e7),
    _e(-13.715e7),
    _s(1.97556e5),
)
CARBON_DIOXIDE = _compound(
    [CARBON, OXYGEN * 2],
    _t(304.21),
    _p(73.38),
    _v(0.094),
    _e(-39.351e7),
    _e(-39.437e7),
    _s(2.13677e5),
)
METHANE = _compound(
    [CARBON, HYDROGEN * 4],
    _t(190.564),
    _p(45.99),
    _v(0.09861),
    _e(-7.452e7),
    _e(-5.049e7),
    _s(1.8627e5),
)
# NOTE: don't forget to add the compound to the __all__ list
