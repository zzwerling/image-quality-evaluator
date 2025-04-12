import requests
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from typing import List

from app.schemas import Image, ImageURLResponse

load_dotenv()
IMGUR_CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")
MAX_IMAGES = 1


def extract_album_hash(imgur_url: str) -> str:
    parts = str(imgur_url).strip("/").split("/")
    if "a" in parts and "imgur.com" in parts:
        return parts[parts.index("a") + 1]
    raise ValueError("Invalid Imgur album URL format")

def fetch_album_image(imgur_url: str) -> ImageURLResponse:
    images = []
    if not IMGUR_CLIENT_ID:
        raise RuntimeError("Missing IMGUR_CLIENT_ID in environment.")

    album_hash = extract_album_hash(imgur_url)
    url = f"https://api.imgur.com/3/album/{album_hash}/images"
    headers = {"Authorization": f"Client-ID {IMGUR_CLIENT_ID}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise RuntimeError("Failed to fetch images from Imgur")
    image_data = response.json().get("data", [])
    
    if not image_data:
        raise HTTPException(400, detail="Imgur album contains no images.")
    
    
    
    return Image(
       
            link=image_data[0]["link"],
            type=image_data[0]["type"],
            width=image_data[0]["width"],
            height=image_data[0]["height"]
        )