import os
import time
import platform
import subprocess
import click
from pathlib import Path
from click_shell import shell

@shell(prompt='mdr > ', intro='Добро пожаловать!')
def mdr():
    """Главная оболочка приложения."""
    pass

# Путь к папке, где лежит main.py (C:\Users\User\projects\mdr\src\mdr)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Поднимаемся на 2 уровня вверх в корень проекта (C:\Users\User\projects\mdr)
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', '..'))

# Строим путь к AMOD от корня проекта
BASE_DIR = os.path.join(ROOT_DIR, 'AMOD', 'EQUIPMENT')


@mdr.command(name='obs')
def launch_obsidian():
    """Открыть базу знаний Obsidian и очистить экран."""
    # Путь к Obsidian (используем сырую строку r'' для путей Windows)
    obsidian_path = r"C:\Users\User\AppData\Local\Programs\Obsidian\Obsidian.exe"
    
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
    syncthing_path = "syncthing"  # Предполагается, что он добавлен в PATH. Если нет, укажите полный путь r"C:\..."
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    url = "http://localhost:8384"

    try:
        # 1. Запуск Syncthing в фоне без консольного окна и браузера
        subprocess.Popen(
            [syncthing_path, "--no-browser"], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW  # Скрывает окно консоли Syncthing на Windows
        )
        
        # 2. Небольшая пауза, чтобы сервис успел подняться
        time.sleep(1)
        
        # 3. Открытие Chrome в режиме инкогнито
        subprocess.Popen(
            [chrome_path, "--incognito", url], 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        
        click.echo("Syncthing запущен. Интерфейс открыт в Chrome.")
        click.clear()
        
    except FileNotFoundError as e:
        click.echo(f"Ошибка: Проверьте правильность путей к программам. {e}")
    except Exception as e:
        click.echo(f"Не удалось запустить Syncthing: {e}")

@mdr.command(name='gem')
def launch_gemini():
    """Открыть Gemini в режиме инкогнито и очистить экран."""
    # Стандартный путь к Google Chrome на Windows
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    gemini_url = "https://google.com"
    
    if not os.path.exists(chrome_path):
        click.echo(f"Ошибка: Исполняемый файл Chrome не найден по пути {chrome_path}")
        return

    try:
        # Запускаем Chrome с флагом инкогнито и ссылкой
        subprocess.Popen([chrome_path, "-incognito", gemini_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
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
        target_dir = os.path.join(BASE_DIR, str(folder_id))
        msg = f"Открыт каталог [{folder_id}]"
    else:
        target_dir = BASE_DIR
        msg = "Открыта главная папка техники"
    
    if not os.path.exists(target_dir):
        click.echo(f"Ошибка! Путь не существует: {target_dir}")
        return

    try:
        current_os = platform.system()
        if current_os == "Windows":
            os.startfile(target_dir)
        elif current_os == "Darwin":
            subprocess.run(["open", target_dir], check=True)
        else:
            subprocess.run(["xdg-open", target_dir], check=True)
            
        click.echo(msg)
    except Exception as e:
        click.echo(f"Не удалось открыть проводник. Ошибка: {e}")

# Подкоманда ADD
@cat.command(name='add')
@click.argument('folder_id', required=True)
def cat_add(folder_id):
    """Создать новый каталог. Пример: cat add 1300"""
    target_dir = os.path.join(BASE_DIR, str(folder_id))
    
    if os.path.exists(target_dir):
        click.echo(f"Папка [{folder_id}] уже существует: {target_dir}")
        return

    try:
        os.makedirs(target_dir)
        click.echo(f"Создана новая папка оборудования: [{folder_id}]")
        
        # Сразу открываем созданную папку
        current_os = platform.system()
        if current_os == "Windows":
            os.startfile(target_dir)
        elif current_os == "Darwin":
            subprocess.run(["open", target_dir], check=True)
        else:
            subprocess.run(["xdg-open", target_dir], check=True)
            
    except Exception as e:
        click.echo(f"Ошибка при создании папки: {e}")


if __name__ == '__main__':
    mdr()