from typing import Protocol, Iterable, Union, List, Iterator

try:
    from typing import TypeAlias  # Python >= 3.10
except ImportError:
    from typing_extensions import TypeAlias  # Python < 3.10
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


class ChemicalSubstance(Protocol):
    """
    A chemical substance is a chemical element or a compound consisting of multiple
    elements of the same or different atoms.
    """

    @property
    def molecular_weight(self) -> float:
        """
        Unitless relative molecular mass of the chemical substance.
        """

    def __add__(self, other: "ChemicalSubstance") -> "ChemicalReactionOperand":
        """
        Defines addition for chemical elements.
        """
        if not isinstance(
            other, (ChemicalElement, ChemicalElementTuple, ChemicalCompound)
        ):
            raise ChemicalUtilsTypeError(
                f"cannot add {other} to self; expected a ChemicalSubstance"
            )
        return ChemicalReactionOperand(
            [
                ChemicalReactionFactor(substance=self),
                ChemicalReactionFactor(substance=other),
            ]
        )

    def __rmul__(self, coeff: int) -> "ChemicalReactionFactor":
        """
        Defines right multiplication between integers and chemical substances.
        The product is a chemical reaction factor.
        """
        if not isinstance(coeff, int):
            raise ChemicalUtilsTypeError(
                f"cannot multiply {self.__class__.__name__} with {coeff}; "
                "expected a positive integer. "
            )
        if not coeff > 0:
            raise ChemicalUtilsValueError(
                f"cannot multiply {self.__class__.__name__} with {coeff}; "
                "expected a positive integer. "
            )
        return ChemicalReactionFactor(self, coeff)


@dataclass(frozen=True)
class ChemicalElement(ChemicalSubstance):
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

    def __mul__(self, other: int) -> "ChemicalElementTuple":
        """
        Defines multiplication between integers and chemical elements.
        The product is an object that holds the element and its' multiplier.subst

        Examples:
            >>> ChemicalElement(1, 1.0080, "H") * 2
            <ChemicalElementTuple: H2>
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
        return ChemicalElementTuple(self, other)

    def __repr__(self) -> str:
        return f"<ChemicalElement: {self.symbol}>"

    def __str__(self) -> str:
        return self.symbol


@dataclass(frozen=True)
class ChemicalElementTuple(ChemicalSubstance):
    """
    Container for a multitude of elements with the same atom.
    """

    element: ChemicalElement
    size: int

    @property
    def molecular_weight(self) -> float:
        return self.element.molecular_weight * self.size

    def __repr__(self) -> str:
        return f"<ChemicalElementTuple: {self.element}{self.size}>"

    def __str__(self) -> str:
        return f"{self.element}{self.size}"


ChemicalCompoundComponent: TypeAlias = Union[ChemicalElement, ChemicalElementTuple]


@dataclass(frozen=True)
class ChemicalCompound(ChemicalSubstance):
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
            mw += component.molecular_weight
        return mw

    def __repr__(self) -> str:
        return f"<ChemicalCompound: {''.join(str(c) for c in self.components)}>"

    def __str__(self) -> str:
        return "".join(str(c) for c in self.components)


@dataclass(frozen=True)
class ChemicalReactionFactor:
    """
    A factor is either a reactant or a product in a chemical reaction.
    """

    substance: ChemicalSubstance
    stoichiometric_coefficient: int = 1

    def __add__(self, other: "ChemicalReactionFactor") -> "ChemicalReactionOperand":
        return ChemicalReactionOperand([self, other])

    def __repr__(self) -> str:
        return f"<ChemicalReactionFactor: {str(self)}>"

    def __str__(self) -> str:
        if self.stoichiometric_coefficient > 1:
            return f"{self.stoichiometric_coefficient}{self.substance}"
        return f"{self.substance}"


@dataclass(frozen=True)
class ChemicalReactionOperand:
    """
    A chemical reaction operand contains a number of chemical reaction factors.
    The operand can either be the reactants or the products of a chemical reaction.
    """

    factors: List[ChemicalReactionFactor]

    def __add__(self, other: ChemicalReactionFactor) -> "ChemicalReactionOperand":
        if isinstance(other, (ChemicalElement, ChemicalElementTuple, ChemicalCompound)):
            other = ChemicalReactionFactor(other)

        if not isinstance(other, ChemicalReactionFactor):
            raise ChemicalUtilsTypeError(
                f"cannot add {other} to {self}; expected a ChemicalReactionFactor. "
            )

        return ChemicalReactionOperand(self.factors + [other])

    def __iter__(self) -> Iterator[ChemicalReactionFactor]:
        return self.factors.__iter__()

    def __repr__(self) -> str:
        return f"<ChemicalReactionOperand: {str(self)}>"

    def __str__(self) -> str:
        return " + ".join(map(str, self.factors))
