import tkinter as tk
from urllib import parse

import validators

from application.db import Database
from application import utils

db = Database()


class TagCounter:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title('Tag Counter')
        self.app.geometry('700x350')
        self.app_text = tk.Text(self.app)
        self.input_field = None
        self.tags_dict = {}
        self.elapsed = ''

        # Start program
        self.build()

    def build(self):
        self.input_field = tk.StringVar(self.app)
        label = tk.Label(text="Введите адрес сайта")
        label.pack()

        entry = tk.Entry(fg="black", bg="white", width=50, textvariable=self.input_field)
        entry.insert(0, "Enter URL here")
        entry.pack()

        find_button = tk.Button(text="Найти теги!")
        find_button.pack()

        show_button = tk.Button(text="Показать из базы!")
        show_button.pack()

        entry.bind("<Return>", self.on_press)
        find_button.bind("<Button-1>", self.on_press)
        show_button.bind("<Button-1>", self.on_press)

        self.app_text.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(command=self.app_text.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)

        self.app_text.config(yscrollcommand=scroll.set)
        self.app_text.configure(state='disabled')

        self.app.mainloop()

    def on_press(self, button_object):
        tags_dict, elapsed = None, None
        url = utils.format_url(url=self.input_field.get())
        self.unlock_text_area_for_result()
        self.app_text.delete('1.0', tk.END)

        if validators.url(url):
            parsed_url = parse.urlparse(url)
            domain = parsed_url.netloc.replace('www.', '')

            if button_object.widget._name in ['!entry', '!button']:
                tags_dict, elapsed = utils.get_tag_count_with_timer(url, domain)

            elif button_object.widget._name == '!button2':
                tags_dict, elapsed = utils.get_from_db(domain=domain)

            if tags_dict:
                for tag in tags_dict:
                    self.app_text.insert(1.0, f'{tag}: {tags_dict[tag]} \n')
            else:
                self.app_text.insert(1.0, f'Данных по домену "{domain}" в базе нет')

            self.app_text.insert(1.0, f'Время запроса: {elapsed} \n')

        else:
            self.app_text.insert(1.0, f'Задан некорректный адрес {url} \n')

        self.app_text.configure(state='disabled')
        self.tags_dict = tags_dict
        self.elapsed = elapsed

    def unlock_text_area_for_result(self):
        text_win_conf = self.app_text.configure()
        if 'disabled' in text_win_conf['state']:
            self.app_text.configure(state='normal')
