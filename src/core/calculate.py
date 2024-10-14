# TODO: Create tests for all calculation functions
from abc import ABC, abstractmethod
from math import pi, tan, radians, sqrt
from typing import List, Tuple, Dict

from .shared.models import PileData, LoadData, FoundationData, SoilLayer


class PileCalculationStrategy(ABC):
    @abstractmethod
    def calculate(
            self,
            pile_data: PileData,
            load_data: LoadData,
            foundation_data: FoundationData
    ) -> Dict[str, float]:
        """Perform calculation and return success or failure"""
        pass


class MainCalculation(PileCalculationStrategy):
    def calculate(
            self,
            pile_data: PileData,
            load_data: LoadData,
            foundation_data: FoundationData
    ) -> Dict[str, float]:

        if len(foundation_data.soil_layers) == 1:
            soil_repulsion = _calculate_soil_repulsion(
                foundation_data.soil_layers[0]
            )
            def_module = foundation_data.soil_layers[0].deformation_modulus
        else:
            soil_repulsions = _get_soil_repulsions(foundation_data)
            soil_repulsion = _calculate_weighted_avg(soil_repulsions)
            def_module = _calculate_weighted_avg(
                [(x.deformation_modulus, x.depth) for x in foundation_data.soil_layers]
            )

        betta = 0.15
        alpha = pile_data.pile_cap_width / pile_data.pile_diameter
        friction_force = betta * soil_repulsion

        height = load_data.first_limit_state.M / load_data.first_limit_state.Q

        coefficient_a, coefficient_b, coefficient_c = _calculate_coefficients(pile_data, alpha, betta, height)

        pivot_depth = sqrt(height ** 2 + 0.5 * coefficient_c) - height

        if pivot_depth <= pile_data.pile_cap_height:
            pivot_depth = 0

        side_cap_moment = _calculate_side_cap_moment(pile_data, soil_repulsion)
        top_side_moment = _calculate_top_side_moment(pile_data, pivot_depth, soil_repulsion)
        bottom_side_moment = _calculate_bottom_side_moment(pile_data, pivot_depth, soil_repulsion)
        vert_cap_moment = _calculate_vertical_cap_moment(pile_data, alpha, soil_repulsion)
        vert_pile_moment = _calculate_vert_pile_moment(pile_data, soil_repulsion)
        contact_moment = _calculate_contact_moment(pile_data, friction_force)

        sum_moment = (side_cap_moment + top_side_moment + bottom_side_moment + vert_cap_moment +
                      vert_pile_moment + contact_moment)

        sum_moment_with_coefficient = 0.9 * sum_moment / 1.1

        is_passed = sum_moment_with_coefficient < load_data.first_limit_state.M

        # TODO: Add M, N, Q
        return {
            "calculation_variables": {
                "soil_repulsion": soil_repulsion,
                "def_module": def_module,
                "betta": betta,
                "alpha": alpha,
                "friction_force": friction_force,
                "height": height,
                "coefficients": (coefficient_a, coefficient_b, coefficient_c),
                "pivot_depth": pivot_depth,
                "side_cap_moment": side_cap_moment,
                "top_side_moment": top_side_moment,
                "bottom_side_moment": bottom_side_moment,
                "vert_cap_moment": vert_cap_moment,
                "vert_pile_moment": vert_pile_moment,
                "contact_moment": contact_moment,
                "sum_moment": sum_moment,
                "sum_moment_with_coefficient": sum_moment_with_coefficient
            },
            "is_passed": is_passed
        }


class PileCalculationContext:
    def __init__(self, strategy: PileCalculationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PileCalculationStrategy):
        self._strategy = strategy

    def execute_calculation(
            self,
            pile_data: PileData,
            load_data: LoadData,
            foundation_data: FoundationData
    ) -> Dict[str, float]:
        return self._strategy.calculate(pile_data, load_data, foundation_data)


def _calculate_contact_moment(
        pile_data: PileData,
        friction_force: float
) -> float:
    """
    Returns reactive moment of friction forces arising at the contact of the base of the cap with the soil
    """
    return (pile_data.pile_cap_width ** 2 - (pi * pile_data.pile_diameter ** 2) / 4) * friction_force * (
            pile_data.pile_length - pile_data.pile_cap_height)


