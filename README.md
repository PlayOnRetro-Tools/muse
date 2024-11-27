# MUSE - Multi Sprite Animation Editor

A multi jointed sprite animation editor for the Megadrive.

## Development Setup

This project uses black and isort for code formatting. To setup your development environment:

1. Install dependencies: `poetry install --with dev`
2. Install pre-commit hooks: `poetry run pre-commit install`

The pre-commit hooks will automatically format your code when you commit.

## For VSCode users

To automatically format your code directly in the editor install the **black** and **isort**
extensions.

Then add this to your `settings.json` to format on save:

```json
{
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    }
}
```
