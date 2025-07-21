# General information about the bot:
# This bot is designed to moderate Discord servers by utilising various features (listed bellow).
#   1. ɪᴛ ᴋɪᴄᴋꜱ ᴛʜᴇ ɪɴᴅɪᴠɪᴅᴜᴀʟ ᴛʜᴀᴛ ʀᴇᴍᴏᴠᴇᴅ ᴛʜᴇ ʙᴏᴛ ꜰʀᴏᴍ ᴛʜᴇ ꜱᴇʀᴠᴇʀ.
#   2. ɪᴛ ᴅᴇʟᴇᴛᴇꜱ ᴍᴇꜱꜱᴀɢᴇꜱ ᴄᴏɴᴛᴀɪɴɪɴɢ ʙʟᴏᴄᴋᴇᴅ ᴡᴏʀᴅꜱ.
#   3. ɪᴛ ᴍᴀɴᴀɢᴇꜱ ᴡᴇʙʜᴏᴏᴋꜱ ʙʏ ᴅᴇʟᴇᴛɪɴɢ ᴛʜᴇᴍ ɪꜰ ᴛʜᴇʏ ᴀʀᴇ ɴᴏᴛ ɴᴇᴇᴅᴇᴅ.
#   4. ɪᴛ ᴍᴏɴɪᴛᴏʀꜱ ʀᴏʟᴇ ᴄʜᴀɴɢᴇꜱ ᴀɴᴅ ᴇɴꜱᴜʀᴇꜱ ᴛʜᴀᴛ ᴘʀᴏᴛᴇᴄᴛᴇᴅ ʀᴏʟᴇꜱ ᴀʀᴇ ɴᴏᴛ ʀᴇᴍᴏᴠᴇᴅ ʙʏ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜꜱᴇʀꜱ.
#   5. ɪᴛ ᴍᴏɴɪᴛᴏʀꜱ ʀᴏʟᴇ ᴜᴘᴅᴀᴛᴇꜱ ᴀɴᴅ ʀᴇᴍᴏᴠᴇꜱ ᴀɴʏ ᴅᴀɴɢᴇʀᴏᴜꜱ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ ꜰʀᴏᴍ ʀᴏʟᴇꜱ.
#   6. ɪᴛ ᴄʜᴇᴄᴋꜱ ғᴏʀ ʀᴀᴛᴇ ʟɪᴍɪᴛꜱ ᴏɴ ᴅᴇsᴛʀᴜᴄᴛɪᴠᴇ ᴀᴄᴛɪᴏɴꜱ (ᴀɴᴛɪ-ɴᴜᴋᴇ).
#   7. ɪᴛ ᴘʀᴇᴠᴇɴᴛꜱ ʀᴀɪᴅꜱ ʙʏ ǫᴜᴀʀᴀɴᴛɪɴɢ ᴍᴇᴍʙᴇʀꜱ ᴡʜᴏ ᴊᴏɪɴ ɪɴ ǫᴜɪᴄᴋ ꜰᴜsꜱ (ᴀɴᴛɪ-ʀᴀɪᴅ).
#   8. ɪᴛ ᴘʀᴏᴠɪᴅᴇꜱ ᴠᴀʀɪᴏᴜꜱ ᴄᴏᴍᴍᴀɴᴅꜱ.


# Bot essentials and imports

from collections import defaultdict
import asyncio
import discord
from discord.ext import commands
from discord import app_commands, Embed
import datetime, time
import json


# Bot token

token = "[REDACTED]"


# Load settings from JSON file (settings.json)

SETTINGS_FILE = 'settings.json'

def load_settings():
    with open(SETTINGS_FILE, 'r') as f:
        return json.load(f)

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

settings = load_settings()


# Lists of protected roles and blocked words

protected_roles = ["Manager", "Administrator", "Moderator", "Support"]

block_words = [
    "antisocial", "shit", "fuck", "bitch", "fucker", "nigga", "nigger", "faggot", "pussy", "analsex", "anal", "niggas", "niggers", "faggots", 
    "assholes", "bitches", "shits", "fucks", "asses", "cum", "cumming", "cums", "fuckface", "cunt", "cuntface", "twat", "twatface"]


