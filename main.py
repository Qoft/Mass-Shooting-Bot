import httpx, discord, json, datetime
from discord.ext import commands, tasks

async def getMassShootings():
	async with httpx.AsyncClient(headers={"Accept":"application/json"}) as client:
		response = await client.get("https://shootings.diamondb.xyz/")
		return response

bot = commands.Bot()

class InviteButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Invite me to your server",
            style=discord.ButtonStyle.link,
            url="https://discord.com/api/oauth2/authorize?client_id=995113890990014464&permissions=0&scope=applications.commands%20bot",
        )

class SrcButton(discord.ui.Button):
	def __init__(self):
		super().__init__(
			label="Get Source",
			style=discord.ButtonStyle.link,
			url="https://github.com/Qoft/Mass-Shooting-Bot",
		)

@bot.slash_command(name="shootings", description="Shows the most recent shootings in the US")
async def shootings(ctx):
	try:
		await ctx.defer()
		shootings = await getMassShootings()
		if shootings.status_code != 200:
			return await ctx.respond(embed=discord.Embed(title="Error", description="Something went wrong while getting the shootings (api prob broke, not qoft issue)", color=0xFF0000))
		shootings = shootings.json()
		shootings_today = shootings["Records"]["Today"]
		
		d = "s" if len(shootings_today) < 1 else ""
		if shootings_today != []:
			embed = discord.Embed(title=f"{len(shootings_today)} Mass shooting{d} today", color=0x00ff00, url=shootings["Records"]["Today"][0]["SourceURL"])
			for shooting in shootings_today:
				for key, value in shooting.items():
					if key == "IncidentURL" or key == "SourceURL" or key == "IncidentID" or "IncidentDate":
						continue
					if key == "NoKilled": key = "Killed"
					if key == "NoInjured": key = "Injured"
					if key == "CityCounty": key = "City/County"
					embed.add_field(name=f"{key}", value=f"{value}")
				embed.add_field(name=f"============================================", value=f"===========================================", inline=False)
			
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
     

@tasks.loop(minutes=5) # repeat after every 10 seconds
async def status():
    shootings = await getMassShootings()
    d = "s" if len(shootings.json()['Records']['Today']) < 1  or 0 else ""
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name=f"{len(shootings.json()['Records']['Today'])} shooting{d} today"))

     
@bot.event
async def on_ready(): 
    print(f"Logged in as {bot.user.name}")
    status.start()
     

with open("config.json") as f: config = json.load(f)
bot.run(config["token"])



