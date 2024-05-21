from dataclasses import dataclass
from typing import Optional
from functools import cached_property

from typing_extensions import Counter

from chemical_utils.substances.substance import (
    ChemicalReactionOperand,
    ChemicalElement,
    ChemicalElementTuple,
    ChemicalCompound,
    ChemicalReactionFactor,
)
from chemical_utils.exceptions.base import ChemicalUtilsTypeError
from chemical_utils.exceptions.reactions.reaction import UnbalancedChemicalReactionError
from chemical_utils.properties.properties import MolarEnergy, Entropy


def r(
    reactants: ChemicalReactionOperand, products: ChemicalReactionOperand
) -> "ChemicalReaction":
    """
    Create a chemical reaction.

    Examples:
        >>> from chemical_utils.substances import *
        >>> r(2*CARBON_MONOXIDE + OXYGEN2, 2*CARBON_DIOXIDE)
        <ChemicalReaction: 2CO + O2 -> 2CO2>
    """
    return ChemicalReaction(reactants, products)


@dataclass(frozen=True)
class ChemicalReaction:
    """
    A chemical reaction object containing reactants and products.

    The atom balance of the reaction is validated.
    """

    reactants: ChemicalReactionOperand
    products: ChemicalReactionOperand

    def __post_init__(self) -> None:
        self._parse_reactants()
        self._parse_products()

        if not self._is_balanced(self.reactants, self.products):
            raise UnbalancedChemicalReactionError(
                f"{self} is not balanced; the number of atoms of each species on the "
                "left side should equal the number of atoms of that species on the "
                "right side. "
            )

    @cached_property
    def standard_enthalpy_change(self) -> Optional[MolarEnergy]:
        """
        Enthalpy change of reaction at standard conditions (25 Celcius, 1 bar).
        """
        diff = MolarEnergy(0)

        for factor in self.products:
            if factor.substance.standard_formation_properties is None:
                return None

            diff += (
                factor.stoichiometric_coefficient
                * factor.substance.standard_formation_properties.enthalpy
            )

        for factor in self.reactants:
            if factor.substance.standard_formation_properties is None:
                return None

            diff -= (
                factor.stoichiometric_coefficient
                * factor.substance.standard_formation_properties.enthalpy
            )

        return diff

    @cached_property
    def standard_gibbs_energy_change(self) -> Optional[MolarEnergy]:
        """
        Gibbs energy change of reaction at standard conditions (25 Celcius, 1 bar).
        """
        diff = MolarEnergy(0)

        for factor in self.products:
            if factor.substance.standard_formation_properties is None:
                return None

            diff += (
                factor.stoichiometric_coefficient
                * factor.substance.standard_formation_properties.gibbs_energy
            )

        for factor in self.reactants:
            if factor.substance.standard_formation_properties is None:
                return None

            diff -= (
                factor.stoichiometric_coefficient
                * factor.substance.standard_formation_properties.gibbs_energy
            )

        return diff

    @cached_property
    def standard_entropy_change(self) -> Optional[Entropy]:
        """
        Entropy change of reaction at standard conditions (25 Celcius, 1 bar).
        """
        diff = Entropy(0)

        for factor in self.products:
            if factor.substance.standard_entropy is None:
                return None

            diff += (
                factor.stoichiometric_coefficient * factor.substance.standard_entropy
            )

        for factor in self.reactants:
            if factor.substance.standard_entropy is None:
                return None

            diff -= (
                factor.stoichiometric_coefficient * factor.substance.standard_entropy
            )

        return diff

    def _parse_reactants(self):
        if isinstance(
            self.reactants, (ChemicalElement, ChemicalElementTuple, ChemicalCompound)
        ):
            object.__setattr__(
                self, "reactants", ChemicalReactionOperand([1 * self.reactants])
            )

        elif isinstance(self.reactants, ChemicalReactionFactor):
            object.__setattr__(
                self, "reactants", ChemicalReactionOperand([self.reactants])
            )

        if not isinstance(self.reactants, ChemicalReactionOperand):
            raise ChemicalUtilsTypeError(
                f"cannot create chemical reaction with reactants: {self.reactants}; "
                "expected a chemical substance or a sum of chemical substances. "
            )

    def _parse_products(self):
        if isinstance(
            self.products, (ChemicalElement, ChemicalElementTuple, ChemicalCompound)
        ):
            object.__setattr__(
                self, "products", ChemicalReactionOperand([1 * self.products])
            )

        elif isinstance(self.products, ChemicalReactionFactor):
            object.__setattr__(
                self, "products", ChemicalReactionOperand([self.products])
            )

        if not isinstance(self.products, ChemicalReactionOperand):
            raise ChemicalUtilsTypeError(
                f"cannot create chemical reaction with products: {self.products}; "
                "expected a chemical substance or a sum of chemical substances. "
            )

    @classmethod
    def _is_balanced(
        cls, reactants: ChemicalReactionOperand, products: ChemicalReactionOperand
    ) -> bool:
        return cls._count_elements(reactants) == cls._count_elements(products)

    @staticmethod
    def _count_elements(operand: ChemicalReactionOperand) -> Counter[ChemicalElement]:
        return Counter(
            [
                element
                for factor in operand
                for element in factor.stoichiometric_elements()
            ]
        )

    def __repr__(self) -> str:
        return f"<ChemicalReaction: {str(self)}>"

    def __str__(self) -> str:
        return f"{self.reactants} -> {self.products}"
