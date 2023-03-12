```zsh
. .env/bin/activate
pip install -r requirements.txt
```
```zsh
uvicorn main:app --reload #アプリをlocalhostで走らせる
```
サーバー: FastAPI  
main.py: API作る場所  
test.py: main.pyにリクエスト送るファイル