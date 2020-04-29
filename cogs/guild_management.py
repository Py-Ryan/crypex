from typing import Optional, Union, Set, List, Callable
from discord.ext.commands import command, guild_only, bot_has_permissions, has_permissions, Cog, \
    CategoryChannelConverter, BadArgument
from discord import Message, VoiceChannel, TextChannel, CategoryChannel, Member, User, Embed, HTTPException, \
    Role, PermissionOverwrite, Object as Snowflake


class GuildManagement(Cog):
    """Guild management commands."""

    def __init__(self, client):
        self.client = client
        self.untouchable_snowflakes: List[Union[Role, Member], PermissionOverwrite] = []

    @command()
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def create_channel(self, ctx):
        check: Callable[[Message], bool] = lambda message_: message_.author == ctx.author
        await ctx.embed(text='What should the channel\'s name be?')
        channel_name: Message = await self.client.wait_for('message', check=check)

        await ctx.embed(text='Should the channel be a VC or Text? Pick one.')
        channel_type: Message = await self.client.wait_for('message', check=check)

        await ctx.embed(text='If you\'d like the channel to be added to a category.'
                             'Enter that categories exact name. If not, say no.')
        category_name: Optional[Message] = await self.client.wait_for('message', check=check)

        try:
            category_name: Optional[CategoryChannel] = \
                await CategoryChannelConverter().convert(ctx, category_name.content)
        except BadArgument:  # In case there is no category matching the argument.
            category_name = None

        channel_options: Set[str] = {'vc', 'voice', 'voicechannel', 'voice_channel'}
        if channel_type.content not in channel_options:
            await ctx.embed(text='Enter a channel topic.')
            topic: Message = await self.client.wait_for('message', check=check)

        if channel_name and channel_type.content.lower() in channel_options:
            await ctx.guild.create_voice_channel(name=channel_name.content,
                                                 category=category_name)

        elif channel_name and channel_type and topic:
            await ctx.guild.create_text_channel(name=channel_name.content,
                                                category=category_name,
                                                topic=topic.content)

        await ctx.embed(text='Alright, done.')

    @command()
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def delete_channel(self, ctx, channel: Union[TextChannel, VoiceChannel], *, reason='None Provided.'):
        try:
            await channel.delete(reason=reason)
            await ctx.embed(text=f'Goodbye, {channel.name}!')
        except Exception:
            raise Exception(f'There is no channel named {str(channel)}')

    @command()
    @guild_only()
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban(self, ctx, user: Union[Member, User, int], *, reason='None Provided'):
        if isinstance(user, Member):
            if ctx.author.top_role <= user.top_role:
                await ctx.embed(text='You can\'t ban a user that\'s higher than you.')

        if isinstance(user, int):
            user: Snowflake = Snowflake(id=user)

        if isinstance(user, Member):
            embed: Embed = self.client.templates.base_embed()
            embed.title = f'You have been banned from {ctx.guild.name}.'
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name='Banned By:', value=f'{ctx.author}\n({ctx.author.id})', inline=True)
            embed.add_field(name='Ban Reason:', value=reason, inline=True)
            embed.set_footer(icon_url=self.client.user.avatar_url, text='Sorry, man. - Crypex Bot')
            await user.send(embed=embed)

        try:
            await ctx.guild.ban(user, reason=reason)
            if isinstance(user, Snowflake):
                user: str = user.id
                # I am aware user.id should return an integer. `user` is annotated as a string
                # because it will be implicitly converted into one in the next line.
            await ctx.embed(text=f'Goodbye, {user}!')
        except Exception:
            if isinstance(user, Snowflake):
                user: str = user.id
            raise Exception(f'I can\'t find anyone on Discord by the ID of {user}.')

    @command()
    @guild_only()
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def unban(self, ctx, user: Union[Member, User, int], *, reason='None provided.'):
        if isinstance(user, int):
            user: Snowflake = Snowflake(id=user)

        try:
            await ctx.guild.unban(user, reason=reason)
            await ctx.embed(text=f'Successfully unbanned {user.id}.')
        except HTTPException:
            raise Exception(f'Either there is no user under that ID that is banned, or, '
                            f'I could not find any users on discord with the ID of {user.id}.')

    @command()
    @guild_only()
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick(self, ctx, user: Member, *, reason='None provided.'):
        if ctx.author.top_role <= user.top_role:
            await ctx.embed(text='You can\'t kick a user that\'s higher than you.')
        else:
            embed: Embed = self.client.templates.base_embed()
            embed.title = f'You have been kicked from {ctx.guild.name}'
            embed.add_field(name='Kicked By:', value=f'{ctx.author}\n({ctx.author.id})', inline=True)
            embed.add_field(name='Reason:', value=reason, inline=True)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(icon_url=self.client.user.avatar_url, text='Sorry, mate. - Crypex Bot.')
            await user.send(embed=embed)
            await user.kick(reason=reason)
            await ctx.embed(text=f'Goodbye, {user.display_name}!')

    @command()
    @guild_only()
    @bot_has_permissions(manage_members=True)
    @has_permissions(manage_members=True)
    async def mute(self, ctx, user: Member, *, reason='None provided.'):
        if ctx.author.top_role <= user.top_role:
            await ctx.embed(text='You can\'t mute a user that\'s higher than you.')
        else:
            for channel in ctx.guild.channels:
                if not isinstance(channel, VoiceChannel):
                    await channel.set_permissions(user, send_messages=False)
                else:
                    await channel.set_permissions(user, speak=False)

            embed: Embed = self.client.templates.base_embed()
            embed.title = f'You\'ve been muted in {ctx.guild.name}.'
            embed.add_field(name='Muted By:', value=f'{ctx.author}\n({ctx.author.id})', inline=True)
            embed.add_field(name='Reason:', value=reason, inline=True)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await user.send(embed=embed)
            await ctx.embed(text=f'{user} will be shutten up until you decide otherwise.')

    @command()
    @guild_only()
    @bot_has_permissions(manage_members=True)
    @has_permissions(manage_members=True)
    async def unmute(self, ctx, user: Member, *, reason='Time\'s up.'):
        if ctx.author.top_role <= user.top_role:
            await ctx.embed(text='You can\'t unmute a user that\'s higher than you.')
        else:
            for channel in ctx.guild.channels:
                if isinstance(channel, (TextChannel, CategoryChannel)):
                    await channel.set_permissions(user, send_messages=True)
                else:
                    await channel.set_permissions(user, speak=True)

            embed: Embed = self.client.templates.base_embed()
            embed.title = f'You\'ve been unmuted in {ctx.guild.name}.'
            embed.add_field(name='Unmuted By:', value=f'{ctx.author}\n({ctx.author.id})', inline=True)
            embed.add_field(name='Reason:', value=reason, inline=True)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await user.send(embed=embed)
            await ctx.embed(text=f'{user} can now speak again.')

    @command()
    @guild_only()
    @bot_has_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int, member: Optional[Member] = None):
        if amount:
            if member:
                await ctx.channel.purge(limit=amount, check=lambda message_: message_.author == member)
            else:
                await ctx.channel.purge(limit=amount)
        else:
            await ctx.embed(text='The amount must be 1 or above, y\'know.')

    @command()
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def clear_channel(self, ctx):
        await ctx.channel.clone()
        await ctx.channel.delete()
        await ctx.embed(text='Successfully cleared the channel.')

    @command()
    @guild_only()
    @bot_has_permissions(administrator=True)
    @has_permissions(administrator=True)
    async def silence(self, ctx):
        for snowflake in ctx.channel.overwrites:
            if ctx.channel.overwrites_for(snowflake).send_messages:  # Avoid touching mute roles.
                await ctx.channel.set_permissions(snowflake, send_messages=False)
            else:
                self.untouchable_snowflakes.append(snowflake)

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.embed(text=f'Silenced {ctx.channel.name}. (:')

    @command()
    @guild_only()
    @bot_has_permissions(administrator=True)
    @has_permissions(administrator=True)
    async def unsilence(self, ctx):
        for snowflake in ctx.channel.overwrites:
            if snowflake not in self.untouchable_snowflakes:
                await ctx.channel.set_permissions(snowflake, send_messages=True)

        await ctx.embed(text=f'Unsilenced {ctx.channel.name}. ):')


def setup(client):
    client.add_cog(GuildManagement(client))
