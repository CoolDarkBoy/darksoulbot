import discord
from discord.ext import commands,tasks
import json
import asyncio
import aiohttp
import random
import datetime


with open("configs.json","r") as f:
	token = json.load(f)["bot"]["token"]
	print("Token Entered. Starting bot...\n")




client = commands.Bot(command_prefix=["#",";-;"],case_insensitive=True)




def colour(r,g,b):
	return discord.Colour.from_rgb(r,g,b)
red = discord.Colour.red()
darkred = discord.Colour.dark_red()
blue = discord.Colour.blue()
darkblue = discord.Colour.dark_blue()
blurple = discord.Colour.blurple()
greyple = discord.Colour.greyple()
purple = discord.Colour.purple()
darkpurple = discord.Colour.dark_purple()
green = discord.Colour.green()
darkgreen = discord.Colour.dark_green()
teal = discord.Colour.teal()
darkteal = discord.Colour.dark_teal()
magenta = discord.Colour.magenta()
darkmagenta = discord.Colour.dark_magenta()
gold = discord.Colour.gold()
darkgold = discord.Colour.dark_gold()
orange = discord.Colour.orange()
darkorange = discord.Colour.dark_orange()



@client.event
async def on_ready():
	with open("configs.json","r") as f:
		data = json.load(f)
	status_text = data["bot"]["status-text"]
	ctime = datetime.datetime.now()
	await client.change_presence(status=discord.Status.online,activity=discord.Game(status_text))
	print(f"Successfully logged in as {client.user}\n")
	print("Time ---> ",ctime.strftime("%H : %M : %S"))
	print("------------------------------------------------------------------------\n")
	files_update.start()

@client.event
async def on_member_join(member:discord.Member):
	await member.add_roles(664183070559043624)
	with open("configs.json","r") as f:
		data = json.load(f)
	channel = member.guild.get_channel(657504989425434624)
	
	welcome_msg = data["configs"]["welcome-msg"].format(member.name)

	embed = discord.Embed()
	embed.set_author(name=welcome_msg,icon_url=member.avatar_url)

	await channel.send(embed=embed)



@client.event
async def on_member_remove(member : discord.Member):
	with open("configs.json","r") as f:
		data = json.load(f)

	channel = member.guild.get_channel(657504989425434624)
	leave_msg = data["configs"]["leave-msg"].format(member.name)

	embed = discord.Embed()
	embed.set_author(name=leave_msg,icon_url=member.avatar_url)

	await channel.send(embed=embed)



@client.command()
async def about(ctx):
	embed = discord.Embed(title="**DarkSoul Bot**",colour="purple",
	description=f"DarkSoul Bot is a multi-utility official bot for the server.\nMade for DarkSoul Server by **{client.get_user(336826908769779712)}**")
	embed.set_author(name=client.name,icon_url=client.avatar_url)
	await ctx.send(embed=embed)



client.filter_data = {}
client.bypass_data = {}

@tasks.loop(seconds=20)
async def files_update():
	with open("filter.json","r") as f:
		client.filter_data = json.load(f)
	with open("bypass.json","r") as f:
		client.bypass_data = json.load(f)



@client.event
async def on_message(message):
	if message.author != client.user:
		filter_list = client.filter_data[str(message.guild.id)]
		if message.content.lower().strip(" ") in filter_list:
			bypass_list = client.bypass_data[str(message.guild.id)]
			if str(message.author.id) not in bypass_list:
				await message.delete()
				await message.channel.send("Please don't use that word.")

	await client.process_commands(message)




@client.command(aliases=["bypass"])
@commands.has_permissions(manage_guild=True)
async def addbypass(ctx,member:discord.Member=None):
	if member is None:
		member = ctx.author
	with open("bypass.json","r") as f:
		data = json.load(f)
		if str(member.id) not in data[str(ctx.guild.id)]:
			data[str(ctx.guild.id)].append(str(member.id))
			with open("bypass.json","w") as f:
				json.dump(data,f)
				await ctx.send(f"Added {member.mention} to bypass priority.")
		else:
			await ctx.send(f"{member.mention} already has bypass priority.")

	
