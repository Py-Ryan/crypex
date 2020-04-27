from os import listdir
from logging import Logger
from discord.ext import commands
from discord import Message, TextChannel
from typing import List, Dict, Any, Union
from .localdata.localdata import LocalData
from crypex.cogs.utils.template_objects import TemplateObjects
from discord.ext.commands import NoEntryPointError, ExtensionFailed, Context

cogs: List[str] = list()


def automatically_append_cogs() -> None:
    for file in listdir('crypex/cogs'):
        if file.endswith('.py'):
            file_name: List[str] = file.split('.')
            try:
                cogs.append(f'crypex.cogs.{file_name[0]}')
            except KeyError:
                raise KeyError('Could not automatically append a cog. Parsed file_name is an invalid list.')


class Crypex(commands.Bot):
    """Represents an instance of Crypex."""

    def __init__(self, logger: Logger) -> None:
        self.data: LocalData = LocalData()
        self.templates: TemplateObjects = TemplateObjects()
        self.logger: Logger = logger

        try:
            self.default_prefix: str = self.data.get('default_prefix')[0]
        except KeyError:
            self.default_prefix: str = ';'
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

    def run(self) -> None:
        """Run the bot."""

        token: List[str] = self.data.get('token')
        try:
            super().run(token[0], reconnect=True)
        except KeyError:
            raise KeyError('Missing client token.')

    async def on_ready(self) -> None:
        print(f'Started on {self.user} with ID {self.user.id}.')

    async def on_message(self, message: Message) -> None:
        prefix: List[str] = self.data.get(str(message.guild.id))
        if not prefix:
            self.data.add({str(message.guild.id): self.default_prefix}, 'guilds')
            prefix: List[str] = self.data.get(str(message.guild.id))

        try:
            if message.content.startswith(prefix[0]) and not message.author.bot:
                await self.process_commands(message)
        except KeyError:
            raise KeyError('Missing prefix.')

    async def on_command_error(self, context: Context, exception) -> None:
        exception = str(getattr(exception, 'original', exception))
        await self.send(context.channel, text=exception)
        self.logger.error(exception)

    async def send(self, channel: TextChannel, **kwargs: Union[Dict[str, Any], str]) -> None:
        await channel.send(embed=self.templates.base_embed(**kwargs))
