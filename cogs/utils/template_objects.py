from random import choice
from inspect import ismethod
from typing import List, Any, Optional
from discord import Color, Colour, Embed


class TemplateObjects:
    """Class containing template objects for quick use by the client."""

    def __init__(self):
        self.colors: List[Color, Colour] = list()
        for name in dir(Color):
            try:
                attr: Any = getattr(Color, str(name))
                if ismethod(attr):
                    return_type: Any = attr()
                    if isinstance(return_type, (Color, Colour)):
                        self.colors.append(return_type)
            except TypeError:   # Ignore argument errors, none of the methods we want have arguments other than self.
                pass

    def get_color(self, color_name: str = 'blurple', random: bool = True) -> Optional[Colour]:
        if random:
            return choice(self.colors)
        else:
            return getattr(self.colors, color_name, None)

    def base_embed(self, text) -> Embed:
        color: Colour = self.get_color()

        return Embed(description=text, colour=color)
