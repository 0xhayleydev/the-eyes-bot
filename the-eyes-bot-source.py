#  ████████╗██╗  ██╗███████╗    ███████╗██╗   ██╗███████╗███████╗    ██████╗  ██████╗ ████████╗    ███████╗ ██████╗ ██╗   ██╗██████╗  ██████╗███████╗
#  ╚══██╔══╝██║  ██║██╔════╝    ██╔════╝╚██╗ ██╔╝██╔════╝██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝    ██╔════╝██╔═══██╗██║   ██║██╔══██╗██╔════╝██╔════╝
#     ██║   ███████║█████╗      █████╗   ╚████╔╝ █████╗  ███████╗    ██████╔╝██║   ██║   ██║       ███████╗██║   ██║██║   ██║██████╔╝██║     █████╗  
#     ██║   ██╔══██║██╔══╝      ██╔══╝    ╚██╔╝  ██╔══╝  ╚════██║    ██╔══██╗██║   ██║   ██║       ╚════██║██║   ██║██║   ██║██╔══██╗██║     ██╔══╝  
#     ██║   ██║  ██║███████╗    ███████╗   ██║   ███████╗███████║    ██████╔╝╚██████╔╝   ██║       ███████║╚██████╔╝╚██████╔╝██║  ██║╚██████╗███████╗
#     ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚══════╝   ╚═╝   ╚══════╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝       ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝
# testing mode, this switches between using token.txt (False)
# and testing_token.txt (True) so the bot can be tested without disrupting the experience
TESTING = False
OLD_SERVER_FILE_EXTENSION = ".json"
NEW_SERVER_FILE_EXTENSION = ".tebserver"

# imports
import os, discord, json, hashlib
from discord.ext import commands

# if the server path doesn't exist, make it
if not os.path.exists("server"):
    os.mkdir("server")

# renmame all json files to server
def rename_json_to_server():
    # for each file in the main directory
    for f in os.listdir():
        # get the prefix and extension of the file name
        pre, ext = os.path.splitext(f)
        # if the extension is the old extension
        if ext == OLD_SERVER_FILE_EXTENSION:
            # set the extension to the new extension
            ext = NEW_SERVER_FILE_EXTENSION
            # replace server\\ (due to bug caused in previous verison) 
            pre = pre.replace("server\\", "")
            # make sure that the file is stored in the server/ folder
            pre = "server/" + pre
            # rename the file
            os.rename(f, pre + ext)

# run the rename command
rename_json_to_server()

# function to get the amount of servers
def get_server_count():
    # set the count to 0
    count = 0
    # list all the files in the server subdirectory
    files = os.listdir("server/")
    # for each file
    for f in files:
        # split the prefix (name) and extension
        pre, ext = os.path.splitext(f)
        # if the extension is the new .tebserver extension
        if ext == NEW_SERVER_FILE_EXTENSION:
            # increase the count
            count += 1
    # print how many servers the bot is in
    print("I am in {} servers".format(count))
    # return how many servers the bot is in
    return count

# default server settings
default_guild_settings = {
    "send_replies": True,
    "add_reactions": True,
    "allow_direct_dms": True,
    "react_to_edited_messages": False
}

# keywords for the bot to listen to
keywords = {
    "good bot": "d:\N{EYES} Thanks for calling me a good bot! \N{EYES}\n\nIf you'd like me on your server, add me here: https://top.gg/bot/769211890407833610.\n\nIf you'd like to stop recieving these messages, please reply with `\N{EYES}blacklist`.",
    "best bot": "d:\N{EYES} Thanks for calling me a good bot! \N{EYES}\n\nIf you'd like me on your server, add me here: https://top.gg/bot/769211890407833610\n\nIf you'd like to stop recieving these messages, please reply with `\N{EYES}blacklist`."
}

# keywords for the bot to listen to that come from the author
author_keywords = {
    "good bot": "r:I know mother, you raised me well. \N{EYES}",
    "best bot": "r:I know mother, you raised me well. \N{EYES}",
    "bad bot": "r:How can you lie to your child like that mOtHeR?! \N{EYES}",
    "love you more": "r:No, I love you more mother. \N{EYES}",
    "love you": "r:I love you too mother. \N{EYES}"
}

