from __future__ import annotations

from discord.ext import commands
from typing import Any, Optional, Union
from discord import TextChannel, DMChannel, Member
from crypex.cogs.utils.template_objects import TemplateObjects

class Context(commands.Context):
    templates: TemplateObjects = ...
    def __init__(self, **kwargs: dict[str, Any]) -> None: ...
    async def embed(self,channel: Optional[Union[TextChannel, DMChannel]] =...,
                    user: Optional[Member] =..., **kwargs: dict[str, Any]) -> None: ...
