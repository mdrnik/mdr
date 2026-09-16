# mdr

Консольная программа для работы с каталогом техники Коматсу.

Для работы с файлами с расширением .md используется программы obsidian.

  

# Установка программы

Скачиваем по ссылке с гитхаба

```

https://github.com/mdrnik/mdr.git

```

или если есть доступ по ssh

```

git clone git.github.com:mdrnik/mdr.git

```

  

Установка с помощью менеджера пакетов uv

```

uv tool install .

```

  

Запуск программы с помошью ps:

```

mdr

```

  

После запуска откроется консоль для ввода комманд.

Для открытия папаок использовать комманды с номером техники. Для доступа к списку техники набрать `list`

  

import os

import platform

import subprocess

from pathlib import Path

import click

from click_shell import shell

  

@shell(prompt='mdr > ', intro='Добро пожаловать!')

def mdr():

    """Главная оболочка приложения."""

    pass

  

# Определение путей с помощью pathlib
```python

CURRENT_DIR = Path(__file__).resolve().parent

ROOT_DIR = CURRENT_DIR.parents[1]  # Поднимаемся на 2 уровня вверх в корень проекта

BASE_DIR = ROOT_DIR / 'AMOD' / 'Equipment'

  

def open_path_in_explorer(target_path: Path, success_msg: str):

    """Утилита для проверки пути и открытия его в операционной системе."""

    # Защита от выхода за пределы BASE_DIR

    if target_path != BASE_DIR and not target_path.resolve().is_relative_to(BASE_DIR.resolve()):

        click.echo("Ошибка! Доступ запрещен. Выход за пределы директории оборудования.")

        return

  

    if not target_path.exists():

        click.echo(f"Ошибка! Путь не существует: {target_path}")

        return

  

    try:

        current_os = platform.system()

        target_str = str(target_path)

        if current_os == "Windows":

            os.startfile(target_str)

        elif current_os == "Darwin":

            subprocess.run(["open", target_str], check=True)

        else:

            subprocess.run(["xdg-open", target_str], check=True)

        click.echo(success_msg)

    except Exception as e:

        click.echo(f"Не удалось открыть проводник. Ошибка: {e}")

  
  

@mdr.command(name='obs')

def launch_obsidian():

    """Открывает базу знаний Obsidian и очищает экран."""

    obsidian_path = Path(r"C:\Users\User\AppData\Local\Programs\Obsidian\Obsidian.exe")

    if not obsidian_path.exists():

        click.echo(f"Ошибка: Исполняемый файл Obsidian не найден по пути {obsidian_path}")

        return

  

    try:

        subprocess.Popen([str(obsidian_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        click.clear()

    except Exception as e:

        click.echo(f"Не удалось запустить Obsidian: {e}")

  
  

# ==========================================

# КОМАНДА ВЫВОДА СПИСКА ТЕХНИКИ (list / лист)

# ==========================================

@mdr.command(name='list')

def list_equipment():

    """Вывести список всей доступной техники."""

    if not BASE_DIR.exists():

        click.echo(f"Ошибка: Директория {BASE_DIR} не найдена.")

        return

  

    # Сканируем BASE_DIR и выбираем только папки

    folders = [f.name for f in BASE_DIR.iterdir() if f.is_dir()]

    if not folders:

        click.echo("В каталоге оборудования пока нет папок техники.")

        return

  

    click.echo("\nДоступный каталог техники:")

    for folder in sorted(folders):

        click.echo(f" 📂 {folder}")

    click.echo("")

  

# Алиас для команды list на случай ввода на русском ("лист")

@mdr.command(name='лист', hidden=True)

@click.pass_context

def list_equipment_ru(ctx):

    ctx.forward(list_equipment)

  
  

# ==========================================

# ПЕРЕИМЕНОВАННАЯ КОМАНДА НАВИГАЦИИ (tech)

# ==========================================

@mdr.command(

    name='tech',

    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)

)

@click.argument('tech_id', required=False)

@click.option('-p', '--page', type=str, help='Открыть конкретную страницу или подпапку (например: -p 23)')

@click.option('-c', '--chapter', type=str, help='Открыть главу/узел (например: -c hydr или -c engine)')

def tech_routing(tech_id, page, chapter):

    """Управление каталогом оборудования.

    Примеры использования:\n

    tech                   -> Открывает главную папку техники\n

    tech 785               -> Открывает папку техники 785\n

    tech 785 -p 23         -> Открывает страницу/папку 23 внутри 785\n

    tech 785 -c hydr       -> Открывает главу/узел hydr внутри 785

    """

    # 1. Если вызван просто `tech` без аргументов — открываем корень

    if not tech_id:

        open_path_in_explorer(BASE_DIR, "Открыта главная папка техники")

        return

  

    # 2. Строим базовый путь к модели (например, BASE_DIR / "785")

    target_dir = BASE_DIR / str(tech_id)

    msg = f"Открыт каталог техники [{tech_id}]"

  

    # 3. Если передан флаг страницы `-p` (например, 23)

    if page:

        target_dir = target_dir / str(page)

        msg += f" -> Страница/Папка [{page}]"

  

    # 4. Если передан флаг главы `-c` (например, hydr)

    elif chapter:

        target_dir = target_dir / str(chapter)

        msg += f" -> Глава/Узел [{chapter}]"

  

    # Открываем итоговый собранный путь

    open_path_in_explorer(target_dir, msg)

  
  

if __name__ == '__main__':

    mdr()
    
```