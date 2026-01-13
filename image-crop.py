#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pillow",
# ]
# ///
"""
Image Crop and Convert Tool

Crop images to specific aspect ratios and convert formats.

Usage:
    uv run image-crop.py input.png -o output.jpg --aspect 16:9
    uv run image-crop.py input.png --aspect 16:9  # outputs input-16x9.jpg
"""

import argparse
import sys
from pathlib import Path

from PIL import Image


def crop_to_aspect(img: Image.Image, aspect_w: int, aspect_h: int) -> Image.Image:
    """Crop image to target aspect ratio, centered."""
    w, h = img.size
    target_ratio = aspect_w / aspect_h
    current_ratio = w / h

    if current_ratio > target_ratio:
        # Image is wider than target, crop width
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        box = (left, 0, left + new_w, h)
    else:
        # Image is taller than target, crop height
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        box = (0, top, w, top + new_h)

    return img.crop(box)


def main():
    parser = argparse.ArgumentParser(
        description='Crop images to aspect ratio and convert format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('input', help='Input image file')
    parser.add_argument('-o', '--output', help='Output file (default: input-WxH.jpg)')
    parser.add_argument('-a', '--aspect', default='16:9', help='Aspect ratio (default: 16:9)')
    parser.add_argument('-q', '--quality', type=int, default=90, help='JPEG quality (default: 90)')

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Parse aspect ratio
    try:
        aspect_w, aspect_h = map(int, args.aspect.split(':'))
    except ValueError:
        print(f"Error: Invalid aspect ratio format: {args.aspect} (use W:H)", file=sys.stderr)
        sys.exit(1)

    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.with_stem(f"{input_path.stem}-{aspect_w}x{aspect_h}").with_suffix('.jpg')

    # Process image
    img = Image.open(input_path)
    original_size = img.size

    cropped = crop_to_aspect(img, aspect_w, aspect_h)

    # Convert to RGB for JPEG (handles RGBA PNGs)
    if output_path.suffix.lower() in ['.jpg', '.jpeg']:
        cropped = cropped.convert('RGB')

    cropped.save(output_path, quality=args.quality)

    print(f"Original: {original_size[0]}x{original_size[1]}")
    print(f"Cropped:  {cropped.size[0]}x{cropped.size[1]}")
    print(f"Output:   {output_path}")


if __name__ == '__main__':
    main()