# Enable necessary intents

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
intents.messages = True


# Create bot instance with command prefix and intents

client = commands.Bot(command_prefix="!", intents=discord.Intents.all(), application_id=1396220606352986234)


# Define the guild ID for the bot to operate in

GUILD_ID = 1394304937789493389
MY_GUILD = discord.Object(id=GUILD_ID)


# Track recent destructive actions
user_actions = defaultdict(list)


# Anti-nuke function to check for rate limits on destructive actions (tracker for user actions)

async def check_rate_limit(guild, user, action_type, threshold=3, seconds=5):
    now = time.time()
    user_actions[(user.id, action_type)] = [
        t for t in user_actions[(user.id, action_type)] if now - t < seconds
    ]
    user_actions[(user.id, action_type)].append(now)
    if len(user_actions[(user.id, action_type)]) >= threshold:
        if not user.bot and user != guild.owner:
            await punish_nuker(guild, user, reason=f"Mass {action_type}")
            user_actions[(user.id, action_type)].clear()


# Bot actions and events (INDLUDES ALL COMMANDS AND EVENTS)

#  1. ʟᴏɢɪɴ ᴅᴏᴄᴜᴍᴇɴᴛᴀᴛɪᴏɴ ᴀɴᴅ ʀᴇᴠᴇɴɢᴇ ᴏɴ ʙᴏᴛ ʀᴇᴍᴏᴠᴇʀ
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="/help for commands"))
    await client.tree.sync(guild=MY_GUILD)
    print(f"✅ Bot logged in as {client.user}")
    if settings.get("revengeOnBotRemoverToggle"):
        for guild in client.guilds:
            async for entry in guild.audit_logs(limit=10, action=discord.AuditLogAction.kick):
                if entry.target == client.user:
                    actor = entry.user
                    if actor != guild.owner and not actor.bot:
                        try:
                            await actor.kick(reason="You attempted to kick the bot.")
                            print(f"Kicked {actor} for trying to remove the bot.")
                        except discord.Forbidden:
                            print(f"Could not punish {actor} (missing permissions).")


#  2. ᴍᴇssᴀɢᴇ ᴅᴇʟᴇᴛɪᴏɴ ᴀɴᴅ ᴡᴀʀɴɪɴɢs (ɪɴᴄʟᴜᴅᴇꜱ ᴡᴇʙʜᴏᴏᴋꜱ)
@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    if settings.get("filterSystemToggle"):  # Check if filter system is enabled
        is_webhook = msg.webhook_id is not None
        is_user = not is_webhook and not any(role.name == "Founder" for role in msg.author.roles)
        if is_webhook or is_user:
            content = msg.content.lower()
            if any(bad_word in content for bad_word in block_words):
                await msg.delete()
                warning_msg = (
                    f"{msg.author.mention}, your message was deleted because it contained inappropriate language."
                    if not is_webhook else
                    "🚫 A webhook message was deleted because it contained inappropriate language."
                )
                await msg.channel.send(warning_msg)
    await client.process_commands(msg)


#  3. ᴡᴇʙʜᴏᴏᴋ ᴅᴇʟᴇᴛɪᴏɴ ᴀɴᴅ ᴜᴘᴅᴀᴛᴇs
@client.event
async def on_webhooks_update(channel):
    if settings.get("webhookDeleterToggle"):  # Check if webhook deleter is enabled
        try:
            webhooks = await channel.webhooks()
            for webhook in webhooks:
                try:
                    await webhook.delete()
                    print(f"Deleted webhook '{webhook.name}' in #{channel.name}")
                except discord.Forbidden:
                    print(f"❌ Permission error: Couldn't delete webhook '{webhook.name}' in #{channel.name}")
                except Exception as e:
                    print(f"⚠️ Unexpected error deleting webhook '{webhook.name}': {e}")
        except Exception as e:
            print(f"⚠️ Failed to fetch webhooks for #{channel.name}: {e}")

