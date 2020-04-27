from logging import Logger
from discord.ext import commands
from discord.ext.commands import Context
from discord import Message, TextChannel
from typing import Any, Dict, List, Union
from crypex.localdata.localdata import LocalData
from crypex.cogs.utils.template_objects import TemplateObjects

cogs: List[str]

def automatically_append_cogs() -> None: ...


class Crypex(commands.Bot):
    data: LocalData = ...
    templates: TemplateObjects = ...
    logger: Logger = ...
    default_prefix: str = ...
    def __init__(self, logger: Logger) -> None: ...
    def run(self) -> None: ...
    async def on_ready(self) -> None: ...
    async def on_message(self, message: Message) -> None: ...
    async def on_command_error(self, context: Context, exception: Any) -> None: ...
    async def send(self, channel: TextChannel, **kwargs: Union[Dict[str, Any], str]) -> None: ...