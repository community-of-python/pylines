import subprocess
from pathlib import Path

import pytest

files = sorted(
    [
        path
        for path in Path(__file__).parent.parent.joinpath("src/code_style_tests/").glob("*.py")
        if path.name not in {"__init__.py", "regex_incorrect.py", "safe_index_incorrect.py", "safe_index_correct.py"}
    ]
)



@pytest.mark.parametrize("file_path", files, ids=[
    one_file.name for one_file in files
])
def test_code_style(file_path: Path):
    is_correct = file_path.name.endswith("_correct.py")
    linters_failed = False

    lint_output = ""

    try:
        result = subprocess.run(
            [
                "just",
                "check-file",
                str(file_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        lint_output = result.stdout + result.stderr
    except subprocess.CalledProcessError as error:
        linters_failed = True
        lint_output = (error.stdout or "") + (error.stderr or "")

    if is_correct:
        assert not linters_failed, (
            "Linters should pass for correct files.\n"
            f"File: {file_path}\n"
            f"Output:\n{lint_output}"
        )
    else:
        assert linters_failed, (
            "Linters should fail for incorrect files.\n"
            f"File: {file_path}\n"
            f"Output:\n{lint_output}"
        )
