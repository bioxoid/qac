```zsh
python venv .env
. .env/bin/activate
pip install -r requirements.txt
```
```zsh
uvicorn main:app --reload
```
サーバー: FastAPI  
main.py: API作る場所  
test.py: main.pyにリクエスト送るファイル
