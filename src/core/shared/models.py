from dataclasses import dataclass
from collections import namedtuple
from typing import List


@dataclass(frozen=True)
class PileData:
    """
    A dataclass representing the main parameters of a single pile.

    Attributes:
        pile_diameter (float): Diameter of the pile.
        pile_length (float): Length of the pile.
        pile_cap_width (float): Width of the pile cap.
        pile_cap_height (float): Height of the pile cap.
        pile_cap_weight (float): Weight of the pile cap.
    """
    pile_diameter: float
    pile_length: float
    pile_cap_width: float
    pile_cap_height: float
    pile_cap_weight: float

    def __str__(self) -> str:
        return (
            f"### Pile Data\n"
            f"- **Diameter**: {self.pile_diameter} m\n"
            f"- **Length**: {self.pile_length} m\n"
            f"- **Cap Width**: {self.pile_cap_width} m\n"
            f"- **Cap Height**: {self.pile_cap_height} m\n"
            f"- **Cap Weight**: {self.pile_cap_weight:.2f} t\n"
        )


@dataclass(frozen=True)
class SoilLayer:
    """Represents a single soil layer in the foundation."""
    friction_angle: float
    cohesion: float
    deformation_modulus: float
    density: float
    depth: float

    def is_empty(self) -> bool:
        list_bool = []
        for param in [self.friction_angle,
                      self.cohesion,
                      self.deformation_modulus,
                      self.density,
                      self.depth]:
            if param is None:
                list_bool.append(True)
            else:
                return False
        return True


@dataclass(frozen=True)
class FoundationData:
    """Represents the foundation data, including geological elements."""
    soil_layers: List[SoilLayer]


LimitState = namedtuple('LimitState', ['M', 'Q', 'N'])


@dataclass(frozen=True)
class LoadData:
    first_limit_state: LimitState
    second_limit_state: LimitState
