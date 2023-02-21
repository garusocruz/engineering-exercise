#!/usr/bin/env bash

docker compose run --rm \
    --entrypoint "/bin/bash -c" \
    app "
    COVERAGE_PROCESS_START=/app/.coveragerc && \
    pip install coverage && \
    coverage erase && \
    coverage run -m pytest -s && coverage report && coverage html"
