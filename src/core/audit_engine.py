from __future__ import annotations
from src.core.exceptions import AuditError
import pandas as pd

from src.utils.logger import get_logger


class AuditEngine:
    """
    Performs data quality analysis on a pandas DataFrame
    and returns a structured audit report.
    """

    def __init__(self) -> None:
        self.logger = get_logger(__name__)

    # ------------------------------------------------------------------ #

    def audit(self, dataframe: pd.DataFrame) -> dict:
        """
        Run all audit checks on the dataframe.
        """

        if dataframe is None:
            raise AuditError("Cannot audit a None dataframe.")

        self.logger.info("Running dataset audit...")

        summary = self._dataset_summary(dataframe)
        missing = self._missing_value_analysis(dataframe)
        duplicates = self._duplicate_analysis(dataframe)
        column_types = self._datatype_analysis(dataframe)
        numeric_stats = self._numeric_statistics(dataframe)
        categorical_stats = self._categorical_statistics(dataframe)
        datetime_stats = self._datetime_statistics(dataframe)

        report = {
            "dataset_summary": summary,
            "missing_values": missing,
            "duplicates": duplicates,
            "column_types": column_types,
            "numeric_statistics": numeric_stats,
            "categorical_statistics": categorical_stats,
            "datetime_statistics": datetime_stats,
        }

        self.logger.info("Audit completed successfully.")

        return report

    # ------------------------------------------------------------------ #

    def _dataset_summary(
        self,
        dataframe: pd.DataFrame
    ) -> dict:
        """
        Basic information about the dataset.
        """

        memory = dataframe.memory_usage(deep=True).sum()

        return {
            "rows": len(dataframe),
            "columns": len(dataframe.columns),
            "memory_mb": float(round(memory / (1024**2), 2))
        }

    # ------------------------------------------------------------------ #

    def _missing_value_analysis(
        self,
        dataframe: pd.DataFrame
    ) -> dict:
        """
        Analyze missing values for every column.
        """

        report = {}

        total_rows = len(dataframe)

        for column in dataframe.columns:

            series = dataframe[column]

            missing = int(series.isnull().sum())

            report[column] = {
                "count": missing,
                "percentage": round(
                    (missing / total_rows) * 100,
                    2,
                ),
            }

        return report

    # ------------------------------------------------------------------ #

    def _duplicate_analysis(
        self,
        dataframe: pd.DataFrame
    ) -> dict:
        """
        Analyze duplicate rows.
        """

        duplicates = int(dataframe.duplicated().sum())

        return {
            "count": duplicates,
            "percentage": round(
                (duplicates / len(dataframe)) * 100,
                2,
            ),
        }

    # ------------------------------------------------------------------ #

    def _datatype_analysis(
        self,
        dataframe: pd.DataFrame
    ) -> dict:
        """
        Categorize columns by datatype.
        """

        report = {
            "numeric": [],
            "categorical": [],
            "datetime": [],
        }

        for column in dataframe.columns:

            series = dataframe[column]

            if pd.api.types.is_numeric_dtype(series):

                report["numeric"].append(column)

            elif pd.api.types.is_datetime64_any_dtype(series):

                report["datetime"].append(column)

            else:

                report["categorical"].append(column)

        return report

    # ------------------------------------------------------------------ #

    def _numeric_statistics(
        self,
        dataframe: pd.DataFrame
    ) -> dict:
        """
        Compute descriptive statistics for numeric columns.
        """

        report = {}

        numeric_df = dataframe.select_dtypes(include="number")

        for column in numeric_df.columns:

            series = numeric_df[column]

            if series.dropna().empty:

                report[column] = {
                    "minimum": None,
                    "maximum": None,
                    "mean": None,
                    "median": None,
                    "std": None,
                    "variance": None,
                    "skewness": None,
                    "kurtosis": None,
                }

                continue

            report[column] = {
                "minimum": float(series.min()),
                "maximum": float(series.max()),
                "mean": float(series.mean()),
                "median": float(series.median()),
                "std": float(series.std()),
                "variance": float(series.var()),
                "skewness": float(series.skew()),
                "kurtosis": float(series.kurt()),
            }

        return report

    # ------------------------------------------------------------------ #

    def _categorical_statistics(
        self,
        dataframe: pd.DataFrame
    ) -> dict:
        """
        Compute descriptive statistics for categorical columns.
        """

        report = {}

        categorical_df = dataframe.select_dtypes(
            include=["object", "category"]
        )

        for column in categorical_df.columns:

            series = categorical_df[column]

            value_counts = series.value_counts(dropna=False)

            mode = series.mode(dropna=False)

            report[column] = {
                "unique_count": int(series.nunique(dropna=True)),
                "most_frequent": (
                    mode.iloc[0]
                    if not mode.empty
                    else None
                ),
                "top_frequency": (
                    int(value_counts.iloc[0])
                    if not value_counts.empty
                    else 0
                ),
            }

        return report

    # ------------------------------------------------------------------ #

    def _datetime_statistics(
        self,
        dataframe: pd.DataFrame
    ) -> dict:
        """
        Compute statistics for datetime columns.
        """

        report = {}

        datetime_df = dataframe.select_dtypes(
            include=["datetime64[ns]", "datetime64"]
        )

        for column in datetime_df.columns:

            series = datetime_df[column].dropna()

            if series.empty:

                report[column] = {
                    "minimum": None,
                    "maximum": None,
                    "range_days": None,
                }

                continue

            report[column] = {
                "minimum": str(series.min()),
                "maximum": str(series.max()),
                "range_days": int(
                    (series.max() - series.min()).days
                ),
            }

        return report