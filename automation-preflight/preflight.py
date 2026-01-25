#!/usr/bin/env python3
"""Automation Preflight Validation Tool - CLI entry point."""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

from core.inventory import load_inventory
from core.connection import get_device_facts
from core.validator import validate_devices
from models.device import DeviceFacts, ValidationReport

# Setup logging directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=str(LOG_DIR / "preflight.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def format_text_output(report: ValidationReport) -> str:
    """
    Format validation report as human-readable text.

    Args:
        report: ValidationReport object

    Returns:
        Formatted text string
    """
    lines = ["=== Preflight Validation Results ===\n"]

    for device_result in report.devices:
        status_symbol = "✓" if device_result.status == "pass" else "✗"
        status_text = "PASS" if device_result.status == "pass" else "FAIL"

        lines.append(
            f"Device: {device_result.hostname} ({device_result.ip})"
        )
        lines.append(f"Status: {status_symbol} {status_text}")

        if device_result.connection_error:
            lines.append(f"  ✗ Connection failed: {device_result.connection_error}")
        else:
            for check_name, check_result in device_result.checks.items():
                check_symbol = "✓" if check_result.status == "pass" else "✗"
                check_display = check_name.replace("_", " ").title()

                if check_result.status == "pass":
                    lines.append(f"  {check_symbol} {check_display} present")
                else:
                    lines.append(
                        f"  {check_symbol} {check_display}: {check_result.reason}"
                    )

        lines.append("")

    lines.append("=== Summary ===")
    lines.append(f"Total devices: {report.summary.total}")
    lines.append(f"Passed: {report.summary.passed}")
    lines.append(f"Failed: {report.summary.failed}")

    return "\n".join(lines)


def format_json_output(report: ValidationReport) -> str:
    """
    Format validation report as JSON.

    Args:
        report: ValidationReport object

    Returns:
        JSON string
    """
    report_dict = report.model_dump()
    return json.dumps(report_dict, indent=2)


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Validate network device readiness before automation runs"
    )
    parser.add_argument(
        "--inventory",
        default="config/inventory.yaml",
        help="Path to inventory YAML file (default: config/inventory.yaml)",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Use mock device facts instead of connecting (safe for demos)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate configuration without connecting (same as --mock)",
    )
    parser.add_argument(
        "--output-format",
        choices=["text", "json"],
        default="text",
        help="Output format: text (default) or json",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)",
    )

    args = parser.parse_args()

    logging.getLogger().setLevel(getattr(logging, args.log_level))

    use_mock = args.mock or args.dry_run

    if args.dry_run:
        logger.info("Dry-run mode: using mock facts")

    try:
        devices = load_inventory(args.inventory)
        logger.info(f"Loaded {len(devices)} devices from inventory")

        if not devices:
            logger.error("No devices found in inventory")
            print("Error: No devices found in inventory", file=sys.stderr)
            return 2

        facts_list = []
        connection_errors = {}

        for device in devices:
            try:
                if use_mock:
                    facts = get_device_facts(device, mock=True)
                else:
                    facts = get_device_facts(device, mock=False)
                facts_list.append(facts)
            except Exception as e:
                logger.error(
                    f"Failed to collect facts from {device.hostname}: {e}",
                    exc_info=True,
                )
                connection_errors[device.hostname] = str(e)
                facts_list.append(
                    DeviceFacts(
                        hostname=device.hostname,
                        os_version=None,
                        uptime=None,
                        variables=device.model_dump(),
                    )
                )

        report = validate_devices(devices, facts_list, connection_errors)

        if args.output_format == "json":
            output = format_json_output(report)
        else:
            output = format_text_output(report)

        print(output)

        if report.summary.failed > 0:
            logger.warning(
                f"Validation completed with {report.summary.failed} device(s) failing"
            )
            return 1
        else:
            logger.info("All devices passed validation")
            return 0

    except FileNotFoundError as e:
        logger.error(f"Inventory file not found: {e}")
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
