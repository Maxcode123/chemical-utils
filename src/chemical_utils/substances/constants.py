from chemical_utils.substances.substance import ChemicalElement, ChemicalCompound

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
    "WATER",
    "CARBON_MONOXIDE",
    "CARBON_DIOXIDE",
    "METHANE",
]


HYDROGEN = ChemicalElement(1, 1.0080, "H")
HELIUM = ChemicalElement(2, 4.00260, "He")
LITHIUM = ChemicalElement(3, 7.0, "Li")
BERYLLIUM = ChemicalElement(4, 9.012183, "Be")
BORON = ChemicalElement(5, 10.81, "B")
CARBON = ChemicalElement(6, 12.011, "C")
NITROGEN = ChemicalElement(7, 14.007, "N")
OXYGEN = ChemicalElement(8, 15.999, "O")
FLUORINE = ChemicalElement(9, 18.99840316, "F")
NEON = ChemicalElement(10, 20.180, "Ne")
SODIUM = ChemicalElement(11, 22.9897693, "Na")
MAGNESIUM = ChemicalElement(12, 24.305, "Mg")
ALUMINUM = ChemicalElement(13, 26.981538, "Al")
SILLICON = ChemicalElement(14, 28.085, "Si")
PHOSPHORUS = ChemicalElement(15, 30.97376200, "P")
SULFUR = ChemicalElement(16, 32.07, "S")
CHLORINE = ChemicalElement(17, 35.45, "Cl")
ARGON = ChemicalElement(18, 39.9, "Ar")
POTASSIUM = ChemicalElement(19, 39.0983, "K")
CALCIUM = ChemicalElement(20, 40.08, "Ca")
SCANDIUM = ChemicalElement(21, 44.95591, "Sc")
TITANIUM = ChemicalElement(22, 47.867, "Ti")
VANADIUM = ChemicalElement(23, 50.9415, "V")
CHROMIUM = ChemicalElement(24, 51.996, "Cr")
MANGANESE = ChemicalElement(25, 54.93804, "Mn")
IRON = ChemicalElement(26, 55.84, "Fe")
COBALT = ChemicalElement(27, 58.93319, "Co")
NICKEL = ChemicalElement(28, 58.693, "Ni")
COPPER = ChemicalElement(29, 63.55, "Cu")
ZINC = ChemicalElement(30, 65.4, "Zn")
GALLIUM = ChemicalElement(31, 69.723, "Ga")
GERMANIUM = ChemicalElement(32, 72.63, "Ge")
ARSENIC = ChemicalElement(33, 74.92159, "As")
SELENIUM = ChemicalElement(34, 78.97, "Se")
BROMINE = ChemicalElement(35, 79.90, "Br")
KRYPTON = ChemicalElement(36, 83.80, "Kr")
RUBIDIUM = ChemicalElement(37, 85.468, "Rb")
STRONTIUM = ChemicalElement(38, 87.62, "Sr")
YTRIUM = ChemicalElement(39, 88.90584, "Y")
ZITRONIUM = ChemicalElement(40, 91.22, "Zr")
NIOBIUM = ChemicalElement(41, 92.90637, "Nb")
MOLYBDENIUM = ChemicalElement(42, 95.95, "Mo")
TECHNETIUM = ChemicalElement(43, 96.90636, "Tc")
RUTHENIUM = ChemicalElement(44, 101.1, "Ru")
RHODIUM = ChemicalElement(45, 102.9055, "Rh")
PALLADIUM = ChemicalElement(46, 106.42, "Pd")
SILVER = ChemicalElement(47, 107.868, "Ag")
CADMIUM = ChemicalElement(48, 112.41, "Cd")
INDIUM = ChemicalElement(49, 114.818, "In")
TIN = ChemicalElement(50, 118.71, "Sn")
ANTIMONY = ChemicalElement(51, 121.760, "Sb")
TELLURIUM = ChemicalElement(52, 127.6, "Te")
IODINE = ChemicalElement(53, 126.9045, "I")
XENON = ChemicalElement(54, 131.29, "Xe")
CESIUM = ChemicalElement(55, 132.9054520, "Cs")
BARIUM = ChemicalElement(56, 137.33, "Ba")
HAFNIUM = ChemicalElement(72, 178.49, "Hf")
TANTALUM = ChemicalElement(73, 180.9479, "Ta")

HYDROGEN2 = ChemicalCompound(HYDROGEN * 2)
WATER = ChemicalCompound(HYDROGEN * 2, OXYGEN)
CARBON_MONOXIDE = ChemicalCompound(CARBON, OXYGEN)
CARBON_DIOXIDE = ChemicalCompound(CARBON, OXYGEN * 2)
METHANE = ChemicalCompound(CARBON, HYDROGEN * 4)
# NOTE: don't forget to add the compound to the __all__ list
