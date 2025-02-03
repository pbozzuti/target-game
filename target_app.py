from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for all origins (you can restrict it to your frontend domain later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for now, replace "*" with your frontend's URL for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],
)

shots = []
target_radius = 75

class Shot(BaseModel):
    x: float
    y: float
    target_x: float
    target_y: float

@app.post("/shoot")
def record(shot: Shot):
    dist = np.sqrt((shot.x - shot.target_x) ** 2 + (shot.y - shot.target_y) ** 2)
    shots.append(dist)
    return {"message": "Shot recorded", "distance": dist}

@app.post("/reset")
def reset():
    global shots
    shots = []
    return {"message": "Game reset"}

@app.get("/shots")
def get_shots():
    return {"shots": shots}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
