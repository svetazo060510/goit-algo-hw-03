# Bибираємо 7 різних кольорів для дисків (для n до 7)
COLORS = [
    "\033[94m", # Blue
    "\033[92m", # Green
    "\033[93m", # Yellow
    "\033[96m", # Cyan
    "\033[95m", # Magenta
    "\033[91m", # Red
    "\033[35m"  # Purple
]
RESET = "\033[0m" # Код для скидання кольору

def get_disk_color(disk_size):
    """Повертає кольоровий код для диска на основі його розміру."""
    # Диски нумеруються від 1 до N. Використовуємо розмір як індекс.
    if disk_size > 0 and disk_size <= len(COLORS):
        # Припускаємо, що диск 1 = COLORS[0], диск 2 = COLORS[1], і т.д.
        return COLORS[disk_size - 1]
    return RESET # Якщо диск надто великий або 0, не фарбуємо

def print_hanoi_state(state: dict, n_disks: int):
    """
    Візуалізує поточний стан Ханойської вежі у текстовому вигляді з кольорами.
    Диски представлені символами '=' та їхнім розміром.
    """
    print(RESET + "=" * 50)
    
    # Визначаємо максимальну ширину, щоб відцентрувати відображення
    max_disk_width = n_disks * 2 + 3 
    
    # Створюємо кожну "лінію" вежі, від найвищої (верхньої) до найнижчої (основи)
    # n_disks - це висота вежі, ми ітеруємо від n_disks до 1
    for i in range(n_disks, 0, -1):
        line = ""
        for peg in ['A', 'B', 'C']:
            # Індекс диска на поточній висоті (i) у стеку
            # Потрібно відняти n_disks - i, оскільки ми ітеруємо зверху вниз
            disk_index = len(state[peg]) - (n_disks - i) - 1
            
            if disk_index >= 0:
                # Якщо на цій висоті є диск
                disk_size = state[peg][disk_index]
                # --- Додавання Кольору ---
                color_code = get_disk_color(disk_size)
                # Створення рядка, що імітує диск (наприклад, '=3=' для диска 3)
                disk_str = f"{color_code}{'=' * disk_size}{disk_size}{'=' * disk_size}{RESET}"
                # Додавання пробілів для центрування на стрижні
                line += disk_str.center(max_disk_width + len(color_code) + len(RESET)) + " "
            else:
                # Якщо на цій висоті немає диска, малюємо порожній стрижень (|)
                line += "|".center(max_disk_width) + " "
        print(line)
        
    # Друк основи та назв стрижнів
    print("-" * (max_disk_width + 1) * 3)
    print(
        "A".center(max_disk_width) + " " + 
        "B".center(max_disk_width) + " " + 
        "C".center(max_disk_width)
    )
    print("=" * 50)


def solve_hanoi(n: int, source: str, destination: str, auxiliary: str, current_state: dict, n_disks: int):
    """
    Рекурсивна функція для переміщення N дисків з джерела на призначення.
    """
    # 1. Базовий Випадок: Зупинка рекурсії
    if n == 0:
        return

    # 2. Крок 1: Перемістити N-1 дисків з Source на Auxiliary
    solve_hanoi(n - 1, source, auxiliary, destination, current_state, n_disks)

    # 3. Крок 2: Перемістити N-й (найбільший) диск з Source на Destination (Один крок)
    
    # Видаляємо диск з верхівки джерела (pop() імітує Стек)
    disk = current_state[source].pop() 
    
    # Додаємо диск на верхівку призначення
    current_state[destination].append(disk)
    
    # Логування кроку
    print(f"Крок: Перемістити диск {disk} з {source} на {destination}")
    print_hanoi_state(current_state, n_disks)
    
    # 4. Крок 3: Перемістити N-1 дисків з Auxiliary на Destination
    solve_hanoi(n - 1, auxiliary, destination, source, current_state, n_disks)


def run_hanoi_towers(n_disks: int):
    """Ініціалізує та запускає процес розв'язання головоломки."""
    if n_disks <= 0:
        print("Кількість дисків має бути більше 0.")
        return

    # Ініціалізація початкового стану: [N, N-1, ..., 1] на стрижні 'A'
    initial_disks = list(range(n_disks, 0, -1)) 
    state = {
        'A': initial_disks,
        'B': [],
        'C': []
    }

    print(f"------------ Ханойська Вежа: {n_disks} дисків ------------")
    print(f"Початковий стан: {state}")
    print_hanoi_state(state, n_disks)
    
    # Запуск рекурсії
    solve_hanoi(n_disks, 'A', 'C', 'B', state, n_disks)
    
    print("--------------------------------------------------")
    print(f"Кінцевий стан: {state}")
    print(f"Загальна кількість кроків: {2**n_disks - 1}")


# --- ЗАПУСК ПРОГРАМИ ---
n_input = 3 # Встановлюємо 3 диски для перевірки прикладу з завдання
run_hanoi_towers(n_input)
