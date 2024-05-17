from typing import Optional, Dict, Any
from typing_extensions import TypeAlias

from chemical_utils.properties.properties import (
    Temperature,
    Pressure,
    MolarVolume,
    CriticalProperties,
    MolarEnergy,
    FormationProperties,
    Entropy,
)


def create_critical_properties(
    substance, temperature: Temperature, pressure: Pressure, volume: MolarVolume
) -> CriticalProperties:
    """
    Create the critical properties of a chemical substance.

    Existing critical properties can be overriden with this function.
    """
    _critical_properties[substance] = CriticalProperties(temperature, pressure, volume)
    return _critical_properties[substance]


def get_critical_properties(substance) -> Optional[CriticalProperties]:
    """
    Get the critical properties of a chemical substance. Returns None if the properties
    have not been created for the given substance.
    """
    return _critical_properties.get(substance, None)


def create_standard_formation_properties(
    substance,
    formation_enthalpy: MolarEnergy,
    formation_gibbs_energy: MolarEnergy,
) -> FormationProperties:
    """
    Create the standard (25 Celcius, 1 bar) formation properties of a chemical
    substance.

    Existing standard formation properties can be overriden with this function.
    """
    _standard_formation_properties[substance] = FormationProperties(
        formation_enthalpy, formation_gibbs_energy
    )
    return _standard_formation_properties[substance]


def get_standard_formation_properties(substance) -> Optional[FormationProperties]:
    """
    Get the standard (25 Celcius, 1 bar) formation properties of a chemical substance.
    Returns None if the properties have not been created for the given substance.
    """
    return _standard_formation_properties.get(substance, None)


def create_standard_entropy(substance, entropy: Entropy) -> Entropy:
    """
    Create the standard (25 Celcius, 1 bar) entropy of a chemical substance.

    Existing standard entropy can be overriden with this function.
    """
    _standard_entropies[substance] = entropy
    return _standard_entropies[substance]


def get_standard_entropy(substance) -> Optional[Entropy]:
    """
    Get the standard (25 Celcius, 1 bar) entropy of a chemical substance. Returns None
    if the entropy has not been created for the given substance.
    """
    return _standard_entropies.get(substance, None)


# ChemicalSubstance cannot be imported here because of circular import. Use this alias
# in this module.
ChemicalSubstanceAlias: TypeAlias = Any

_critical_properties: Dict[ChemicalSubstanceAlias, CriticalProperties] = {}

_standard_formation_properties: Dict[ChemicalSubstanceAlias, FormationProperties] = {}

_standard_entropies: Dict[ChemicalSubstanceAlias, Entropy] = {}
