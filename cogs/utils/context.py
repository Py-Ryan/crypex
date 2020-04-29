from discord.ext import commands
from ...localdata.localdata import LocalData
from .template_objects import TemplateObjects


class Context(commands.Context):
    """Customized context object."""

    def __init__(self, *args, **kwargs):
        self.__templates__ = TemplateObjects()
        self.__data__ = LocalData()
        super().__init__(*args, **kwargs)

    async def embed(self, **kwargs):
        await self.channel.send(embed=self.__templates__.base_embed(**kwargs))

    async def get(self, **kwargs):
        return self.__data__.get(**kwargs)

    async def edit(self, **kwargs):
        return self.__data__.edit(**kwargs)
