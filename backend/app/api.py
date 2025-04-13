import joblib
import logging
import torch
import clip

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from contextlib import asynccontextmanager

from app.schemas import ImageURLRequest, ImageURLResponse
from app.imgur import fetch_album_image
from app.evaluator import evaluate_photo


BASE_DIR = Path(__file__).resolve().parent.parent 
MODEL_PATH = BASE_DIR / "models" / "lgbm_model.pkl"

ORIGINS = ["http://localhost:8000", "http://localhost:5173"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(app: FastAPI):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"Loading model on: {device}")
    
    try: 
        model, preprocess = clip.load("ViT-L/14@336px", device=device)
        regressor = joblib.load(MODEL_PATH)

        app.state.model = model
        app.state.preprocess = preprocess
        app.state.regressor = regressor
        logger.info(f"Successfully loaded model from {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Failed to load model from {MODEL_PATH}")
        raise

    yield  

app_obj = FastAPI(lifespan=lifespan)
    

app_obj.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app_obj.post("/evaluate", response_model=ImageURLResponse)
#@limiter.limit("5/hour")
def conversation_feedback_route(image_request: ImageURLRequest, request: Request):
    image = fetch_album_image(image_request.imgur_url)
    logger.info("Successfully fetched image from imgur")
    score = evaluate_photo(image.link, request.app.state.model, request.app.state.preprocess, request.app.state.regressor)

    return ImageURLResponse(image=image, score=score)