@client.command(aliases=[])
@commands.has_permissions(manage_guild=True)
async def removebypass(ctx,member:discord.Member=None):
	if member is None:
		member = ctx.author
	with open("bypass.json","r") as f:
		data = json.load(f)
		if str(member.id) in data[str(ctx.guild.id)]:
			data[str(ctx.guild.id)].remove(str(member.id))
			with open("bypass.json","w") as f:
				json.dump(data,f)
				await ctx.send(f"Removed {member.mention} from bypass priority.")
		else:
			await ctx.send(f"{member.mention} already has no bypass priority.")


@client.command(aliases=["listbypasses"])
@commands.has_permissions(manage_roles=True)
async def listbypass(ctx):
	with open("bypass.json","r") as f:
		data = json.load(f)
	bypass_list = data[str(ctx.guild.id)]
	bypass = []
	for x in bypass_list:
		bypass.append(ctx.guild.get_member(int(x)).name)
	bypass = str(bypass).replace("['","").replace("']","").replace("'","")
	await ctx.send(f"{ctx.author.mention} Please check your DMs.")
	await ctx.author.send(f"__List of all bypassed members for {ctx.guild.name}__\n**{bypass}**")



@client.command(aliases=[])
@commands.has_permissions(manage_roles=True)
async def addfilter(ctx,*,word:str):
	if len(word) < 3:
		await ctx.send("Please use a word with more than 2 characters.")
	else:
		word = word.lower()
		with open("filter.json","r") as f:
			data = json.load(f)
		if word not in data[str(ctx.guild.id)]:
			data[str(ctx.guild.id)].append(word)
			with open("filter.json","w") as f:
				json.dump(data,f)
			await ctx.send(f"Added `{word}` to filter.")
		else:
			await ctx.send(f"`{word}` is already in the filter.")


@client.command(aliases=[])
@commands.has_permissions(manage_roles=True)
async def removefilter(ctx,*,word:str):
	word = word.lower()
	with open("filter.json","r") as f:
		data = json.load(f)
	if word in data[str(ctx.guild.id)]:
		data[str(ctx.guild.id)].remove(word)
		with open("filter.json","w") as f:
			json.dump(data,f)
		await ctx.send(f"Removed `{word}` from filter.")
	else:
		await ctx.send(f"Unable to find `{word}` in filter.")


@client.command(aliases=["listfilter"])
@commands.has_permissions(manage_roles=True)
async def listfilters(ctx):
	with open("filter.json","r") as f:
		data = json.load(f)
	filters = str(data[str(ctx.guild.id)]).strip("[").strip("]").replace("'","")
	await ctx.send(f"{ctx.author.mention} Please check your DMs.")
	await ctx.author.send(f"__List of all filters for {ctx.guild.name}__\n**{filters}**")










@client.command(aliases=[])
@commands.has_permissions(kick_members=True)
async def kick(ctx,member : discord.Member ,*,reason=None):
	await member.kick(reason=reason)
	embed = discord.Embed(colour=red
		)
	embed.set_author(name=f"{member.name} was kicked from the server")
	await ctx.send(embed=embed)


@client.command() 
@commands.has_permissions(ban_members=True)
async def ban(ctx,member : discord.Member , *,reason=None):
	if member.guild_permissions.ban_members:
		if member == ctx.author:
			await ctx.send("You can't ban yourself")
		else:
			await ctx.send("You can't ban this member using me!")
	await member.ban(reason = reason)
	embed = discord.Embed(colour=darkblue
		)
	embed.set_author(name=f"{member.name} was banned from the server")
	await ctx.send(embed=embed)





