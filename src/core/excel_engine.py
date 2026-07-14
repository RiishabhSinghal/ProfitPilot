from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.core.exceptions import (
    EmptyFileError,
    FileReadError,
    InvalidFileError,
    SchemaExtractionError,
)
from src.utils.logger import get_logger


class ExcelEngine:
    """
    Handles loading, validating, reading and schema extraction
    of structured datasets.
    """

    SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}

    CSV_ENCODINGS = (
        "utf-8",
        "latin-1",
        "cp1252",
    )

    def __init__(self) -> None:

        self.file_path: Path | None = None
        self.dataframe: pd.DataFrame | None = None
        self.schema: dict | None = None

        self.logger = get_logger(__name__)

    # ------------------------------------------------------------------ #

    def load_file(self, file_path: str) -> None:
        """
        Load a dataset.

        Pipeline:
            1. Validate file
            2. Read file
            3. Extract schema
        """

        self.logger.info(f"Loading file: {file_path}")

        self.file_path = Path(file_path)

        self._validate_file()
        self._read_file()
        self._extract_schema()

        self.logger.info("Dataset loaded successfully.")

    # ------------------------------------------------------------------ #

    def _validate_file(self) -> None:
        """
        Validate the supplied file.
        """

        if self.file_path is None:
            raise InvalidFileError("No file path has been provided.")

        if not self.file_path.exists():
            raise InvalidFileError(
                f"File not found: {self.file_path}"
            )

        if not self.file_path.is_file():
            raise InvalidFileError(
                f"Expected a file but received a directory: {self.file_path}"
            )

        if self.file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise InvalidFileError(
                f"Unsupported file type '{self.file_path.suffix}'. "
                f"Supported types: {', '.join(sorted(self.SUPPORTED_EXTENSIONS))}"
            )

        if self.file_path.stat().st_size == 0:
            raise EmptyFileError("The uploaded file is empty.")

    # ------------------------------------------------------------------ #

    def _read_file(self) -> None:
        """
        Read the dataset into a pandas DataFrame.
        """

        suffix = self.file_path.suffix.lower()

        try:

            if suffix == ".csv":

                for encoding in self.CSV_ENCODINGS:

                    try:

                        self.dataframe = pd.read_csv(
                            self.file_path,
                            encoding=encoding,
                        )

                        self.logger.info(
                            f"CSV loaded successfully using '{encoding}' encoding."
                        )

                        return

                    except UnicodeDecodeError:
                        continue

                raise FileReadError(
                    "Unable to read CSV using supported encodings."
                )

            self.dataframe = pd.read_excel(self.file_path)

            self.logger.info("Excel file loaded successfully.")

        except FileReadError:
            raise

        except Exception as e:
            raise FileReadError(
                f"Failed to read file: {self.file_path}"
            ) from e

    # ------------------------------------------------------------------ #

    def _extract_schema(self) -> None:
        """
        Extract schema and metadata from the loaded dataframe.
        """

        if self.dataframe is None:
            raise SchemaExtractionError(
                "No dataframe loaded."
            )

        try:

            schema = {
                "row_count": len(self.dataframe),
                "column_count": len(self.dataframe.columns),
                "columns": {},
            }

            for column in self.dataframe.columns:

                series = self.dataframe[column]

                null_count = int(series.isnull().sum())

                column_info = {
                    "dtype": str(series.dtype),
                    "nullable": null_count > 0,
                    "null_count": null_count,
                    "non_null_count": len(series) - null_count,
                    "unique_count": int(series.nunique(dropna=True)),
                    "is_numeric": pd.api.types.is_numeric_dtype(series),
                    "is_datetime": pd.api.types.is_datetime64_any_dtype(series),
                    "sample_values": series.dropna().head(5).tolist(),
                }

                if column_info["is_numeric"]:

                    if series.dropna().empty:

                        column_info["statistics"] = {
                            "min": None,
                            "max": None,
                            "mean": None,
                            "std": None,
                        }

                    else:

                        column_info["statistics"] = {
                            "min": float(series.min()),
                            "max": float(series.max()),
                            "mean": float(series.mean()),
                            "std": float(series.std()),
                        }

                schema["columns"][column] = column_info

            self.schema = schema

            self.logger.info("Schema extracted successfully.")

        except Exception as e:

            raise SchemaExtractionError(
                "Failed to extract schema."
            ) from e
                

       