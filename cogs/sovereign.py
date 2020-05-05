import discord
from typing import Any
from io import StringIO
from textwrap import indent
from contextlib import redirect_stdout
from discord.ext.commands import Cog, command, is_owner, ExtensionNotLoaded


class Sovereign(Cog):
    """Bot owner-only commands."""

    def __init__(self, client):
        self.client = client

    @command()
    @is_owner()
    async def shutdown(self, ctx):
        await ctx.embed(text='Are you sure?')
        response: discord.Message = await self.client.wait_for('message',
                                                               check=lambda message_: message_.author == ctx.author)
        if response.content.startswith('y'):
            await ctx.embed(text='Alright, logging out...')
            await self.client.logout()
        else:
            await ctx.embed(text='Alright.')

    @command()
    @is_owner()
    async def reload(self, ctx, cog_name):
        try:
            self.client.reload_extension(f'crypex.cogs.{cog_name}')
            await ctx.embed(text=f'Reloaded {cog_name}.')
        except ExtensionNotLoaded  as e:
            await ctx.embed(text=str(e))

    @command()
    @is_owner()
    async def eval(self, ctx, *, code):
        env: dict[str, Any] = {
            'discord': discord,
            'commands': discord.ext.commands,
            'ctx': ctx
        }
        env.update(globals())
        std_out_handle: StringIO = StringIO()

        pre_compiled_code: str = f'async def _eval():\n{indent(code, "    ")}'
        exec(pre_compiled_code, env)
        try:
            _eval: Any = env['_eval']
            with redirect_stdout(std_out_handle):
                await _eval()
                if code.find('send') == -1 or not code.find('embed') == -1:
                    await ctx.embed(text=f'```\n{std_out_handle.getvalue()}```')
                await ctx.message.add_reaction('✅')
        except Exception as e:
            e = getattr(e, 'original', e)
            await ctx.embed(text=f'```\n{str(e)}```')
            await ctx.message.add_reaction('❌')


def setup(client):
    client.add_cog(Sovereign(client))