@client.command(aliases=[])
@commands.has_permissions(manage_roles=True)
async def mute(ctx,member : discord.Member):
	role = discord.utils.get(ctx.guild.roles, name='Muted')
	await member.add_roles(role)
	embed = discord.Embed(colour=darkred)
	embed.set_author(name=f"{member.display_name} has been muted")
	await ctx.send(embed=embed)


@client.command(aliases=["addrole"])
@commands.has_permissions(manage_roles=True)
async def role(ctx,member:discord.Member,roles:discord.Role,*,reason=None):
	await member.add_roles(roles,reason=reason)
	await ctx.send(f"{member.name} has been given the {roles} role.")


@client.command(aliases=[])
@commands.has_permissions(manage_roles=True)
async def unmute(ctx,member : discord.Member):
	role = discord.utils.get(ctx.guild.roles, name='Muted')
	await member.remove_roles(role)
	embed = discord.Embed(colour=darkblue)
	embed.set_author(name=f"{member.display_name} has been unmuted")
	await ctx.send(embed=embed)


@client.command(aliases=["setnick"])
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx,member:discord.Member,*,nick):
	if member is None:
		member = ctx.author
	
	embed = discord.Embed(colour=teal,
	description=f"Nickname set to {nick}")
	embed.set_author(name=member.name,icon_url=member.avatar_url)
	await ctx.send(embed=embed)
	await member.edit(nick=nick)






@client.command(aliases=["nickreset"])
@commands.has_permissions(manage_nicknames=True)
async def resetnick(ctx,member : discord.Member=None):
	if member is None:
		member = ctx.author
	embed = discord.Embed(colour=teal,
	description=f"Nickname has been removed")
	embed.set_author(name=member.name,icon_url=member.avatar_url)
	await ctx.send(embed=embed)
	await member.edit(nick=member.name)




@client.command()
@commands.has_permissions(manage_guild=True)
async def say(ctx,*,message):
	rcolours = [discord.Colour.blue(),discord.Colour.red()]
	await ctx.message.delete()
	embed = discord.Embed(colour=random.choice(rcolours),description=message)
	embed.set_footer(text="DarkSoul Network (Staff Team)")
	await ctx.send(embed=embed)



@client.command(aliases=["clear"])
@commands.has_permissions(manage_messages=True)
async def purge(ctx,amount : int):
	yellow = discord.Colour.from_rgb(243,243,58)
	await ctx.channel.purge(limit=amount+1)
	if amount < 2:
		embed = discord.Embed(colour=yellow,
			description=f"Cleared {amount} message :white_check_mark:"
			)
	else:
		embed = discord.Embed(colour=yellow,
			description=f"Cleared {amount} messages :white_check_mark:"
			)
	await ctx.send(embed=embed,delete_after=10)



@client.command(aliases=["announcement"])
@commands.has_permissions(manage_guild=True)
async def announce(ctx,*,message):
	await ctx.message.delete()
	embed = discord.Embed(title="__**DARKSOUL ANNOUNCEMENT**__",
		description=f"\n{message}")
	embed.set_footer(text=f"DarkSoul Network (Staff Team) \N{SMALL ORANGE DIAMOND}")
	await ctx.send(embed=embed)




@client.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx,member:discord.Member):
	with open("warns.json","r") as f:
		data = json.load(f)
		if str(member.id) in data:
			warns = data[str(member.id)]
			warns = str(int(warns) + 1)
			data[str(member.id)] = warns
			embed = discord.Embed(color=red,description=f"{member.mention} has been warned")
			if warns == "3":
				embed = discord.Embed(colour=darkred,
				description=f"{member.mention} was kicked for having 3 warns")
				await member.kick(reason="Member was punished for 3 warns")
			elif warns == "5":
				role = discord.utils.get(ctx.guild.roles, name='Muted')
				await member.add_roles(role)
				embed = discord.Embed(colour=darkred,
				description=f"{member.mention} was muted for having 5 warns")
			elif warns == "6":
				embed = discord.Embed(colour=darkred,
				description=f"{member.mention} was banned for exceeding the warn limit")
				await member.ban(reason="Member was banned for exceeding warns")
		else:
			data.update({str(member.id):"1"})
			embed = discord.Embed(color=red,description=f"{member.mention} has been warned for the first time")

	
	with open("warns.json","w") as f:
			json.dump(data,f,indent=4)
	await ctx.send(embed=embed)





