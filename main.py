import discord
from discord.ext import tasks
from discord import app_commands
import feedparser
import os
import json
import time
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

RSS_URL = "https://www.reddit.com/r/FreeGameFindings/new/.rss"
HISTORY_FILE = "history.json"
CONFIG_FILE = "config.json"

def load_json(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {} if filename == CONFIG_FILE else []
    return {} if filename == CONFIG_FILE else []

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_store_link(entry):
    description = entry.description if hasattr(entry, 'description') else ""
    match = re.search(r'href=[\'"]?(https?://(?:store\.steampowered\.com|store\.epicgames\.com|www\.gog\.com)[^\'" >]+)', description)
    if match:
        return match.group(1)
    return entry.link

# --- WEB SCRAPERS (KAZIYICILAR) ---
def get_image_from_url(url):
    """Magaza linkine gidip 'og:image' etiketinden oyunun orjinal kapak fotografini ceker."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            meta_img = soup.find('meta', property='og:image')
            if meta_img and meta_img.get('content'):
                return meta_img['content']
    except Exception as e:
        pass
    return None

def get_original_price(url):
    """
    Gelecekte oyunun gercek fiyatini ($39.99 vb.) cekecek olan fonksiyon.
    Simdilik sistemin cokmesini engellemek (Fallback) icin guvenli bir sekilde None dondurur.
    """
    return None

# --- CHANNEL SETUP COMMANDS ---
@tree.command(name="set_steam", description="Set this channel for free Steam games.")
@app_commands.default_permissions(manage_channels=True)
async def set_steam(interaction: discord.Interaction):
    config = load_json(CONFIG_FILE)
    config["STEAM_CHANNEL_ID"] = interaction.channel_id
    save_json(CONFIG_FILE, config)
    await interaction.response.send_message(f"✅ Free **Steam** games will now be posted in `#{interaction.channel.name}`!", ephemeral=False)

@tree.command(name="set_epic", description="Set this channel for free Epic Games.")
@app_commands.default_permissions(manage_channels=True)
async def set_epic(interaction: discord.Interaction):
    config = load_json(CONFIG_FILE)
    config["EPIC_CHANNEL_ID"] = interaction.channel_id
    save_json(CONFIG_FILE, config)
    await interaction.response.send_message(f"✅ Free **Epic Games** will now be posted in `#{interaction.channel.name}`!", ephemeral=False)

@tree.command(name="set_gog", description="Set this channel for free GOG games.")
@app_commands.default_permissions(manage_channels=True)
async def set_gog(interaction: discord.Interaction):
    config = load_json(CONFIG_FILE)
    config["GOG_CHANNEL_ID"] = interaction.channel_id
    save_json(CONFIG_FILE, config)
    await interaction.response.send_message(f"✅ Free **GOG** games will now be posted in `#{interaction.channel.name}`!", ephemeral=False)

@tree.command(name="set_other", description="Set this channel for other platforms (Itch.io, Ubisoft, etc.).")
@app_commands.default_permissions(manage_channels=True)
async def set_other(interaction: discord.Interaction):
    config = load_json(CONFIG_FILE)
    config["OTHER_CHANNEL_ID"] = interaction.channel_id
    save_json(CONFIG_FILE, config)
    await interaction.response.send_message(f"✅ Free games from **Other Platforms** will now be posted in `#{interaction.channel.name}`!", ephemeral=False)

# --- CORE SCANNER ENGINE ---
async def scan_for_games(client_instance):
    history = load_json(HISTORY_FILE)
    config = load_json(CONFIG_FILE)
    
    feed = feedparser.parse(RSS_URL)
    now = datetime.now()
    one_day_ago = now - timedelta(hours=24)
    new_games_count = 0

    for entry in feed.entries:
        try:
            published_time = datetime.fromtimestamp(time.mktime(entry.published_parsed))
            
            if published_time > one_day_ago:
                title = entry.title
                store_link = get_store_link(entry)
                title_upper = title.upper()
                
                target_channel_id = None
                embed_color = None
                platform_name = ""

                if "STEAM" in title_upper:
                    target_channel_id = config.get("STEAM_CHANNEL_ID")
                    embed_color = discord.Color.blue()
                    platform_name = "Steam"
                elif "EPIC" in title_upper or "EPICGAMES" in title_upper:
                    target_channel_id = config.get("EPIC_CHANNEL_ID")
                    embed_color = discord.Color.dark_grey()
                    platform_name = "Epic Games"
                elif "GOG" in title_upper:
                    target_channel_id = config.get("GOG_CHANNEL_ID")
                    embed_color = discord.Color.purple()
                    platform_name = "GOG"
                else:
                    target_channel_id = config.get("OTHER_CHANNEL_ID")
                    embed_color = discord.Color.green()
                    platform_name = "Other Platforms"

                if target_channel_id and store_link not in history:
                    channel = client_instance.get_channel(int(target_channel_id))
                    
                    if channel:
                        # --- FIYAT KONTROLU VE B PLANI (FALLBACK) ---
                        cekilen_fiyat = get_original_price(store_link)
                        
                        if cekilen_fiyat:
                            fiyat_metni = f"💸 ~~{cekilen_fiyat}~~ ➡️ **100% FREE!**"
                        else:
                            fiyat_metni = f"🎁 **100% FREE!**"
                            
                        embed_desc = (
                            f"**{title}**\n\n"
                            f"{fiyat_metni}\n"
                            f"***\n"
                            f"🔗 **[Click Here to Grab the Game]({store_link})**"
                        )
                        
                        embed = discord.Embed(
                            title=f"New {platform_name} Deal!",
                            description=embed_desc,
                            color=embed_color,
                            timestamp=published_time
                        )
                        embed.set_footer(text="The Freebie Hunter 🕶️ | Open Source")
                        
                        image_url = get_image_from_url(store_link)
                        if image_url:
                            embed.set_image(url=image_url)
                        
                        await channel.send(embed=embed)
                        print(f"✅ Found and posted: {title} ({platform_name})")
                        
                        history.append(store_link)
                        save_json(HISTORY_FILE, history)
                        new_games_count += 1
        except Exception as e:
            pass
            
    return new_games_count

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Free Games 👀"))
    print(f'🤖 {client.user} is online and hunting!')
    try:
        await tree.sync()
    except Exception as e:
        pass
    if not check_free_games.is_running():
        check_free_games.start()

@tree.command(name="status", description="Force a manual scan for new free games.")
async def status(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=False)
    new_games_count = await scan_for_games(interaction.client)
    if new_games_count > 0:
        await interaction.followup.send(f"✅ Manual scan complete! Found and posted **{new_games_count} new games**.")
    else:
        await interaction.followup.send("🔍 Scan complete. No new free games found at the moment.")

@tasks.loop(minutes=15)
async def check_free_games():
    await scan_for_games(client)

client.run(os.getenv('DISCORD_TOKEN'))