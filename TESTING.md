# Testing Reliafy CLI

This document describes the test structure and how to run tests locally.

## Test Structure

### Unit Tests

Located in `tests/`, unit tests validate CLI command routing and option handling without hitting the live API.

- `test_cli_commands_problem_file.py` — Verifies that the `--problem-file` option is correctly routed to `run_app()` for `analyze`, `design`, and `simulate` commands.
- `test_cli_main.py` — General CLI behavior validation.
- `test_profile_management.py` — Profile creation, editing, and listing.

**Run with:**
```zsh
python -m unittest discover tests -p 'test_*.py' -v
```

### Integration Tests

Located in `tests/test_cli_api_integration.py`, integration tests run real commands against the live API and validate output files.

**Prerequisites:**
- Valid authentication token (runs `reliafy analyze default --help` or similar to trigger login if needed)
- Internet access to the API endpoint
- Sufficient rate limit quota (see below)

**Run with:**
```zsh
RELIAFY_RUN_API_TESTS=1 python -m unittest tests.test_cli_api_integration -v
```

By default, integration tests are skipped unless `RELIAFY_RUN_API_TESTS=1` is set.

## Rate Limiting

The Reliafy API enforces a per-user rate limit of **10 requests per minute**. Integration tests respect this by inserting a **7-second delay** between each command invocation, ensuring the 7-command test suite completes in under 1 minute without exceeding the limit.

If you modify integration tests to add new examples, preserve the `time.sleep(7)` call after each test example loop to avoid hitting rate limits.

## Contributing

At this time, external code contributions are not accepted directly. If you find a bug or have a feature request, please open an issue on the repository.

## Local Development

To set up a development environment:

```zsh
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install in editable mode with test dependencies
pip install -e .
pip install pytest unittest

# Run tests
python -m unittest discover tests -p 'test_*.py' -v
```
