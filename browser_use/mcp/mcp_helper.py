"""Helper utilities for the MCP server."""

import base64
import io
from PIL import Image


def compress_png_to_jpg(
    png_b64: str,
    max_size_mb: float = 0.9,
    initial_quality: int = 85,
    quality_step: int = 5,
    min_quality: int = 10,
) -> tuple[str, str]:
    """
    Compress a PNG image (base64 encoded) to JPG with size constraint.

    Args:
        png_b64: Base64 encoded PNG image data.
        max_size_mb: Maximum size in MB for the output image. Default is 0.9 MB.
        initial_quality: Starting JPEG quality (0-100). Default is 85.
        quality_step: Amount to reduce quality on each iteration. Default is 5.
        min_quality: Minimum quality to try before giving up. Default is 10.

    Returns:
        A tuple of (base64_encoded_jpg, mime_type).
        If compression succeeds, returns the compressed JPG.
        If the image cannot be compressed under the threshold, returns the smallest achieved.
    """
    max_size_bytes = int(max_size_mb * 1024 * 1024)

    # Decode base64 PNG
    png_bytes = base64.b64decode(png_b64)
    img = Image.open(io.BytesIO(png_bytes))

    # Convert to RGB if necessary (PNG may have alpha channel)
    if img.mode in ('RGBA', 'LA', 'P'):
        # Create white background for transparency
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    quality = initial_quality
    jpg_bytes = None

    while quality >= min_quality:
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        jpg_bytes = buffer.getvalue()

        if len(jpg_bytes) <= max_size_bytes:
            break

        quality -= quality_step

    # Return the best we could achieve
    jpg_b64 = base64.b64encode(jpg_bytes).decode('utf-8')
    return jpg_b64, 'image/jpeg'
