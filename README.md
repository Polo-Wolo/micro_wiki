# Install environment
```sh
python3 -m venv .venv

source ./.venv/bin/activate

pip3 install -r requirements.txt
```

# Run server
```sh
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```