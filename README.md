# Flask JWT Auth [POC]

A Flask based JWT Auth system

### What is this repository for?

- A micro-service based application to cover the requirement of an Auth System
- Adds `pytest` for unit testing.

## How do you get set up?

### How to set up

To set-up the project locally you need to clone this repo, from `master` or `develop` branch or some latest `TAG`

- install `pipenv` if you don't have already

### Directory Structure

- **Root**: `ap-auth-service`
- **Source-Code**: `ap-auth-service/src`
- **Tests Directory**: `ap-auth-service/tests`

### Configuration

Set environment variables:

- `cp .env.example .env`

Update `.env` at roor according to your settings

Please sync and resolve dependencies by using

- **`pipenv install`**
- Activate `virtual environment` by running **`pipenv shell`**

### Run App

- `flask run`

### Test App

- Run **`pytest`**
  OR
- Run **`pytest -vs`** with vorbose and print-logs
  OR
- Run **`pytest --cov-report term-missing --cov=src --cov-report=html -v && open htmlcov/index.html`** to open unit test coverage report

### Execute pre-commit quality checks

- Run **`pre-commit run --all-files`**

## System Requirements

- [Python 3.8](https://www.python.org/downloads/release/python-383/)
- [VS Code](https://code.visualstudio.com/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Flask-JWT-Extended](https://pypi.org/project/Flask-JWT-Extended/)
- [PipEnv](https://pypi.org/project/pipenv/)
- [pytest](https://pypi.org/project/pytest/)
- [Bitbicket](www.bitbucket.org)
- [Bitbicket-pipelines](https://bitbucket.org/product/features/pipelines)

## Dependencies

- See [`PipFile`](/PipFile)

## Distribution

### Postman Environments

- DEV: https://www.dropbox.com/s/axjle3fdzee9t7d/%5Benv-dev%5D%20alethea.postman_environment.json?dl=0

### Postman Collection

- Download Collection: https://www.getpostman.com/collections/4778cbfb898d356bfc96