# function to read json data from a file
# param: file_name -> the name of the file
# param: default_value -> the value to use if the file cannot be found
def read_json_from_file(file_name, default_value):
    # try to open the file and return the data
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    # if it throws JSONDecodeError, write to the file
    except json.JSONDecodeError:
        write_json_to_file(file_name, default_value)
    # if it throws FileNotFoundError, write to, then read from the file
    except FileNotFoundError:
        write_json_to_file(file_name, default_value)
        read_json_from_file(file_name, default_value)

# function to write json data to a file
# param: file_name -> the name of the file
# param: value -> the data to write
def write_json_to_file(file_name, value):
    # open the file and dump the json to the file
    with open(file_name, 'w+') as file:
        json.dump(value, file)

# get the list of blacklisted users
blacklist_users = read_json_from_file('blacklist.txt', '[]')

# function to find the sha256 hash of an key
# param: key -> the data to hash
def get_hash(key):
    return hashlib.sha256(bytes(str(key), 'utf-8')).hexdigest()

# function to check the blacklist
# param: user_id -> the user id to check the blacklist for
def check_blacklist_for_user(user_id):
    # if the user_id exists in the blacklist, return True, otherwise, returrn false
    if user_id in blacklist_users:
        return True
    return False

# function to get the server's settings file
# param: guild_id -> the id of the guild to find a file for
def get_guild_file(guild_id):
    # return the server file's location after hashing the guild id
    return "server/" + get_hash(guild_id) + NEW_SERVER_FILE_EXTENSION

# if testing mode enabled
if TESTING:
    # read the testing token file
    with open('testing_token.txt', 'r') as file:
        TOKEN = file.read()
else:
    # read the normal token file
    with open('token.txt', 'r') as file:
        TOKEN = file.read()
    

# instantiate the bot with the prefix of :eyes:
bot = commands.Bot(command_prefix="\N{EYES}")
    

#  ███████╗██╗   ██╗███████╗███╗   ██╗████████╗███████╗
#  ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
#  █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ███████╗
#  ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ╚════██║
#  ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████║
#  ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝                                                                                                                                                                                            
# function to run when the bot starts
@bot.event
async def on_ready():
    # log that the bot has connected
    print(f'{bot.user} has connected to Discord!')
    
    # set the game activity
    _activity = discord.Activity(name='{} servers \N{EYES}'.format(get_server_count()), type=discord.ActivityType.watching)

    # set the status
    _status = discord.Status.online

    # set the bot's prescense
    await bot.change_presence(status=_status, activity=_activity)

# function to run when the bot sees a new message
# param: msg -> the message which is recived
@bot.event
async def on_message(msg):
    # if the message is sent into a server
    if msg.guild:
        # load the server's specific settings
        guild_settings = read_json_from_file(get_guild_file(msg.guild.id), default_guild_settings)
    else:
        # load the default settings
        guild_settings = default_guild_settings

    # get the content of the message all as lowercase
    content = msg.content.lower()
    
    # if the bot is mentioned and the server allows dms or replies
    if bot.user.mentioned_in(msg) and (guild_settings["allow_direct_dms"] or guild_settings["send_replies"]):
        # get the user hash of the mesage author
        user_hash = get_hash(msg.author.id)
        # if the user hash isn't in the blacklist
        if user_hash not in blacklist_users:
            # if the message author is the bot author and doesn't start with a !
            if msg.author.id == 175635927954227200 and not content[0] == '!':
                # get the author keywords
                keywords_to_check = author_keywords
            else:
                # get the normal keywords
                keywords_to_check = keywords

            # run through the keywords to check
            for key in keywords_to_check.keys():
                # if the key is in the content
                if key in content:
                    # get the value of the key
                    value = keywords_to_check[key]
                    # if the value starts with 'r:'
                    if value[0:2] == 'r:':
                        # if the server allows sending replies
                        if guild_settings["send_replies"]:
                            # send a message reply with the value
                            await msg.reply(value[2:])
                    # if the value starts with 'd:'
                    elif value[0:2] == 'd:':
                        # if the server allows sending dms
                        if guild_settings["allow_direct_dms"]:
                            # send a dm with the value
                            await msg.author.send(value[2:])
                    # stop running through the keys
                    break
    
    # if eyes emoji is in the message or the bot is mentioned and the server allows reactions
    if ('\N{EYES}' in content or bot.user.mentioned_in(msg)) and guild_settings["add_reactions"]:
        # get the bot's permissions
        permissions = msg.guild.me.permissions_in(msg.channel)
        # if the bot has the permission to add rections
        if permissions.add_reactions:
            # add the eyes reaction to the message
            await msg.add_reaction('\N{EYES}')
        # if the bot lacks the permission to add reactions
        else:
            # add that to the guild settings
            guild_settings["add_reactions"] = False
            # update the server's json file
            write_json_to_file(get_guild_file(msg.guild.id), guild_settings)

    
    # make the bot process commands
    await bot.process_commands(msg)

