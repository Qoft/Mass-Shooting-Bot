import aiohttp, discord, json, datetime
from discord.ext import commands

async def getMassShootings():
	async with aiohttp.ClientSession(headers={"Accept":"application/json"}) as session:
		async with session.get('https://shootings.diamondb.xyz/') as resp:
			data = await resp.json()
			return data

bot = commands.Bot()












class InviteButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Invite me to your server",
            style=discord.ButtonStyle.link,
            url="https://discord.com/api/oauth2/authorize?client_id=995113890990014464&permissions=8&scope=bot%20applications.commands",
        )

class SrcButton(discord.ui.Button):
	def __init__(self):
		super().__init__(
			label="Get Souce",
			style=discord.ButtonStyle.link,
			url="https://github.com/Qoft/Mass-Shooting-Bot",
		)

@bot.slash_command(name="shootings", description="Shows the most recent shootings in the US")
async def shootings(ctx):
	try:
		await ctx.defer()
		shootings = await getMassShootings()
		daysSince = shootings["DaysSince"]
		shootings_today = shootings["Records"]["Today"]
		
		d = "s" if len(shootings_today) < 1 else ""
		if shootings_today != []:
			embed = discord.Embed(title=f"{len(shootings_today)} Mass shooting{d} today", color=0x00ff00, url=shootings["Records"]["Today"][0]["SourceURL"])
			for shooting in shootings_today:
				for key, value in shooting.items():
					if key == "IncidentURL" or key == "SourceURL" or key == "IncidentID":
						continue
					else:
						embed.add_field(name=f"{key}", value=f"{value}")
			
		else:
			embed = discord.Embed(title=f"0 Mass shootings today", color=0x00ff00, url="https://github.com/Qoft/Mass-Shooting-Bot")
			embed.add_field(name="Woohoo USA!", value=f"No mass shootings today!")
		embed.set_footer(text=f"Api made by diamondburned: https://shootings.diamondb.xyz/ • Bot made by Qoft")


		view = discord.ui.View()
		view.add_item(InviteButton())
		view.add_item(SrcButton())

		await ctx.respond(embed=embed, view=view)
	except Exception as e:
		embed = discord.Embed(title="Error", description=f"{e}", color=0xFF0000)
		await ctx.respond(embed=embed)
     
@bot.event
async def on_ready(): print(f"Logged in as {bot.user.name}") 

with open("config.json") as f: config = json.load(f)
bot.run(config["token"])



