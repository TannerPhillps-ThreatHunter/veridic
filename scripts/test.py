"""Dependency-free Veridic test runner."""

from __future__ import annotations

import importlib.util
import inspect
import sys
import traceback
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

sys.path.insert(
    0,
    str(SRC),
)

TEST_ROOT = ROOT / "tests"


def load_module(path: Path):
    name = (
        "veridic_test_"
        + path.stem
    )

    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"Unable to load {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(module)

    return module


def main() -> int:
    passed = 0
    failed = 0

    for path in sorted(
        TEST_ROOT.glob("test_*.py")
    ):
        module = load_module(path)

        functions = [
            (name, value)
            for name, value
            in vars(module).items()
            if (
                name.startswith("test_")
                and inspect.isfunction(value)
            )
        ]

        for name, function in sorted(functions):
            signature = inspect.signature(
                function
            )

            if signature.parameters:
                print(
                    f"\nUNSUPPORTED {path.name}::{name}"
                )
                print(
                    "Native test functions must "
                    "take zero arguments."
                )
                failed += 1
                continue

            try:
                function()
            except BaseException:
                print(
                    f"\nFAIL {path.name}::{name}"
                )
                traceback.print_exc()
                failed += 1
            else:
                print(
                    ".",
                    end="",
                    flush=True,
                )
                passed += 1

    print()
    print()
    print(
        f"{passed} passed, "
        f"{failed} failed"
    )

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
