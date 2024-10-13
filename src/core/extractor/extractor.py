from typing import Union

from openpyxl.worksheet.worksheet import Worksheet

from data_extractor import (
    DataExtractor,
    PileDataExtractor,
    FoundationDataExtractor,
    LoadDataExtractor
)
from src.shared.models import PileData, FoundationData, LoadData


class ExtractorFactory:
    @staticmethod
    def create_extractor(extractor_type: str) -> DataExtractor:
        """
        Creates an extractor instance based on the given extractor type.

        Args:
            extractor_type (str): The type of extractor to create (e.g., "PileData", "FoundationData").

        Returns:
            DataExtractor: An instance of the specified extractor.

        Raises:
            ValueError: If the extractor type is unknown.
        """
        if extractor_type == "PileData":
            return PileDataExtractor()
        elif extractor_type == "FoundationData":
            return FoundationDataExtractor()
        elif extractor_type == "LoadData":
            return LoadDataExtractor()
        else:
            raise ValueError(f"Unknown extractor type: {extractor_type}")


def extract_data_from_sheet(sheet: Worksheet, extractor_type: str) -> Union[PileData, FoundationData, LoadData]:
    """
    Returns data from the given sheet.
    Args:
        sheet: sheet with data.
        extractor_type: special extractor type (e.g., "PileData", "FoundationData").

    Returns:
        PileData, FoundationData, LoadData: An instance of the specified extractor type and data extractor.
    """

    extractor = ExtractorFactory.create_extractor(extractor_type)
    return extractor.extract(sheet)