# function to run when messages are edited
# param: before -> the message before the edit
# param: after -> the message after the edit
@bot.event
async def on_message_edit(before, after):
    # if the message is in a guild
    if before.guild:
        # get the guild settings
        guild_settings = read_json_from_file(get_guild_file(before.guild.id), default_guild_settings)
    # if the message is in dms
    else:
        # stop running
        return

    # if the server allows reactions and reactions to edited messages
    if guild_settings["react_to_edited_messages"] and guild_settings["add_reactions"]:
        # if eyes or the bot is pinged in message add the reaction
        if ('\N{EYES}' in after.content or bot.user.mentioned_in(after)):
            await after.add_reaction('\N{EYES}')
        # if eyes isn't mentioned or the bot isn't pinged in message remove the reaction
        else:
            await after.remove_reaction('\N{EYES}', bot.user)

# function to run when the bot is added to a server
# param: guild -> the guild the bot is added to
@bot.event
async def on_guild_join(guild):
    write_json_to_file(get_guild_file(guild.id), default_guild_settings)

    # set the game activity
    _activity = discord.Activity(name='{} servers \N{EYES}'.format(get_server_count()), type=discord.ActivityType.watching)

    # set the status
    _status = discord.Status.online

    # set the bot's prescense
    await bot.change_presence(status=_status, activity=_activity)

# function to run when the bot is removed from a server
# param: guild -> the guild the bot is removed from
@bot.event
async def on_guild_remove(guild):
    os.remove(get_guild_file(guild.id))

    # set the game activity
    _activity = discord.Activity(name='{} servers \N{EYES}'.format(get_server_count()), type=discord.ActivityType.watching)

    # set the status
    _status = discord.Status.online

    # set the bot's prescense
    await bot.change_presence(status=_status, activity=_activity)

#   ██████╗ ██████╗ ███╗   ███╗███╗   ███╗ █████╗ ███╗   ██╗██████╗ ███████╗
#  ██╔════╝██╔═══██╗████╗ ████║████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝
#  ██║     ██║   ██║██╔████╔██║██╔████╔██║███████║██╔██╗ ██║██║  ██║███████╗
#  ██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██╔══██║██║╚██╗██║██║  ██║╚════██║
#  ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║  ██║██║ ╚████║██████╔╝███████║
#   ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝
# class for the dm commands which inherits from commands.Cog
# param: name -> the name of the category
class DM_Commands(commands.Cog, name="Direct Message Commands"):
    # create a new command called blacklist
    @commands.command(
        name="blacklist",
        description="Add yourself to the blacklist for the bot.",
        help="This will prevent me from sending you Direct Messages."
    )
    # param: ctx -> the context of the message
    async def blacklist(self, ctx):
        # if the context is in a guild
        if ctx.guild:
            # reply telling the user to DM the bot
            await ctx.reply("Please DM me if you would like to use that command!")
        else:
            # get the user hash
            user_hash = get_hash(ctx.author.id)
            # if the hash isn't on the blacklist
            if check_blacklist_for_user(user_hash) == False:#
                # add the hash to the blacklist
                blacklist_users.append(user_hash)
                # write to new blacklist data to the blacklist file
                write_json_to_file('blacklist.txt', blacklist_users)
                # tell the user that they have been added to the blacklist
                await ctx.author.send("You've been successfully added to the blacklist! I will no longer send you DMs. If you would like to be removed from the blacklist, please reply `\N{EYES}whitelist` at any time!")
            else:
                # if they are already on the blacklist, tell the user they already are on the blacklist
                await ctx.author.send("You're already on the blacklist! If you would like to be removed from the blacklist, please reply `\N{EYES}whitelist` at any time!")

    # create a new command called whitelist
    @commands.command(
        name="whitelist",
        description="Remove yourself to the blacklist for the bot.",
        help="This will allow me to send you Direct Messages."
    )
    # param: ctx -> the context of the message
    async def whitelist(self, ctx):
        # if the context is in a guild
        if ctx.guild:
            # reply telling the user to DM the bot
            await ctx.reply("Please DM me if you would like to use that command!")
        else:
            # get the user hash
            user_hash = get_hash(ctx.author.id)
            # if the hash is on the blacklist
            if check_blacklist_for_user(user_hash) == True:
                # remove the hash from the blacklist
                blacklist_users.remove(user_hash)
                # write to new blacklist data to the blacklist file
                write_json_to_file('blacklist.txt', blacklist_users)
                # tell the user that they have been removed from the blacklist
                await ctx.author.send("You've been successfully removed from the blacklist! I will now be able to send you DMs. If you would like to be added to the blacklist again, please reply `\N{EYES}blacklist` at any time!")
            else:
                # if they aren't on the blacklist, tell the user that they aren't on the blacklist
                await ctx.author.send("Hmmm. Looks like you aren't on the blacklist! If you'd like to be added to the blacklist, please reply `\N{EYES}blacklist` at any time!")

