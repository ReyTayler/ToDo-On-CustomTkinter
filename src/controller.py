import time
from src.model import JsonBase

js_base = JsonBase("config/list_do.json")
current_data = js_base.load_data()


def add_todo(todo_frame, text):
    global current_data

    # Читаем текущее время
    time_create = time.localtime()

    # Создаём новую запись как элемент словаря
    new_data = {time.strftime("%d/%m/%Y, %H:%M:%S", time_create): text}
    # Пример {"29/12/2024, 12:30:00": "Пойти гулять"}

    # Добавляем новую запись в файл
    js_base.add_new_data(new_data, current_data)

    # Стираем список всех дел с фрейма
    for widget in todo_frame.pack_slaves():
        widget.pack_forget()

    current_data = js_base.load_data()
    # Обновляем список всех дел в фрейме
    todo_frame.show_list(current_data)


def delete_todo(todo_frame):
    global current_data

    # Список ключей записей, который удалим
    keys = []
    # Пробегаемся по каждому чекбоксу в скролингфрейме
    for check in todo_frame.checkbox_list:
        # Проверяем, чтоб чекбокс был выделен
        if check.get() == 1:
            # Из чекбокса выделяем первые 20 символов (это дата и время)
            del_key = check.cget("text")[:20]
            # Добавляем полученную строку символов в список ключей
            keys.append(del_key)

    # Удаляем все выбранные записи дел
    js_base.delete_todo(current_data, keys)

    # Стираем список всех дел с фрейма
    for widget in todo_frame.pack_slaves():
        widget.pack_forget()

    current_data = js_base.load_data()
    # Обновляем список всех дел в фрейме
    todo_frame.show_list(current_data)
