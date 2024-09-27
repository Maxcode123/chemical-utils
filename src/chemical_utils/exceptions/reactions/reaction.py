from chemical_utils.exceptions.base import (
    ChemicalUtilsValidationError,
    ChemicalUtilsException,
)


class UnbalancedChemicalReactionError(ChemicalUtilsValidationError):
    """
    A chemical reaction is unbalanced.
    """


class ChemicalReactionSubtractionError(ChemicalUtilsException):
    """
    Reaction A, which is not a subreaction of reaction B, is subtracted from reaction B.
    """
