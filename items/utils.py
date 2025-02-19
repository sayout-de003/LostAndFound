import torch
import torchvision.transforms as T
from torchvision.models.segmentation import deeplabv3_resnet101
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from sentence_transformers import SentenceTransformer
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import googlemaps
import os

# Load AI Models
deeplab_model = deeplabv3_resnet101(pretrained=True).eval()
clip_model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")
bert_model = SentenceTransformer("all-MiniLM-L6-v2")  # Efficient NLP model for location comparison

# Google Maps API (Add your key)
GOOGLE_MAPS_API_KEY = "AIzaSyDV__fcHGKtsviQcNHHsrz3veK2KGg8P3s"
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
geolocator = Nominatim(user_agent="geoapiExercises")


def segment_image(image_path, output_path):
    """Removes background from an image using DeepLabV3."""
    image = Image.open(image_path).convert("RGB")
    transform = T.Compose([T.ToTensor()])
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = deeplab_model(input_tensor)["out"][0]
    mask = output.argmax(0).byte().cpu()

    segmented_image = Image.composite(image, Image.new("RGB", image.size, (0, 0, 0)), mask)
    segmented_image.save(output_path)

    return output_path


def match_image_text(image_path, text_query):
    """Returns similarity score between an image and a text description using CLIP."""
    image = Image.open(image_path)
    inputs = clip_processor(text=[text_query], images=image, return_tensors="pt")
    outputs = clip_model(**inputs)
    similarity_score = outputs.logits_per_image.item()
    return similarity_score


def get_coordinates(location):
    """Converts a location into latitude & longitude using Google Maps API."""
    try:
        result = gmaps.geocode(location)
        if result:
            return result[0]["geometry"]["location"]["lat"], result[0]["geometry"]["location"]["lng"]
    except Exception:
        return None


def calculate_distance(coord1, coord2):
    """Calculates the Haversine distance (in km) between two coordinate points."""
    return geodesic(coord1, coord2).km


def match_locations(desc1, desc2):
    """Uses BERT to calculate similarity score between two location descriptions."""
    embeddings = bert_model.encode([desc1, desc2])
    similarity = torch.nn.functional.cosine_similarity(
        torch.tensor(embeddings[0]).unsqueeze(0), torch.tensor(embeddings[1]).unsqueeze(0)
    )
    return similarity.item()
