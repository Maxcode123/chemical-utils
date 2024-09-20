from chemical_utils.exceptions import ChemicalUtilsException


class MissingDataError(ChemicalUtilsException):
    """
    Substance data needed to perform calculations is missing (has not been created).
    """


class InvalidDataError(ChemicalUtilsException):
    """
    Substance data needed to perform calculations is invalid (produces invalid
    calculated values).
    """
