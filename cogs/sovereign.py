from discord.ext import commands


class Sovereign(commands.Cog):
    """Bot owner-only commands."""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, extension_name):
        self.client.reload_extension(f'crypex.cogs.{extension_name}')
        await self.client.send(ctx.channel, text=f'Successfully reloaded {extension_name}.')


def setup(client):
    client.add_cog(Sovereign(client))
