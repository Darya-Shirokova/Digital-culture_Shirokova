import os
import shutil
import logging
from typing import List, Optional


def setup_logging() -> logging.Logger:
    """
    Создание логгера который будет выводить сообщение про каждый файл который смог
    или не смог отсортировать, ошибки и тд
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def sort_files_by_extension(
        root_directory: str,
        ignore_hidden: bool = True
) -> Optional[List[str]]:
    """
    Сортирует файлы в заданном каталоге и его подкаталогах по их расширениям.

    Args:
        root_directory (str): Путь к каталогу в котором хотим сортировать файлы
        По умолчанию отсортирует файл с проектом (плохая идея)
        ignore_hidden (bool): Пропускать ли скрытые файлы/каталоги, по умолчанию True

    Returns:
        Optional[List[str]]: Список перемещенных файлов, или None, если произошла ошибка
    """
    logger = setup_logging()

    # Проверяем действителен ли путь к каталогу
    if not os.path.isdir(root_directory):
        logger.error(f"Invalid directory path: {root_directory}")
        return None

    moved_files = []

    try:
        # Проходит по всем каталогам и подкаталогам
        for current_dir, _, files in os.walk(root_directory):
            for filename in files:
                # Пропускаем скрытые файлы если так указано выше
                if ignore_hidden and filename.startswith('.'):
                    continue

                file_path = os.path.join(current_dir, filename)

                # Пропускаем если это не файл
                if not os.path.isfile(file_path):
                    continue

                # Получаем расширение файла
                file_extension = os.path.splitext(filename)[1][1:].lower()

                # Пропускаем файлы без расширений
                if not file_extension:
                    continue

                # Создаем папку с названием конкретного расширения
                target_dir = os.path.join(root_directory, file_extension)
                os.makedirs(target_dir, exist_ok=True)

                # Создаем путь к папке с подходящим названием
                target_path = os.path.join(target_dir, filename)

                # Обработка конфликта файлов с одинаковым названием (добавляем счетчик)
                counter = 1
                while os.path.exists(target_path):
                    name, ext = os.path.splitext(filename)
                    target_path = os.path.join(target_dir, f"{name}_{counter}{ext}")
                    counter += 1

                # Перемещаем файл
                shutil.move(file_path, target_path)
                moved_files.append(target_path)

                logger.info(f"Moved {file_path} to {target_path}")

        return moved_files

    except PermissionError:
        logger.error("Permission denied when accessing files or directories")
    except Exception as e:
        logger.error(f"Unexpected error during file sorting: {e}")

    return None


def main():
    """
    Функция Main
    """
    import sys

    # Выбирает какую директорию использовать, ту в которой лежит проект или указанную
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'

    logger = setup_logging()
    logger.info(f"Starting file sorting in: {directory}")

    result = sort_files_by_extension(directory)

    if result:
        logger.info(f"Successfully sorted {len(result)} files")
    else:
        logger.warning("No files were sorted")


if __name__ == "__main__":
    main()