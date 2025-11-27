import turtle


"""
    Малює одну сторону фракталу Коха рекурсивно.
    t: об'єкт turtle.Turtle
    order: рівень рекурсії
    size: довжина поточного сегмента
"""
def koch_side(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        # Кожен сегмент розділяється на 4 менші сегменти
        # Довжина кожного нового сегмента становить size / 3
        new_size = size / 3.0
        
        # 1. Перша третина
        koch_side(t, order - 1, new_size)
        t.left(60)
        # 2. Друга третина (вершина)
        koch_side(t, order - 1, new_size)
        t.right(120) # Зміна напрямку для створення "шипа"
        # 3. Третя третина
        koch_side(t, order - 1, new_size)
        t.left(60)
        # 4. Четверта третина
        koch_side(t, order - 1, new_size)

def draw_koch_snowflake(t, order, size):
    """
    Малює цілу сніжинку Коха, викликаючи koch_side тричі.
    t: об'єкт turtle.Turtle
    order: рівень рекурсії
    size: довжина сторони початкового трикутника
    """
    for _ in range(3):
        koch_side(t, order, size)
        t.right(120) # Поворот для малювання наступної сторони трикутника

# --- Основна частина програми ---
if __name__ == "__main__":
    # Отримання рівня рекурсії від користувача
    try:
        depth = int(input("Введіть рівень рекурсії для сніжинки Коха (наприклад, 0-4): "))
        if depth < 0:
            raise ValueError
    except ValueError:
        print("Будь ласка, введіть ціле невід'ємне число.")
        exit()

    # Налаштування Turtle
    screen = turtle.Screen()
    screen.setup(width=600, height=600)
    screen.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed("fastest") # Максимальна швидкість малювання
    t.penup() # Підняти перо, щоб переміститися без малювання
    
    # Початкова позиція для малювання (центр екрану)
    initial_size = 200 # Довжина початкової сторони трикутника
    t.goto(-initial_size / 2, initial_size / (2 * (3**0.5))) # Розміщення для симетричного малювання
    t.pendown() # Опустити перо, щоб почати малювати
    
    t.pencolor("blue") # Колір фракталу
    t.pensize(2) # Товщина лінії

    # Малювання сніжинки Коха
    draw_koch_snowflake(t, depth, initial_size)

    t.hideturtle() # Приховати черепашку після завершення малювання
    screen.mainloop() # Залишає вікно відкритим до закриття користувачем