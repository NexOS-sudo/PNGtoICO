# Icon_Converter_Algorithm.py

import logging
import os
import math
from PIL import Image
from typing import Tuple, Optional
import colorsys


class IconConverter:
    """
    A utility to convert an image to an ICO, with manual and automatic
    subject-color cropping.
    """
    TARGET_SIZES = [
        (16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)
    ]

    def __init__(self, input_path: str):
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")
        self.input_path = input_path
        self.image: Optional[Image.Image] = None

    def _color_distance(self, c1: Tuple[int, ...], c2: Tuple[int, ...]) -> float:
        """Calculates the Euclidean distance between two RGB colors."""
        r1, g1, b1, *_ = c1
        r2, g2, b2, *_ = c2
        return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    def find_dominant_color(self) -> Optional[Tuple[int, int, int]]:
        """
        UPDATED: Analyzes the image to find the most dominant AND vibrant color.
        """
        logging.info("🔍 Analyzing image for dominant color...")
        img = Image.open(self.input_path).convert('RGBA')

        corners = [
            img.getpixel((0, 0)), img.getpixel((img.width - 1, 0)),
            img.getpixel((0, img.height - 1)), img.getpixel((img.width - 1, img.height - 1))
        ]
        bg_color = max(set(corners), key=corners.count)
        logging.info(f"Detected background color: {bg_color[:3]}")

        img.thumbnail((256, 256))

        color_counts = {}
        for x in range(img.width):
            for y in range(img.height):
                r, g, b, a = img.getpixel((x, y))
                if a < 128 or self._color_distance((r, g, b), bg_color[:3]) < 50:
                    continue
                rgb_tuple = (r, g, b)
                color_counts[rgb_tuple] = color_counts.get(rgb_tuple, 0) + 1

        if not color_counts:
            logging.error("Could not find any dominant color candidates.")
            return None

        # --- LOGIC TO FIND THE BEST COLOR ---
        best_color = None
        max_score = -1

        for color, count in color_counts.items():
            # Convert RGB to HSL to get saturation. HSL values are 0-1.
            r, g, b = [x / 255.0 for x in color]
            _, lightness, saturation = colorsys.rgb_to_hls(r, g, b)

            # Ignore colors that are too dark, too bright, or not saturated enough
            if not (0.1 < lightness < 0.9 and saturation > 0.15):
                continue

            # Score is based on count and how colorful it is (saturation)
            score = count * (saturation ** 2)

            if score > max_score:
                max_score = score
                best_color = color

        if best_color is None:
            logging.error("Could not find any vibrant color candidates.")
            return None

        logging.info(f"✅ Dominant color found: {best_color}")
        return best_color

    def _crop_to_subject(self, img: Image.Image, subject_color: Tuple[int, int, int], tolerance: int) -> Image.Image:
        """Crops an image by finding all pixels similar to a given subject_color."""
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        logging.info(f"Scanning for subject color similar to {subject_color} with tolerance {tolerance}.")
        mask = Image.new('L', img.size, 0)
        mask_pixels = mask.load()
        source_pixels = img.load()

        for y in range(img.height):
            for x in range(img.width):
                if self._color_distance(source_pixels[x, y], subject_color) <= tolerance:
                    mask_pixels[x, y] = 255

        bbox = mask.getbbox()

        if bbox:
            logging.info(f"Subject found. Cropping to bounding box: {bbox}")
            return img.crop(bbox)
        else:
            logging.warning("⚠️ Could not find any pixels matching the subject color. No crop applied.")
            return img

    def convert(self, output_path: Optional[str], subject_color: Tuple[int, int, int], tolerance: int):
        """Loads, crops, and converts the image to an ICO."""
        try:
            self.image = Image.open(self.input_path)
            logging.info(f"Source image loaded: {self.image.size}, Mode: {self.image.mode}")
            original_size = self.image.size

            self.image = self._crop_to_subject(self.image, subject_color, tolerance)

            if self.image.size != original_size:
                logging.info(f"✅ Successfully cropped image from {original_size} to {self.image.size}.")
            else:
                logging.warning("⚠️ Image was not cropped. Check your subject color and try a higher tolerance.")

            final_output_path = output_path or f"{os.path.splitext(self.input_path)[0]}.ico"
            self.image.save(final_output_path, format='ICO', sizes=self.TARGET_SIZES)
            logging.info(f"✅ Icon created successfully at: {final_output_path}")

        except Exception as e:
            logging.error(f"❌ An unexpected error occurred: {e}")
            raise
