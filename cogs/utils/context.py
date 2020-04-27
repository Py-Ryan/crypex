from discord.ext import commands
from .template_objects import TemplateObjects


class Context(commands.Context):
    """Customized context object."""

    def __init__(self, *args, **kwargs):
        self.templates = TemplateObjects()
        super().__init__(*args, **kwargs)

    async def embed(self, **kwargs):
        await self.channel.send(embed=self.templates.base_embed(**kwargs))
