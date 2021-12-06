import logging

from notion.block import EmbedBlock, ImageBlock
from notion.client import NotionClient

from private_credentials import TOKEN_V2


def get_client():
    return NotionClient(token_v2=TOKEN_V2)


def add_page_cover(page, image_url):
    # This was found by looking at get() without any arguments which returns
    # all the cached properties. dir() is also a useful way to get all the
    # top level dot properties.
    if page.get('type') == 'page':
        page.set('format.page_cover', image_url)


def add_gallery_embedded_image(block, image_url):
    # For content card galleries
    if not image_url:
        logging.warning(f"No image url provided for {block.title}")
        return
    if block.children and isinstance(block.children[0], EmbedBlock):
        logging.warning(f"Already embedded image for {block.title}! Removing...")
        del block.children[0]
    # Add embedded image at the end of the current block
    # Use ImageBlocks to avoid bad data validation
    embedded_image = block.children.add_new(ImageBlock)
    embedded_image.set_source_url(image_url)
    if len(block.children) > 1:
        # The library only allows for adding to end then moving to first
        logging.warning(f"Moving embedded image to top of page...")
        embedded_image.move_to(block, 'first-child')
