import json


class JsonBase:
    def __init__(self, path):
        # Атрибут для хранения пути к JSON-файлу
        self.file = path

    def load_data(self) -> dict:
        with open(self.file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def add_new_data(self, new_data, current_data):
        current_data.update(new_data)

        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(current_data, f, ensure_ascii=False)

    def delete_todo(self, current_data, del_keys):
        for el in del_keys:
            del current_data[el]

        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(current_data, f, ensure_ascii=False)

