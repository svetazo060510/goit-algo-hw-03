import os
import shutil
import argparse
from pathlib import Path

# =================================================================
# 0. ANSI КОДИ КОЛЬОРІВ
# =================================================================

# Кольори для терміналу
COLOR_SUCCESS = "\033[92m" # Green - Успіх
COLOR_INFO = "\033[94m"    # Blue - Інформація
COLOR_WARNING = "\033[93m"  # Yellow - Попередження
COLOR_ERROR = "\033[91m"    # Red - Помилка
COLOR_RESET = "\033[0m"     # Скидання кольору

# =================================================================
# 1. ФУНКЦІЯ РЕКУРСИВНОГО СОРТУВАННЯ ТА КОПІЮВАННЯ
# =================================================================

def recursive_file_sorter(source_path, output_dir):
    """
    Рекурсивно сканує вихідну директорію, копіює файли до директорії 
    призначення та сортує їх у піддиректорії за розширенням.

    :param source_path: Поточний шлях для сканування (початково - вихідна директорія).
    :param output_dir: Шлях до директорії призначення (dist).
    """
    try:
        # 1. Перебір елементів у поточній директорії
        for item in source_path.iterdir():
            
            # 2. Якщо елемент є директорією -> РЕКУРСИВНИЙ ВИКЛИК
            if item.is_dir():
                # Логування рекурсивного входу
                print(f"{COLOR_INFO} Вхід до директорії: {item.name}{COLOR_RESET}")
                # Виклик функції самої себе для піддиректорії
                recursive_file_sorter(item, output_dir)
            
            # 3. Якщо елемент є файлом -> КОПІЮВАННЯ ТА СОРТУВАННЯ
            elif item.is_file():
                # Отримання розширення файлу (наприклад, '.jpg' або 'txt')
                # Якщо розширення відсутнє, використовуємо "no_extension"
                extension = item.suffix.strip('.') 
                if not extension:
                    extension = "no_extension"
                
                # Створення шляху до піддиректорії в директорії призначення
                # (наприклад, dist/jpg, dist/txt)
                target_subdirectory = output_dir / extension
                
                # Створення піддиректорії, якщо вона ще не існує
                target_subdirectory.mkdir(parents=True, exist_ok=True)
                
                # Копіювання файлу: shutil.copy2 зберігає метадані
                try:
                    shutil.copy2(item, target_subdirectory)
                    print(f"{COLOR_SUCCESS} Копіювання: {item.name} -> {target_subdirectory}{COLOR_RESET}")
                except Exception as e:
                    print(f"{COLOR_ERROR} Помилка копіювання файлу {item.name}: {e}{COLOR_RESET}")

    except PermissionError:
        print(f"{COLOR_ERROR} Помилка: Недостатньо прав для доступу до директорії {source_path}{COLOR_RESET}")
    except Exception as e:
        print(f"{COLOR_WARNING} Виникла несподівана помилка при обробці {source_path}: {e}{COLOR_RESET}")


# =================================================================
# 2. ОБРОБКА АРГУМЕНТІВ КОМАНДНОГО РЯДКА ТА ЗАПУСК
# =================================================================

def main():
    """Парсинг аргументів та запуск основного процесу сортування."""
    parser = argparse.ArgumentParser(description="Рекурсивне сортування файлів за розширенням.")
    
    # Обов'язковий аргумент: шлях до вихідної директорії
    parser.add_argument("source_dir", 
                        type=str, 
                        help="Шлях до вихідної директорії для сканування.")
    
    # Необов'язковий аргумент: шлях до директорії призначення
    parser.add_argument("dest_dir", 
                        type=str, 
                        nargs='?', # Аргумент може бути відсутнім
                        default="dist", # Значення за замовчуванням
                        help="Шлях до директорії призначення. За замовчуванням 'dist'.")

    args = parser.parse_args()
    
    # Використовуємо pathlib.Path для крос-платформної роботи зі шляхами
    source_path = Path(args.source_dir)
    output_dir = Path(args.dest_dir)

    # Перевірка існування вихідної директорії
    if not source_path.is_dir():
        print(f"{COLOR_ERROR}Помилка: Вихідна директорія '{source_path}' не існує.{COLOR_RESET}")
        return

    # Створення директорії призначення, якщо вона ще не існує
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"{COLOR_ERROR}Помилка при створенні директорії призначення '{output_dir}': {e}{COLOR_RESET}")
        return

    print(f"\n{COLOR_INFO}-------- Запуск сортування --------{COLOR_RESET}")
    print(f"Вихідна директорія: {COLOR_INFO}{source_path.resolve()}{COLOR_RESET}")
    print(f"Директорія призначення: {COLOR_INFO}{output_dir.resolve()}{COLOR_RESET}")
    print("-" * 35)
    
    # Запуск рекурсивного процесу
    recursive_file_sorter(source_path, output_dir)
    
    print("-" * 35)
    print(f"{COLOR_SUCCESS}------ Сортування завершено! ------{COLOR_RESET}\n")

if __name__ == "__main__":
    main()

# from the folder: python3 sorter.py source_test