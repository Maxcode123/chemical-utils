from chemical_utils.substances.substance import (
    ChemicalElement,
    ChemicalElementTuple,
    ChemicalCompound,
)
from chemical_utils.reactions.reaction import r
from chemical_utils.properties.registry import (
    create_standard_formation_properties,
    create_standard_entropy,
    create_thermal_capacity_coefficients,
)
from chemical_utils.properties.properties import MolarEnergy, Entropy
from chemical_utils.properties.coefficients import ThermalCapacityCoefficient

TESTIUM = ChemicalElement(10, 17.32, "Ts")
TESTIUM2 = ChemicalElementTuple(TESTIUM, 2)
PYTHONIUM = ChemicalElement(11, 23.09, "Py")
PYTHONIUM3 = ChemicalElementTuple(PYTHONIUM, 3)
ANACONDIUM = ChemicalElement(12, 29, "An")
TS_PY = ChemicalCompound(TESTIUM, PYTHONIUM)
TS2_PY3 = ChemicalCompound(TESTIUM2, PYTHONIUM3)
TS_PY_AN = ChemicalCompound(TESTIUM, PYTHONIUM, ANACONDIUM)

create_standard_formation_properties(TESTIUM2, MolarEnergy(0), MolarEnergy(0))
create_standard_entropy(TESTIUM2, Entropy(50))
create_thermal_capacity_coefficients(
    TESTIUM2, ThermalCapacityCoefficient(A=5.34, B=0.0115, C=0, D=0)
)

create_standard_formation_properties(PYTHONIUM3, MolarEnergy(0), MolarEnergy(0))
create_standard_entropy(PYTHONIUM3, Entropy(45))
create_thermal_capacity_coefficients(
    PYTHONIUM3, ThermalCapacityCoefficient(A=8.22, B=0.00015, C=0.0000034, D=0)
)


create_standard_formation_properties(TS_PY, MolarEnergy(50), MolarEnergy(100))
create_standard_entropy(TS_PY, Entropy(100))
create_thermal_capacity_coefficients(
    TS_PY, ThermalCapacityCoefficient(A=10.34, B=0.00274, C=0, D=-195500)
)


create_standard_formation_properties(TS2_PY3, MolarEnergy(100), MolarEnergy(200))
create_standard_entropy(TS2_PY3, Entropy(200))
create_thermal_capacity_coefficients(
    TS2_PY3, ThermalCapacityCoefficient(A=6.60, B=0.00120, C=0, D=0)
)

reaction_1 = r(TESTIUM2 + PYTHONIUM3, TS2_PY3)
reaction_2 = r(TESTIUM + PYTHONIUM, TS_PY)
reaction_3 = r(4 * TESTIUM2 + 3 * PYTHONIUM3, TS2_PY3 + 6 * TS_PY)
