from discord.ext import commands
from typing import Union, Optional
from .template_objects import TemplateObjects
from discord import TextChannel, DMChannel, Member


class Context(commands.Context):
    """Customized context object."""

    def __init__(self, **kwargs):
        self.__templates__ = TemplateObjects()
        super().__init__(**kwargs)

    async def embed(self, channel: Optional[Union[TextChannel, DMChannel]] = None,
                    user: Optional[Member] = None, **kwargs):
        channel = channel or user or self.channel
        await channel.send(embed=self.__templates__.base_embed(**kwargs))
