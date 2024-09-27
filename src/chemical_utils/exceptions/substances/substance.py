from chemical_utils.exceptions import ChemicalUtilsException


class ChemicalReactionOperandSubtractionError(ChemicalUtilsException):
    """
    Error during subtraction of chemical reaction operands.

    A subtrahend chemical reaction factor either does not exist in the minuend factors
    or the stoichiometric coefficient of a subtrahend is bigger than that of the minuend.
    """
