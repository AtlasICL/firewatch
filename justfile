oxfmt_file_types := "'**/*.{js,mjs,cjs,jsx,ts,mts,cts,tsx,json,yaml}'"

default:
    @just --list

# Format files
fix:
    -ruff check --fix .
    ruff format .
    ruff check .
    -npx oxlint --fix --no-error-on-unmatched-pattern
    npx oxfmt --no-error-on-unmatched-pattern {{oxfmt_file_types}}
    npx oxlint --deny-warnings --no-error-on-unmatched-pattern

# Check linting and formatting (read-only)
check:
    ruff check .
    ruff format --check .
    npx oxlint --deny-warnings --no-error-on-unmatched-pattern
    npx oxfmt --check --no-error-on-unmatched-pattern {{oxfmt_file_types}}

# Run all tests
test:
    python3 -m unittest
