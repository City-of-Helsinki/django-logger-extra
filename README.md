# Logger extras for simplified structured logging.

`django-logger-extra` is a collection of logger extras that makes structured logging setup easier.

## Adding django-logger-extra your Django project

Add `django-logger-extra` in your project's dependencies.

### Adding django-resilient-logger Django apps

To install this logger, add `INSTALLED_APPS` in settings.py:

```python
INSTALLED_APPS = (
    'logger_extra',
    ...
)
```

### Configuring logger formatter in settings.py:
```python
LOGGING = {
    'formatters': {
        'json': {
            '()': 'logger_extra.formatter.JSONFormatter',
        }
        ...
    },
    ...
}
```

### Configuring middleware in settings.py:
```python
MIDDLEWARE = [
    'logger_extra.middleware.XRequestIdMiddleware',
    ...
]
```

# Development

Virtual Python environment can be used. For example:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install package requirements:

```bash
pip install -e .
```

Install development requirements:

```bash
pip install -r requirements-test.txt
```

## Running tests

```bash
pytest
```

## Code format

This project uses [Ruff](https://docs.astral.sh/ruff/) for code formatting and quality checking.

Basic `ruff` commands:

* lint: `ruff check`
* apply safe lint fixes: `ruff check --fix`
* check formatting: `ruff format --check`
* format: `ruff format`

[`pre-commit`](https://pre-commit.com/) can be used to install and
run all the formatting tools as git hooks automatically before a
commit.


## Git blame ignore refs

Project includes a `.git-blame-ignore-revs` file for ignoring certain commits from `git blame`.
This can be useful for ignoring e.g. formatting commits, so that it is more clear from `git blame`
where the actual code change came from. Configure your git to use it for this project with the
following command:

```shell
git config blame.ignoreRevsFile .git-blame-ignore-revs
```


## Commit message format

New commit messages must adhere to the [Conventional Commits](https://www.conventionalcommits.org/)
specification, and line length is limited to 72 characters.

When [`pre-commit`](https://pre-commit.com/) is in use, [`commitlint`](https://github.com/conventional-changelog/commitlint)
checks new commit messages for the correct format.