import tensorflow as tf
import numpy as np
from PIL import Image
import exifread
import io
import os

# Mock model loading - In a real scenario, this would load a saved .h5 or .pb model
# model = tf.keras.models.load_model('model.h5')

def classify_road_damage(image_bytes):
    """
    Classifies the image for road damage.
    In a real implementation, this would use a CNN model.
    """
    # For demonstration, we'll simulate classification
    # Real logic: img = Image.open(io.BytesIO(image_bytes)).resize((224, 224))
    # prediction = model.predict(np.expand_dims(np.array(img), axis=0))
    
    # Simple heuristic to simulate "invalid image" vs "road damage"
    # If the image is too small or uniform, we might call it invalid
    img = Image.open(io.BytesIO(image_bytes))
    width, height = img.size
    
    if width < 100 or height < 100:
        return "Invalid Image - Resolution too low"
    
    # Simulate AI classification
    import random
    choices = ["Road Damage Detected", "No Road Damage", "Invalid Image - Not Road Related"]
    # We'll bias it towards Road Damage for the demo
    result = random.choices(choices, weights=[0.7, 0.2, 0.1])[0]
    
    # Sub-classification (Potholes, Cracks, etc.)
    damage_types = ["Pothole", "Crack", "Surface Damage"]
    detected_type = random.choice(damage_types) if result == "Road Damage Detected" else None
    
    return {
        "status": "success",
        "result": result,
        "type": detected_type,
        "confidence": random.uniform(0.85, 0.99) if result != "Invalid Image - Not Road Related" else 0.0
    }

def extract_gps_data(image_bytes):
    """
    Extracts GPS coordinates from image EXIF data using Pillow.
    """
    try:
        from PIL.ExifTags import TAGS, GPSTAGS
        img = Image.open(io.BytesIO(image_bytes))
        exif_info = img._getexif()
        
        if not exif_info:
            print("No EXIF data found in image.")
            return None

        gps_info = {}
        for tag, value in exif_info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                for t in value:
                    sub_tag = GPSTAGS.get(t, t)
                    gps_info[sub_tag] = value[t]

        if not gps_info:
            print("No GPS info found in EXIF.")
            return None

        def _convert_to_degrees(value):
            d = float(value[0])
            m = float(value[1])
            s = float(value[2])
            return d + (m / 60.0) + (s / 3600.0)

        lat = _convert_to_degrees(gps_info['GPSLatitude'])
        if gps_info['GPSLatitudeRef'] != 'N':
            lat = -lat

        lon = _convert_to_degrees(gps_info['GPSLongitude'])
        if gps_info['GPSLongitudeRef'] != 'E':
            lon = -lon

        print(f"Extracted GPS: {lat}, {lon}")
        return {"latitude": lat, "longitude": lon}

    except Exception as e:
        print(f"GPS Extraction failed: {e}")
        
    return None
