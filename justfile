oxfmt_file_types := "'**/*.{js,mjs,cjs,jsx,ts,mts,cts,tsx,json,yaml,md}'"

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

# Run the test suite
test:
    python3 -m unittest

# Run the performance benchmarks
perf:
    python3 -m unittest discover -s benchmarks -p "test_*.py"; \
    status=$?; \
    echo "\n"; \
    cat benchmarks/benchmark_output.txt; \
    echo "\n"; \
    exit $status