# class for the server commands which inherits from commands.Cog
# param: name -> the name of the category
class Server_Commands(commands.Cog, name="Server Commands"):
    # create a new command called allow replies
    @commands.command(
        aliases=["replies"],
        name="allowreplies",
        description="Allow bot replies to messages.",
        help="This will allow me to send messages into the server. Default: True.",
        usage="\N{EYES}allowreplies true|false"
    )
    # make sure the user has the admin permission
    @commands.has_permissions(administrator=True)
    # param: ctx -> the context of the message
    # param: value -> the value passed through via the message
    async def allow_replies(self, ctx, value=""):
        # get the guild settings
        guild_settings = read_json_from_file(get_guild_file(ctx.guild.id), default_guild_settings)

        # if the value isn't set
        if value == "":
            # tell the user the current value of the setting
            await ctx.reply("`Allow Sending Replies = {}`".format(guild_settings["send_replies"]))
            # don't run any more of the function
            return
        
        # convert the value to lower
        value = value.lower()

        # if the value is true
        if value == "true":
            # set the setting to true
            setting = True
        # if the value is false
        elif value == "false":
            # set the setting to false
            setting = False
        # if the value is invalid
        else:
            # tell the user how the command is used
            await ctx.reply("Incorrect usage.\nPlease try: `{}`".format(Server_Commands.allow_replies.usage))
            # don't run any more of the function
            return
        
        # set the guild setting of send_replies to the setting
        guild_settings["send_replies"] = setting
        
        # write the new data to the setting file
        write_json_to_file(get_guild_file(ctx.guild.id), guild_settings)
        
        # send a reply saying the setting has been updated
        await ctx.reply("Send replies set to {}".format(setting))
    
    # create a command called allow rections
    @commands.command(
        aliases=["reactions"],
        name="allowreactions",
        description="Allow bot to add reactions to messages. Default: True.",
        help="This will allow me to add reactions.",
        usage="\N{EYES}allowreactions true|false"
    )
    # make sure the user has the admin permission
    @commands.has_permissions(administrator=True)
    # param: ctx -> the context of the message
    # param: value -> the value passed through via the message
    async def allow_reactions(self, ctx, value=""):
        # get the guild settings
        guild_settings = read_json_from_file(get_guild_file(ctx.guild.id), default_guild_settings)

        # if the value isn't set
        if value == "":
            # tell the user the current value of the setting
            await ctx.reply("`Allow Adding Reactions = {}`".format(guild_settings["add_reactions"]))
            # don't run any more of the function
            return

        # convert the value to lower
        value = value.lower()

        # if the value is true
        if value == "true":
            # set the setting to true
            setting = True
        # if the value is false
        elif value == "false":
            # set the setting to false
            setting = False
        else:
            # tell the user how the command is used
            await ctx.reply("Incorrect usage.\nPlease try: `{}`".format(Server_Commands.allow_reactions.usage))
            # don't run any more of the function
            return
        
        # set the guild setting of allow_reactions to the setting
        guild_settings["add_reactions"] = setting
        
        # write the new data to the setting file
        write_json_to_file(get_guild_file(ctx.guild.id), guild_settings)
        
        # send a reply saying the setting has been updated
        await ctx.reply("Allow reactions set to {}".format(setting))
    
    # create a command called allow dms
    @commands.command(
        aliases=["dms"],
        name="allowdms",
        description="Allow bot to send direct messages to users.",
        help="This will allow me to send direct messages to users when, for example, they say 'good bot' to me. Default: True.",
        usage="\N{EYES}allowdms true|false"
    )
    # make sure the user has the admin permission
    @commands.has_permissions(administrator=True)
    # param: ctx -> the context of the message
    # param: value -> the value passed through via the message
    async def allow_dms(self, ctx, value=""):
        # get the guild settings
        guild_settings = read_json_from_file(get_guild_file(ctx.guild.id), default_guild_settings)

        # if the value isn't set
        if value == "":
            # tell the user the current value of the setting
            await ctx.reply("`Allow Direct Messages = {}`".format(guild_settings["allow_direct_dms"]))
            # don't run any more of the function
            return

        # convert the value to lower
        value = value.lower()

        # if the value is true
        if value == "true":
            # set the setting to true
            setting = True
        # if the value is false
        elif value == "false":
            # set the setting to false
            setting = False
        else:
            # tell the user how the command is used
            await ctx.reply("Incorrect usage.\nPlease try: `{}`".format(Server_Commands.allow_dms.usage))
            # don't run any more of the function
            return
        
        # set the guild setting of allow_direct_dms to the setting
        guild_settings["allow_direct_dms"] = setting
        
        # write the new data to the setting file
        write_json_to_file(get_guild_file(ctx.guild.id), guild_settings)
        
        # send a reply saying the setting has been updated
        await ctx.reply("Allow Direct Messages set to {}".format(setting))
    
    # create a command called allow edits
    @commands.command(
        aliases=["edits"],
        name="allowedits",
        description="Allow me to change reactions when messages are edited.",
        help="This will allow me to change reactions when messages are edited. Disabling this saves server capacity and helps keep latency low. Default: False.",
        usage="\N{EYES}allowedits true|false"
    )
    # make sure the user has the admin permission
    @commands.has_permissions(administrator=True)
    # param: ctx -> the context of the message
    # param: value -> the value passed through via the message
    async def allow_edits(self, ctx, value=""):
        # get the guild settings
        guild_settings = read_json_from_file(get_guild_file(ctx.guild.id), default_guild_settings)

        # if the value isn't set
        if value == "":
            # tell the user the current value of the setting
            await ctx.reply("`React To Edited Messages = {}`".format(guild_settings["react_to_edited_messages"]))
            # don't run any more of the function
            return
        
        # convert the value to lower
        value = value.lower()

        # if the value is true
        if value == "true":
            # set the setting to true
            setting = True
        # if the value is false
        elif value == "false":
            # set the setting to false
            setting = False
        else:
            # tell the user how the command is used
            await ctx.reply("Incorrect usage.\nPlease try: `{}`".format(Server_Commands.allow_edits.usage))
            # don't run any more of the function
            return

        # set the guild setting of allow_direct_dms to the setting
        guild_settings["react_to_edited_messages"] = setting
        
        # write the new data to the setting file
        write_json_to_file(get_guild_file(ctx.guild.id), guild_settings)
        
        # send a reply saying the setting has been updated
        await ctx.reply("Allow Reaction Edits set to {}".format(setting))
    
    # create a command called reset
    @commands.command(
        name="reset",
        description="Reset my configuration.",
        help="This will reset the config which has been set up."
    )
    # make sure the user has the admin permission
    @commands.has_permissions(administrator=True)
    # param: ctx -> the context of the message
    async def reset_settings(self, ctx):
        # write the default guild settings to a file
        write_json_to_file(get_guild_file(ctx.guild.id), default_guild_settings)

# add the DM_Commands cog to the bot
bot.add_cog(DM_Commands())
# add the Server_Commands cog to the bot
bot.add_cog(Server_Commands())

# run the bot
bot.run(TOKEN)