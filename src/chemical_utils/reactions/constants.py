from chemical_utils.substances.constants import *
from chemical_utils.reactions.reaction import r

STEAM_METHANE_REFORMING = r(METHANE + WATER, CARBON_MONOXIDE + 3 * HYDROGEN2)
WATER_GAS_SHIFT = r(CARBON_MONOXIDE + WATER, CARBON_DIOXIDE + HYDROGEN2)
