# Community of Python Flake8 Plugin - Check Files

This directory contains individual check files, each implementing a specific rule (COP error code).

## Current Checks

| File | Error Code | Description |
|------|------------|-------------|
| `cop001.py` | COP001 | Use module import when importing more than two names |
| `cop002.py` | COP002 | Import standard library modules as whole modules |
| `cop003.py` | COP003 | Avoid explicit scalar type annotations |
| `cop004.py` | COP004 | Name must be at least 8 characters |
| `cop005.py` | COP005 | Function name must be a verb |
| `cop006.py` | COP006 | Avoid get_ prefix in async function names |
| `cop007.py` | COP007 | Avoid temporary variables used only once |
| `cop008.py` | COP008 | Classes should be marked typing.final |
| `cop009.py` | COP009 | Wrap module dictionaries with types.MappingProxyType |
| `cop010.py` | COP010 | Use dataclasses with kw_only=True, slots=True, frozen=True |

## File Structure

Each check file follows this pattern:
- Contains a single class that inherits from `ast.NodeVisitor`
- Implements visit methods for the AST nodes it needs to check
- Stores violations in a `self.violations` list
- Each file is responsible for exactly one error code

## Adding New Checks

To add a new check:
1. Create a new file `copXXX.py` where XXX is the next available error code
2. Implement a check class following the pattern of existing checks
3. Add the import and instantiation in `__init__.py`
4. Add tests in the test file
5. Update this README