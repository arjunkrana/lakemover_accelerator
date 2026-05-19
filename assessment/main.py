import logging

from connectors.postgres_connector import (
    get_connection
)

from connectors.lakebase_connector import (
    get_lakebase_connection
)

from metadata_extractor import get_tables

from validators.naming_validator import (
    validate_table_names
)

from validators.extension_validator import (
    validate_extensions
)

from validators.null_byte_validator import (
    validate_null_bytes
)

from validators.procedure_validator import (
    validate_procedures
)

from validators.table_size_validator import (
    validate_table_size
)

from validators.trigger_validator import (
    validate_triggers
)

from readiness_score import (
    calculate_readiness_score
)

from report.report_generator import (
    generate_report
)

from migration.schema_migrator import (
    migrate_schema
)

from migration.table_migrator import (
    migrate_table_data
)

from migration.validation_runner import (
    validate_row_counts
)

from migration.checkpoint_validator import (
    create_checkpoint
)

from migration.checksum_validator import (
    validate_checksums
)

from migration.retry_manager import (
    retry_operation
)

# LOGGING CONFIGURATION
logging.basicConfig(
    filename="logs/assessment.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

print("\nStarting Migration Accelerator")

logging.info("Migration Accelerator Started")

# SOURCE CONNECTION
print("\nConnecting Source PostgreSQL")

source_engine = get_connection()

print("Source Connected")

# LAKEBASE CONNECTION
print("\nConnecting Lakebase")

lakebase_engine = get_lakebase_connection()

print("Lakebase Connected")

# EXTRACT TABLES
print("\nExtracting Metadata")

tables_df = get_tables(source_engine)

print(f"Tables Detected: {len(tables_df)}")

# STORE FINDINGS
findings = []

# VALIDATIONS
print("\nRunning Assessment Validators")

findings.extend(
    validate_table_names(tables_df)
)

findings.extend(
    validate_extensions(source_engine)
)

findings.extend(
    validate_null_bytes(
        source_engine,
        tables_df
    )
)

findings.extend(
    validate_procedures(source_engine)
)

findings.extend(
    validate_table_size(source_engine)
)

findings.extend(
    validate_triggers(source_engine)
)

print("Assessment Completed")

# READINESS SCORE
score = calculate_readiness_score(
    findings
)

print(f"\nReadiness Score: {score}%")

# GENERATE REPORT
generate_report(
    findings,
    score
)

logging.info(
    f"Assessment Completed - Score: {score}"
)

# SCHEMA MIGRATION
print("\nStarting Schema Migration")

try:

    retry_operation(
        migrate_schema,
        retries=3,
        delay=5,
        source_engine=source_engine,
        lakebase_engine=lakebase_engine
    )

    print("Schema Migration Completed")

except Exception as error:

    logging.error(
        f"Schema Migration Failed: {error}"
    )

    print(
        f"Schema Migration Failed: {error}"
    )

# DATA MIGRATION
print("\nStarting Data Migration")

for _, row in tables_df.iterrows():

    table_name = row["table_name"]

    print(f"\nProcessing Table: {table_name}")

    try:

        # MIGRATE DATA
        retry_operation(
            migrate_table_data,
            retries=3,
            delay=5,
            source_engine=source_engine,
            lakebase_engine=lakebase_engine,
            table_name=table_name
        )

        # ROW COUNT VALIDATION
        row_validation = validate_row_counts(
            source_engine,
            lakebase_engine,
            table_name
        )

        print("\nRow Validation")
        print(row_validation)

        # CHECKSUM VALIDATION
        checksum_validation = validate_checksums(
            source_engine,
            lakebase_engine,
            table_name
        )

        print("\nChecksum Validation")
        print(checksum_validation)

        # CHECKPOINT STATUS
        if (
            row_validation["status"] == "PASS"
            and
            checksum_validation["status"] == "PASS"
        ):

            migration_status = "SUCCESS"

        else:

            migration_status = "FAILED"

        # CREATE CHECKPOINT
        create_checkpoint(
            table_name,
            migration_status
        )

        logging.info(
            f"{table_name} migration completed"
        )

        print(
            f"\nMigration Status: "
            f"{migration_status}"
        )

    except Exception as error:

        logging.error(
            f"{table_name} migration failed: {error}"
        )

        print(
            f"\nMigration failed for "
            f"{table_name}"
        )

        print(error)

        create_checkpoint(
            table_name,
            "FAILED"
        )

print("\nMigration Accelerator Completed")

logging.info(
    "Migration Accelerator Completed"
)