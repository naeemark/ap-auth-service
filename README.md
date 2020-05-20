# AletheaProduct Auth Service [ap-auth-service]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

A Flask based JWT Auth system

### What is this repository for?

- A micro-service based application to cover the requirement of an Auth System
- Adds `pytest` for unit testing.

## How do you get set up?

### How to set up

To set-up the project locally you need to clone this repo, from `master` or `develop` branch or some latest `TAG`

- Install `pipenv` if you don't have already

### Directory Structure

- **Root**: `ap-auth-service`
- **Source-Code**: `ap-auth-service/src`
- **Tests Directory**: `ap-auth-service/tests`

### Configuration

Set environment variables:

- **`cp .env.example .env`**

Update `.env` in the root directory according to your settings

Please sync and resolve `default` and `dev` dependencies by using

- **`pipenv install --dev`**
- Activate `virtual environment` by running **`pipenv shell`**
- Setup pre-commit: **`pre-commit install`**

### Test App

- Run **`pytest`**
  OR
- Run **`pytest -vs`** with vorbose and print-logs
  OR
- Run **`pytest --cov-report term-missing --cov=src --cov-report=html -v && open htmlcov/index.html`** to open unit test coverage report

### Run App

- `flask run`

### Execute pre-commit quality checks

- Run **`pre-commit run --all-files`**

  OR

- Run **`pre-commit run --all-files --show-diff-on-failure`**

_NOTE_: `pre-commit run --all-files` should always be validated before doing a code-commit. Otherwise, it could be a potential reason for **failed pipeline builds**

## System Requirements

- [Python 3.8](https://www.python.org/downloads/release/python-383/)
- [VS Code](https://code.visualstudio.com/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Flask-JWT-Extended](https://pypi.org/project/Flask-JWT-Extended/)
- [pipenv](https://pypi.org/project/pipenv/)
- [pytest](https://pypi.org/project/pytest/)
- [pre-commit](https://pre-commit.com/)
- [Bitbicket](www.bitbucket.org)
- [Bitbicket-pipelines](https://bitbucket.org/product/features/pipelines)

## Dependencies

- See [`Pipfile`](/Pipfile)

### API endpoint
- /user/register `<- require(access_token)`
- /user/login `<- require(access_token) | -> generate(fresh_access_token)`
- /user/changePassword `<- require(fresh_token)`
- /auth/StartSession `-> generate(acess_token,refresh_token)`
- /auth/refresh `<- require(refresh_token)`



## Distribution

### Postman Environments

- DEV: https://www.dropbox.com/s/axjle3fdzee9t7d/%5Benv-dev%5D%20alethea.postman_environment.json?dl=0

### Postman Collection

- Download Collection: https://www.getpostman.com/collections/4778cbfb898d356bfc96
