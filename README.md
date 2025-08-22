# FPL Toolkit

Toolkit leve para Fantasy Premier League:
- Fetch de dados oficiais (bootstrap, fixtures)
- Projeções simples (form + dificuldade de fixture)
- CLI com ranking por posição

## Quickstart (Codespaces/browser)
```bash
pip install -r requirements.txt
pip install -e .
python -m fplkit.cli top --pos MID --n 10

## Qualidade
```bash
ruff check .
mypy src
pytest -q