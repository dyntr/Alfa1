import os
import json
import discord
import asyncio
import aiohttp  # Pro stahování souborů
from multiprocessing import Queue
from src.config import DISCORD_TOKEN, UPLOAD_CHANNEL_ID, DISCORD_UPLOAD_LIMIT

# Inicializace Discord bota
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

# Složky a logy
DOWNLOAD_FOLDER = "downloads"
SPLIT_FOLDER = "split_files"
UPLOAD_LOG = "uploaded_files.json"

# Zajištění složek a logů
for folder in [DOWNLOAD_FOLDER, SPLIT_FOLDER]:
    os.makedirs(folder, exist_ok=True)

if not os.path.exists(UPLOAD_LOG):
    with open(UPLOAD_LOG, 'w') as f:
        json.dump([], f)

# -------------------------------
# Metadata a správa souborů
# -------------------------------

def save_uploaded_file(file_info):
    """Uložení informací o nahraných souborech do JSON logu."""
    try:
        with open(UPLOAD_LOG, 'r') as f:
            uploaded_files = json.load(f)
        uploaded_files.append(file_info)
        with open(UPLOAD_LOG, 'w') as f:
            json.dump(uploaded_files, f, indent=4)
    except Exception as e:
        print(f"Error saving metadata: {e}")


def load_uploaded_files():
    """Načtení seznamu nahraných souborů."""
    try:
        with open(UPLOAD_LOG, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading metadata: {e}")
        return []


# -------------------------------
# Funkce pro rozdělování a skládání souborů
# -------------------------------

def split_file(file_path):
    """Rozdělení souboru na části podle limitu Discordu."""
    parts = []
    try:
        with open(file_path, 'rb') as file:
            part_number = 1
            while chunk := file.read(DISCORD_UPLOAD_LIMIT):
                part_name = f"{os.path.basename(file_path)}.part{part_number}"
                part_path = os.path.join(SPLIT_FOLDER, part_name)
                with open(part_path, 'wb') as part_file:
                    part_file.write(chunk)
                parts.append(part_path)
                part_number += 1
        return parts
    except Exception as e:
        print(f"Error splitting file: {e}")
        return []


def join_files(parts, output_path):
    """Složení rozdělených částí zpět do původního souboru."""
    try:
        with open(output_path, 'wb') as output_file:
            for part in parts:
                with open(part, 'rb') as part_file:
                    output_file.write(part_file.read())
        print(f"File reassembled: {output_path}")
        return "Reassembly successful"
    except Exception as e:
        print(f"Error joining files: {e}")
        return f"Error: {str(e)}"


# -------------------------------
# Discord funkce
# -------------------------------

async def upload_file(channel_id, file_path):
    """Nahrání souboru na Discord (včetně rozdělení na části)."""
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)

    if not channel:
        return "Channel not found"

    # Rozdělení souboru, pokud je větší než limit
    file_size = os.path.getsize(file_path)
    parts = split_file(file_path) if file_size > DISCORD_UPLOAD_LIMIT else [file_path]

    for part in parts:
        try:
            with open(part, 'rb') as f:
                message = await channel.send(file=discord.File(f, os.path.basename(part)))
                for attachment in message.attachments:
                    save_uploaded_file({
                        "name": attachment.filename,
                        "url": attachment.url,
                        "is_part": len(parts) > 1,
                        "original_name": os.path.basename(file_path) if len(parts) > 1 else os.path.basename(file_path),
                        "total_parts": len(parts) if len(parts) > 1 else 1
                    })
        except Exception as e:
            return f"Error: {str(e)}"

        # Smazání dočasných částí
        if part != file_path:
            os.remove(part)

    return "Upload successful"


async def download_and_reassemble(file_info_list, output_path):
    """Stažení částí souboru a složení zpět."""
    try:
        part_paths = []
        async with aiohttp.ClientSession() as session:
            for file_info in file_info_list:
                # Kontrola URL a názvu souboru
                file_url = file_info["url"]
                file_name = file_info["name"]
                part_path = os.path.join(DOWNLOAD_FOLDER, file_name)

                # Stažení části
                async with session.get(file_url) as response:
                    if response.status == 200:
                        with open(part_path, 'wb') as part_file:
                            while chunk := await response.content.read(1024):
                                part_file.write(chunk)
                        part_paths.append(part_path)
                    else:
                        print(f"Failed to download {file_name}")
                        return f"Failed to download {file_name}"

            # Složení částí
            return join_files(part_paths, output_path)
    except Exception as e:
        return f"Error: {str(e)}"


# -------------------------------
# Bot Events
# -------------------------------

@bot.event
async def on_ready():
    """Událost spuštění bota."""
    print(f"Logged in as {bot.user}")
    for guild in bot.guilds:
        print(f"Connected to guild: {guild.name} (ID: {guild.id})")


async def bot_task_processor(task_queue, result_queue):
    """Procesor úloh pro Discord bota."""
    while True:
        if not task_queue.empty():
            task = task_queue.get()

            # Zastavení bota
            if task == "STOP":
                await bot.close()
                break

            # Stažení souborů
            elif "download_files" in task:
                files = load_uploaded_files()
                selected_indexes = task.get("download_files", [])
                file_info_list = [files[i] for i in selected_indexes]
                original_name = file_info_list[0].get("original_name", "output_file")
                output_path = os.path.join(DOWNLOAD_FOLDER, original_name)

                # Stáhnout a složit zpět
                result = await download_and_reassemble(file_info_list, output_path)

            # Nahrání souboru
            else:
                file_path = task.get("file_path")
                result = await upload_file(UPLOAD_CHANNEL_ID, file_path)

            result_queue.put(result)


# ----------------------------
# Hlavní procesy
# ----------------------------

async def start_bot_and_processor(task_queue, result_queue):
    processor_task = asyncio.create_task(bot_task_processor(task_queue, result_queue))
    await bot.start(DISCORD_TOKEN)
    await processor_task


def bot_process(task_queue: Queue, result_queue: Queue):
    asyncio.run(start_bot_and_processor(task_queue, result_queue))
