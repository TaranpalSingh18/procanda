from fastapi import FastAPI

app = FastAPI()



@app.get('/')
async def get_health():
    return {"message":"healthy"}