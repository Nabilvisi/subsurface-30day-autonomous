from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

SECRET_PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9_-]{20,}"), "OpenAI-like secret"),
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key"),
    (re.compile(r"(?i)(api[_-]?key|password)\s*=\s*['\"][^'\"]{8,}['\"]"), "hardcoded credential"),
]
BANNED_BUILTINS = {"eval", "exec", "compile", "__import__"}
BANNED_IMPORTS = {"pickle", "shelve", "marshal"}


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.issues: list[str] = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name.split(".")[0] in BANNED_IMPORTS:
                self.issues.append(f"Line {node.lineno}: banned import {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module and node.module.split(".")[0] in BANNED_IMPORTS:
            self.issues.append(f"Line {node.lineno}: banned import {node.module}")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in BANNED_BUILTINS:
            self.issues.append(f"Line {node.lineno}: banned builtin {node.func.id}()")
        if isinstance(node.func, ast.Attribute) and node.func.attr in {"run", "call", "Popen"}:
            for kw in node.keywords:
                if kw.arg == "shell" and isinstance(kw.value, ast.Constant) and kw.value.value is True:
                    self.issues.append(f"Line {node.lineno}: shell=True is prohibited")
        self.generic_visit(node)


def audit(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    for pattern, label in SECRET_PATTERNS:
        if pattern.search(text):
            issues.append(f"{path}: possible {label}")
    try:
        tree = ast.parse(text, filename=str(path))
    except SyntaxError as exc:
        return [f"{path}: syntax error: {exc}"]
    visitor = Visitor()
    visitor.visit(tree)
    issues.extend(f"{path}: {x}" for x in visitor.issues)
    return issues


def main() -> int:
    targets = [Path(x) for x in sys.argv[1:]] or [Path("app.py")]
    issues: list[str] = []
    for target in targets:
        issues.extend(audit(target))
    if issues:
        print("SECURITY GATE FAILED")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("SECURITY GATE PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
