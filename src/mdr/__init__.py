import os
import platform
import subprocess
import click
from click_shell import shell

@shell(prompt='mdr > ', intro='Добро пожаловать!')
def mdr():
    """Главная оболочка приложения."""
    pass

# Базовый путь выносим в константу для удобства
BASE_DIR = os.path.expanduser('~/projects/AMOD/Equipment')

# # Включаем запуск группы без обязательного указания подкоманды
@mdr.group(name='cat', invoke_without_command=True)
def cat():
    pass
# @click.pass_context
# def cat(ctx):
#     """Управление каталогом оборудования (open, add)."""
#     # Если пользователь ввел просто "cat", перенаправляем его на команду "open" без ID
#     if ctx.invoked_subcommand is None:
#         ctx.invoke(cat_open, folder_id='')

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