import logging
import re

from notion.block import EmbedBlock, ImageBlock
from notion.client import COLLECTION_VIEW_TYPES, CollectionView, NotionClient

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


def get_collection_view(client, url_or_id, collection=None, force_refresh=False):
    """
    THIS IS OVERRIDDEN TO SUPPORT QUERIES OF MORE THAN 100 rows.

    Retrieve an instance of a subclass of CollectionView that maps to the appropriate type.
    The `url_or_id` argument can either be the URL for a database page, or the ID of a collection_view (in which case
    you must also pass the collection)
    """
    # if it's a URL for a database page, try extracting the collection and view IDs
    if url_or_id.startswith("http"):
        match = re.search("([a-f0-9]{32})\?v=([a-f0-9]{32})", url_or_id)
        if not match:
            raise Exception("Invalid collection view URL")
        block_id, view_id = match.groups()
        collection = client.get_block(
            block_id, force_refresh=force_refresh, limit=5000
        ).collection
    else:
        view_id = url_or_id
        assert (
            collection is not None
        ), "If 'url_or_id' is an ID (not a URL), you must also pass the 'collection'"

    view = client.get_record_data(
        "collection_view", view_id, force_refresh=force_refresh
    )
    return (
        COLLECTION_VIEW_TYPES.get(view.get("type", ""), CollectionView)(
            self, view_id, collection=collection
        )
        if view
        else None
    )
