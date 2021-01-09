TESTING = False

#imports
import os, discord, json, hashlib, os
from discord.ext import commands

if not os.path.exists("server"):
    os.mkdir("server")

default_guild_settings = {
    "send_replies": True,
    "add_reactions": True,
    "allow_direct_dms": True,
    "react_to_edited_messages": False
}

keywords = {
    "good bot": "d:\N{EYES} Thanks for calling me a good bot! \N{EYES}\n\nIf you'd like me on your server, add me here: https://top.gg/bot/769211890407833610.\n\nIf you'd like to stop recieving these messages, please reply with `\N{EYES}blacklist`.",
    "best bot": "d:\N{EYES} Thanks for calling me a good bot! \N{EYES}\n\nIf you'd like me on your server, add me here: https://top.gg/bot/769211890407833610\n\nIf you'd like to stop recieving these messages, please reply with `\N{EYES}blacklist`."
}

author_keywords = {
    "good bot": "r:I know mother, you raised me well. \N{EYES}",
    "best bot": "r:I know mother, you raised me well. \N{EYES}",
    "bad bot": "r:How can you lie to your child like that mOtHeR?! \N{EYES}",
    "love you more": "r:No, I love you more mother. \N{EYES}",
    "love you": "r:I love you too mother. \N{EYES}"
}

blacklist_users = []

def read_json_from_file(file_name, default_value):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        write_json_to_file(file_name, default_value)
    except FileNotFoundError:
        write_json_to_file(file_name, default_value)
        read_json_from_file(file_name, default_value)

def write_json_to_file(file_name, value):
    with open(file_name, 'w+') as file:
        json.dump(value, file)

def get_hash(user):
    return hashlib.sha256(bytes(str(user), 'utf-8')).hexdigest()

blacklist_users = read_json_from_file('blacklist.txt', '[]')

def check_blacklist_for_user(user_id):
    if user_id in blacklist_users:
        return True
    return False

def get_guild_file(guild_id):
    return "server\\" + get_hash(guild_id) + ".json"

# token and bot info
if TESTING:
    with open('testing_token.txt', 'r') as file:
        TOKEN = file.read()
else:
    with open('token.txt', 'r') as file:
        TOKEN = file.read()
bot = commands.Bot(command_prefix="\N{EYES}")

#  ███████╗██╗   ██╗███████╗███╗   ██╗████████╗███████╗
#  ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
#  █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ███████╗
#  ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ╚════██║
#  ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████║
#  ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝                                                                                                                                                                                            
# bot event on ready
@bot.event
async def on_ready():
    # log that the bot has connected
    print(f'{bot.user} has connected to Discord!')

    # store the game activity
    _activity = discord.Activity(name='my DMs \N{EYES}', type=discord.ActivityType.watching)

    # store the status
    if TESTING:
        _status = discord.Status.offline
    else:
        _status = discord.Status.online

    # set the prescense
    await bot.change_presence(status=_status, activity=_activity)
    
# bot event on message
@bot.event
async def on_message(msg):
    guild_settings = read_json_from_file(get_guild_file(msg.guild.id), default_guild_settings)

    # get the content of the message all as lowercase
    content = msg.content.lower()
    
    if bot.user.mentioned_in(msg) and (guild_settings["allow_direct_dms"] or guild_settings["send_replies"]):
        user_hash = get_hash(msg.author.id)
        if user_hash not in blacklist_users:
            if msg.author.id == 175635927954227200 and not content[0] == '!':
                keywords_to_check = author_keywords
            else:
                keywords_to_check = keywords
            for key in keywords_to_check.keys():
                if key in content:
                    value = keywords_to_check[key]
                    if value[0:2] == 'r:':
                        if guild_settings["send_replies"]:
                            await msg.reply(value[2:])
                    elif value[0:2] == 'd:':
                        if guild_settings["allow_direct_dms"]:
                            await msg.author.send(value[2:])
                    break
    
    if ('\N{EYES}' in content or bot.user.mentioned_in(msg)) and guild_settings["add_reactions"]:
        # add the eyes reaction
        await msg.add_reaction('\N{EYES}')
    
    await bot.process_commands(msg)

# bot event message edits
@bot.event
async def on_message_edit(before, after):
    guild_settings = read_json_from_file(get_guild_file(before.guild.id), default_guild_settings)

    if guild_settings["react_to_edited_messages"] and guild_settings["add_reactions"]:
        # if eyes or the bot is pinged in message add the reaction
        if ('\N{EYES}' in after.content or bot.user.mentioned_in(after)):
            await after.add_reaction('\N{EYES}')
        # if eyes isn't mentioned or the bot isn't pinged in message remove the reaction
        else:
            await after.remove_reaction('\N{EYES}', bot.user)