#  4. ʀᴏʟᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ (ᴘʀᴏᴛᴇᴄᴛᴇᴅ ʀᴏʟᴇs)
@client.event
async def on_member_update(before, after):
    if settings.get("roleProtectionToggle"):  # Check if role protection is enabled
        removed_roles = [role for role in before.roles if role not in after.roles]
        for role in removed_roles:
            if role.name in protected_roles:
                guild = after.guild
                async for entry in guild.audit_logs(limit=5, action=discord.AuditLogAction.member_role_update):
                    if entry.target.id == after.id:
                        removed = entry.changes.before.roles if hasattr(entry.changes.before, 'roles') else []
                        added = entry.changes.after.roles if hasattr(entry.changes.after, 'roles') else []
                        if role in removed and role not in added:
                            actor = entry.user
                            if actor != client.user and not actor.bot:
                                try:
                                    await actor.edit(roles=[])
                                    await actor.send(
                                        f"You have been stripped of all roles for removing the role `{role.name}` from {after.mention}."
                                    )
                                    print(f"🔒 Removed all roles from {actor.name} for modifying protected roles.")
                                except discord.Forbidden:
                                    print(f"⚠️ Permission error: cannot modify roles for {actor.name}.")
                            break

#  5. ʀᴏʟᴇ ᴜᴘᴅᴀᴛᴇ ᴡɪᴛʜ ᴅᴀɴɢᴇʀᴏᴜꜱ ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ
@client.event
async def on_guild_role_update(before: discord.Role, after: discord.Role):
    if settings.get("permissionPreventerToggle"):  # Toggle check
        dangerous_perms = [
            "administrator",
            "manage_roles",
            "manage_channels",
            "manage_guild",
            "kick_members",
            "ban_members",
            "mention_everyone",
            "manage_webhooks"
        ]
        for perm in dangerous_perms:
            before_value = getattr(before.permissions, perm)
            after_value = getattr(after.permissions, perm)
            if not before_value and after_value:
                print(f"[SECURITY] Dangerous permission '{perm}' was added to role '{after.name}'")
                try:
                    fixed_perms = after.permissions
                    perms_dict = fixed_perms._values.copy()
                    perms_dict[perm] = False
                    new_perms = discord.Permissions(**perms_dict)
                    await after.edit(permissions=new_perms, reason="Dangerous permissions removed automatically")
                    print(f"[SECURITY] Removed dangerous permission '{perm}' from role '{after.name}'")
                except discord.Forbidden:
                    print(f"[WARNING] Cannot edit role '{after.name}'. Lacking permission.")
                    return
                guild = after.guild
                async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update):
                    if entry.target.id == after.id:
                        culprit = entry.user
                        if culprit != guild.owner and not culprit.bot:
                            try:
                                await culprit.edit(roles=[])
                                quarantine_role = discord.utils.get(guild.roles, name="Quarantine")
                                if quarantine_role:
                                    await culprit.add_roles(quarantine_role)
                                    print(f"[SECURITY] {culprit} punished and placed in Quarantine.")
                                else:
                                    print("[WARNING] 'Quarantine' role not found. Create it manually!")
                                try:
                                    await culprit.send(
                                        f"You have been quarantined for adding dangerous permissions "
                                        f"(`{perm}`) to the role `{after.name}`."
                                    )
                                except discord.Forbidden:
                                    print(f"[INFO] Could not DM {culprit}")
                            except discord.Forbidden:
                                print(f"[WARNING] Cannot punish {culprit}. Lacking permission.")
                        break
                break

#  6.  ᴀɴᴛɪ-ɴᴜᴋᴇ ᴍᴏᴅᴜʟᴇ
@client.event                                                                                         # Mass Deleting Channels
async def on_guild_channel_delete(channel):
    if settings.get("antiNukeToggle"):
        guild = channel.guild
        async for entry in guild.audit_logs(limit=3, action=discord.AuditLogAction.channel_delete):
            await check_rate_limit(guild, entry.user, "channel_delete")
@client.event                                                                                         # Mass Creating Channels
async def on_guild_channel_create(channel):
    if settings.get("antiNukeToggle"):
        guild = channel.guild
        async for entry in guild.audit_logs(limit=3, action=discord.AuditLogAction.channel_create):
            await check_rate_limit(guild, entry.user, "channel_create")
