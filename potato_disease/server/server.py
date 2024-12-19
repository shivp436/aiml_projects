from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import util

app = FastAPI()

# Enable CORS so that the frontend can make requests to this server
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/", response_class=HTMLResponse)
# async def get_index():
#     try:
#         with open("static/app.html", "r") as file:
#             return HTMLResponse(content=file.read(), status_code=200)
#     except FileNotFoundError:
#         raise HTTPException(status_code=404, detail="app.html not found")

@app.post("/")
async def post_index(request: Request):
    try:
        data = await request.json()
        base64_string = data.get('image')

        if not base64_string:
            raise HTTPException(status_code=400, detail="No image found")

        img_class = util.predict_class(base64_str=base64_string)

        return JSONResponse(content={"class": img_class}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    print("Starting server...")
    util.load_artifacts()
    uvicorn.run(app, host="0.0.0.0", port=5000)
