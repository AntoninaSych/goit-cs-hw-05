import asyncio
import aiofiles
from aiopath import AsyncPath
from argparse import ArgumentParser
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def copy_file(src_file, dest_folder):
    """Копіює файл у відповідну підпапку у цільовій папці на основі його розширення"""
    ext = src_file.suffix
    target_folder = dest_folder / ext[1:]  # видаляємо перший символ '.' з розширення
    await target_folder.mkdir(parents=True, exist_ok=True)
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
    async for entry in src_folder.iterdir():
        if await entry.is_dir():
            await read_folder(entry, dest_folder)
        elif await entry.is_file():
            await copy_file(entry, dest_folder)
        else:
            logging.warning(f'Невідомий тип: {entry}')

async def main():
    parser = ArgumentParser(description="Асинхронне сортування файлів за розширенням")
    parser.add_argument('src_folder', type=str, nargs='?', help="Вихідна папка")
    parser.add_argument('dest_folder', type=str, nargs='?', help="Цільова папка")
    
    args = parser.parse_args()

    # Запит на введення адреси вихідної та цільової папок, якщо не задано аргументами командного рядка
    if not args.src_folder:
        args.src_folder = input("Введіть шлях до вихідної папки: ").strip()
    if not args.dest_folder:
        args.dest_folder = input("Введіть шлях до цільової папки: ").strip()

    src_folder = await AsyncPath(args.src_folder).resolve()
    dest_folder = await AsyncPath(args.dest_folder).resolve()
    
    if not await src_folder.exists():
        logging.error(f'Вихідна папка не існує: {src_folder}')
        return
    
    await read_folder(src_folder, dest_folder)

if __name__ == "__main__":
    asyncio.run(main())
