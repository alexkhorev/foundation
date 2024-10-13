from abc import ABC, abstractmethod

from openpyxl.worksheet.worksheet import Worksheet

from ..shared.models import (
    PileData,
    SoilLayer,
    FoundationData,
    LimitState,
    LoadData,
)


class DataExtractor(ABC):
    @abstractmethod
    def extract(self, sheet: Worksheet):
        pass


class PileDataExtractor(DataExtractor):
    def extract(self, sheet: Worksheet) -> PileData:
        return PileData(
            pile_diameter=sheet['B3'].value,
            pile_length=sheet['B4'].value,
            pile_cap_width=sheet['B5'].value,
            pile_cap_height=sheet['B6'].value,
            pile_cap_weight=sheet['B7'].value,
        )


class FoundationDataExtractor(DataExtractor):
    def extract(self, sheet: Worksheet) -> FoundationData:

        soil_layers = []

        for row in range(3, 100):

            soil_layer = SoilLayer(
                friction_angle=sheet[f'C{row}'].value,
                cohesion=sheet[f'D{row}'].value,
                deformation_modulus=sheet[f'E{row}'].value,
                density=sheet[f'F{row}'].value,
                depth=sheet[f'G{row}'].value,
            )

            if not soil_layer.is_empty():
                soil_layers.append(soil_layer)
            else:
                break

        return FoundationData(
            soil_layers=soil_layers,
        )


class LoadDataExtractor(DataExtractor):
    def extract(self, sheet: Worksheet) -> LoadData:
        first_limit_state = LimitState(
            sheet['B3'].value,
            sheet['B4'].value,
            sheet['B5'].value,
        )

        second_limit_state = LimitState(
            sheet['B7'].value,
            sheet['B8'].value,
            sheet['B9'].value,
        )

        return LoadData(
            first_limit_state=first_limit_state,
            second_limit_state=second_limit_state,
        )
