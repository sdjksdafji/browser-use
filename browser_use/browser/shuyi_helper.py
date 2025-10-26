import asyncio
import random


def get_realistic_click(element_handle):
    async def realistic_click():
        if element_handle:
            # First hover over the element to simulate realistic user behavior
            await element_handle.hover(timeout=1_000)

            delay = random.uniform(0.1, 0.5)
            await asyncio.sleep(delay)
            # Then perform the click
            await element_handle.click(timeout=1_500)
        else:
            raise ValueError("Element handle is None")

    return realistic_click


def get_realistic_js_click(element_handle, page):
    async def realistic_js_click():
        if element_handle:
            # Hover first, then JS click
            await element_handle.hover(timeout=1_000)
            delay = random.uniform(0.05, 0.2)
            await asyncio.sleep(delay)
            await page.evaluate('(el) => el.click()', element_handle)
        else:
            raise ValueError("Element handle is None")

    return realistic_js_click


def get_realistic_coordinate_click(x, y, page):
    async def realistic_coordinate_click():
        # Move mouse to the element (hover simulation)
        await page.mouse.move(x / 2, y / 2)
        await page.mouse.move(x, y, steps=100)
        # Small delay to simulate human behavior
        delay = random.uniform(0.1, 0.5)
        await asyncio.sleep(delay)
        # Then click
        await page.mouse.click(x, y, delay=500)

    return realistic_coordinate_click


async def get_screen_position(element_handle):
    x, y = None, None
    # Get coordinates dynamically from element_handle
    if element_handle:
        bounding_box = await element_handle.bounding_box()
        if bounding_box:
            x = bounding_box['x'] + bounding_box['width'] / 2
            y = bounding_box['y'] + bounding_box['height'] / 2
    return x, y
