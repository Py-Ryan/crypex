import random
import discord
from typing import Optional


class TemplateObjects:
    """Class containing template objects for quick use by the client."""

    def __init__(self) -> None:
        self.color_list: dict = dict(
            Blurple=discord.Colour.blurple(),
            Purple=discord.Color.purple(),
            Blue=discord.Color.blue(),
            DarkBlue=discord.Color.dark_blue(),
            DarkGold=discord.Color.dark_gold(),
            DarkGreen=discord.Color.dark_green(),
            DarkGrey=discord.Color.dark_grey(),
            DarkMagenta=discord.Color.dark_magenta(),
            DarkPurple=discord.Color.dark_purple(),
            DarkOrange=discord.Color.dark_orange(),
            DarkTeal=discord.Color.dark_teal(),
            DarkerGray=discord.Color.darker_grey(),
            Gold=discord.Color.gold(),
            Green=discord.Color.green(),
            Greyple=discord.Color.greyple(),
            LightGrey=discord.Color.light_grey(),
            LighterGrey=discord.Color.lighter_grey(),
            Red=discord.Color.red(),
            Teal=discord.Color.teal())

    def get_color(self, color_name: str) -> Optional[discord.Colour]:
        """Get a color, if it exists.

            Parameters:
                color_name: (str)
                    The name of the color to try and return.

            Return Type:
                typing.Optional[discord.Colour]
        """
        _list = dict(self.color_list)
        return _list[color_name] or None

    def base_embed(self, text: str, random_color: bool = True, _color: str = 'Blurple') -> discord.Embed:
        """Construct a basic embed with a description only.

            Parameters:
                text: (str)
                    The text for the embed description.
                random_color: (bool)
                    Whether to assign a random color
                _color: (str)
                    If random_color is false, pick a color.

            Return Type:
                discord.Embed
        """
        if random_color:
            color = self.get_color(random.choice(list(self.color_list)))
        else:
            color = self.get_color(_color) or discord.Color.blurple()

        return discord.Embed(description=text, colour=color)
