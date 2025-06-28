start:
	uv run python rpc_server.py

install:
	uv venv
	uv pip install -r requirements.txt || true
	uv pip install -e . || true  # 如果你用 pyproject.toml 管理本地包

freeze:
	uv pip freeze > requirements.txt