def _calculate_vert_pile_moment(
        pile_data: PileData,
        soil_repulsion: float
) -> float:
    """
    Returns reactive moment of the vertical backstop acting on the base area of the column
    """
    return (pi * pile_data.pile_diameter ** 3) / 12 * soil_repulsion


def _calculate_vertical_cap_moment(
        pile_data: PileData,
        alpha: float,
        soil_repulsion: float
) -> float:
    """
    Returns reactive moment of the vertical backstop acting on the area of the square cap
    """
    return (pile_data.pile_cap_width - (pi * pile_data.pile_diameter ** 2) / 4) * soil_repulsion * (
            2 * alpha - 1) / 6


def _calculate_bottom_side_moment(pile_data: PileData, pivot_depth: float, soil_repulsion: float) -> float:
    """
    Returns reactive moment of lateral rebound of the pile below the point ‘0’ of conditional rotation
    of the pile in the ground at the depth Z0
    """
    return -soil_repulsion * pile_data.pile_diameter * ((pile_data.pile_length - pivot_depth) ** 2) / 2


def _calculate_top_side_moment(pile_data: PileData, pivot_depth: float, soil_repulsion: float) -> float:
    """
    Returns reactive moment of lateral support of the pile above the point ‘0’
    of the conditional pile rotation
    """
    return soil_repulsion * pile_data.pile_diameter * (
            pivot_depth - pile_data.pile_cap_height) * (
            pile_data.pile_length - pile_data.pile_cap_height / 2 - pivot_depth / 2)


def _calculate_coefficients(
        pile_data: PileData,
        alpha: float,
        betta: float,
        height: float,
) -> Tuple[float, float, float]:
    coefficient_a = pile_data.pile_cap_height * (pile_data.pile_length - (pile_data.pile_cap_height ** 2) / 2) * (
            alpha - 1) + (
                            (pi * pile_data.pile_diameter ** 2) / 12) * (
                            1 + 0.25 * (alpha ** 2 - 1) * (2 * alpha - 1)) + betta * (
                            (pi * pile_data.pile_diameter) / 4) * (alpha ** 2 - 1) * (
                            pile_data.pile_length - pile_data.pile_cap_height)
    coefficient_b = pile_data.pile_cap_height * (alpha - 1) + betta * ((pi * pile_data.pile_diameter) / 4) * alpha ** 2
    coefficient_c = abs(
        pile_data.pile_length ** 2 + 2 * height * (
                pile_data.pile_length - coefficient_b) - 2 * pile_data.pile_length * coefficient_b - 2 * coefficient_a)
    return coefficient_a, coefficient_b, coefficient_c


def _calculate_side_cap_moment(
        pile_data: PileData,
        soil_repulsion: float
) -> float:
    """
    Returns reactive moment of lateral rebound along the height of cap
    """
    return soil_repulsion * pile_data.pile_cap_width * pile_data.pile_cap_height * (
            pile_data.pile_length - pile_data.pile_cap_height / 2)


def _calculate_soil_repulsion(soil_layer: SoilLayer) -> float:
    """
    Calculate the soil repulsion.
    """
    return pi * soil_layer.cohesion * tan(radians(45 + soil_layer.friction_angle / 2)) ** 3


def _get_soil_repulsions(foundation_data: FoundationData) -> List[Tuple[float, float]]:
    """
    Calculate soil repulsion for every geological element from foundation data

    Returns:
        List[float]: list of soil repulsion with depth layer
    """
    soil_repulsions = []
    for i, soil_layer in enumerate(foundation_data.soil_layers):
        soil_repulsion = _calculate_soil_repulsion(soil_layer)
        soil_repulsions.append((soil_repulsion, soil_layer.depth))
    return soil_repulsions

# TODO: Create function for defining compressible depth or fix formula
def _calculate_weighted_avg(vars_with_weight: List[Tuple[float, float]]) -> float:
    """
    Calculate average soil repulsion by depth layer
    """
    sum_depth = sum([x[1] for x in vars_with_weight])
    soil_repulsion = sum([x * y for x, y in vars_with_weight])
    return soil_repulsion / sum_depth


if __name__ == "__main__":
    a = _calculate_weighted_avg([(1, 1.6), (2, 1.4)])
    print(a)
