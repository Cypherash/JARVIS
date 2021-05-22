import feedparser
import re
from decimal import Decimal
from password import KEY, IEX_TOKEN, CMK_TOKEN
from discord.ext import commands
import json
from weather import *
import requests

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
Weather_api_key ="c0142903c7c65d3f19547fa1d8714ed9"



description = '''Discord bot for fetching Crypto and Stock Prices in discord'''
bot = commands.Bot(command_prefix='[!,$]', description=description)


portfolio = {}

@bot.event
async  def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="~weather.[location]"))
    #await client.change_presence(
        #activity=discord.Activity(type=discord.ActivityType.listening, name="~Command.Name"))
@bot.event
async def on_member_join(member):
    guild = client.get_guild(841236654629847041)
    channel = guild.get_channel(841236655151120406)
    await channel.send(
        f''' HEY {member.mention}!:partying_face:, Welcome to the Cypherash & Sam's Clubhouse
        If you got your interests with you and a will you help
        others. This is the place you've been looking for .
        I'm JARVIS , A tour guide and 24*7 ready Virtual Assitant 
        for anyone in this Clubhouse.
        Wanna know what I can do? Check Your DM:''')
    await member.send(
        f'''Sup?{member.name} 
        Here are some tips to use JARVIS Properly
         1. "~" this is the symbol for calling ME.
         2.''')



@bot.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.content.lower().startswith("~Hello.Jarvis"):
        await message.channel.send("Greetings , This Is Me JARVIS!")
    elif message.author != client.user and message.content.startswith("~weather." or "~Weather."):
        location = message.content.replace("~weather." or "~Weather.", '').lower()
        if len(location) >= 1:
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={Weather_api_key}&units=metric"
                data = json.loads(requests.get(url).content)
                data = parse_data(data)
                await message.channel.send(embed=weather_message(data, location))
            except KeyError:
                await message.channel.send(embed=weather_error_message(location))
    elif message.content.lower().startswith(('!help')):
        await message.channel.trigger_typing()
        Help = discord.Embed(title="Help Menu", description="Commands")
        Help.add_field(name="!COIN_TICKER", value="Gets the latest cryptocurrency price")
        Help.add_field(name="\u200B", value="\u200B")
        Help.add_field(name="\u200B", value="\u200B")
        Help.add_field(name="$STOCK_TICKER", value="Gets the latest stock price")
        Help.add_field(name="\u200B", value="\u200B")
        Help.add_field(name="\u200B", value="\u200B")
        Help.add_field(name="!prez, !dprez, !rprez", value="PredictIt Market info for presidential candidate")
        Help.add_field(name="\u200B", value="\u200B")
        Help.add_field(name="\u200B", value="\u200B")
        Help.add_field(name="!news", value="Crypto News")
        await message.channel.send(embed=Help)
    elif message.content.lower().startswith('!news'):
        await message.channel.trigger_typing()
        crypto = feedparser.parse(
            "https://news.google.com/news/rss/search/section/q/cryptocurrency/cryptocurrency?hl=en&gl=US&ned=us/.rss")
        cryptoLinks = []
        for post in crypto.entries:
            cryptoLinks.append(post.link)
        await message.channel.send(str(cryptoLinks[0] + '\n' + cryptoLinks[1]))
    elif re.match("(^![a-zA-Z]{2}$)", message.content) != None:
        await message.channel.trigger_typing()
        t = str(message.content[1:].split()[0]).lower()
        await message.channel.send(embed=COVID(t))
        # function call here
    elif message.content.startswith("!"):
        await message.channel.trigger_typing()
        t = str(message.content[1:].split()[0])
        coin, cost, per = coinMarketCapPrice(t.upper())
        # If ticker not found
        if (cost == -1):
            await message.channel.send('```Ticker Not Found```')
        else:
            # change colors of message if coin is currently up or down
            if (float(per) < 0):
                c = discord.Colour(0xCD0000)
            elif (float(per) > 0):
                c = discord.Colour(0x00ff00)
            else:
                c = discord.Colour(0xffffff)
            chart = 'http://c.stockcharts.com/c-sc/sc?s=%24' + t.upper() + 'USD&p=D&b=5&g=0&i=0'
            # Creates embeded message
            embedCoin = discord.Embed(title=coin, description=t.upper() + ": $" + cost + " " + per + "% ", color=(c))
            embedCoin.set_image(url=chart)
            await message.channel.send(embed=embedCoin)

    elif message.content.startswith("$"):
        await message.channel.trigger_typing()
        t = str(message.content[1:].split()[0])
        company, cost, per = IEXPrice(t.upper())
        if (cost == -1):
            await message.channel.send('```Ticker Not Found```')
        else:
            # change colors of message if stock is currently up or down
            if (float(per) < 0):
                c = discord.Colour(0xCD0000)
            elif (float(per) > 0):
                c = discord.Colour(0x00ff00)
            else:
                c = discord.Colour(0xffffff)
            # get chart (. is replace with / for things like brk.a)
            chart = 'http://c.stockcharts.com/c-sc/sc?s=' + t.upper().replace('.', '/') + '&p=D&b=5&g=0&i=0'
            # Creates embeded message
            embed = discord.Embed(title=company, description=t.upper() + ": $" + str(cost) + " " + str(per) + "% ",
                                  color=(c))
            embed.set_image(url=chart)
            await message.channel.send(embed=embed)