#   ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗
#  ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝
#  ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗
#  ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║
#  ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║
#   ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝
class DM_Commands(commands.Cog, name="Direct Message Commands"):
    @commands.command(
        name="blacklist",
        description="Add yourself to the blacklist for the bot.",
        help="This will prevent me from sending you Direct Messages."
    )
    async def blacklist(self, ctx):
        if ctx.guild:
            await ctx.reply("Please DM me if you would like to use that command!")
        else:
            user_hash = get_hash(ctx.author.id)
            if check_blacklist_for_user(user_hash) == False:
                blacklist_users.append(user_hash)
                write_json_to_file('blacklist.txt', blacklist_users)
                await ctx.author.send("You've been successfully added to the blacklist! I will no longer send you DMs. If you would like to be removed from the blacklist, please reply `\N{EYES}whitelist` at any time!")
            else:
                await ctx.author.send("You're already on the blacklist! If you would like to be removed from the blacklist, please reply `\N{EYES}whitelist` at any time!")

    @commands.command(
        name="whitelist",
        description="Remove yourself to the blacklist for the bot.",
        help="This will allow me to send you Direct Messages."
    )
    async def whitelist(self, ctx):
        if ctx.guild:
            await ctx.reply("Please DM me if you would like to use that command!")
        else:
            user_hash = get_hash(ctx.author.id)
            if check_blacklist_for_user(user_hash) == True:
                blacklist_users.remove(user_hash)
                write_json_to_file('blacklist.txt', blacklist_users)
                await ctx.author.send("You've been successfully removed from the blacklist! I will now be able to send you DMs. If you would like to be added to the blacklist again, please reply `\N{EYES}blacklist` at any time!")
            else:
                await ctx.author.send("Hmmm. Looks like you aren't on the blacklist! If you'd like to be added to the blacklist, please reply `\N{EYES}blacklist` at any time!")

class Server_Commands(commands.Cog, name="Server Commands"):
    @commands.command(
        aliases=["replies"],
        name="allowreplies",
        description="Allow bot replies to messages.",
        help="This will allow me to send messages into the server. Default: True.",
        usage="\N{EYES}allowreplies true|false"
    )
    @commands.has_permissions(administrator=True)
    async def allow_replies(self, ctx, value):
        guild_settings = read_json_from_file(get_guild_file(ctx.guild.id), default_guild_settings)
        value = value.lower()

        if value == "true":
            setting = True
        elif value == "false":
            setting = False
        else:
            await ctx.reply("Incorrect usage. Please try `\N{EYES}allowreplies true|false`")
            return
        guild_settings["send_replies"] = setting
        
        write_json_to_file(get_guild_file(ctx.guild.id), guild_settings)

        await ctx.reply("Send replies set to {}".format(setting))
    
    @commands.command(
        aliases=["reactions"],
        name="allowreactions",
        description="Allow bot to add reactions to messages. Default: True.",
        help="This will allow me to add reactions.",
        usage="true|false"
    )
    @commands.has_permissions(administrator=True)
    async def allow_reactions(self, ctx, value):
        guild_settings = read_json_from_file(get_guild_file(ctx.guild.id), default_guild_settings)
        value = value.lower()

        if value == "true":
            setting = True
        elif value == "false":
            setting = False
        else:
            await ctx.reply("Incorrect usage. Please try `\N{EYES}allowreactions true|false`")
            return
        guild_settings["allow_reactions"] = setting
        
        write_json_to_file(get_guild_file(ctx.guild.id), guild_settings)

        await ctx.reply("Allow reactions set to {}".format(setting))
    
    @commands.command(
        aliases=["dms"],
        name="allowdms",
        description="Allow bot to send direct messages to users.",
        help="This will allow me to send direct messages to users when, for example, they say 'good bot' to me. Default: True.",
        usage="true|false"
    )
    @commands.has_permissions(administrator=True)
    async def allow_dms(self, ctx, value):
        guild_settings = read_json_from_file(get_guild_file(ctx.guild.id), default_guild_settings)
        value = value.lower()

        if value == "true":
            setting = True
        elif value == "false":
            setting = False
        else:
            await ctx.reply("Incorrect usage. Please try `\N{EYES}allowdms true|false`")
            return
        guild_settings["allow_direct_dms"] = setting
        
        write_json_to_file(get_guild_file(ctx.guild.id), guild_settings)

        await ctx.reply("Allow Direct Messages set to {}".format(setting))
    
    @commands.command(
        aliases=["edits"],
        name="allowedits",
        description="Allow me to change reactions when messages are edited.",
        help="This will allow me to change reactions when messages are edited. Disabling this saves server capacity and helps keep latency low. Default: False.",
        usage="true|false"
    )
    @commands.has_permissions(administrator=True)
    async def allow_edits(self, ctx, value):
        guild_settings = read_json_from_file(get_guild_file(ctx.guild.id), default_guild_settings)
        value = value.lower()

        if value == "true":
            setting = True
        elif value == "false":
            setting = False
        else:
            await ctx.reply("Incorrect usage. Please try `\N{EYES}allowedits true|false`")
            return
        guild_settings["allow_direct_dms"] = setting
        
        write_json_to_file(get_guild_file(ctx.guild.id), guild_settings)
        
        await ctx.reply("Allow Reaction Edits set to {}".format(setting))
    
    @commands.command(
        name="reset",
        description="Reset my configuration.",
        help="This will reset the config which has been set up."
    )
    @commands.has_permissions(administrator=True)
    async def reset_settings(self, ctx):
        guild_settings = default_guild_settings
        
        write_json_to_file(get_guild_file(ctx.guild.id), guild_settings)

bot.add_cog(DM_Commands())
bot.add_cog(Server_Commands())

# run the bot using the token
bot.run(TOKEN)