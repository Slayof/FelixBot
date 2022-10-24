import random # std
from random import choice
# 3rd
import roliwrapper
from discord import File, Embed, Colour, AllowedMentions
from discord.ext import commands, tasks

items = roliwrapper.ItemCache()
token = 'token here'
mad = '😡'
love = '😍'
bot = commands.Bot(
    command_prefix='.',
    allowed_mentions=AllowedMentions(roles=False, users=False, everyone=False)
)
messages = ['THEY ARE IN MY EYES',
            'MY SKIN IS GETTING VERY ITCHY',
            'THESE SCABS ARE PEELING OFF',
            'HELP ME! PLEASE!',
            'OH GOD THERE IN MY WALLS'
            ]
                #slay
exe_whitelist = [475872645586616330]

async def send_content(ctx, content):
    content = str(content)
    if len(content) <= 2000:
        await ctx.send(content)
        return

    with open('ids.txt', 'w+') as f:
        f.write(content)

    await ctx.send('Result is larger than 2,000 characters, uploading text file', file=File('ids.txt'), delete_after=1800)

async def new_embed(title, color, fields):
    embed = Embed(title=title, color=getattr(Colour, color)(), description=''.join(f'**{i}**: {fields[i] or "None"}\n' for i in fields))
    return embed

@bot.event
async def on_ready():
    global channel
    channel = await bot.fetch_channel('958566249930035260')
    print('Ready')
    update_vals.start()
    schizo.start()

@tasks.loop(minutes=10)
async def update_vals():
    items.update()

@tasks.loop(minutes=1440)
async def schizo():
    msg = choice(messages)
    await channel.send(msg)

@bot.command(name='item', help='shows all information by ID so you dont have to search.')
async def item(ctx, id_: int = None):
    if not id_:
        await ctx.send('No item id provided')
        return

    item = items[id_]
    if not item:
        await ctx.send('Invalid item id provided')
        return

    attrs = ['Id','Acronym','Rap','Value','Default_Value','Demand','Trend','Projected','Hyped','Rare']
    em = await new_embed(item.Name, 'teal', {i: getattr(item, i) for i in attrs})
    await ctx.send(embed=em)


@bot.command(name='proj', help='shows all flagged projecteds by rolimon')
async def proj(ctx):
    await send_content(ctx, proj())

@bot.command(name='valued', help='grabs all valued ids given by rolimon')
async def valued(ctx):
    await send_content(ctx, items.valued())

@bot.command(name='unvalued', help='grabs all unvalued rolimon items')
async def unvalued(ctx):
    await send_content(ctx, items.unvalued())

@bot.command(name='rare', help='grabs all rarevalued items')
async def rare(ctx):
    await send_content(ctx, items.rares())

@bot.command(name='trend', help='uses itemtable and sorts trend value')
async def trend(ctx, value):
    found_items = items.fetch_by_trend(value)
    await send_content(ctx, found_items or 'None, Lowering, Unstable, Stable, Raising, Fluctuating')

@bot.command(name='demand', help='uses itemtable and sorts which demand value')
async def demand(ctx, value):
    found_items = items.fetch_by_demand(value)
    await send_content(ctx, found_items or f'No items found with trend value ({value}) or incorrect value was passed. Trend values: None, Terrible, Low, Normal, High, Amazing')

@bot.command(name='get', help='gets id list that fit the name')
async def get(ctx, *names):
    names = [i.lower() for i in names]
    found_items = [i.Id for i in items if any(True for name in names if name in i.Name.lower() or i.Acronym.lower() == name)]
    await send_content(ctx, found_items or f'No items found with keyword(s) {", ".join(i for i in names)}')

@bot.command(name='fetch', help='Grabs ID lists either Higher / Lower to your criteria')
async def fetch(ctx, value=None, amount: int = None):
   if not value or value.lower() not in ['lower', 'higher']:
        await ctx.send('Invalid value provided. Values: lower, higher')
        return

    if not amount:
        await ctx.send('Invalid amount passed')
        return

    value = value.lower()
    found_items = [i.Id for i in items if value == 'lower' and i.Value <= amount or value == 'higher' and i.Value >= amount]
    await send_content(ctx, found_items or f'No items found with value {value} than {amount}')

@bot.check
def blacklist_check(ctx):
    blacklisted = [674014243267411998] # Write a function that gets every blacklisted user's ID from your database
    return ctx.author.id not in blacklisted # Checks if the author is in your blacklist

@bot.command(name='exe', help='only can be used by felix development for research')
async def exe(ctx, command: str = None):
    if ctx.author.id not in exe_whitelist:
        return

    result = eval(command)
    await ctx.send(result)

bot.run(token)