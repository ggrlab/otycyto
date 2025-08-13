# Quick contribution guide

```bash
    git clone git@github.com:ggrlab/otycyto

    #  Use uv-managed virtualenv
    uv sync  --python /bin/python3.11

    # Using your default python:
    # uv sync
    uv run pre-commit run --all-files
    uv run pre-commit autoupdate

    # Run common tasks via uv
    uv run pytest                # tests
    uv build                     # build sdist/wheel when ready to publish

    # Documentation
    uv run mkdocs build
    uv run mkdocs serve
```
