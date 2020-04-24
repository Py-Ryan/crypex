import random
import discord
from typing import Optional


class TemplateObjects:
    """Class containing template objects for quick use by the client."""

    def __init__(self) -> None:
        self.colors = [key for key in discord.Color.__dict__.keys() if not str(key).startswith('__')]

    @staticmethod
    def get_color(color_name: Optional[str]) -> Optional[discord.Colour]:
        """Get a color, if it exists.

            Parameters
            ----------
                color_name: (str)
                    The name of the color to try and return.

            Return Type
            -----------
                Optional[discord.Colour]
        """
        return getattr(discord.Color, color_name, discord.Color.blurple)()

    def base_embed(self, text: str = '_ _') -> discord.Embed:
        """Construct a basic embed with a description only.

            Parameters
            ----------
                text: (str)
                    The text for the embed description.

            Return Type
            -----------
                discord.Embed
        """
        color = self.get_color(random.choice(list(self.colors)))

        return discord.Embed(description=text, colour=color)
