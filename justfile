default:
    @just --list

# Format files
fix:
    -ruff check --fix .
    ruff format .
    ruff check .

# Check linting and formatting (read-only)
check:
    ruff check .
    ruff format --check .

# Run all tests
test:
    python3 -m unittest
