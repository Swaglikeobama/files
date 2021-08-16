import discord
from wakeonlan import send_magic_packet
from discord.ext import commands
from discord.ext.commands.errors import CommandOnCooldown, CommandNotFound
import json
token = ""
mac_adrress = ""
import asyncio
from EmbedEngine import EmbedGen

EmbedManger = EmbedGen('Bot by Andreas Flodstroem', 'https://media.discordapp.net/attachments/748306934179823627/876837730322108446/IMG20210515151134.jpg?width=480&height=640')

with open("config.json", 'r') as CONFIG_FILE:
    CONFIG = json.load(CONFIG_FILE)
    token = CONFIG["TOKEN"]
    mac_adrress = CONFIG["mac_adrress"]

bot = commands.Bot(command_prefix='=' ,help_command=None)
@bot.event
async def on_ready():
    print("Hi i started Up :)")
    print(f"Mac Adrress:\n{mac_adrress}")

@bot.event
async def on_command_error(ctx, exception):
    if isinstance(exception, CommandNotFound):
        await ctx.send(embed=EmbedManger.error_gen(f'Command Not found'))
    elif isinstance(exception, CommandOnCooldown):
        await ctx.send(embed=EmbedManger.error_gen(exception)) 
    else:
        await ctx.send(embed=EmbedManger.error_gen(exception))

@commands.cooldown(1, 10)
@bot.command(name='start', aliases=['s'])
async def start(ctx):
    message = await ctx.send(embed=EmbedManger.description_embed("Are you sure about sending the Magic Packet", title='Magic Packet Confirmation'))
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def check(reaction, user):
        return (
            user == ctx.author and str(reaction.emoji) in ["✅", "❌"]
            and reaction.message.id == message.id
        )
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
            if str(reaction.emoji) == '✅':
                await ctx.send(embed=EmbedManger.embed_gen(colour=discord.Colour.green(),
                                            title="Sending Magic Packet",
                                            desc=f"MAC address: ``{mac_adrress}``",
                                            footer=True))
                send_magic_packet(mac_adrress)
                await ctx.send(embed=EmbedManger.embed_gen(colour=discord.Colour.green(),
                                                            title="",
                                                            desc="Successfully Sent Magic Packet.",
                                                            footer=True))
                await message.delete()
                break
            elif str(reaction.emoji) == '❌':
                await message.delete()
                break
        except asyncio.TimeoutError:
            await message.delete()
            break


@commands.cooldown(1, 10)
@bot.command(name='change_mac')
async def start(ctx, newmac):
    global mac_adrress
    global CONFIG
    message = await ctx.send(embed=EmbedManger.description_embed("Are you sure about changing the MAC Adrress ?", title='Magic Packet Confirmation'))
    await message.add_reaction("✅")
    await message.add_reaction("❌")

    def check(reaction, user):
        return (
            user == ctx.author and str(reaction.emoji) in ["✅", "❌"]
            and reaction.message.id == message.id
        )
    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
            if str(reaction.emoji) == '✅':
                mac_adrress = newmac
                CONFIG["mac_adrress"] = newmac
                with open("config.json", "w") as CONFIG_F:
                    CONFIG_F.write(json.dumps(CONFIG))
                await ctx.send(embed=EmbedManger.embed_gen(colour=discord.Colour.green(),
                                                            title="",
                                                            desc="Successfully Changed MAC Address.",
                                                            footer=True))
                await message.delete()
                break
            elif str(reaction.emoji) == '❌':
                await message.delete()
                break
        except asyncio.TimeoutError:
            await message.delete()
            break



bot.run(token)
