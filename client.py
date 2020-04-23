import discord
from discord.ext import commands
from .localdata import localdata
from typing import List
from crypex.cogs.utils.template_objects import TemplateObjects


class Crypex(commands.Bot):
    """Represents an instance of Crypex."""

    def __init__(self) -> None:
        self.ld_handle = localdata.LocalData()
        self.templates = TemplateObjects()
        super().__init__(command_prefix=self.ld_handle.get('default_prefix')[0])

    def run(self) -> None:
        """Run the bot instance."""
        super().run(self.ld_handle.get('token')[0], reconnect=True)

    async def close(self) -> None:
        """Close the bot instance."""
        await super().close()

    async def on_ready(self) -> None:
        print(f'Started on {self.user} with ID {self.user.id}.')

    async def on_message(self, message: discord.Message) -> None:
        prefix: List[str] = self.ld_handle.get(str(message.guild.id))
        if not prefix:
            self.ld_handle.add({str(message.guild.id): ';'}, 'guilds')
            prefix: List[str] = self.ld_handle.get(str(message.guild.id))

        if message.content.startswith(prefix[0]) and not message.author.bot:
            await self.process_commands(message)

    async def on_command_error(self, context: commands.Context, exception) -> None:
        exception = getattr(exception, 'original', exception)  # Unwrap CommandInvokeError safely.

        await context.send(embed=self.templates.base_embed(f'{str(exception)}.'))
