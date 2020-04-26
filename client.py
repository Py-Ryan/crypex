import os
import discord
from discord.ext import commands
from .localdata import localdata
from crypex.cogs.utils.template_objects import TemplateObjects

cogs = list()


def _automatically_append_cogs():
    for file in os.listdir('crypex/cogs'):
        if file.endswith('.py'):
            file_name = file.split('.')
            cogs.append(f'crypex.cogs.{file_name[0]}')


class Crypex(commands.Bot):
    """Represents an instance of Crypex."""

    def __init__(self):
        self.ld_handle = localdata.LocalData()
        self.templates = TemplateObjects()
        super().__init__(command_prefix=self.ld_handle.get('default_prefix')[0])

        _automatically_append_cogs()
        for cog in cogs:
            try:
                self.load_extension(cog)
                print(f'Mounted Extension: {cog[12:]}')
            except Exception as msg:
                raise Exception(msg)

    def run(self):
        """Run the bot instance."""
        super().run(self.ld_handle.get('token')[0], reconnect=True)

    async def on_ready(self):
        print(f'Started on {self.user} with ID {self.user.id}.')

    async def on_message(self, message):
        try:
            prefix = self.ld_handle.get(str(message.guild.id))
            if not prefix:
                self.ld_handle.add({str(message.guild.id): ';'}, 'guilds')
                prefix = self.ld_handle.get(str(message.guild.id))

            if message.content.startswith(prefix[0]) and not message.author.bot:
                await self.process_commands(message)
        except Exception:
            pass

    async def on_command_error(self, context: commands.Context, exception) -> None:
        exception = getattr(exception, 'original', exception)  # Unwrap CommandInvokeError safely.

        await context.send(embed=self.templates.base_embed(f'{str(exception)}'))

    async def send(self, channel: discord.TextChannel, **kwargs):
        await channel.send(embed=self.templates.base_embed(**kwargs))
