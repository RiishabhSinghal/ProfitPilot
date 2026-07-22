from __future__ import annotations
from src.core.business_state import BusinessState
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

    SALES_FOLDER = "sales"
    REGION_FOLDER = "region"
    TIME_FOLDER = "time"
    
    def __init__(self) -> None:
        self.logger = get_logger(__name__)

        self.output_dir = Path("charts")
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

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

    def generate_default_charts(
        self,
        state,
    ) -> None:
        """
        Generate the default set of charts
        for the current business analysis.
        """

        self.logger.info(
            "Generating default charts..."
        )

        self.generate_sales_charts(state)
        self.generate_region_charts(state)
        self.generate_time_charts(state)

        self.logger.info(
            "Default charts generated successfully."
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

    def generate_sales_charts(
        self,
        state,
    ) -> None:
        """
        Generate charts related to sales analysis.
        """

        sales = state.analytics_report["sales"]

        path = self.create_bar_chart(
            data=sales["revenue_by_region"],
            title="Revenue by Region",
            x_label="Region",
            y_label="Revenue",
            folder=self.SALES_FOLDER,
            filename="revenue_by_region.html",
        )

        state.add_chart(
            "revenue_by_region",
            path,
        )

    def generate_region_charts(
        self,
        state,
    ) -> None:
        """
        Generate charts related to region analysis.
        """

        region = state.analytics_report["region"]

        path = self.create_bar_chart(
            data=region["profit_by_region"],
            title="Profit by Region",
            x_label="Region",
            y_label="Profit",
            folder=self.REGION_FOLDER,
            filename="profit_by_region.html",
        )

        state.add_chart(
            "profit_by_region",
            path,
        )

        path = self.create_pie_chart(
            data=region["region_contribution"],
            title="Regional Revenue Contribution",
            folder=self.REGION_FOLDER,
            filename="region_contribution.html",
        )

        state.add_chart(
            "region_contribution",
            path,
        )

    def generate_time_charts(
        self,
        state,
    ) -> None:
        """
        Generate charts related to time-series analysis.
        """

        time = state.analytics_report["time"]

        path = self.create_line_chart(
            data=time["monthly_sales"],
            title="Monthly Sales Trend",
            x_label="Month",
            y_label="Sales",
            folder=self.TIME_FOLDER,
            filename="monthly_sales.html",
        )

        state.add_chart(
            "monthly_sales",
            path,
        )