from fastapi import FastAPI

app = FastAPI()

# request matches the get method and "/"

@app.get("/")
async def root():
    return {"message": "Welcome to my API- Sourav"}

@app.get("/posts")

def get_posts():
    return {"data": "This is post data"}