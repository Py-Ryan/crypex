from ..cogs.utils.context import Context
from discord.ext.commands import Cog, Bot


class Crypto(Cog):
    client: Bot
    def __init__(self, client: Bot) -> None: ...
    def hex(self, ctx: Context, *, string: str) -> None: ...

def setup(client: Bot) -> None: ...