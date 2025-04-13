import argparse
import os
import clip
import joblib

# Extend sys.path to allow imports from the backend module when running this script directly.
# This is a temporary solution for local CLI development. For production or packaging, use a proper module install.
import sys
import os
import logging
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.app.evaluator import evaluate_photo_from_path, get_image_feedback


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

MODEL_PATH = "../backend/models/lgbm_model_v2.pkl"

try:
    SCALER = joblib.load("../backend/models/scaler.pkl")
    logger.info("Successfully loaded scaler!")

    MODEL, PREPROCESS = clip.load("ViT-L/14@336px", device="cpu")
    REGRESSOR = joblib.load(MODEL_PATH)
    logger.info(f"Successfully loaded model from {MODEL_PATH}!")

except Exception as e:
    logger.error(f"Failed to load model from {MODEL_PATH}")

def main():
    parser = argparse.ArgumentParser(description="Score an image using the CLIP+LightGBM model")
    parser.add_argument("image_path", help="Path to the image file")
    parser.add_argument("--json", action="store_true", help="Return output as JSON")

    args = parser.parse_args()

    if not os.path.exists(args.image_path):
        print(f"Error: File {args.image_path} does not exist.")
        return

    result = {}
    logger.info(f"Fetching score of photo at {args.image_path}")
    result['score'] = evaluate_photo_from_path(args.image_path, MODEL, PREPROCESS, REGRESSOR, SCALER)
    
    logger.info(f"Fetching feedback of photo at {args.image_path}")
    result['feedback'] = get_image_feedback(args.image_path, result['score'])

    if args.json:
        import json
        print(json.dumps(result, indent=2))
    else:
        print(f"Score: {result['score']:.2f}")
        print(f"Feedback: {result['feedback']}")

if __name__ == "__main__":
    main()