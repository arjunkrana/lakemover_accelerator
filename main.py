import os
import logging

from connectors.postgres_connector import (
    get_connection
)

from connectors.lakebase_connector import (
    get_lakebase_connection
)

from assessment.metadata_extractor import (
    get_tables
)

from assessment.validators.naming_validator import (
    validate_table_names
)

from assessment.validators.extension_validator import (
    validate_extensions
)

from assessment.validators.null_byte_validator import (
    validate_null_bytes
)

from assessment.validators.procedure_validator import (
    validate_procedures
)

from assessment.validators.table_size_validator import (
    validate_table_size
)

from assessment.validators.trigger_validator import (
    validate_triggers
)

from assessment.validators.datatype_validator import (
    validate_datatypes
)

from assessment.readiness_score import (
    calculate_readiness_score
)

from assessment.report.report_generator import (
    generate_report
)

from migration.schema_migrator import (
    migrate_schema
)

from migration.batch_loader import (
    migrate_in_batches
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

from migration.rollback_manager import (
    rollback_table
)

from validation.sample_diff_validator import (
    validate_sample_diff
)

from audit.audit_logger import (
    log_audit_event
)

from parallel_run.drift_detector import (
    detect_drift
)

from pipeline_migration.sql_parser import (
    get_sql_files,
    parse_sql_script
)

from pipeline_migration.sql_validator import (
    validate_sql
)

from pipeline_migration.sql_converter import (
    convert_sql
)

from pipeline_migration.dependency_analyzer import (
    analyze_dependencies
)

from pipeline_migration.pipeline_report_generator import (
    generate_pipeline_report
)

# ==========================================
# LOGGING CONFIGURATION
# ==========================================

logging.basicConfig(
    filename="logs/assessment.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

print("\nStarting Migration Accelerator")

logging.info(
    "Migration Accelerator Started"
)

# ==========================================
# SOURCE CONNECTION
# ==========================================

print("\nConnecting Source PostgreSQL")

source_engine = get_connection()

print("Source Connected")

logging.info(
    "Source PostgreSQL Connected"
)

# ==========================================
# LAKEBASE CONNECTION
# ==========================================

print("\nConnecting Lakebase")

lakebase_engine = get_lakebase_connection()

print("Lakebase Connected")

logging.info(
    "Lakebase Connected"
)

# ==========================================
# EXTRACT TABLES
# ==========================================

print("\nExtracting Metadata")

tables_df = get_tables(source_engine)

print(
    f"Tables Detected: {len(tables_df)}"
)

logging.info(
    f"Tables Extracted: {len(tables_df)}"
)

# ==========================================
# RUN ASSESSMENT VALIDATORS
# ==========================================

findings = []

print("\nRunning Assessment Validators")

logging.info(
    "Assessment Started"
)

findings.extend(
    validate_table_names(tables_df)
)

findings.extend(
    validate_extensions(source_engine)
)

findings.extend(
    validate_datatypes(source_engine)
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

logging.info(
    "Assessment Completed"
)

# ==========================================
# READINESS SCORE
# ==========================================

score = calculate_readiness_score(
    findings
)

print(
    f"\nReadiness Score: {score}%"
)

logging.info(
    f"Readiness Score: {score}"
)

# ==========================================
# GENERATE REPORT
# ==========================================

generate_report(
    findings,
    score
)

logging.info(
    "Assessment Report Generated"
)

# ==========================================
# AUDIT LOGGING
# ==========================================

log_audit_event(
    "ASSESSMENT",
    "SUCCESS",
    {
        "readiness_score": score,
        "total_findings": len(findings)
    }
)

# ==========================================
# SQL PIPELINE MIGRATION ASSESSMENT
# ==========================================

print("\nStarting SQL Pipeline Assessment")

pipeline_path = input(
    "\nEnter SQL pipeline folder path "
    "(press enter to skip): "
).strip()

all_parsed_statements = []

if pipeline_path:

    if os.path.exists(pipeline_path):

        sql_files = get_sql_files(
            pipeline_path
        )

        print(
            f"\nSQL Files Detected: "
            f"{len(sql_files)}"
        )

        for sql_file in sql_files:

            parsed_statements = parse_sql_script(
                sql_file
            )

            all_parsed_statements.extend(
                parsed_statements
            )

        print("\nParsed SQL Statements")

        for stmt in all_parsed_statements:

            print(stmt)

        # ==================================
        # SQL VALIDATION
        # ==================================

        validation_findings = validate_sql(
            all_parsed_statements
        )

        print("\nSQL Validation Findings")

        for finding in validation_findings:

            print(finding)

        # ==================================
        # DEPENDENCY ANALYSIS
        # ==================================

        dependencies = analyze_dependencies(
            all_parsed_statements
        )

        print("\nDependency Analysis")

        for dependency in dependencies:

            print(dependency)

        # ==================================
        # SQL CONVERSION
        # ==================================

        converted_sql_statements = []

        for stmt in all_parsed_statements:

            converted_sql = convert_sql(
                stmt["statement"]
            )

            converted_sql_statements.append(
                converted_sql
            )

        print("\nConverted SQL Statements")

        for sql in converted_sql_statements:

            print(sql)

        # ==================================
        # GENERATE PIPELINE REPORT
        # ==================================

        generate_pipeline_report(
            all_parsed_statements,
            validation_findings,
            dependencies
        )

        print(
            "\nPipeline Migration Report Generated"
        )

        logging.info(
            "SQL Pipeline Assessment Completed"
        )

    else:

        print(
            "\nPipeline path does not exist"
        )

        logging.warning(
            "Invalid pipeline path"
        )

else:

    print(
        "\nPipeline assessment skipped"
    )

# ==========================================
# MIGRATION DECISION
# ==========================================

blockers = [
    finding
    for finding in findings
    if finding["severity"] == "BLOCKER"
]

warnings = [
    finding
    for finding in findings
    if finding["severity"] == "WARNING"
]

print("\nAssessment Summary")

print(
    f"Readiness Score: {score}%"
)

print(
    f"Blockers: {len(blockers)}"
)

print(
    f"Warnings: {len(warnings)}"
)

if blockers:

    print(
        "\nBlocker Findings Detected:"
    )

    for blocker in blockers:

        print(
            f"- {blocker['issue']}"
        )

    proceed = input(
        "\nDo you want to continue "
        "migration? (yes/no): "
    ).strip().lower()

    if proceed != "yes":

        print(
            "\nMigration stopped by user"
        )

        logging.warning(
            "Migration stopped by user"
        )

        exit()

# ==========================================
# SCHEMA MIGRATION
# ==========================================

print("\nStarting Schema Migration")

logging.info(
    "Schema Migration Started"
)

try:

    retry_operation(
        migrate_schema,
        retries=3,
        delay=5,
        source_engine=source_engine,
        lakebase_engine=lakebase_engine
    )

    print(
        "Schema Migration Completed"
    )

    logging.info(
        "Schema Migration Completed"
    )

except Exception as error:

    logging.error(
        f"Schema Migration Failed: {error}"
    )

    print(
        f"Schema Migration Failed: {error}"
    )

    log_audit_event(
        "SCHEMA_MIGRATION",
        "FAILED",
        {
            "error": str(error)
        }
    )

    exit()

# ==========================================
# DATA MIGRATION
# ==========================================

print("\nStarting Data Migration")

logging.info(
    "Data Migration Started"
)

for _, row in tables_df.iterrows():

    table_name = row["table_name"]

    print(
        f"\nProcessing Table: {table_name}"
    )

    logging.info(
        f"Processing Table: {table_name}"
    )

    try:

        # ==================================
        # DATA MIGRATION
        # ==================================

        retry_operation(
            migrate_in_batches,
            retries=3,
            delay=5,
            source_engine=source_engine,
            lakebase_engine=lakebase_engine,
            table_name=table_name
        )

        print(
            "Data Migration Completed"
        )

        # ==================================
        # ROW VALIDATION
        # ==================================

        row_validation = validate_row_counts(
            source_engine,
            lakebase_engine,
            table_name
        )

        print("\nRow Validation")
        print(row_validation)

        # ==================================
        # DRIFT DETECTION
        # ==================================

        if row_validation.get("status") == "PASS":

            drift_result = detect_drift(
                row_validation["source_count"],
                row_validation["target_count"]
            )

        else:

            drift_result = {
                "status": "SKIPPED"
            }

        print("\nDrift Detection")
        print(drift_result)

        # ==================================
        # CHECKSUM VALIDATION
        # ==================================

        checksum_validation = validate_checksums(
            source_engine,
            lakebase_engine,
            table_name
        )

        print("\nChecksum Validation")
        print(checksum_validation)

        # ==================================
        # SAMPLE DIFF VALIDATION
        # ==================================

        sample_validation = validate_sample_diff(
            source_engine,
            lakebase_engine,
            table_name
        )

        print("\nSample Diff Validation")
        print(sample_validation)

        # ==================================
        # FINAL STATUS
        # ==================================

        row_status = row_validation.get(
            "status",
            "FAILED"
        )

        checksum_status = checksum_validation.get(
            "status",
            "FAILED"
        )

        sample_status = sample_validation.get(
            "status",
            "FAILED"
        )

        # ==================================
        # CHECKSUM WARNING
        # ==================================

        if checksum_status == "FAIL":

            print(
                "\nWARNING: "
                "Checksum mismatch detected"
            )

            logging.warning(
                f"{table_name} checksum mismatch"
            )

        # ==================================
        # SAMPLE DIFF WARNING
        # ==================================

        if sample_status == "FAIL":

            print(
                "\nWARNING: "
                "Sample diff mismatches detected"
            )

            logging.warning(
                f"{table_name} sample diff mismatch"
            )

        # ==================================
        # MIGRATION SUCCESS CRITERIA
        # ==================================

        # PRIMARY VALIDATION:
        # ROW COUNTS MUST MATCH

        if row_status == "PASS":

            migration_status = "SUCCESS"

        else:

            migration_status = "FAILED"

        # ==================================
        # CHECKPOINT
        # ==================================

        create_checkpoint(
            table_name,
            migration_status
        )

        # ==================================
        # AUDIT LOGGING
        # ==================================

        log_audit_event(
            "TABLE_MIGRATION",
            migration_status,
            {
                "table": table_name,
                "row_validation":
                row_validation,
                "drift_detection":
                drift_result,
                "checksum_validation":
                checksum_validation,
                "sample_validation":
                sample_validation
            }
        )

        # ==================================
        # ROLLBACK
        # ==================================

        if migration_status == "FAILED":

            rollback_table(
                lakebase_engine,
                table_name
            )

            print(
                f"Rollback Completed: "
                f"{table_name}"
            )

            logging.warning(
                f"Rollback completed: "
                f"{table_name}"
            )

    except Exception as error:

        logging.error(
            f"{table_name} migration failed: "
            f"{error}"
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

        log_audit_event(
            "TABLE_MIGRATION",
            "FAILED",
            {
                "table": table_name,
                "error": str(error)
            }
        )

        rollback_table(
            lakebase_engine,
            table_name
        )

        print(
            f"Rollback Completed: "
            f"{table_name}"
        )

# ==========================================
# FINAL COMPLETION
# ==========================================

print(
    "\nMigration Accelerator Completed"
)

logging.info(
    "Migration Accelerator Completed"
)

log_audit_event(
    "MIGRATION_ACCELERATOR",
    "SUCCESS",
    {
        "tables_processed":
        len(tables_df)
    }
)