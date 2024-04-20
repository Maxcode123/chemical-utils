from chemical_utils.exceptions.base import ChemicalUtilsValidationError


class UnbalancedChemicalReactionError(ChemicalUtilsValidationError):
    """
    A chemical reaction is unbalanced.
    """