@client.event                                                                                         # Mass Banning Members
async def on_member_ban(guild, user):
    if settings.get("antiNukeToggle"):
        async for entry in guild.audit_logs(limit=7, action=discord.AuditLogAction.ban):
            await check_rate_limit(guild, entry.user, "ban")
@client.event                                                                                         # Mass Kicking Members
async def on_member_remove(member):
    if settings.get("antiNukeToggle"):
        guild = member.guild
        async for entry in guild.audit_logs(limit=7, action=discord.AuditLogAction.kick):
            await check_rate_limit(guild, entry.user, "kick")
@client.event                                                                                         # Mass Role Creation
async def on_guild_role_create(role):
    if settings.get("antiNukeToggle"):
        guild = role.guild
        async for entry in guild.audit_logs(limit=4, action=discord.AuditLogAction.role_create):
            await check_rate_limit(guild, entry.user, "role_create")
@client.event                                                                                         # Mass Role Deletion
async def on_guild_role_delete(role):
    if settings.get("antiNukeToggle"):
        guild = role.guild
        async for entry in guild.audit_logs(limit=4, action=discord.AuditLogAction.role_delete):
            await check_rate_limit(guild, entry.user, "role_delete")
async def punish_nuker(guild, user, reason="Nuking behavior"):
    try:
        quarantine = discord.utils.get(guild.roles, name="Quarantine")
        if not quarantine:
            quarantine = await guild.create_role(name="Quarantine", permissions=discord.Permissions.none())
        await user.edit(roles=[quarantine], reason=reason)
        await guild.system_channel.send(f"🚨 {user.mention} was quarantined: {reason}")
    except discord.Forbidden:
        print(f"Could not punish {user}. Missing permissions.")

#  7.  ᴀɴᴛɪ-ʀᴀɪᴅ ᴍᴏᴅᴜʟᴇ
join_tracker = defaultdict(list)

@client.event
async def on_member_join(member):
    if not settings.get("antiRaidToggle"):
        return
    now = time.time()
    guild = member.guild
    join_tracker[guild.id] = [t for t in join_tracker[guild.id] if now - t < 10]
    join_tracker[guild.id].append(now)
    if len(join_tracker[guild.id]) >= 5:
        await trigger_anti_raid(guild)
async def trigger_anti_raid(guild):
    raid_role = discord.utils.get(guild.roles, name="Quarantine")
    if not raid_role:
        raid_role = await guild.create_role(name="Quarantine", permissions=discord.Permissions.none())
    async for member in guild.fetch_members(limit=200):
        if member.joined_at and (discord.utils.utcnow() - member.joined_at).total_seconds() < 10:
            try:
                await member.edit(roles=[raid_role], reason="Anti-raid triggered")
            except discord.Forbidden:
                print(f"⚠️ Couldn't quarantine {member}")
    if guild.system_channel:
        await guild.system_channel.send("⚠️ Raid detected! Lockdown initiated and members quarantined.")


#  8a. /ʙᴀɴ ᴄᴏᴍᴍᴀɴᴅ
@client.tree.command(name="ban", description="Ban a member from the server")
@app_commands.describe(user="User to ban", time="Ban duration (e.g., 1d, 2h)", reason="Reason for the ban")
async def ban(interaction: discord.Interaction, user: discord.Member, time: str, reason: str):
    if interaction.user.guild_permissions.ban_members:
        await user.ban(reason=reason)
        await interaction.response.send_message(f"🔨 Banned {user.mention} for `{reason}` (Duration: {time})", ephemeral=True)
    else:
        await interaction.response.send_message("❌ You don't have permission to ban members.", ephemeral=True)
#  8b. /ᴋɪᴄᴋ ᴄᴏᴍᴍᴀɴᴅ
@client.tree.command(name="kick", description="Kick a member from the server")
@app_commands.describe(user="User to kick", reason="Reason for the kick")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str):
    if interaction.user.guild_permissions.kick_members:
        await user.kick(reason=reason)
        await interaction.response.send_message(f"👢 Kicked {user.mention} for `{reason}`", ephemeral=True)
    else:
        await interaction.response.send_message("❌ You don't have permission to kick members.", ephemeral=True)
