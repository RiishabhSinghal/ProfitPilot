from src.analytics.analytics_engine import AnalyticsEngine
from src.core.business_state import BusinessState
from src.core.excel_engine import ExcelEngine
from src.utils.logger import get_logger

logger = get_logger(__name__)

DATASET_PATH = "datasets/superstore.csv"
SEPARATOR = "=" * 60


def main() -> None:
    """
    Entry point for ProfitPilot.
    """

    logger.info("ProfitPilot started.")

    try:
        # -------------------------------------------------------------- #
        # Initialize Business State
        # -------------------------------------------------------------- #

        state = BusinessState()

        # -------------------------------------------------------------- #
        # Load Dataset
        # -------------------------------------------------------------- #

        engine = ExcelEngine()
        engine.load_file(DATASET_PATH)

        # -------------------------------------------------------------- #
        # Run Business Analytics
        # -------------------------------------------------------------- #

        analytics_engine = AnalyticsEngine()

        analytics_report = analytics_engine.analyze(
            engine.dataframe
        )

        # -------------------------------------------------------------- #
        # Store Everything
        # -------------------------------------------------------------- #

        state.set_dataset(
            dataframe=engine.dataframe,
            schema=engine.schema,
            audit_report=engine.audit_report,
            analytics_report=analytics_report,
        )

        # -------------------------------------------------------------- #
        # Display Summary
        # -------------------------------------------------------------- #

        print(SEPARATOR)
        print("ProfitPilot")
        print(SEPARATOR)

        print(f"Dataset : {engine.file_path.name}")
        print(f"Rows    : {state.schema['row_count']}")
        print(f"Columns : {state.schema['column_count']}")

        # -------------------------------------------------------------- #
        # Dataset Summary
        # -------------------------------------------------------------- #

        summary = state.audit_report["dataset_summary"]

        print("\nDataset Summary")
        print("-" * 40)

        print(f"Rows       : {summary['rows']}")
        print(f"Columns    : {summary['columns']}")
        print(f"Memory(MB) : {summary['memory_mb']}")

        # -------------------------------------------------------------- #
        # Overview KPIs
        # -------------------------------------------------------------- #

        overview = state.analytics_report["overview"]

        print("\nOverview KPIs")
        print("-" * 40)

        print(
            f"Total Revenue        : {overview['sales']['total_revenue']}"
        )

        print(
            f"Total Profit         : {overview['profit']['total_profit']}"
        )

        print(
            f"Profit Margin (%)    : {overview['profit']['profit_margin']}"
        )

        print(
            f"Total Orders         : {overview['orders']['total_orders']}"
        )

        print(
            f"Total Customers      : {overview['customers']['total_customers']}"
        )

        print(
            f"Total Products       : {overview['products']['total_products']}"
        )

        print(
            f"Average Order Value  : {overview['sales']['average_order_value']}"
        )

        print(
            f"Average Discount     : {overview['discount']['average_discount']}"
        )

        

        profit = state.analytics_report["profit"]

        print("\nProfit Analysis")
        print("-" * 40)

        print("Profit by Region")
        print(profit["profit_by_region"])

        print("\nTop Profitable Products")
        print(profit["top_profitable_products"])

        print("\nLoss Making Products")
        print(profit["loss_making_products"])

        print("\nProfit Contribution")
        print(profit["profit_contribution"])

        sales = state.analytics_report["sales"]

        print("\nSales Analysis")
        print("-" * 40)

        print("Revenue by Region")
        print(sales["revenue_by_region"])

        print("\nRevenue by Category")
        print(sales["revenue_by_category"])

        print("\nTop Customers")
        print(sales["top_customers"])

        print("\nTop Products")
        print(sales["top_products"])

        print("\nTop Revenue Sub-categories")
        print(sales["revenue_by_subcategory"])

        logger.info("ProfitPilot completed successfully.")

    except Exception:
        logger.exception("ProfitPilot execution failed.")
        raise


if __name__ == "__main__":
    main()