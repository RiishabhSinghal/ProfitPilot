from __future__ import annotations
import pandas as pd

from src.utils.logger import get_logger


class AnalyticsEngine:
    """
    Performs business analytics on a structured dataset.

    Responsible for generating business KPIs and metrics
    that can later be interpreted by an LLM.
    """

    SALES_COLUMN = "Sales"
    PROFIT_COLUMN = "Profit"
    DISCOUNT_COLUMN = "Discount"

    ORDER_COLUMN = "Order ID"

    CUSTOMER_ID_COLUMN = "Customer ID"
    CUSTOMER_NAME_COLUMN = "Customer Name"

    PRODUCT_ID_COLUMN = "Product ID"
    PRODUCT_NAME_COLUMN = "Product Name"

    REGION_COLUMN = "Region"
    CATEGORY_COLUMN = "Category"
    SUBCATEGORY_COLUMN = "Sub-Category"
    SEGMENT_COLUMN = "Segment"

    TOP_N = 10


    def __init__(self) -> None:

        self.logger = get_logger(__name__)

    # ------------------------------------------------------------------ #

    def analyze(self, dataframe: pd.DataFrame) -> dict:
        """
        Run all analytics modules and return a consolidated report.
        """

        if dataframe is None:
            raise ValueError("Cannot analyze a None dataframe.")

        self.logger.info("Running business analytics...")

        report = {
            "overview": self._overview(dataframe),
            "sales": self._sales_analysis(dataframe),
            "profit": self._profit_analysis(dataframe),
            # "customer": self._customer_analysis(dataframe),
            # "region": self._region_analysis(dataframe),
            # "discount": self._discount_analysis(dataframe),
        }

        self.logger.info("Business analytics completed successfully.")

        return report

    # ------------------------------------------------------------------ #

    def _overview(self, dataframe: pd.DataFrame) -> dict:
        """
        Compute high-level business KPIs.
        """

        self.logger.info("Computing overview KPIs...")

        # -------------------------------------------------------------- #
        # Column Names
        # -------------------------------------------------------------- #

        sales_col = self.SALES_COLUMN
        profit_col = self.PROFIT_COLUMN
        order_col = self.ORDER_COLUMN
        customer_col = self.CUSTOMER_ID_COLUMN
        product_col = self.PRODUCT_ID_COLUMN
        discount_col = self.DISCOUNT_COLUMN

        # -------------------------------------------------------------- #
        # Basic Counts
        # -------------------------------------------------------------- #

        total_orders = dataframe[order_col].nunique()
        total_customers = dataframe[customer_col].nunique()
        total_products = dataframe[product_col].nunique()

        # -------------------------------------------------------------- #
        # Sales Metrics
        # -------------------------------------------------------------- #

        total_revenue = dataframe[sales_col].sum()

        average_order_value = (
            total_revenue / total_orders
            if total_orders
            else 0.0
        )

        # -------------------------------------------------------------- #
        # Profit Metrics
        # -------------------------------------------------------------- #

        total_profit = dataframe[profit_col].sum()

        profit_margin = (
            (total_profit / total_revenue) * 100
            if total_revenue
            else 0.0
        )

        average_profit_per_order = (
            total_profit / total_orders
            if total_orders
            else 0.0
        )

        # -------------------------------------------------------------- #
        # Discount Metrics
        # -------------------------------------------------------------- #

        average_discount = dataframe[discount_col].mean()

        self.logger.info("Overview KPIs computed successfully.")

        return {

            "sales": {
                "total_revenue": round(float(total_revenue), 2),
                "average_order_value": round(float(average_order_value), 2),
            },

            "profit": {
                "total_profit": round(float(total_profit), 2),
                "profit_margin": round(float(profit_margin), 2),
                "average_profit_per_order": round(
                    float(average_profit_per_order),
                    2,
                ),
            },

            "customers": {
                "total_customers": int(total_customers),
            },

            "orders": {
                "total_orders": int(total_orders),
            },

            "products": {
                "total_products": int(total_products),
            },

            "discount": {
                "average_discount": round(float(average_discount), 2),
            },
        }

    def _sales_analysis(self, dataframe):
        """
        Perform sales-related business analysis.
        """

        self.logger.info("Running sales analysis...")

        report = {
            "revenue_by_region": self._revenue_by_region(dataframe),
            "revenue_by_category": self._revenue_by_category(dataframe),
            "revenue_by_subcategory": self._revenue_by_subcategory(dataframe),
            "revenue_by_segment": self._revenue_by_segment(dataframe),
            "top_customers": self._top_customers(dataframe),
            "top_products": self._top_products(dataframe),
    }

        self.logger.info("Sales analysis completed.")

        return report
        
    # ------------------------------------------------------------------ #

    def _groupby_sum(
        self,
        dataframe: pd.DataFrame,
        group_column: str,
        value_column: str,
    ) -> dict:
        """
        Calculate the sum of a numeric column grouped by another column.
        """

        return (
            dataframe.groupby(group_column)[value_column]
            .sum()
            .sort_values(ascending=False)
            .round(2)
            .to_dict()
        )

    # ------------------------------------------------------------------ #

    def _top_n(
        self,
        dataframe: pd.DataFrame,
        group_column: str,
        value_column: str,
        n: int,
    ) -> dict:
        """
        Return the Top-N groups ranked by the sum of a numeric column.
        """

        return (
            dataframe.groupby(group_column)[value_column]
            .sum()
            .sort_values(ascending=False)
            .head(n)
            .round(2)
            .to_dict()
        )

    # ------------------------------------------------------------------ #

    def _revenue_by_region(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Calculate total revenue generated by each region.
        """

        return self._groupby_sum(
            dataframe,
            group_column=self.REGION_COLUMN,
            value_column=self.SALES_COLUMN,
        )

    # ------------------------------------------------------------------ #

    def _revenue_by_category(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Calculate total revenue generated by each product category.
        """
        return self._groupby_sum(
            dataframe,
            group_column=self.CATEGORY_COLUMN,
            value_column=self.SALES_COLUMN,
        )

    # ------------------------------------------------------------------ #

    def _revenue_by_subcategory(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Calculate total revenue generated by each product sub-category.
        """
        return self._groupby_sum(
            dataframe,
            group_column=self.SUBCATEGORY_COLUMN,
            value_column=self.SALES_COLUMN,
        ) 

    # ------------------------------------------------------------------ #

    def _revenue_by_segment(
    self,
    dataframe: pd.DataFrame,
    ) -> dict:
        """
        Calculate total revenue generated by each customer segment.
        """

        return self._groupby_sum(
            dataframe,
            group_column=self.SEGMENT_COLUMN,
            value_column=self.SALES_COLUMN,
        )   

    # ------------------------------------------------------------------ #

    def _top_customers(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Return the top customers ranked by revenue.
    """

        return self._top_n(
            dataframe,
            group_column=self.CUSTOMER_NAME_COLUMN,
            value_column=self.SALES_COLUMN,
            n=self.TOP_N,
        )

    # ------------------------------------------------------------------ #

    def _top_products(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Return the top products ranked by revenue.
        """

        return self._top_n(
            dataframe,
            group_column=self.PRODUCT_NAME_COLUMN,
            value_column=self.SALES_COLUMN,
            n=self.TOP_N,
        )

    def _profit_analysis(self, dataframe: pd.DataFrame) -> dict:
        """
        Perform profit-related business analysis.
        """

        self.logger.info("Running profit analysis...")

        report = {
            "profit_by_region": self._profit_by_region(dataframe),
            "profit_by_category": self._profit_by_category(dataframe),
            "profit_by_subcategory": self._profit_by_subcategory(dataframe),
            "profit_by_segment": self._profit_by_segment(dataframe),
            "top_profitable_customers": self._top_profitable_customers(dataframe),
            "top_profitable_products": self._top_profitable_products(dataframe),
            "loss_making_products": self._loss_making_products(dataframe),
            "loss_making_categories": self._loss_making_categories(dataframe),
            "profit_contribution": self._profit_contribution(dataframe),
        }

        self.logger.info("Profit analysis completed successfully.")

        return report

    def _negative_values(
        self,
        dataframe: pd.DataFrame,
        group_column: str,
        value_column: str,
    ) -> dict:
        """
        Return groups having a negative aggregated value.
        """

        report = (
            dataframe.groupby(group_column)[value_column]
            .sum()
            .loc[lambda x: x < 0]
            .sort_values()
            .round(2)
            .to_dict()
        )

        return report

    def _profit_by_region(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Calculate profit generated by each region.
        """

        return self._groupby_sum(
            dataframe,
            group_column=self.REGION_COLUMN,
            value_column=self.PROFIT_COLUMN,
        )

    def _profit_by_category(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Calculate profit generated by each category.
        """

        return self._groupby_sum(
            dataframe,
            group_column=self.CATEGORY_COLUMN,
            value_column=self.PROFIT_COLUMN,
        )

    def _profit_by_subcategory(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Calculate profit generated by each sub-category.
        """

        return self._groupby_sum(
            dataframe,
            group_column=self.SUBCATEGORY_COLUMN,
            value_column=self.PROFIT_COLUMN,
        )

    def _profit_by_segment(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Calculate profit generated by each customer segment.
        """

        return self._groupby_sum(
            dataframe,
            group_column=self.SEGMENT_COLUMN,
            value_column=self.PROFIT_COLUMN,
        )

    def _top_profitable_customers(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Return the top N customers ranked by profit.
        """

        return self._top_n(
            dataframe,
            group_column=self.CUSTOMER_NAME_COLUMN,
            value_column=self.PROFIT_COLUMN,
            n=self.TOP_N,
        )

    def _top_profitable_products(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Return the top products by profit.
        """

        return self._top_n(
            dataframe,
            group_column=self.PRODUCT_NAME_COLUMN,
            value_column=self.PROFIT_COLUMN,
            n=self.TOP_N,
        )

    def _loss_making_products(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Identify products generating losses.
        """

        return self._negative_values(
            dataframe,
            group_column=self.PRODUCT_NAME_COLUMN,
            value_column=self.PROFIT_COLUMN,
        )

    def _loss_making_categories(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Identify categories generating losses.
        """

        return self._negative_values(
            dataframe,
            group_column=self.CATEGORY_COLUMN,
            value_column=self.PROFIT_COLUMN,
        )

    def _profit_contribution(
        self,
        dataframe: pd.DataFrame,
    ) -> dict:
        """
        Calculate percentage contribution of each category
        to the overall profit.
        """

        profit = (
            dataframe.groupby(self.CATEGORY_COLUMN)[self.PROFIT_COLUMN]
            .sum()
        )

        total_profit = profit.sum()

        contribution = (
            (profit / total_profit) * 100
        ).round(2)

        return (
            contribution
            .sort_values(ascending=False)
            .to_dict()
        )

