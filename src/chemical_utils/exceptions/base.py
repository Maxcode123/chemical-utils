class ChemicalUtilsException(Exception):
    """
    Base exception for chemical-utils library. Any exception raised from the
    modules of this library inherits from this class.
    """


class ChemicalUtilsValueError(ChemicalUtilsException):
    """
    Wrong argument value of correct type.
    """


class ChemicalUtilsTypeError(ChemicalUtilsException):
    """
    Wrong argument type.
    """


class ChemicalUtilsValidationError(ChemicalUtilsException):
    """
    An object is created with invalid values.
    """
