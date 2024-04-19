from chemical_utils.substances.substance import (
    ChemicalElement,
    ChemicalElementTuple,
    ChemicalCompound,
)

TESTIUM = ChemicalElement(10, 17.32, "Ts")
TESTIUM2 = ChemicalElementTuple(TESTIUM, 2)
PYTHONIUM = ChemicalElement(11, 23.09, "Py")
PYTHONIUM3 = ChemicalElementTuple(PYTHONIUM, 3)
ANACONDIUM = ChemicalElement(12, 29, "An")
TS_PY_AN = ChemicalCompound(TESTIUM, PYTHONIUM, ANACONDIUM)
