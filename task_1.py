import asyncio
import aiofiles
import shutil
from aiofiles.os import makedirs, path, scandir
from argparse import ArgumentParser
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(src_file, dest_folder):
    """Копіює файл у відповідну підпапку у цільовій папці на основі його розширення"""
    ext = src_file.suffix
    target_folder = dest_folder / ext[1:]  # видаляємо перший символ '.' з розширення
    await makedirs(target_folder, exist_ok=True)
    dest_file = target_folder / src_file.name

    async with aiofiles.open(src_file, 'rb') as src:
        async with aiofiles.open(dest_file, 'wb') as dest:
            while True:
                chunk = await src.read(1024)
                if not chunk:
                    break
                await dest.write(chunk)
    
    logging.info(f'Копіювання {src_file} до {dest_file}')

async def read_folder(src_folder, dest_folder):
    """Рекурсивно читає всі файли у вихідній папці та її підпапках"""
    async for entry in scandir(src_folder):
        if entry.is_dir():
            await read_folder(entry.path, dest_folder)
        elif entry.is_file():
            await copy_file(entry.path, dest_folder)
        else:
            logging.warning(f'Невідомий тип: {entry.path}')

def main():
    parser = ArgumentParser(description="Асинхронне сортування файлів за розширенням")
    parser.add_argument('src_folder', type=str, help="Вихідна папка")
    parser.add_argument('dest_folder', type=str, help="Цільова папка")
    
    args = parser.parse_args()

    src_folder = path.abspath(args.src_folder)
    dest_folder = path.abspath(args.dest_folder)
    
    if not path.exists(src_folder):
        logging.error(f'Вихідна папка не існує: {src_folder}')
        return
    
    asyncio.run(read_folder(src_folder, dest_folder))

if __name__ == "__main__":
    main()
