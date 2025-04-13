import torch
import requests
import warnings
import os
import logging 
import base64

from openai import OpenAI
from PIL import Image
from io import BytesIO
from pydantic import HttpUrl
from dotenv import load_dotenv
warnings.filterwarnings("ignore", message="X does not have valid feature names")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)


def load_prompt(variables):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'feedback_prompt.txt')
    file_path = os.path.abspath(file_path)

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().format(**variables)

def load_image_from_url(url):
    
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                   (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
     "Referer": "https://imgur.com"

}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
    except Exception as e:
        logger.exception("Failed to load imgur image from URL")
    
    logger.info(f"Image loaded with status code {response.status_code}")

    image = Image.open(BytesIO(response.content)).convert("RGB")
    return image


def evaluate_photo(url, model, preprocess, regressor):
    
    image_data = load_image_from_url(url)
    
    image = preprocess(image_data).unsqueeze(0).to("cpu")

    with torch.no_grad():
        embedding = model.encode_image(image).cpu().numpy()

    score = regressor.predict(embedding)[0]
    return round(score, 2)

def evaluate_photo_from_path(path, model, preprocess, regressor, scaler):
    image_data = Image.open(path).convert("RGB")

    image = preprocess(image_data).unsqueeze(0).to("cpu")

    with torch.no_grad():
        embedding = model.encode_image(image).cpu().numpy()

    pred_scaled = regressor.predict(embedding)[0]
    score = scaler.inverse_transform([[pred_scaled]])[0][0]
    return round(score, 2)


def get_image_feedback(image_path, score):
    variables = {"score": score}

    feedback_prompt = load_prompt(variables=variables)
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": feedback_prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                    }
                }
            ]
        }
        ],
        max_tokens=5000
        
        
    )
    return response.choices[0].message.content