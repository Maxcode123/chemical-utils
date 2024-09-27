from dataclasses import dataclass
from typing import Optional
from functools import cached_property
from math import log

from typing_extensions import Counter
from property_utils.constants import GLOBAL_GAS_CONSTANT
from property_utils.units import CELCIUS, KELVIN, CALORIE, MOL
from property_utils.properties import Property, p

from chemical_utils.substances.substance import (
    ChemicalReactionOperand,
    ChemicalElement,
    ChemicalElementTuple,
    ChemicalCompound,
    ChemicalReactionFactor,
)
from chemical_utils.exceptions.base import ChemicalUtilsTypeError
from chemical_utils.exceptions.reactions import (
    UnbalancedChemicalReactionError,
    ChemicalReactionSubtractionError,
)
from chemical_utils.exceptions.substances import (
    MissingDataError,
    InvalidDataError,
    ChemicalReactionOperandSubtractionError,
)
from chemical_utils.properties.properties import (
    MolarEnergy,
    Entropy,
    Temperature,
    EquilibriumConstant,
    Conditions,
    NonDimensionalProperty,
)
from chemical_utils.properties.coefficients import ThermalCapacityCoefficient


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

    def _calculate_equilibrium_constant(
        self, temperature: Temperature
    ) -> EquilibriumConstant:
        """
        NOT TESTED FOR CORRECTNESS OF THE ARITHMETIC RESULT.

        Returns the equilibrium constant of the reaction at the given temperature.

        raises `exceptions.substances.MissingDataError` if some of the data
        needed to calculate the equilibrium constant is missing (has not been created).

        raises `exceptions.substances.InvalidDataError` if invalid values are produced
        during the calculations.

        The equilibrium constant is calculated from the below equation:

        ln(K) = -gibbs_term + enthalpy_term - first_integral_term + second_integral_term

        gibbs_term:
            ΔG0/R/T0

        enthalpy_term:
            (ΔH0/R/T0) * (τ-1)/τ

        first_integral_term:
            (1/R/T)*(ΔA*T0*(τ-1) + (ΔB/2)*(T0^2)*(τ^2-1) + (ΔC/3)*(T0^3)*(τ^3-1) + (ΔD/T0)*(τ-1)/τ)

        second_integral_term:
            (1/R)*(ΔΑ*ln(τ) + (ΔB*T0 + (ΔC*(T0^2) + (ΔD/τ^2/T0^2)*(τ+1)/2))*(τ-1))
        """
        # use a Property object for calculations, where you don't need validations
        _temperature = p(value=temperature.value, unit=temperature.unit).to_unit(KELVIN)

        gibbs_term = self._calculate_gibbs_term()
        enthalpy_term = self._calculate_enthalpy_term(_temperature)
        first_integral_term = self._calculate_first_integral_term(_temperature)
        second_integral_term = self._calculate_second_integral_term(_temperature)

        lnK = (  # pylint: disable=invalid-name
            -gibbs_term + enthalpy_term - first_integral_term + second_integral_term
        ).value

        if lnK <= 0:
            raise InvalidDataError(
                "cannot calculate equilibrium constant at the requested temperature: "
                f"{temperature}; at least one of the substances "
                "participating in the reaction has invalid registered data, either "
                "standard format properties or thermal capacity coefficients. Examine "
                "calls to 'create_standard_formation_properties' and "
                "'create_thermal_capacity_coefficients'. "
            )

        K = log(lnK)  # pylint: disable=invalid-name

        value = NonDimensionalProperty(value=K)
        conditions = Conditions(properties=[_temperature])
        eq_constant = EquilibriumConstant(value=value, conditions=conditions)
        return eq_constant

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

    def _calculate_gibbs_term(self) -> Property:
        """
        First term of the equilibrium constant equation.

        ΔG0/R/T0
        """
        if self.standard_gibbs_energy_change is None:
            raise MissingDataError(
                "cannot calculate equilibrium constant; at least one of the substances "
                "participating in the reaction does not have a standard formation "
                "Gibbs energy. Register a formation Gibbs energy with "
                "'properties.registry.create_standard_formation_properties'. "
            )

        return (
            self.standard_gibbs_energy_change
            / GLOBAL_GAS_CONSTANT
            / self._standard_temperature
        )

    def _calculate_enthalpy_term(self, temperature: Property) -> Property:
        """
        Second term of the equilibrium constant equation.

        (ΔH0/R/T0) * (τ-1)/τ
        """
        if self.standard_enthalpy_change is None:
            raise MissingDataError(
                "cannot calculate equilibrium constant; at least one of the substances "
                "participating in the reaction does not have a standard formation "
                "enthalpy. Register a formation enthalpy with "
                "'properties.registry.create_standard_formation_properties'. "
            )

        return (
            (
                self.standard_enthalpy_change
                / GLOBAL_GAS_CONSTANT
                / self._standard_temperature
            )
            * (self._tau(temperature) - p(1))
            / self._tau(temperature)
        )

    def _calculate_first_integral_term(self, temperature: Property) -> Property:
        """
        Third term in the equilibrium constant equation.

        integral =
        ΔA*T0*(τ-1) + (ΔB/2)*(T0^2)*(τ^2-1) + (ΔC/3)*(T0^3)*(τ^3-1) + (ΔD/T0)*(τ-1)/τ

        whole term =
        (1/R/T)*integral
        """
        if self._thermal_capacity_coefficient_change is None:
            raise MissingDataError(
                "cannot calculate equilibrium constant; at least one of the substances "
                "participating in the reaction does not have thermal capacity "
                "coefficients. Register thermal capacity coefficients with "
                "'properties.registry.create_thermal_capacity_coefficients'. "
            )

        tau = self._tau(temperature)
        T0 = self._standard_temperature  # pylint: disable=invalid-name

        # ΔA*T0*(τ-1)
        first_integral_part = (
            self._thermal_capacity_coefficient_change.A * T0 * (tau - p(1))
        )

        # (ΔB/2)*(T0^2)*(τ^2-1)
        second_integral_part = (
            self._thermal_capacity_coefficient_change.B / 2 * (T0**2) * (tau**2 - p(1))
        )

        # (ΔC/3)*(T0^3)*(τ^3-1)
        third_integral_part = (
            self._thermal_capacity_coefficient_change.C / 3 * (T0**3) * (tau**3 - p(1))
        )

        # (ΔD/T0)*(τ-1)/τ
        fourth_integral_part = (
            (self._thermal_capacity_coefficient_change.D / T0) * (tau - p(1)) / tau
        )

        integral_part = p(
            first_integral_part.value
            + second_integral_part.value
            + third_integral_part.value
            + fourth_integral_part.value,
            CALORIE / MOL,
        )

        whole_term = (
            integral_part
            / GLOBAL_GAS_CONSTANT.to_unit(CALORIE / MOL / KELVIN)
            / temperature
        )

        return whole_term

    def _calculate_second_integral_term(self, temperature: Property) -> Property:
        """
        Fourth term in the equilibrium constant equation.

        integral =
        ΔΑ*ln(τ) + (ΔB*T0 + (ΔC*(T0^2) + (ΔD/τ^2/T0^2)*(τ+1)/2))*(τ-1)

        whole term =
        (1/R)*integral
        """
        if self._thermal_capacity_coefficient_change is None:
            raise MissingDataError(
                "cannot calculate equilibrium constant; at least one of the substances "
                "participating in the reaction does not have thermal capacity "
                "coefficients. Register thermal capacity coefficients with "
                "'properties.registry.create_thermal_capacity_coefficients'. "
            )

        tau = self._tau(temperature)
        T0 = self._standard_temperature  # pylint: disable=invalid-name

        # ΔΑ*ln(τ)
        first_integral_part = self._thermal_capacity_coefficient_change.A * log(
            tau.value
        )

        # ΔB*T0
        second_integral_part = self._thermal_capacity_coefficient_change.B * T0

        # ΔC*(T0^2)
        third_integral_part = self._thermal_capacity_coefficient_change.C * (T0**2)

        # (ΔD/τ^2/T0^2)*(τ+1)/2
        fourth_integral_part = (
            (self._thermal_capacity_coefficient_change.D / (tau**2) / (T0**2))
            * (tau + p(1))
            / 2
        )

        # τ-1
        fifth_integral_part = tau - p(1)

        integral_part = p(
            first_integral_part
            + (
                second_integral_part.value
                + (third_integral_part.value + fourth_integral_part.value)
            )
            * fifth_integral_part.value,
            CALORIE / MOL / KELVIN,
        )

        whole_term = integral_part / GLOBAL_GAS_CONSTANT.to_unit(CALORIE / MOL / KELVIN)
        return whole_term

    @cached_property
    def _thermal_capacity_coefficient_change(  # pylint: disable=invalid-name
        self,
    ) -> Optional[ThermalCapacityCoefficient]:
        A = 0.0
        B = 0.0
        C = 0.0
        D = 0.0

        for factor in self.products:
            if factor.substance.thermal_capacity_coefficients is None:
                return None

            A += (
                factor.stoichiometric_coefficient
                * factor.substance.thermal_capacity_coefficients.A
            )
            B += (
                factor.stoichiometric_coefficient
                * factor.substance.thermal_capacity_coefficients.B
            )
            C += (
                factor.stoichiometric_coefficient
                * factor.substance.thermal_capacity_coefficients.C
            )
            D += (
                factor.stoichiometric_coefficient
                * factor.substance.thermal_capacity_coefficients.D
            )

        for factor in self.reactants:
            if factor.substance.thermal_capacity_coefficients is None:
                return None

            A -= (
                factor.stoichiometric_coefficient
                * factor.substance.thermal_capacity_coefficients.A
            )
            B -= (
                factor.stoichiometric_coefficient
                * factor.substance.thermal_capacity_coefficients.B
            )
            C -= (
                factor.stoichiometric_coefficient
                * factor.substance.thermal_capacity_coefficients.C
            )
            D -= (
                factor.stoichiometric_coefficient
                * factor.substance.thermal_capacity_coefficients.D
            )

        diff = ThermalCapacityCoefficient(A=A, B=B, C=C, D=D)
        return diff

    @property
    def _standard_temperature(self) -> Property:
        """
        Standard temperature 25 C.
        """
        return p(value=25, unit=CELCIUS).to_unit(KELVIN)

    def _tau(self, temperature: Property) -> Property:
        # ALWAYS convert to absolute units (Kelvin or Rankine) before division!
        return temperature.to_unit(KELVIN) / self._standard_temperature

    def __repr__(self) -> str:
        return f"<ChemicalReaction: {str(self)}>"

    def __str__(self) -> str:
        return f"{self.reactants} -> {self.products}"

    def __add__(self, other: "ChemicalReaction") -> "ChemicalReaction":
        if not isinstance(other, ChemicalReaction):
            raise ChemicalUtilsTypeError(
                f"cannot add {other} to a chemical reaction; only a chemical reaction can"
                " be added to chemical reactions. "
            )

        reactants = self.reactants.add(other.reactants)
        products = self.products.add(other.products)
        reaction = ChemicalReaction(reactants, products)

        return reaction

    def __radd__(self, other: "ChemicalReaction") -> "ChemicalReaction":
        return self.__add__(other)

    def __sub__(self, other: "ChemicalReaction") -> "ChemicalReaction":
        if not isinstance(other, ChemicalReaction):
            raise ChemicalUtilsTypeError(
                f"cannot subtract {other} from a chemical reaction; only a chemical "
                "reaction can be subtracted from chemical reactions. "
            )

        try:
            reactants = self.reactants.subtract(other.reactants)
            products = self.products.subtract(other.products)
        except ChemicalReactionOperandSubtractionError:
            raise ChemicalReactionSubtractionError(
                f"cannot subtract {other} from {self}; {other} must be a subreaction of "
                f"{self}. "
            ) from None

        reaction = ChemicalReaction(reactants, products)

        return reaction
