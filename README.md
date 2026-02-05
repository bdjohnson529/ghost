# Installation Instructions


Backend setup
```
cd backend
uv venv --python 3.11
source .venv/bin/activate
pip3 install -r requirements.txt
```

Backend run
```
uv run uvicorn src.api:app --reload
```

Frotend
```
cd frontend
npm install
npm run dev
```