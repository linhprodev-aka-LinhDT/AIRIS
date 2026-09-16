"""Download the AIRIS training dataset from Roboflow Universe."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from roboflow import Roboflow


DEFAULT_WORKSPACE = "kyunghee-university-ada5d"
DEFAULT_PROJECT = "smoking-detection-3gefl"
DEFAULT_FORMAT = "yolov8"
DEFAULT_OUTPUT = Path(__file__).resolve().parents[1] / "data" / "dataset"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a Roboflow Universe dataset")
    parser.add_argument("--version", type=int, required=True, help="Roboflow dataset version to download")
    parser.add_argument("--workspace", default=DEFAULT_WORKSPACE)
    parser.add_argument("--project", default=DEFAULT_PROJECT)
    parser.add_argument("--format", default=DEFAULT_FORMAT, dest="dataset_format")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    api_key = os.environ.get("ROBOFLOW_API_KEY")
    if not api_key:
        raise SystemExit(
            "ROBOFLOW_API_KEY is not set. Create a Roboflow API key and set it in PowerShell "
            "with: $env:ROBOFLOW_API_KEY = 'your-key'"
        )

    args.output.mkdir(parents=True, exist_ok=True)
    roboflow = Roboflow(api_key=api_key)
    project = roboflow.workspace(args.workspace).project(args.project)
    version = project.version(args.version)
    dataset = version.download(args.dataset_format, location=str(args.output), overwrite=True)

    print(f"Downloaded {args.workspace}/{args.project}/{args.version}")
    print(f"Format: {args.dataset_format}")
    print(f"Location: {dataset.location}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())