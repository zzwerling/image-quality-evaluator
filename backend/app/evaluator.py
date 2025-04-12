import torch
import requests
import warnings

from PIL import Image
from io import BytesIO
from pydantic import HttpUrl

warnings.filterwarnings("ignore", message="X does not have valid feature names")

def load_image_from_url(url):
    
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                   (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
    response = requests.get(url, headers=headers)
    response.raise_for_status() 

    image = Image.open(BytesIO(response.content)).convert("RGB")
    return image


def evaluate_photo(url, model, preprocess, regressor):
    
    image_data = load_image_from_url(url)
    
    image = preprocess(image_data).unsqueeze(0).to("cpu")

    with torch.no_grad():
        embedding = model.encode_image(image).cpu().numpy()

    score = regressor.predict(embedding)[0]
    return round(score, 2)



    
  