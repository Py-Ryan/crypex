import discord
import datetime
from discord.ext import commands
from typing import Optional, List, Union


class GuildManagement(commands.Cog):
    """Guild management commands."""

    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def create_channel(self, ctx: commands.Context):
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
        try:
            def _check_(message) -> bool:
                return message.author == ctx.author

            await ctx.send(embed=self.client.templates.base_embed('What should the channel\'s name be?'))
            channel_name: str = await self.client.wait_for('message', check=_check_)

            await ctx.send(embed=self.client.templates.base_embed('Should the channel be a VC or Text? Pick one.'))
            channel_type: str = await self.client.wait_for('message', check=_check_)

            await ctx.send(embed=self.client.templates.base_embed(
                'If you\'d like the channel to be added to a category, enter that categories exact name. Else say no.'))
            category_name: str = await self.client.wait_for('message', check=_check_)

            try:
                category_name: Optional[discord.CategoryChannel] = \
                    await commands.CategoryChannelConverter().convert(ctx, category_name.content)
            except commands.BadArgument:    # In case there is no category matching the argument.
                pass

            #   Thanks d.py. commands.CategoryChannelConverter().convert(...) returns an exception, rather than a falsy.
            if not isinstance(category_name, discord.CategoryChannel):
                category_name = None

            await ctx.send(embed=self.client.templates.base_embed('Enter a channel topic.'))
            topic: str = await self.client.wait_for('message', check=_check_)

            if channel_name and channel_type.content.lower() in {'vc', 'voice', 'voicechannel', 'voice_channel'}:
                await ctx.guild.create_voice_channel(name=channel_name.content,
                                                     category=category_name)
            elif channel_name and channel_type and topic:
                await ctx.guild.create_text_channel(name=channel_name.content,
                                                    category=category_name,
                                                    topic=topic.content)
        except Exception as e:
            raise Exception('Oops. I can\'t create a channel with the information you gave, sorry!')

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def delete_channel(self, ctx: commands.Context, channel: Union[discord.TextChannel, discord.VoiceChannel],
                             *reason) -> None:
        """Delete a channel.

            Parameters
            ----------
            channel: (str)
                The exact name of the channel to delete.
            reason: (Optional[str])
                The reason for deleting the channel.
        """
        if not reason:
            reason = ['None']
        try:
            await channel.delete(reason=' '.join(reason))
            await ctx.send(embed=self.client.templates.base_embed(f'Goodbye, {str(channel)}!'))
        except Exception:
            raise Exception(f'There is no channel named {str(channel)}')

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, _user: Union[discord.Member, discord.User, int], *reason) -> None:
        """Ban a guild member.

            member: (discord.Member)
                The member to ban.
            reason: (Optional[str])
                The reason for the ban.
        """
        user = _user
        if type(user) is int:
            try:
                user = discord.Object(id=_user)
            except Exception:
                raise Exception(f'There is no user with the id {user}')

        # Prevent 'reason' from appearing as an empty tuple.
        if not reason:
            reason = ['None']

        if user in ctx.guild.members:
            embed = self.client.templates.base_embed()
            embed.title = f'You have been banned from {ctx.guild.name}.'
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name='Banned By:', value=f'{ctx.author}\n({ctx.author.id})', inline=True)
            embed.add_field(name='Ban Reason:', value=' '.join(reason), inline=True)
            embed.set_footer(icon_url=user.avatar_url, text='Sorry, man. - Crypex Bot')
            await user.send(embed=embed)

        await ctx.guild.ban(user, reason=' '.join(reason))
        # So the embed does not show 'user' as a class representation.
        if user.__class__ not in {discord.Member, discord.User}:
            user = _user
        await ctx.send(embed=self.client.templates.base_embed(f'Goodbye, {user}!'))


def setup(client: commands.Bot) -> None:
    client.add_cog(GuildManagement(client))
