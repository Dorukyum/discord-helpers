from discord import Embed as OriginalEmbed, Colour, Color
from typing import Union


def Embed(
    title: str = "",
    description: str = "",
    colour: Union[int, Colour, Color] = 0x202225,
    footer: str = "",
    footer_icon: str = None,
    author: str = "",
    author_icon: str = None,
    thumbnail: str = None,
    image: str = None,
):
    embed = OriginalEmbed(title=title, description=description, colour=colour)
    if footer_icon is not None:
        embed.set_footer(text=footer, icon_url=footer_icon)
    else:
        embed.set_footer(text=footer)
    if author_icon is not None:
        embed.set_author(name=author, icon_url=author_icon)
    else:
        embed.set_author(name=author)
    if thumbnail is not None:
        embed.set_thumbnail(url=thumbnail)
    if image is not None:
        embed.set_image(url=image)
    return embed