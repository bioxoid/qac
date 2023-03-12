from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
class Star(BaseModel):
	name: str #星座名
	description: str #神話
	image: List[int] #画像の配列

"""
curl -X POST -H "Content-Type: application/json" -d '{"name": "orion", "description": "hero", "image": [0,1]}' localhost:8000/
"orion"が返ってくる！
"""

@app.post("/")
def post_root(star: Star):
	# ここで色々処理を行う
	return star


# @app.get("/items/{item_id}")
# def get_items(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}