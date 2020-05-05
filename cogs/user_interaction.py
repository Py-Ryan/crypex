from typing import Union, Optional
from discord import Member, User, Embed
from discord.ext.commands import Cog, command


class UserInteraction(Cog):
    """Commands for general user interaction"""

    def __init__(self, client):
        self.client = client

    @command()
    async def av(self, ctx, user: Optional[Union[Member, User]] = None):
        """Get the avatar of the user mentioned.

            If no user is mentioned, the user defaults to the command invoker.

            Examples (with ; as example prefix):
                ;av @herbs

            Parameters
            ----------
                user:
                    The user in mention.
        """
        user: Union[Member, User] = user or ctx.author
        embed: Embed = Embed().set_image(url=user.avatar_url)
        embed.title = f'{user.name}\'s avatar:'
        embed.set_footer(text=f'Requested by {ctx.author.name} ({ctx.author.id})')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(UserInteraction(client))
