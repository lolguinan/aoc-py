# Advent of Code

## Status

```
               1111111111222222
      1234567890123456789012345
2021  ggggggggggggggggggg sg gs
```

> `g` => _gold_ (two stars), `s` => _silver_ (one star)

## aoc-py

### Quickstart: Docker

Install Docker: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

Build an image:

```
docker build -t lolguinan/aoc-py .
```

Run a container:

```
docker run --rm -it lolguinan/aoc-py <run.py arguments>
```

> This passes your arguments directly to the `run.py` script inside the container.
> See _Usage_ section below for `<run.py arguments>`.

### Requirements

Requires Python 3.10 so I can finally use match-case for something (though so far it's only an extra level of indentation really).

Recommend using `pyenv-installer` on MacOS or GNU/Linux. On Windows, try WSL2 or VirtualBox. :D

[https://github.com/pyenv/pyenv-installer](https://github.com/pyenv/pyenv-installer)

Assuming a recent version of `pyenv` and `pyenv-virtualenv` are available:

```
pyenv install 3.10.0
pyenv virtualenv 3.10.0 aoc-py
pyenv activate aoc-py
```

Once you've got a virtualenv by your preferred method:

```
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

> I'm trying out this `pyproject.toml` + `setup.cfg` thing and don't know how to install packages for testing without a requirements-style file.

### Usage

Run the simple and non-comprehensive tests:

```
pytest
```

> These are extremely minimal and exist to validate the test case(s) presented in the description.

Run a particular (year, day, part):

```
python3 -m year2021.day01a
```

...but that's annoying, so instead:

```
./run.py --day 1 --part a
```

or

```
./run.py --all
```

> See `./run.py -h` for options.

### Developing

To start hacking on a new day, I recommend starting early enough that simple commands like `ssh` and `cp` are a good warm up to remember how to computer. Thus, copy a previous day's files onto a new day:

* `src/year${year}/day${day}${part}.py`
* `tests/test_day${day}${part}.py`

> Exercise left to the reader.

Once the first part is solved, and you're warmed up, and doing another set of `cp` sounds really tedious:

```
./scripts/copy_a_b.py ${day}
```

> Don't forget to update the import in the test file!

Nested folder structures aren't fun, so:

```
./scripts/edit.sh ${day}${part}
```

These are little bespoke helper scripts, so hopefully there's just enough inconsistency in the way arguments must be submitted to keep you awake now.


