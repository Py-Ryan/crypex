from discord.ext import commands


class Crypt(commands.Cog):
    """Cryptographic commands."""

    def __init__(self, client: commands.Bot) -> None:
        self.client = client
