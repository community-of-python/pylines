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

ignored_prefixes = {
    "avoid_magic_",
    "class_design_",
    "control_flow_",
    "exception_prefer_check_",
    "exception_try_block_",
    "immutability_class_",
    "immutability_final_",
    "immutability_mapping_",
    "module_import_",
    "narrow_types_",
    "no_scalar_annotation_",
    "pep257_",
    "pep526_",
    "pep8_import_",
    "regex_",
    "resilience_",
    "safe_index_",
    "safe_index_error_",
    "self_documenting_",
    "variable_name_",
    "zen_",
}


@pytest.mark.parametrize("file_path", files, ids=[
    one_file.name for one_file in files
])
def test_code_style(file_path: Path):
    if any(file_path.name.startswith(prefix) for prefix in ignored_prefixes):
        return

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
