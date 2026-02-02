import subprocess
from pathlib import Path

import pytest

files = sorted(
    [
        path
        for path in Path(__file__).parent.parent.joinpath("src/code_style_tests/").glob("*.py")
        if path.name != "__init__.py"
    ]
)



@pytest.mark.parametrize("file_path", files, ids=[
    one_file.name for one_file in files
])
def test_code_style(file_path: Path):
    is_correct = file_path.name.endswith("_correct.py")
    linters_failed = False

    try:
        subprocess.run(
            [
                "just",
                "check-file",
                str(file_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as error:
        linters_failed = True
        print(error.stdout)
        print(error.stderr)

    if is_correct:
        assert not linters_failed, "Linters should pass for correct files"
    else:
        assert linters_failed, "Linters should fail for incorrect files"
