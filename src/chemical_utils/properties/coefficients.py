from dataclasses import dataclass


@dataclass
class ThermalCapacityCoefficient:
    """
    Coefficients of the equation:
    Cp = A + B*T + C*(T^2) + D/(T^2)

    Thermal capacity is calculated in cal/mol/K.
    """

    # pylint: disable=invalid-name
    A: float
    B: float
    C: float
    D: float