# 8c. /ᴛɪᴍᴇᴏᴜᴛ ᴄᴏᴍᴍᴀɴᴅ
@client.tree.command(name="timeout", description="Timeout a member from the server")
@app_commands.describe(user="User to timeout", time="Duration (e.g., 10m, 2h)", reason="Reason for the timeout")
async def timeout(interaction: discord.Interaction, user: discord.Member, time: str, reason: str):
    if interaction.user.guild_permissions.moderate_members:
        units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        try:
            duration = int(time[:-1]) * units[time[-1]]
            until = discord.utils.utcnow() + datetime.timedelta(seconds=duration)
            await user.timeout(until, reason=reason)
            await interaction.response.send_message(f"⏱️ Timed out {user.mention} for `{reason}` (Duration: {time})", ephemeral=True)
        except:
            await interaction.response.send_message("❌ Invalid time format! Use `5m`, `2h`, `1d`, etc.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ You don't have permission to timeout members.", ephemeral=True)
#  8d. /ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅ
@client.tree.command(name="help", description="General assitance regarding this bot", guild=MY_GUILD)
async def help_command(interaction: discord.Interaction):
    embed = Embed(title="📘 Delta Security Bot Help", color=0x00ffcc)
    embed.add_field(name="==================================================" , value="ᴄᴏᴍᴍᴀɴᴅꜱ", inline=False)
    embed.add_field(name="📊 /about", value="Displays bot information and statistics.", inline=False)
    embed.add_field(name="🔨 /ban  <user>  <time>  <reason>", value="Ban a member temporarily or permanently.", inline=False)
    embed.add_field(name="👟 /kick  <user>  <reason>", value="Kick a member from the server.", inline=False)
    embed.add_field(name="⏳ /timeout  <user>  <time>  <reason>", value="Timeout a user for a duration.", inline=False)
    embed.add_field(name="=================================================" , value="ꜰᴇᴀᴛᴜʀᴇꜱ", inline=False)
    embed.add_field(name="🧹 Auto-Filter", value="Automatically filters slurs and harmful words.", inline=False)
    embed.add_field(name="🚫 Anti-Nuke", value="Prevents mass deletions, role changes, and other destructive actions.", inline=False)
    embed.add_field(name="🛡️ Anti-Raid", value="Quarantines members who join too quickly to prevent raids.", inline=False)
    embed.add_field(name="🕷️ Anti-Webhook", value="Deletes webhooks instantly to prevent exploits.", inline=False)
    embed.add_field(name="🔒 Role Protection", value="Protects specified roles from unauthorized changes.", inline=False)
    embed.add_field(name="🛡️ Role Management", value="Monitors role changes and prevents dangerous permissions.", inline=False)
    embed.add_field(name="==================================================", value="Delta Security Bot | Protecting your server.", inline=False)
    """embed.set_footer(text="Delta Security Bot | Protecting your server.")"""
    await interaction.response.send_message(embed=embed, ephemeral=True)
# 8e. /ᴀʙᴏᴜᴛ ᴄᴏᴍᴍᴀɴᴅ
@client.tree.command(name="about", description="Shows information about the bot")
async def about_command(interaction: discord.Interaction):
    bot_user = client.user
    guild_count = len(client.guilds)
    ping = round(client.latency * 1000)
    version = "1.0.0"
    embed = Embed(color=0x00ffff)
    embed.add_field(name="**Name**", value=f"{bot_user.name}#{bot_user.discriminator}", inline=True)
    embed.add_field(name="**ID**", value=f"{bot_user.id}", inline=True)
    embed.add_field(name="**Version**", value=version, inline=True)
    embed.add_field(name="**Guilds**", value=f"{guild_count:,} Guilds", inline=True)
    embed.add_field(name="**Ping**", value=f"{ping}ms", inline=True)
    await interaction.response.send_message(embed=embed, ephemeral=True)


# If the bot disconnects, it will attempt to reconnect automatically

@client.event
async def on_disconnect():
    try:
        print("Bot disconnected. Attempting to reconnect...")
        await client.connect(reconnect=True)
        if client.is_connected():
            print("Bot reconnected successfully.")
    except Exception as e:
        print(f"Failed to reconnect: {e}")


# Run the bot with the provided token

client.run(token)
