import os
import discord
from config import DISCORD_UPLOAD_LIMIT
from core.logger import Logger

logger = Logger()


class FileUploader:
    def __init__(self, split_folder="split_files", download_folder="downloads"):
        """
        Inicializace FileUploader s výchozími složkami pro rozdělené a stažené soubory.
        """
        self.split_folder = split_folder
        self.download_folder = download_folder

        # Zajištění existence složek
        for folder in [self.split_folder, self.download_folder]:
            os.makedirs(folder, exist_ok=True)
            logger.info(f"Folder '{folder}' checked/created.")

    def split_file(self, file_path):
        """
        Rozdělení velkého souboru na menší části podle limitu Discordu.
        """
        try:
            part_size = DISCORD_UPLOAD_LIMIT
            parts = []

            with open(file_path, 'rb') as file:
                part_number = 1
                while chunk := file.read(part_size):
                    part_name = f"{os.path.basename(file_path)}.part{part_number}"
                    part_path = os.path.join(self.split_folder, part_name)

                    with open(part_path, 'wb') as part_file:
                        part_file.write(chunk)

                    parts.append(part_path)
                    logger.info(f"Created part: {part_path}")
                    part_number += 1

            return parts

        except Exception as e:
            logger.error(f"Error splitting file: {e}")
            return []

    async def send_file(self, file_path, channel):
        """
        Odeslání souboru nebo části na Discord kanál.
        """
        try:
            with open(file_path, 'rb') as f:
                await channel.send(file=discord.File(f, os.path.basename(file_path)))
                logger.info(f"Sent file: {file_path}")
                return "Upload successful"
        except Exception as e:
            logger.error(f"Error sending file {file_path}: {e}")
            return f"Error: {str(e)}"

    async def upload_file_to_discord(self, file_path, channel):
        """
        Nahraje soubor na Discord, pokud je větší než limit, rozdělí jej na části.
        """
        try:
            file_size = os.path.getsize(file_path)

            if file_size <= DISCORD_UPLOAD_LIMIT:
                return await self.send_file(file_path, channel)

            # Rozdělení souboru a odeslání částí
            part_files = self.split_file(file_path)
            for part_file in part_files:
                result = await self.send_file(part_file, channel)
                os.remove(part_file)  # Úklid dočasných částí
                if "Error" in result:
                    return result

            return "Upload successful"

        except Exception as e:
            logger.error(f"Failed to upload file: {e}")
            return f"Error: {str(e)}"

    def join_files(self, parts, output_path):
        """
        Spojí rozdělené části souboru zpět do jednoho souboru.
        """
        try:
            with open(output_path, 'wb') as output_file:
                for part in parts:
                    with open(part, 'rb') as part_file:
                        output_file.write(part_file.read())
                        logger.info(f"Joined part: {part}")
            logger.info(f"File reassembled: {output_path}")
            return "Reassembly successful"
        except Exception as e:
            logger.error(f"Error reassembling file: {e}")
            return f"Error: {str(e)}"

    async def download_and_reassemble(self, file_info_list, output_path):
        """
        Stáhne části souboru a spojí je zpět do původního souboru.
        """
        try:
            import aiohttp

            part_paths = []
            async with aiohttp.ClientSession() as session:
                for file_info in file_info_list:
                    # Kontrola klíče 'url'
                    file_url = file_info.get("url")
                    if not file_url:
                        raise KeyError(f"Missing 'url' in metadata: {file_info}")

                    file_name = file_info["name"]
                    part_path = os.path.join(self.download_folder, file_name)

                    async with session.get(file_url) as response:
                        if response.status == 200:
                            # Správný asynchronní zápis souboru
                            with open(part_path, 'wb') as part_file:
                                while chunk := await response.content.read(1024):
                                    part_file.write(chunk)

                            part_paths.append(part_path)
                            logger.info(f"Downloaded part: {file_name}")
                        else:
                            logger.error(f"Failed to download {file_name} (Status: {response.status})")
                            return f"Download failed for {file_name}"

            # Spojení částí
            result = self.join_files(part_paths, output_path)

            # Vyčištění stažených částí
            for part in part_paths:
                os.remove(part)
                logger.info(f"Removed part: {part}")

            return result

        except Exception as e:
            logger.error(f"Download and reassembly failed: {e}")
            return f"Error: {str(e)}"
