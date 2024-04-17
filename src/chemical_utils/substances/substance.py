from typing import Protocol, Iterable
from dataclasses import dataclass

from chemical_utils.exceptions.base import (
    ChemicalUtilsTypeError,
    ChemicalUtilsValueError,
)


def c(*components) -> "ChemicalCompound":
    """
    Create a chemical compound from the given components.

    Examples:
        >>> from chemical_utils.substances import CARBON, HYDROGEN
        >>> c(CARBON, HYDROGEN*4)
        <ChemicalCompound: CH4>
    """
    return ChemicalCompound(*components)


# pylint: disable=too-few-public-methods
class ChemicalSubstance(Protocol):
    """
    A chemical substance is a chemical element or a compound consisting of multiple
    elements of the same or different atmoms.
    """

    @property
    def molecular_weight(self) -> float:
        """
        Unitless relative molecular mass of the chemical substance.
        """


class ChemicalCompoundComponent(Protocol):
    """
    Component of a chemical compound.
    """

    def __mul__(self, other: int) -> "ChemicalElementList": ...

    def __rmul__(self, other: int) -> "ChemicalElementList": ...


@dataclass(frozen=True)
class ChemicalElement:
    """
    Element of the periodic table.
    """

    atomic_number: int
    atomic_mass: float
    symbol: str

    @property
    def molecular_weight(self) -> float:
        """
        Unitless relative molecular mass of the chemical element.
        """
        return self.atomic_mass

    def __mul__(self, other: int) -> "ChemicalElementList":
        """
        Defines multiplication between integers and chemical elements.
        The product is an object that holds the element and its' multiplier.

        Examples:
            >>> ChemicalElement(1, 1.0080, "H") * 2
            <ChemicalElementList: H2>
        """
        if not isinstance(other, int):
            raise ChemicalUtilsTypeError(
                f"cannot multiply ChemicalElement with {other}; "
                "expected a positive integer. "
            )
        if not other > 0:
            raise ChemicalUtilsValueError(
                f"cannot multiply ChemicalElement with {other}; "
                "expected a positive integer. "
            )
        return ChemicalElementList(self, other)

    def __rmul__(self, other: int) -> "ChemicalElementList":
        """
        Defines right multiplication between integers and chemical elements.
        The product is an object that holds the element and its' multiplier.

        Examples:
            >>> 2 * ChemicalElement(1, 1.0080, "H")
            <ChemicalElementList: H2>
        """
        return self.__mul__(other)

    def __repr__(self) -> str:
        return f"<ChemicalElement: {self.symbol}>"

    def __str__(self) -> str:
        return self.symbol


@dataclass(frozen=True)
class ChemicalElementList:
    """
    Container for a multitude of elements with the same atom.
    """

    element: ChemicalElement
    number_of_elements: int

    def __mul__(self, other: int) -> "ChemicalElementList":
        """
        Defines multiplication between integers and chemical element lists.

        Examples:
            >>> ChemicalElementList(ChemicalElement(1, 1.0080, "H"), 2) * 2
            <ChemicalElementList: H4>
        """
        if not isinstance(other, int):
            raise ChemicalUtilsTypeError(
                f"cannot multiply ChemicalElementList with {other}; "
                "expected a positive integer. "
            )
        if not other > 0:
            raise ChemicalUtilsValueError(
                f"cannot multiply ChemicalElementList with {other}; "
                "expected a positive integer. "
            )
        return ChemicalElementList(self.element, self.number_of_elements * other)

    def __rmul__(self, other: int) -> "ChemicalElementList":
        """
        Defines right multiplication between integers and chemical elements lists.

        Examples:
            >>> 2 * ChemicalElementList(ChemicalElement(1, 1.0080, "H"), 2)
            <ChemicalElementList: H4>
        """
        return self.__mul__(other)

    def __repr__(self) -> str:
        return f"<ChemicalElementList: {self.element}{self.number_of_elements}>"

    def __str__(self) -> str:
        return f"{self.element}{self.number_of_elements}"


@dataclass(frozen=True)
class ChemicalCompound:
    """
    A chemical compound can contain any number of chemical components.
    """

    components: Iterable[ChemicalCompoundComponent]

    def __init__(self, *components) -> None:
        try:
            _components = list(components)
        except Exception as exc:
            raise ChemicalUtilsTypeError(
                f"cannot create ChemicalCompound from {components}; "
                "components must be iterable ",
                exc,
            ) from None
        object.__setattr__(self, "components", _components)

    @property
    def molecular_weight(self) -> float:
        """
        Unitless relative molecular mass of the chemical compound.
        """
        mw = 0.0
        for component in self.components:
            if isinstance(component, ChemicalElementList):
                mw += component.element.molecular_weight * component.number_of_elements
            elif isinstance(component, ChemicalElement):
                mw += component.molecular_weight
        return mw

    def __repr__(self) -> str:
        return f"<ChemicalCompound: {''.join(str(c) for c in self.components)}>"

    def __str__(self) -> str:
        return "".join(str(c) for c in self.components)
