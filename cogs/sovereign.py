from discord import Message
from discord.ext import commands


class Sovereign(commands.Cog):
    """Bot owner-only commands."""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, extension_name):
        self.client.reload_extension(f'crypex.cogs.{extension_name}')
        await ctx.embed(text=f'Successfully reloaded {extension_name}.')

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.embed(text='Are you sure?')
        response: Message = await self.client.wait_for('message', check=lambda message_: message_.author == ctx.author)
        if response.content.startswith('y'):
            await ctx.embed(text='Alright, logging out...')
            await self.client.logout()
        else:
            await ctx.embed(text='Alright.')


def setup(client):
    client.add_cog(Sovereign(client))
