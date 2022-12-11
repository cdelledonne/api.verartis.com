#!/usr/bin/env bash

REPO_PATH=$(git rev-parse --show-toplevel)
APP_PATH=${REPO_PATH}/app

# Format app files using isort and Black
pipenv run isort "${APP_PATH}"
pipenv run black "${APP_PATH}"
