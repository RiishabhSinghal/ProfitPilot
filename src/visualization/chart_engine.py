from __future__ import annotations

from pathlib import Path

import plotly.express as px
from plotly.graph_objects import Figure

from src.utils.logger import get_logger


class ChartEngine:
    """
    Generates business charts from analytics results.

    Responsible only for visualization.
    It does NOT perform analytics.
    """

    def __init__(self) -> None:
        self.logger = get_logger(__name__)

        self.output_dir = Path("charts")
        self.output_dir.mkdir(exist_ok=True)

        self.logger.info("ChartEngine initialized.")

    # ------------------------------------------------------------------ #
    # Private Helpers
    # ------------------------------------------------------------------ #

    def _apply_default_layout(
        self,
        figure: Figure,
    ) -> None:
        """
        Apply a consistent layout to all charts.
        """

        figure.update_layout(
            template="plotly_white",
            title_x=0.5,
        )

        figure.update_xaxes(
            tickangle=-45
        )

    # ------------------------------------------------------------------ #
    # Utility Functions
    # ------------------------------------------------------------------ #

    def save_chart(
        self,
        figure: Figure,
        folder: str,
        filename: str,
    ) -> str:
        """
        Save a Plotly figure as an HTML file.
        """

        output_dir = self.output_dir / folder
        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = output_dir / filename

        figure.write_html(output_path)

        self.logger.info(
            f"Chart saved to {output_path}"
        )

        return str(output_path)

    def show_chart(
        self,
        figure: Figure,
    ) -> None:
        """
        Display a Plotly chart.
        """

        figure.show()

    # ------------------------------------------------------------------ #
    # Bar Chart
    # ------------------------------------------------------------------ #

    def create_bar_chart(
        self,
        data: dict,
        title: str,
        x_label: str,
        y_label: str,
        folder: str,
        filename: str,
    ) -> str:
        """
        Create a bar chart from a dictionary.
        """

        if not data:
            raise ValueError(
                "Cannot create bar chart from empty data."
            )

        self.logger.info(
            f"Creating bar chart: {title}"
        )

        figure = px.bar(
            x=list(data.keys()),
            y=list(data.values()),
            title=title,
            labels={
                "x": x_label,
                "y": y_label,
            },
        )

        figure.update_traces(
            hovertemplate="%{x}<br>%{y:,.2f}<extra></extra>"
        )

        self._apply_default_layout(figure)

        return self.save_chart(
            figure=figure,
            folder=folder,
            filename=filename,
        )

    # ------------------------------------------------------------------ #
    # Line Chart
    # ------------------------------------------------------------------ #

    def create_line_chart(
        self,
        data: dict,
        title: str,
        x_label: str,
        y_label: str,
        folder: str,
        filename: str,
    ) -> str:
        """
        Create a line chart from a dictionary.
        """

        if not data:
            raise ValueError(
                "Cannot create line chart from empty data."
            )

        self.logger.info(
            f"Creating line chart: {title}"
        )

        figure = px.line(
            x=list(data.keys()),
            y=list(data.values()),
            title=title,
            labels={
                "x": x_label,
                "y": y_label,
            },
            markers=True,
        )

        figure.update_traces(
            hovertemplate="%{x}<br>%{y:,.2f}<extra></extra>"
        )

        self._apply_default_layout(figure)

        return self.save_chart(
            figure=figure,
            folder=folder,
            filename=filename,
        )

    # ------------------------------------------------------------------ #
    # Pie Chart
    # ------------------------------------------------------------------ #

    def create_pie_chart(
        self,
        data: dict,
        title: str,
        folder: str,
        filename: str,
    ) -> str:
        """
        Create a pie chart from a dictionary.
        """

        if not data:
            raise ValueError(
                "Cannot create pie chart from empty data."
            )

        self.logger.info(
            f"Creating pie chart: {title}"
        )

        figure = px.pie(
            names=list(data.keys()),
            values=list(data.values()),
            title=title,
        )

        figure.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hovertemplate="%{label}<br>%{value:,.2f}<extra></extra>",
        )

        self._apply_default_layout(figure)

        return self.save_chart(
            figure=figure,
            folder=folder,
            filename=filename,
        )