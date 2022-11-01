@REM `-e py` is a predefined environment factor. See https://tox.wiki/en/latest/config.html#tox-environments
@python -m pip install tox --quiet --constraint constraints.txt  --disable-pip-version-check && tox -e py,check_formatting --quiet --parallel
