from PIL import Image
from customtkinter import *
import json
import src.controller as controller

with open('config/settings.json', 'r', encoding='utf-8') as settings:
    setting = json.load(settings)

set_appearance_mode(setting["set_theme_mode"])


class ToDoListApp(CTk):
    def __init__(self):
        # Основные настройки окна
        CTk.__init__(self)
        # Устанавливаем ограничение на изменяемость размеров окна
        self.resizable(False, False)
        # Устанавливаем размеры окна
        self.geometry(f'{setting["win_width"]}x{setting["win_height"]}')
        # Устанавливаем название окна
        self.title(setting["title"])

        # Шапка приложения (картинка)
        # Создаём картинку для шапки
        self.top_image = CTkImage(light_image=Image.open(setting["top_image"]),
                                  size=(setting["win_width"], 70))
        # Создаём лейбл, на котором разместим картинку
        self.header = CTkLabel(master=self, image=self.top_image, text='')

        # Размещаем шапку
        self.header.pack(fill=X, side=TOP)

        # Текстовый заголовок
        self.header_text = CTkLabel(master=self, text=setting["header"]["text"],
                                    font=tuple(setting["header"]["font"]),
                                    text_color=setting["header"]["text_color"],
                                    fg_color=setting["header"]["fg_color"])

        # Размещаем текст заголовка на шапке
        self.header_text.place(relx=0.5, y=30, anchor=CENTER)

        # Иконка
        self.icon_image = CTkImage(light_image=Image.open(setting["icon_image"]),
                                   size=(29, 35))
        self.icon = CTkLabel(master=self,
                             image=self.icon_image,
                             text='',
                             fg_color='#42B4FB')

        # Размещаем иконку
        self.icon.place(x=setting["win_width"] // 2 + 150, y=30, anchor=CENTER)

        # Фрейм для поля ввода и кнопки "Добавить"
        self.todo_add_frame = CTkFrame(master=self,
                                       width=setting["win_width"],
                                       height=setting["entry_frame"]["height"],
                                       fg_color=setting["entry_frame"]["fg_color"])

        # Кнопка "Добавить"
        self.btn_image = CTkImage(light_image=Image.open(setting["add_button_img"]),
                                  size=(setting["entry_frame"]["height"] - 20, setting["entry_frame"]["height"] - 20))
        self.add_button = CTkButton(master=self.todo_add_frame,
                                    image=self.btn_image,
                                    corner_radius=setting["add_button"]["corner_radius"],
                                    text=setting["add_button"]["text"],
                                    font=tuple(setting["add_button"]["font"]),
                                    compound=setting["add_button"]["compound"], command=self.add)

        # Поле ввода нового дела
        self.todo_entry = CTkEntry(master=self.todo_add_frame,
                                   corner_radius=setting["todo_entry"]["corner_radius"],
                                   font=tuple(setting["todo_entry"]["font"]))

        # Поле для отображения всех имеющихся дел
        self.list = ToDoScrollableFrame(self, controller.current_data)

        # Кнопка "Удалить"
        self.delete_image = CTkImage(light_image=Image.open(setting["delete_button_img"]),
                                     size=(53, 53))
        self.delete_button = CTkButton(master=self,
                                       image=self.delete_image,
                                       text=setting["delete_button"]["text"],
                                       font=tuple(setting["delete_button"]["font"]),
                                       fg_color=setting["delete_button"]["fg_color"],
                                       hover_color=setting["delete_button"]["hover_color"], command=self.delete)

        self.delete_all_btn = CTkButton(master=self,
                                        text='Удалить всё',
                                        font=("Arial", 20, "bold"),
                                        fg_color='#956B11',
                                        command=self.delete_all)

        # Размещаем кнопку "Удалить выбранное" в самом низу интерфейса
        self.delete_button.pack(side=BOTTOM, pady=5)
        # Размещаем кнопку "Удалить всё"
        self.delete_all_btn.pack(side=BOTTOM)
        # Размещаем скролинг-фрейм для записей в самом низу интерфейса перед кнопкой "Удалить выбранное"
        self.list.pack(side=BOTTOM, padx=10, fill=X)

        # Размещаем фрейм для кнопки и поля ввода в самом низу интерфейса перед скролинг-фреймом
        self.todo_add_frame.pack(side=BOTTOM, pady=10)

        # Размещаем кнопку "Добавить" внутри фрейма
        self.add_button.place(anchor=NE, relheight=1.0, relwidth=0.3, x=self.todo_add_frame["width"], y=0)
        # Размещаем поле ввода внутри фрейма
        self.todo_entry.place(anchor=NW, relheight=1.0, relwidth=0.69, x=0, y=0)

    def add(self):
        # Читаем текст с поля ввода
        text = self.todo_entry.get()
        # Стираем содержимое поля ввода
        self.todo_entry.delete(0, END)
        # Добавляем новую запись в JSON-файл;
        # Передаём в функцию созданный скроллинг-фрейм (self.list) и текст новой записи (text)
        controller.add_todo(self.list, text)

    def delete(self):
        controller.delete_todo(self.list)

    def delete_all(self):
        controller.delete_all_todo(self.list)


class ToDoScrollableFrame(CTkScrollableFrame):
    def __init__(self, window, list_item):
        CTkScrollableFrame.__init__(self, master=window)
        self.configure(border_width=5, height=375)
        # Список для хранения экземпляров чекбоксов, размещённых на скроллинг-фрейме
        self.checkbox_list = []
        # Вызываем метод для отображения записей сразу же при создании экземпляра скроллинг-фрейма
        self.show_list(list_item)

    def show_list(self, item):
        # Обнуляем список, удаляя тем самым все чекбоксы из него, чтобы избежать дублирования
        self.checkbox_list = []
        # Методом items() бегаем по каждому элементу словаря записей дел,
        # разделяя каждый элемент на ключ и значение
        for key, value in item.items():
            # Создаём чекбокс с текстом вида "ключ записи: текст записи"
            checkbox = CTkCheckBox(self, text=f"{key}:  {value}")
            checkbox.pack(fill=X, pady=5)
            # Добавляем созданный чекбокс в список чекбоксов
            self.checkbox_list.append(checkbox)

# app = ToDoListApp()  # Создаём экземпляр класса нашего окна
# app.mainloop()  # Запускаем жизненный цикл для этого окна