@client.command()
async def warns(ctx,member : discord.Member=None):
	if member is None:
		member = ctx.author
	with open("warns.json","r") as f:
		data = json.load(f)
	if str(member.id) not in data:
		warns = 0
	else:
		warns = data[str(member.id)]

	embed = discord.Embed(colour=greyple,title="**Warns**",
	description=f"{member.display_name} has {warns} warns")
	embed.set_author(name=member.name,icon_url=member.avatar_url)
	embed.set_footer(text=f"Called by {ctx.author}")

	await ctx.send(embed=embed)



@client.command(aliases=["removewarn"])
@commands.has_permissions(kick_members=True)
async def removewarns(ctx,member:discord.Member,amount:int=1):
	with open("warns.json","r") as f:
		data = json.load(f)
	if str(member.id) in data:
		warns = int(data[str(member.id)])
		if amount > warns:
			amount = warns
		
		warns = warns - amount
		if warns == 0:
			embed = discord.Embed(colour=blue,
			description=f"Removed all warns from {member.mention}")
		elif amount == 1:
			embed = discord.Embed(colour=blue,
			description=f"Removed 1 warn from {member.mention}")
		else:
			embed = discord.Embed(colour=blue,
			description=f"Removed {amount} warns from {member.mention}")
		data[str(member.id)] = str(warns)
		with open("warns.json","w") as f:
			json.dump(data,f,indent=4)
	else:
		embed = discord.Embed(colour=blue,
		description=f"{member.mention} already has no warns")
	await ctx.send(embed=embed)





@client.command()
async def punishments(ctx):
	embed = discord.Embed(colour=red,title="Punishments",
		description="""Please read the following punishments carefully. Not
		complying with rules can result in you being warned. With every warn, 
		the punishment gets stricter."""

		)
	embed.add_field(name="**Kick** :leg:",value="On 3 warns",inline=True)
	embed.add_field(name="**Mute** :zzz:",value="On 5 warns",inline=True)
	embed.add_field(name="__**Ban**__ :hammer:",value="On 6 warns",inline=False)

	with open("warns.json","r") as f:
		data = json.load(f)
		if str(ctx.author.id) in data:
			warns = data[str(ctx.author.id)]
		else:
			warns = 0
	embed.set_footer(text=f"{ctx.author.display_name} currently has {warns} warns.")
	await ctx.send(embed=embed)







@client.command(aliases=["new"])
async def ticket(ctx,*,reason=None):
	if reason is None:
		reason = "No reason given."
	guild = ctx.guild
	ri = random.randint(100,999)

	overwrites = { 
   	guild.get_role(657588359841054752):discord.PermissionOverwrite(read_messages=True,send_messages=True,manage_messages=True),
	guild.default_role:discord.PermissionOverwrite(read_messages=False),
	guild.me : discord.PermissionOverwrite(send_messages=True,manage_messages=True),
	ctx.author : discord.PermissionOverwrite(read_messages=True,send_messages=True),
	
	}
	role = ctx.guild.get_role(657588359841054752)
	embed = discord.Embed(title="**Ticket Created**",colour=gold,
	description=f"Ticket channel opened by {ctx.author.mention}\n**Reason** : {reason}\n{role.mention} will assist you shortly")
	embed.set_footer(text="Please wait till DarkSoul Support Team assists you")
	channel = await guild.create_text_channel(f"Ticket-{ri}",overwrites=overwrites,position=0,
	category=discord.utils.get(guild.categories,name="Tickets"),reason=reason,topic=str(reason))
	await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} Ticket channel {channel.mention} created."))
	await channel.send(embed=embed)




