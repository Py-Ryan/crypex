from discord.ext import commands
from typing import Optional, Union
from discord.ext.commands import command, guild_only, bot_has_permissions, has_permissions, Context
from discord import Message, VoiceChannel, TextChannel, CategoryChannel, Member, User, Embed, Object


class GuildManagement(commands.Cog):
    """Guild management commands."""

    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client

    @command()
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def create_channel(self, ctx: Context) -> None:
        def check(message: Message) -> bool:
            return message.author == ctx.author

        await self.client.send(ctx.channel, text='What should the channel\'s name be?')
        channel_name: Message = await self.client.wait_for('message', check=check)

        await self.client.send(ctx.channel, text='Should the channel be a VC or Text? Pick one.')
        channel_type: Message = await self.client.wait_for('message', check=check)

        await self.client.send(ctx.channel, text='If you\'d like the channel to be added to a category.'
                                                 'Enter that categories exact name. If not, say no.')
        category_name: Optional[Message] = await self.client.wait_for('message', check=check)

        try:
            category_name: Optional[CategoryChannel] = \
                await commands.CategoryChannelConverter().convert(ctx, category_name.content)
        except commands.BadArgument:  # In case there is no category matching the argument.
            category_name = None
            pass

        channel_options = {'vc', 'voice', 'voicechannel', 'voice_channel'}
        if channel_type.content not in channel_options:
            await self.client.send(ctx.channel, text='Enter a channel topic.')
            topic: Message = await self.client.wait_for('message', check=check)

        if channel_name and channel_type.content.lower() in channel_options:
            await ctx.guild.create_voice_channel(name=channel_name.content,
                                                 category=category_name)

        elif channel_name and channel_type and topic:
            await ctx.guild.create_text_channel(name=channel_name.content,
                                                category=category_name,
                                                topic=topic.content)

        await self.client.send(ctx.channel, text='Alright, done.')

    @command()
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def delete_channel(self, ctx: Context, channel: Union[TextChannel, VoiceChannel], *, reason='None Provided.'):
        try:
            await channel.delete(reason=reason)
            await self.client.send(ctx.channel, text=f'Goodbye, {channel.name}!')
        except Exception:
            raise Exception(f'There is no channel named {str(channel)}')

    @command()
    @guild_only()
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban(self, ctx: Context, user: Union[Member, User, int], *, reason: str = 'None Provided'):
        if isinstance(user, int):
            user: Object = Object(id=user)

        if user in ctx.guild.members:
            embed: Embed = self.client.templates.base_embed()
            embed.title = f'You have been banned from {ctx.guild.name}.'
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name='Banned By:', value=f'{ctx.author}\n({ctx.author.id})', inline=True)
            embed.add_field(name='Ban Reason:', value=reason, inline=True)
            embed.set_footer(icon_url=self.client.user.avatar_url, text='Sorry, man. - Crypex Bot')
            await user.send(embed=embed)

        try:
            await ctx.guild.ban(user, reason=reason)
            if isinstance(user, Object):
                user: str = user.id

            await self.client.send(ctx.channel, text=f'Goodbye, {user}!')
        except Exception:
            if isinstance(user, Object):
                user: str = user.id

            raise Exception(f'I can\'t find anyone on Discord by the ID of {user}.')


def setup(client):
    client.add_cog(GuildManagement(client))
