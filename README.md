# Michael Bilow EqualExperts Code Test

## Testing

I use `poetry` as the package manager, `pytest` for tests, and `coverage`.
Code is formatted with `black`. The following commands will run tests
and generate a coverage report.

```
$ poetry install
$ poetry run pytest
$ poetry run coverage run -m pytest
$ poetry run coverage report
$ poetry run coverage html
$ open htmlcov/index.html
```