@client.command()
async def close(ctx,reason=None):
	if reason is None:
		reason="No reason given."

	channel = ctx.channel
	if "ticket" in str(channel.name):
		await ctx.send(f"Channel {channel.mention} deleted.")
		await channel.delete()
	else:
		await ctx.send("Please use this command in a ticket channel.")




@client.command(aliases=[])
async def cat(ctx):
	async with aiohttp.ClientSession() as session:
		async with session.get('http://aws.random.cat/meow') as r:
			if r.status == 200:
				data = await r.json()
				embed = discord.Embed(colour=magenta)
				embed.set_image(url=data["file"])
				embed.set_footer(text=f"Called by {ctx.author}")
				
			else:
				embed = discord.Embed(description="Unable to fetch cat images. Try later!")
			await ctx.send(embed=embed)



@client.command(aliases=[])
async def dog(ctx):
	async with aiohttp.ClientSession() as session:
		async with session.get('https://dog.ceo/api/breeds/image/random') as r:
			if r.status == 200:
				data = await r.json()
				embed = discord.Embed(colour=blue)
				embed.set_image(url=data["message"])
				embed.set_footer(text=f"Called by {ctx.author}")
			else:
				embed = discord.Embed(description="Unable to fetch dog images. Try later!")
			await ctx.send(embed=embed)





@client.command(aliases=[])
async def shibe(ctx):
	async with aiohttp.ClientSession() as session:
		async with session.get(f'http://shibe.online/api/shibes?urls=true&httpsUrls=true') as r:
			if r.status == 200:
				data = await r.json()
				embed = discord.Embed(colour=blue)
				embed.set_image(url=data[0])
				embed.set_footer(text=f"Called by {ctx.author}")
			else:
				embed = discord.Embed(description="Unable to fetch any cute shibe")
	await ctx.send(embed=embed)



@client.command(aliases=["battle"])
async def fight(ctx,member : discord.Member):

	intro = await ctx.send(f"__{ctx.author.display_name} **VS** {member.display_name}__\n")
	member_hp = 100
	author_hp = 100

	first_hit = random.choice(["author","member"])

	display = await ctx.send(f"{ctx.author.display_name} health - {author_hp}\n{member.display_name} health - {member_hp}")
	while author_hp > 0 or member_hp > 0:
		
		if first_hit == "author":
			author_dmg = random.randint(8,18)
			member_dmg = random.randint(8,18)

			member_hp = member_hp - author_dmg
			if member_hp <= 0:
				await display.edit(content=f"{ctx.author.display_name} health - {author_hp}\n{member.display_name} health - 0")
				break
			else:
				author_hp = author_hp - member_dmg
			if author_hp <= 0:
				await display.edit(content=f"{ctx.author.display_name} health - 0\n{member.display_name} health - {member_hp}")
				break


		else:
			member_dmg = random.randint(8,18)
			author_dmg = random.randint(8,18)

			author_hp = author_hp - member_dmg
			if author_hp <= 0:
				await display.edit(content=f"{ctx.author.display_name} health - 0\n{member.display_name} health - {member_hp} **(WINNER)**")
				break
			else:
				member_hp = member_hp - author_dmg
			if member_hp <= 0:
				await display.edit(content=f"{ctx.author.display_name} health - {author_hp} **(WINNER)**\n{member.display_name} health - 0")
				break


		await display.edit(content=f"{ctx.author.display_name} health - {author_hp}\n{member.display_name} health - {member_hp}")


async def is_dev(ctx):
	return ctx.author.id == 336826908769779712

# ONLY TO BE USED IN CASE OF BOT ABUSE BY SERVER OR BREACH OF DISCORD TOS
# ONLY EDIT IF YOU KNOW WHAT YOU'RE DOING
@client.command()
@commands.check(is_dev)
async def override(ctx,hidden=True):
	await ctx.send("Override Initiated because of bot abuse.")
	client.close()




client.run(token)