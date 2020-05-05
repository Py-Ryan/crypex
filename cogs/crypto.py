from discord import DMChannel, Embed
from discord.ext.commands import Cog, command


class Crypto(Cog):

    def __init__(self, client):
        self.client = client

    @command()
    async def hex(self, ctx, *, string):
        """Convert a string to hexadecimal.

            Examples (with ; as example prefix)
            ;hex bro bruh needle LMAOOOOO

            Parameters
            ----------
            string:
                The string to convert into hexadecimal.
        """
        _hex = ''.join(map(hex, string.encode())).replace('0x', '')
        if len(string) > 100 and not isinstance(ctx.channel, DMChannel):
            await ctx.embed(text=f'Long request. I\'ll send it to your DMs, {ctx.author}')
            await ctx.embed(user=ctx.author, text=_hex)
        else:
            await ctx.embed(text=_hex)

    @command()
    async def dehex(self, ctx, *, digest):
        """Convert a crypex hex digest back to a string.

            Examples (with ; as example prefix):
                ;dehex 6173646d6b616c646b6d776b

            Parameters
            ----------
            digest:
                The digest to convert back to a string.
        """
        _string = bytearray.fromhex(digest).decode()
        if len(digest) > 200 and not isinstance(ctx.channel, DMChannel):
            await ctx.embed(text=f'Long request. I\'ll send it to your DMs, {ctx.author}')
            await ctx.embed(user=ctx.author, text=_string)
        else:
            await ctx.embed(text=_string)


def setup(client):
    client.add_cog(Crypto(client))
