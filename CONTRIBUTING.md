# Contributing

## Development standards

- Keep changes focused and small.
- Run formatting, linting, typing, and tests before pushing:

```sh
./scripts/format.sh
./scripts/validate.sh
python -m unittest discover -s tests -p "test_*.py"
```

- Prefer explicit error handling and structured logs for new runtime paths.
- Document any new environment variables in both `README.md` and `.env.example`.

## Pull request expectations

- Describe assumptions and known limitations.
- Include test evidence (command + result).
- Keep commits coherent and atomic.
