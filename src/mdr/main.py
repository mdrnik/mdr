import os
import time
import shutil
import platform
import subprocess
import click
from pathlib import Path
from click_shell import shell

def _open_in_explorer(target_path: Path):
    """Внутренний помощник для открытия папки в системном проводнике."""
    current_os = platform.system()
    if current_os == "Windows":
        os.startfile(target_path)
    elif current_os == "Darwin":
        subprocess.run(["open", target_path], check=True)
    else:
        subprocess.run(["xdg-open", target_path], check=True)

@shell(prompt='mdr > ', intro='Welcome!\n(Наберите help для вывода доступных комманд, exit дл выхода из программы.)')
def mdr():
    """Главная оболочка приложения."""
    pass

# Путь к файлу
BASE_DIR = Path(__file__).resolve().parents[2] / 'AMOD' / 'EQUIPMENT'
CHROME_PATH = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")


@mdr.command(name='obs')
def launch_obsidian():
    """Открыть базу знаний Obsidian и очистить экран."""
    # Путь к Obsidian (используем сырую строку r'' для путей Windows)
    obsidian_path = Path.home() / "AppData" / "Local" / "Programs" / "Obsidian" / "Obsidian.exe"
    
    if not os.path.exists(obsidian_path):
        click.echo(f"Ошибка: Исполняемый файл Obsidian не найден по пути {obsidian_path}")
        return

    try:
        subprocess.Popen([obsidian_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Очищаем экран консоли аналогично `clear`
        click.clear()
    except Exception as e:
        click.echo(f"Не удалось запустить Obsidian: {e}")


@mdr.command(name='sync')
def launch_syncthing():
    """Запустить Syncthing в фоне и открыть веб-интерфейс в Chrome."""
    syncthing_name = "syncthing"
    url = "http://localhost:8384"

    # Проверяем, доступен ли syncthing в системе (в PATH) или по указанному пути
    if not shutil.which(syncthing_name):
        click.echo(
            f"Ошибка: Исполняемый файл '{syncthing_name}' не найден в PATH."
        )
        return

    # Проверяем существование Chrome
    if not CHROME_PATH.exists():
        click.echo(
            f"Ошибка: Исполняемый файл Chrome не найден по пути {CHROME_PATH}"
        )
        return

    try:
        # 1. Запуск Syncthing в фоне без консольного окна и браузера
        subprocess.Popen(
            [syncthing_name, "--no-browser"], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW  # Скрывает окно консоли Syncthing на Windows
        )
        
        # 2. Небольшая пауза, чтобы сервис успел подняться
        time.sleep(1)
        
        # 3. Открытие Chrome в режиме инкогнито
        subprocess.Popen(
            [CHROME_PATH, "--incognito", url], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        
        click.echo("Syncthing запущен. Интерфейс открыт в Chrome.")
        click.clear()
        
    except Exception as e:
        click.echo(f"Не удалось запустить Syncthing: {e}")

@mdr.command(name='gem')
def launch_gemini():
    """Открыть Gemini в режиме инкогнито и очистить экран."""
    # Стандартный путь к Google Chrome на Windows
    gemini_url = "https://gemini.google.com"
    
    if not CHROME_PATH.exists():
        click.echo(f"Ошибка: Исполняемый файл Chrome не найден по пути {chrome_path}")
        return

    try:
        # Запускаем Chrome с флагом инкогнито и ссылкой
        subprocess.Popen([CHROME_PATH, "--incognito", gemini_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Очищаем экран консоли
        click.clear()
    except Exception as e:
        click.echo(f"Не удалось запустить Chrome: {e}")



# # Включаем запуск группы без обязательного указания подкоманды
@mdr.group(name='cat', invoke_without_command=True)
def cat():
    pass

# Подкоманда OPEN
@cat.command(name='open')
@click.argument('folder_id', required=False, default='')
def cat_open(folder_id):
    """Открыть каталог. Пример: cat open 1200 или cat open (главная папка)."""
    if folder_id:
        target_dir = BASE_DIR / str(folder_id)
        msg = f"Открыт каталог [{folder_id}]"
    else:
        target_dir = BASE_DIR
        msg = "Открыта главная папка техники"
    
    if not target_dir.exists():
        click.echo(f"Ошибка! Путь не существует: {target_dir}")
        return

    try:
        _open_in_explorer(target_dir)
        click.echo(msg)
    except Exception as e:
        click.echo(f"Не удалось открыть проводник. Ошибка: {e}")

# Подкоманда ADD
@cat.command(name='add')
@click.argument('folder_id', required=True)
def cat_add(folder_id):
    """Создать новый каталог. Пример: cat add 1300"""
    target_dir = BASE_DIR / str(folder_id)
    
    if target_dir.exists():
        click.echo(f"Папка [{folder_id}] уже существует: {target_dir}")
        return

    try:
        target_dir.mkdir(parents=True, exist_ok=False)
        click.echo(f"Создана новая папка оборудования: [{folder_id}]")
        
        # Сразу открываем созданную папку
        _open_in_explorer(target_dir)
            
    except Exception as e:
        click.echo(f"Ошибка при создании папки: {e}")


if __name__ == '__main__':
    mdr()