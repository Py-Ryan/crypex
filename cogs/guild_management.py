import discord
from discord.ext import commands
from typing import Optional, Union


class GuildManagement(commands.Cog):
    """Guild management commands."""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def create_channel(self, ctx):
        """Create a channel.

            Parameters
            ----------
                channel_name: (str)
                    The name of the channel.
                channel_type: (str)
                    Either vc, or text.
                category_name: (str) Optional
                    The name of the category to put the channel in.
                topic: (str)
                    The topic of the channel.
        """

        def _check_(message) -> bool:
            return message.author == ctx.author

        await self.client.send(ctx.channel, text='What should the channel\'s name be?')
        channel_name: str = await self.client.wait_for('message', check=_check_)

        await self.client.send(ctx.channel, text='Should the channel be a VC or Text? Pick one.')
        channel_type: str = await self.client.wait_for('message', check=_check_)

        await self.client.send(ctx.channel, text='If you\'d like the channel to be added to a category.'
                                                 'Enter that categories exact name. If not, say no.')
        category_name: str = await self.client.wait_for('message', check=_check_)

        try:
            category_name: Optional[discord.CategoryChannel] = \
                await commands.CategoryChannelConverter().convert(ctx, category_name.content)
        except commands.BadArgument:  # In case there is no category matching the argument.
            category_name = None
            pass

        await self.client.send(ctx.channel, text='Enter a channel topic.')
        topic: str = await self.client.wait_for('message', check=_check_)

        if channel_name and channel_type.content.lower() in {'vc', 'voice', 'voicechannel', 'voice_channel'}:
            await ctx.guild.create_voice_channel(name=channel_name.content,
                                                 category=category_name)
        elif channel_name and channel_type and topic:
            await ctx.guild.create_text_channel(name=channel_name.content,
                                                category=category_name,
                                                topic=topic.content)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def delete_channel(self, ctx, channel: Union[discord.TextChannel, discord.VoiceChannel], *,
                             reason='None Provided.'):
        """Delete a channel from your guild.

            Parameters
            ----------
            channel: (str)
                The exact name of the channel to delete.
            reason: (Optional[str])
                The reason for deleting the channel.
        """
        try:
            await channel.delete(reason=reason)
            await self.client.send(ctx.channel, text=f'Goodbye, {channel.name}!')
        except Exception:
            raise Exception(f'There is no channel named {str(channel)}')

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: Union[discord.Member, discord.User, int], *, reason='None Provided'):
        """Ban a user on discord from your guild.

            user: (Union[discord.Member, discord.User, discord.Object])
                The member to ban.
            reason: (Optional[str])
                The reason for the ban.
        """
        if isinstance(user, int):
            user = discord.Object(id=user)

        if user in ctx.guild.members:
            embed = self.client.templates.base_embed()
            embed.title = f'You have been banned from {ctx.guild.name}.'
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name='Banned By:', value=f'{ctx.author}\n({ctx.author.id})', inline=True)
            embed.add_field(name='Ban Reason:', value=reason, inline=True)
            embed.set_footer(icon_url=user.avatar_url, text='Sorry, man. - Crypex Bot')
            await user.send(embed=embed)

        try:
            await ctx.guild.ban(user, reason=reason)
            if isinstance(user, discord.Object):
                user = user.id

            await self.client.send(ctx.channel, text=f'Goodbye, {user}!')
        except Exception:
            if isinstance(user, discord.Object):
                user = user.id

            raise Exception(f'I can\'t find anyone on Discord by the ID of {user}.')


def setup(client):
    client.add_cog(GuildManagement(client))
