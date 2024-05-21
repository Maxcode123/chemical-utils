from chemical_utils.substances.substance import (
    ChemicalElement,
    ChemicalElementTuple,
    ChemicalCompound,
)
from chemical_utils.reactions.reaction import r
from chemical_utils.properties.registry import (
    create_standard_formation_properties,
    create_standard_entropy,
)
from chemical_utils.properties.properties import MolarEnergy, Entropy

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
create_standard_formation_properties(PYTHONIUM3, MolarEnergy(0), MolarEnergy(0))
create_standard_entropy(PYTHONIUM3, Entropy(45))
create_standard_formation_properties(TS2_PY3, MolarEnergy(100), MolarEnergy(200))
create_standard_entropy(TS2_PY3, Entropy(200))

reaction_1 = r(TESTIUM2 + PYTHONIUM3, TS2_PY3)
reaction_2 = r(TESTIUM + PYTHONIUM, TS_PY)
