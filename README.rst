.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/otcyto.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/otcyto
    .. image:: https://readthedocs.org/projects/otcyto/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://otcyto.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/otcyto/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/otcyto
    .. image:: https://img.shields.io/pypi/v/otcyto.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/otcyto/
    .. image:: https://img.shields.io/conda/vn/conda-forge/otcyto.svg
        :alt: Conda-Forge
        :target: https://anaconda.org/conda-forge/otcyto
    .. image:: https://pepy.tech/badge/otcyto/month
        :alt: Monthly Downloads
        :target: https://pepy.tech/project/otcyto
    .. image:: https://img.shields.io/twitter/url/http/shields.io.svg?style=social&label=Twitter
        :alt: Twitter
        :target: https://twitter.com/otcyto

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/

|

======
otcyto
======


    Add a short description here!


A longer description of your project goes here...


Package setup
=============

This project has been set up using PyScaffold 4.4. For details and usage
information on PyScaffold see https://pyscaffold.org/

.. code-block:: bash

    pip install --upgrade pyscaffold
    putup otcyto
    cd otcyto
    # Create otcyto within gitlab, without README
    git branch -m master main
    git remote add origin git@github.com:ggrlab/otycyto
    git push -u origin --all

    # add-apt-repository ppa:deadsnakes/ppa
    # apt install python3.11

    #  Use uv-managed virtualenv
    # uv sync  --python /bin/python3.11

    # (Optional) Add deps with uv (writes to pyproject.toml) to testing:
    uv add --dev pytest ruff pytest-cov pre-commit
    # Use pre-commit:
    # https://docs.astral.sh/uv/guides/integration/pre-commit/

    uv sync  --python /bin/python3.11  # or whatever python you want to use.
    # Using your default python:
    # uv sync
    uv run pre-commit run --all-files
    uv run pre-commit autoupdate
    # uv sync including test dependencies:


    # Run common tasks via uv
    uv run pytest                # tests
    uv build                     # build sdist/wheel when ready to publish
    # uv publish  # to publish on pypi

    # Pre-commit with Ruff via PyScaffold extension
    # If you haven’t used the extension on creation:
    pipx run pyscaffold putup --update . --pre-commit-ruff
    pre-commit install
    pre-commit autoupdate

    # Run the CI locally with act. (pure development)
    wget https://github.com/nektos/act/releases/download/v0.2.80/act_Linux_x86_64.tar.gz
    tar -xzf act_Linux_x86_64.tar.gz
    sudo mv act /usr/local/bin/
    rm act_Linux_x86_64.tar.gz

    # From https://github.com/nektos/act/blob/a78b3f305a43a143283fb7d02f3b24df1577ce3e/cmd/root.go#L719
    # 	switch answer {
    # 	case "Large":
    # 		option = "-P ubuntu-latest=catthehacker/ubuntu:full-latest\n-P ubuntu-22.04=catthehacker/ubuntu:full-22.04\n-P ubuntu-20.04=catthehacker/ubuntu:full-20.04\n-P ubuntu-18.04=catthehacker/ubuntu:full-18.04\n"
    # 	case "Medium":
    # 		option = "-P ubuntu-latest=catthehacker/ubuntu:act-latest\n-P ubuntu-22.04=catthehacker/ubuntu:act-22.04\n-P ubuntu-20.04=catthehacker/ubuntu:act-20.04\n-P ubuntu-18.04=catthehacker/ubuntu:act-18.04\n"
    # 	case "Micro":
    # 		option = "-P ubuntu-latest=node:16-buster-slim\n-P ubuntu-22.04=node:16-bullseye-slim\n-P ubuntu-20.04=node:16-buster-slim\n-P ubuntu-18.04=node:16-buster-slim\n"
    # 	}
    # Use the medium image for act:
    echo "-P ubuntu-latest=catthehacker/ubuntu:act-latest\n-P ubuntu-22.04=catthehacker/ubuntu:act-22.04\n-P ubuntu-20.04=catthehacker/ubuntu:act-20.04\n-P ubuntu-18.04=catthehacker/ubuntu:act-18.04\n" > .actrc

.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.6. For details and usage
information on PyScaffold see https://pyscaffold.org/.
