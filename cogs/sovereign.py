from discord import Message
from discord.ext import commands
from discord.ext.commands import command, is_owner


class Sovereign(commands.Cog):
    """Bot owner-only commands."""

    def __init__(self, client):
        self.client = client

    @command()
    @is_owner()
    async def reload(self, ctx, *, extension_name):
        self.client.reload_extension(f'crypex.cogs.{extension_name}')
        await self.client.send(ctx.channel, text=f'Successfully reloaded {extension_name}.')

    @command()
    @is_owner()
    async def shutdown(self, ctx):
        await self.client.send(ctx.channel, text='Are you sure?')

        def check(message: Message) -> bool:
            return message.author == ctx.author

        response: Message = await self.client.wait_for('message', check=check)
        if response.content.startswith('y'):
            await self.client.send(ctx.channel, text='Alright, logging out...')
            await self.client.logout()
        else:
            await self.client.send(ctx.channel, text='Alright.')


def setup(client):
    client.add_cog(Sovereign(client))
