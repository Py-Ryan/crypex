import random
import discord
from typing import Optional
from inspect import ismethod


class TemplateObjects:
    """Class containing template objects for quick use by the client."""

    def __init__(self):
        self.colors = []
        for name in dir(discord.Color):
            try:
                attr = getattr(discord.Color, str(name))
                if ismethod(attr):
                    return_type = attr()
                    if isinstance(return_type, (discord.Color, discord.Colour)):
                        self.colors.append(return_type)
            except TypeError:   # Ignore argument errors, none of the methods we want have arguments other than self.
                pass

    def get_color(self, color_name='blurple', random_=True):
        """Get a color, if it exists.

            Parameters
            ----------
                color_name: (str)
                    The name of the color to try and return.
                random_: (bool)
                    Whether to pick a random color.

            Return Type
            -----------
                Optional[discord.Colour]
        """
        if random_:
            return random.choice(self.colors)
        else:
            return getattr(self.colors, color_name)

    def base_embed(self, text):
        """Construct a basic embed with a description only.

            Parameters
            ----------
                text: (str)
                    The text for the embed description.

            Return Type
            -----------
                discord.Embed
        """
        color = self.get_color()

        return discord.Embed(description=text, colour=color)
