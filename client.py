from os import listdir
from typing import List
from traceback import extract_tb
from discord.ext import commands
from .localdata.localdata import LocalData
from crypex.cogs.utils.context import Context
from crypex.cogs.utils.template_objects import TemplateObjects
from discord.ext.commands import NoEntryPointError, ExtensionFailed

cogs = list()


def automatically_append_cogs():
    for file in listdir('crypex/cogs'):
        if file.endswith('.py'):
            try:
                cogs.append(f'crypex.cogs.{file[:-3]}')
            except KeyError:
                raise KeyError('Could not automatically append a cog. Parsed file_name is an invalid list.')


class Crypex(commands.Bot):
    """Represents an instance of Crypex."""

    def __init__(self, logger):
        self.data = LocalData()
        self.templates = TemplateObjects()
        self.logger = logger

        try:
            self.default_prefix = self.data.get('default_prefix')[0]
        except KeyError:
            self.default_prefix = ';'
            raise KeyError('Missing default_prefix.')

        super().__init__(command_prefix=self.default_prefix)

        automatically_append_cogs()
        for cog in cogs:
            try:
                self.load_extension(cog)
                print(f'Mounted Extension: {cog[12:]}')
            except NoEntryPointError as msg:
                raise NoEntryPointError(msg)
            except ExtensionFailed as msg:
                raise ExtensionFailed(msg, msg.original)

    def run(self):
        """Run the bot."""

        token: List[str] = self.data.get('token')
        try:
            super().run(token[0], reconnect=True)
        except KeyError:
            raise KeyError('Missing client token.')

    async def on_ready(self):
        print(f'Started on {self.user} with ID {self.user.id}.')

    async def on_message(self, message):
        prefix: List[str] = self.data.get(str(message.guild.id))
        if not prefix:
            self.data.add({str(message.guild.id): self.default_prefix}, 'guilds')
            prefix: List[str] = self.data.get(str(message.guild.id))
        try:
            if message.content.startswith(prefix[0]) and not message.author.bot:
                ctx = await self.get_context(message, cls=Context)
                await self.invoke(ctx)
        except KeyError:
            raise KeyError('Missing prefix.')

    async def on_command_error(self, context, exception):
        exception = getattr(exception, 'original', exception)

        await self.send(context.channel, text=str(exception))
        self.logger.error(str(extract_tb(exception.__traceback__)))

    async def send(self, channel, **kwargs):
        await channel.send(embed=self.templates.base_embed(**kwargs))
