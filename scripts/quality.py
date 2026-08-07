"""Dependency-free Veridic quality and purity gate."""

from __future__ import annotations

import ast
import compileall
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "veridic"

ALLOWED_ROOTS = (
    set(sys.stdlib_module_names)
    | {
        "__future__",
        "veridic",
    }
)


def check_imports() -> list[str]:
    violations: list[str] = []

    for path in SRC.rglob("*.py"):
        tree = ast.parse(
            path.read_text(),
            filename=str(path),
        )

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [
                    alias.name
                    for alias in node.names
                ]

            elif isinstance(
                node,
                ast.ImportFrom,
            ):
                if node.level > 0:
                    continue

                names = (
                    [node.module]
                    if node.module
                    else []
                )

            else:
                continue

            for name in names:
                root = name.split(
                    ".",
                    maxsplit=1,
                )[0]

                if root not in ALLOWED_ROOTS:
                    violations.append(
                        f"{path}: "
                        f"external import {name!r}"
                    )

    return violations


def check_whitespace() -> list[str]:
    violations: list[str] = []

    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue

        if any(
            part in {
                ".git",
                ".venv",
                "__pycache__",
            }
            for part in path.parts
        ):
            continue

        if path.suffix not in {
            ".py",
            ".md",
            ".toml",
        }:
            continue

        try:
            lines = path.read_text().splitlines()
        except UnicodeDecodeError:
            continue

        for number, line in enumerate(
            lines,
            start=1,
        ):
            if line.rstrip() != line:
                violations.append(
                    f"{path}:{number}: "
                    "trailing whitespace"
                )

    return violations


def main() -> int:
    failures: list[str] = []

    print("compile:", end=" ")

    if not compileall.compile_dir(
        ROOT / "src",
        quiet=1,
    ):
        print("FAIL")
        failures.append(
            "Python compilation failed"
        )
    else:
        print("PASS")

    print("imports:", end=" ")

    imports = check_imports()

    if imports:
        print("FAIL")
        failures.extend(imports)
    else:
        print("PASS")

    print("whitespace:", end=" ")

    whitespace = check_whitespace()

    if whitespace:
        print("FAIL")
        failures.extend(whitespace)
    else:
        print("PASS")

    if failures:
        print()
        print("QUALITY FAILURES")
        print("================")

        for failure in failures:
            print(failure)

        return 1

    print()
    print(
        "Veridic purity law satisfied."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
