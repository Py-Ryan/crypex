import random
import discord
from typing import Optional


class TemplateObjects:
    """Class containing template objects for quick use by the client."""

    def __init__(self) -> None:
        self.colors = discord.Color.__dict__.keys()

    @classmethod
    def get_color(cls, color_name: Optional[str]) -> Optional[discord.Colour]:
        """Get a color, if it exists.

            Parameters
            ----------
                color_name: (str)
                    The name of the color to try and return.

            Return Type
            -----------
                typing.Optional[discord.Colour]
        """
        return getattr(discord.Color, color_name, discord.Color.blurple)()

    def base_embed(self, text: str = '_ _') -> discord.Embed:
        """Construct a basic embed with a description only.

            Parameters
            ----------
                text: (str)
                    The text for the embed description.
                random_color: (bool)
                    Whether to assign a random color
                _color: (str)
                    If random_color is false, pick a color.

            Return Type
            -----------
                discord.Embed
        """
        try:
            color = self.get_color(random.choice(list(self.colors)))
        except Exception:
            color = discord.Color.blurple()
            pass

        return discord.Embed(description=text, colour=color)
