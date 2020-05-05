from __future__ import annotations

from typing import Optional, Union
from discord.ext.commands import command, guild_only, bot_has_permissions, has_permissions, Cog, \
    CategoryChannelConverter, BadArgument
from discord import Message, VoiceChannel, TextChannel, CategoryChannel, Member, User, Embed, HTTPException, \
    Role, PermissionOverwrite, Object as Snowflake


class GuildManagement(Cog):
    """Guild management commands."""

    def __init__(self, client):
        self.client = client
        self.untouchable_snowflakes: list[Union[Role, Member], PermissionOverwrite] = []

    @command()
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def channel(self, ctx, action, channel: Optional[Union[TextChannel, VoiceChannel]] = None,
                      *, reason: Optional[str] = 'Deleted by '):
        """Create or delete a discord text channel, or voice channel.

            Both the bot, and the command invoker require the MANAGE_CHANNELS permission.

            Channel creation flow works in a series of questions rather than putting the info in a single command line.

            Channel deletion is all in one line.

            Examples (; is example prefix)
            ------------------------------
            Deleting a channel:
                ;channel delete channel-name you are USELESS!
            Creating a channel:
                ;channel create

            Parameters
            ----------
                action:
                    The action to do. Pick between "create" and "delete".
                channel:
                    Append this if you are deleting a channel.
                reason:
                    Optional. Append this if you are deleting a channel.
        """
        if action in ('delete', 'del', 'remove'):
            if channel:
                reason += f'(Deleted by: {ctx.author.id}'
                await channel.delete(reason=reason)
                await ctx.embed(text=f'I deleted the channel "{str(channel)}" for you, {ctx.author.name}.')
            else:
                await ctx.embed(text='Please enter a channel to delete. Either ID or name.')
        elif action in ('add', 'new', 'create', 'generate'):
            check: callable[[Message], bool] = lambda message_: message_.author == ctx.author

            async def c_wait_for(msg: str, check_: callable[[Message], bool] = check) -> str:
                await ctx.embed(text=msg)
                res: Message = await self.client.wait_for('message', check=check_)
                return res.content

            channel_name: str = await c_wait_for('Enter a channel name.')
            channel_type: str = await c_wait_for('Enter a channel type. Either "Text" or "Voice"')
            channel_category: Optional[CategoryChannel, str] = \
                await c_wait_for('Enter a category to put the channel in, or "None"')

            try:
                channel_category = await CategoryChannelConverter().convert(ctx, channel_category)
            except BadArgument:
                channel_category = None

            try:
                if not channel_type.lower() in {'vc', 'voice', 'voice_channel', 'voicechannel'}:
                    channel_topic: str = await c_wait_for('Enter a channel topic.')
                    await ctx.guild.create_text_channel(
                        name=channel_name,
                        topic=channel_topic,
                        category=channel_category)
                else:
                    await ctx.guild.create_voice_channel(
                        name=channel_name,
                        category=channel_category)

                await ctx.embed(text=f'Done! Created a {channel_type} channel named "{channel_name}"!')
            except Exception as message:
                await ctx.embed(text='Discord won\'t let me create a channel. The info you gave does not work. ):')
                raise message
        else:
            await ctx.embed(text='Pick an action to do! "create" a channel, or "delete" a channel!')

    @command()
    @guild_only()
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def ban(self, ctx, user: Union[Member, User, int], *, reason='None Provided'):
        """Ban a discord user, whether in the guild, or not.

            Both the bot, and the command invoker require the BAN_MEMBERS permission.

            This command supports hackbanning, the idea of banning a user not in your guild.

            You can hackban a user by inputting their Discord ID, or Name#Discrim as the user argument.

            Sadly, name#tag hackbanning does not support users with a space in their username.
            Stick to ID for these users ^

            Examples (; is example prefix):
            -------------------------------

            Normal ban:
                ;ban @member looool!!!!

            Hack ban #1:
                ;ban herbs#0082 piss off.

            Hack ban #2 (preferred):
                ;ban 198233322080567296 goodbye!

            Parameters
            ---------
                user:
                    The user to ban.
                reason:
                    Optional. Why you are banning the user.
        """
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
        """Unban a user from your guild.

            Both the bot, and the command invoker require the BAN_MEMBERS permission.

            This also supports hackunbanning in the same formats as the ban command.

            Examples (; as example prefix):
                Preferred:
                    ;unban 198233322080567296 come back, please!
                Other:
                    ;unban herbs#0082 wake!

            Parameters
            ---------
                user:
                    The user to unban. Preferred a user ID.
                reason:
                    Optional. The reason the user is being unbanned.
        """
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
        """Kick a member from your guild.

            Both the bot, and the command invoker require the KICK_MEMBERS permission.

            Examples (; as example prefix):
                ;kick @member peace out, dawg!

            Parameters:
                user:
                    The guild member you want to kick.
                reason:
                    Optional. Why they're being kicked.
        """
        if ctx.author.top_role <= user.top_role:
            await ctx.embed(text=f'You can\'t kick a user that\'s higher than you, {ctx.author.name}.')
        else:
            embed: Embed = self.client.templates.base_embed()
            embed.title = f'You have been kicked from {ctx.guild.name}'
            embed.add_field(name='Kicked By:', value=f'{ctx.author}\n({ctx.author.id})', inline=True)
            embed.add_field(name='Reason:', value=reason, inline=True)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.set_footer(icon_url=self.client.user.avatar_url, text='Sorry, mate. - Crypex Bot.')
            await user.send(embed=embed)
            await user.kick(reason=reason)
            await ctx.embed(text=f'Goodbye, {user.name}!')

    @command()
    @guild_only()
    @bot_has_permissions(manage_members=True)
    @has_permissions(manage_members=True)
    async def mute(self, ctx, user: Member, *, reason='None provided.'):
        """Mute a member in your guild.

            Both the bot and the command invoker require the MANAGE_MEMBERS permission.

            There is no auto-unmute or tempmute. You are responsible for unmuting your members.

            This command does not rely on a mute role.

            Examples (with ; as example prefix):
                ;mute @user SHUT UP!

            Parameters:
                user:
                    The guild member to mute.
                reason:
                    Optional. Why they're being muted.
        """
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
        """Unmute a member in your guild.

            Both the bot and the command invoker require the MANAGE_MEMBERS permission.

            Due to their being no mute role used for muting, this is about the fastest and best way to unmute a member.

            Examples (with ; as example prefix):
                ;unmute @user Time's up, bud.

            Parameters:
                user:
                    The guild member to unmute.
                reason:
                    Optional. Why they're being unmuted.
        """
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
        """Purge x amount of message from a channel. Use clear_channel command for bulk deletion above 1000.

            Both the bot and the command invoker require the MANAGE_MESSAGES permission.

            Purge supports amounts up to 1000 with a (future) command cooldown to avoid API Abuse.

            If you wish to delete a large amount of messages quickly, use the clear_channel command.

            Examples (with ; as example prefix):
                ;purge 100
                ;purge 100 @member

            Parameters:
                amount:
                    The amount of messages to delete.
                member:
                    Optional. If set, this will only delete messages that are authored by member.
        """
        if amount <= 1000:
            if member:
                await ctx.channel.purge(limit=amount, check=lambda message_: message_.author == member)
            else:
                await ctx.channel.purge(limit=amount)
        elif amount > 1000:
            await ctx.embed(text=f'The amount cannot be larger than 1000, {ctx.author.name}.')
        elif not amount:
            await ctx.embed(text=f'That is not a valid amount, {ctx.author.name}.')

    @command()
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def clear_channel(self, ctx):
        """"Clear" a channel by deleting it, then cloning it.

            Both the bot and the command invoker require the MANAGE_CHANNELS permission.

            This command is best for massive bulk message deletion.

            Also, the cloned channel is completely identical to the original channel.

            Examples (with ; as example prefix):
                ;clear_channel
        """
        await ctx.channel.clone()
        await ctx.channel.delete()
        await ctx.embed(text='Successfully cleared the channel.')

    @command()
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def silence(self, ctx):
        """Stop literally everyone from being able to send a message in the channel.

            Both the bot, and the command invoker require the MANAGE_CHANNELS permission.

            This stops everyone, except Administrators from being able to chat in the channel the command is called in.

            Examples (with ; as example prefix):
                ;silence
        """
        for snowflake in ctx.channel.overwrites:
            if ctx.channel.overwrites_for(snowflake).send_messages:  # Avoid touching mute roles.
                await ctx.channel.set_permissions(snowflake, send_messages=False)
            else:
                self.untouchable_snowflakes.append(snowflake)

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.embed(text=f'Silenced {ctx.channel.name}. (:')

    @command()
    @guild_only()
    @bot_has_permissions(manage_channels=True)
    @has_permissions(manage_channels=True)
    async def unsilence(self, ctx):
        """This unsilences a silenced channel.

            Both the bot, and the command invoker require the MANAGE_CHANNELS permission.

            Examples (with ; as the example prefix):
                ;unsilence
        """
        for snowflake in ctx.channel.overwrites:
            if snowflake not in self.untouchable_snowflakes:
                await ctx.channel.set_permissions(snowflake, send_messages=True)

        await ctx.embed(text=f'Unsilenced {ctx.channel.name}. ):')


def setup(client):
    client.add_cog(GuildManagement(client))
