from community_of_python_flake8_plugin.violation_codes import (
    VIOLATION_CODES,
    get_all_violation_codes,
    get_violation_description,
)


def test_violation_codes_structure() -> None:
    """Test that all violation codes have the required structure."""
    for violation in VIOLATION_CODES:
        assert "code" in violation
        assert "description" in violation
        assert violation["code"].startswith("COP")
        assert len(violation["description"]) > 0


def test_get_all_violation_codes() -> None:
    """Test that get_all_violation_codes returns all codes."""
    codes = get_all_violation_codes()
    assert len(codes) == len(VIOLATION_CODES)
    assert all(code.startswith("COP") for code in codes)
    assert codes == sorted(codes)  # Should be in order


def test_get_violation_description() -> None:
    """Test getting descriptions for violation codes."""
    assert get_violation_description("COP001") == "Use module import when importing more than two names"
    assert get_violation_description("COP010") == "Use dataclasses with kw_only=True, slots=True, frozen=True"
    assert get_violation_description("INVALID") is None


def test_all_codes_are_present() -> None:
    """Test that all COP001-COP010 codes are present."""
    expected_codes = [f"COP{i:03d}" for i in range(1, 11)]
    actual_codes = get_all_violation_codes()
    assert actual_codes == expected_codes