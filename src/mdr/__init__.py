import os
import platform
import subprocess
import click
from click_shell import shell

@shell(prompt='mdr > ', intro='Добро пожаловать!\n\t(help - показать команды)\n\t(exit - выход)')
def mdr():
    """Главная оболочка приложения."""
    pass

@mdr.command(name='cat')
@click.argument('folder_id', required=False, default='')
def cat(folder_id):
    """Открыть каталог оборудования. Пример: cat 785 или просто cat."""
    # Базовый путь
    base_dir = os.path.expanduser('~/projects/AMOD/Equipment')
    
    # Если номер указан, добавляем его к пути, если нет — открываем корень Equipment
    if folder_id:
        target_dir = os.path.join(base_dir, str(folder_id))
        msg = f"🚀 Открыт каталог [{folder_id}]"
    else:
        target_dir = base_dir
        msg = f"🚀 Открыта главная папка оборудования"
    
    # # Создаем папку, если её нет
    # if not os.path.exists(target_dir):
    #     os.makedirs(target_dir)
    #     click.echo(f"📁 Создана новая папка: {target_dir}")

    # Открываем в проводнике ОС
    try:
        if platform.system() == "Windows":
            os.startfile(target_dir)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", target_dir], check=True)
        else:  # Linux
            subprocess.run(["xdg-open", target_dir], check=True)
            
        click.echo(msg)
    except Exception:
        click.echo(f"`Ошибка! Каталог не существует`")

if __name__ == '__main__':
    mdr()
