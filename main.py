from src.core.business_state import BusinessState
from src.core.excel_engine import ExcelEngine
from src.core.audit_engine import AuditEngine
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():

    logger.info("ProfitPilot started.")

    try:

        state = BusinessState()

        engine = ExcelEngine()

        file_path = "datasets/superstore.csv"

        engine.load_file(file_path)

        audit_engine = AuditEngine()

        audit_report = audit_engine.audit(engine.dataframe)

        state.set_dataset(
            dataframe=engine.dataframe,
            schema=engine.schema,
            audit_report=audit_report,
        )

        print("=" * 60)
        print("ProfitPilot")
        print("=" * 60)

        print(f"Dataset : {engine.file_path.name}")
        print(f"Rows     : {state.schema['row_count']}")
        print(f"Columns  : {state.schema['column_count']}")

        summary = state.audit_report["dataset_summary"]

        print("\nDataset Summary")
        print("-" * 40)
        print(f"Rows       : {summary['rows']}")
        print(f"Columns    : {summary['columns']}")
        print(f"Memory(MB) : {summary['memory_mb']}")

        logger.info("ProfitPilot completed successfully.")

    except Exception:
        logger.exception("ProfitPilot execution failed.")
        raise


if __name__ == "__main__":
    main()