# coinbase price
def coinBasePrice(x):
    TWOPLACES = Decimal(10) ** -2
    OVERPLACE = Decimal(1000) ** -2
    current = float(requests.get('https://api.coinbase.com/v2/prices/' + x + '-USD/spot').json()['data']['amount'])
    per = round(((current / float(
        requests.get('https://api.pro.coinbase.com/products/' + x + '-USD/stats').json()['open'])) - 1) * 100, 2)
    current = Decimal(current).quantize(OVERPLACE) if current < .1 else Decimal(current).quantize(TWOPLACES)
    per = Decimal(per).quantize(TWOPLACES)
    return str(current), str(per)


# coinMarketCapPrice
# Return coin info
def coinMarketCapPrice(t):
    price = 0
    try:
        coinInfo = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?&symbol=' + t,
                                headers={'X-CMC_PRO_API_KEY': CMK_TOKEN}).json()
        coin = coinInfo['data'][t]['name']
        try:
            cost, per = coinBasePrice(t)  # gets coinbase price if avaliable
        except:
            TWOPLACES = Decimal(10) ** -2
            OVERPLACE = Decimal(1000) ** -2
            cost = Decimal(coinInfo['data'][t]['quote']['USD']['price']).quantize(TWOPLACES) if Decimal(
                coinInfo['data'][t]['quote']['USD']['price']) > .1 else Decimal(
                coinInfo['data'][t]['quote']['USD']['price']).quantize(OVERPLACE)
            per = Decimal(coinInfo['data'][t]['quote']['USD']['percent_change_24h']).quantize(TWOPLACES)
    except:
        price = -1
    # if ticker not found
    if (price == -1):
        price = -1
        return price, price, price
    return str(coin), str(cost), str(per)


# IEXPrice
# Returns stock info
def IEXPrice(t):
    try:
        stockInfo = requests.get('https://cloud.iexapis.com/stable/stock/' + (t) + '/quote?token=' + IEX_TOKEN).json()
        company = stockInfo['companyName']
        if (stockInfo['latestSource'] == 'Close'):
            if (stockInfo['extendedPrice'] == None):
                cost = stockInfo['latestPrice']
                per = stockInfo['changePercent']
            else:
                cost = stockInfo['extendedPrice']
                per = stockInfo['extendedChangePercent']
        else:
            cost = stockInfo['latestPrice']
            per = stockInfo['changePercent']
        price = str(company) + ' $'
        price += str(round(float(cost), 2)) + ' '
        price += str(round((float(per) * 100), 2)) + '%'
    except:
        # if ticker not found
        price = -1
        return price, price, price
    return company, round(float(cost), 2), round((float(per) * 100), 2)


# COVID CASES
def COVID(state):
    c = discord.Colour(0x040000)
    states = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California", "CO": "Colorado",
              "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho",
              "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana",
              "ME": "Maine", "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota",
              "MS": "Mississippi", "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
              "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
              "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
              "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
              "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
              "WI": "Wisconsin", "WY": "Wyoming", "GU": "Guam", "PR": "Puerto Rico", "VI": "Virgin Islands"}
    if (state == 'us'):
        stats = requests.get('https://covidtracking.com/api/v1/' + state + '/current.json')
        stats0 = stats.json()[0]
        rate = discord.Embed(title="USA COVID Info", description=str(stats0['dateChecked']), color=(c))
    else:
        stats = requests.get('https://covidtracking.com/api/v1/states/' + state + '/current.json')
        stats0 = stats.json()
        rate = discord.Embed(title=str(states[state.upper()]) + " COVID Data", description=str(stats0['lastUpdateEt']),
                             color=(c))
    rate.add_field(name="Daily Cases", value=str(stats0['positiveIncrease']), inline=True)
    rate.add_field(name="Daily Deaths", value=str(stats0['deathIncrease']), inline=True)
    rate.add_field(name="\u200B", value="\u200B")
    rate.add_field(name="Total Cases", value=str(stats0['positive']), inline=True)
    rate.add_field(name="Total Deaths", value=str(stats0['death']), inline=True)
    rate.add_field(name="\u200B", value="\u200B")
    return rate


bot.run(KEY)
