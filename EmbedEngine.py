import discord
from datetime import datetime

class EmbedGen():
    def __init__(self, footer, icon_url):
        self.footer = footer
        self.icon = icon_url
    
    def error_gen(self, content):
        embed = discord.Embed(colour=discord.Color.dark_red(), description=content)
        embed.set_thumbnail(url='https://statsify.net/img/assets/error.gif')
        return embed
    
    def leaderboard_embed(self, content, mode, page):
        embed = discord.Embed(colour=discord.Color.dark_blue(), description=content, title=f'LeaderBoard {mode.upper()} #{page}', timestamp=datetime.utcnow())
        embed.set_footer(text=self.footer, icon_url=self.icon)
        return embed
    
    def description_embed(self, content, thun=None, title=''):
        embed = discord.Embed(title=title, colour=discord.Color.blue(), description=content, timestamp=datetime.utcnow())
        embed.set_footer(text=self.footer, icon_url=self.icon)
        if thun != None:
            embed.set_thumbnail(url=thun)
        return embed

    def feild_embed(self, title, fields:list):
        embed = discord.Embed(title=title, colour=discord.Color.blue(),  timestamp=datetime.utcnow())
        embed.set_footer(text=self.footer, icon_url=self.icon)
        for field in fields:
            embed.add_field(
                name=field['name'],
                value=field['value'] or '\u2063',
                inline=False
            )
        return embed

    def embed_gen(self, title="", fields=None, desc="", colour=0, thun=None, timestamp=None, footer=False, author=None):
        if timestamp:
            embed = discord.Embed(title=title, description=desc, colour=colour, timestamp=timestamp)
        else:
            embed = discord.Embed(title=title, description=desc, colour=colour)
        if thun: embed.set_thumbnail(url=thun)
        if footer: embed.set_footer(text=self.footer, icon_url=self.icon)
        if fields:
            for field in fields:
                embed.add_field(
                    name=field['name'],
                    value=field.get("value", "\u2063"),
                    inline=field.get("inline", False)
                )
        if author:
            embed.set_author(name=author[0], icon_url=author[1])
        return embed
