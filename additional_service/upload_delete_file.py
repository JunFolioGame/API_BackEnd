import os
import time

from additional_service.services_interfaces import AdditionalServiceInterface


class AdditionalService(AdditionalServiceInterface):
    def upload_file_to_s3(self, group_name: str, object_name: str, bytesio_file) -> str:
        # Генеруємо ім'я файлу для зображення
        filename = f"{object_name}_{bytesio_file.name}"
        # Створення директорії для збереження зображень (якщо вона ще не існує)
        image_directory = f"./cloud_img/{group_name}"
        if not os.path.exists(image_directory):
            os.makedirs(image_directory)
        image_directory += f"/{object_name}"
        if not os.path.exists(image_directory):
            os.makedirs(image_directory)
        else:
            # якщо папка вже існує, то напевне там є малюнки
            if filename[-4:] == "jpeg":
                filename = f"{filename[:-5]}_{int(time.time())}{filename[-5:]}"
            else:
                filename = f"{filename[:-4]}_{int(time.time())}{filename[-4:]}"

        # Завантажуємо зображення
        raw_file = bytesio_file.file
        # Генеруємо ім'я файлу для зображення
        image_filename = f"{filename}"
        # Шлях до зображення
        image_path = os.path.join(image_directory, image_filename)
        # Зберігаємо зображення
        with open(image_path, "wb") as image_file:
            image_file.write(raw_file.read())
        print(f"Зображення збережено: {image_path}")
        return image_path

    def delete_file_from_s3(self, photo_url: str) -> None:
        try:
            if os.path.isfile(photo_url):
                os.remove(photo_url)
                print(f"Файл {photo_url} видалено!")
                folder_path = os.path.dirname(photo_url)
                while folder_path != "" and folder_path != "'./cloud_img'":
                    if not os.listdir(folder_path):
                        os.rmdir(folder_path)
                        print(f"Папка {folder_path} видалена!")
                        folder_path = os.path.dirname(folder_path)
                    else:
                        break
            else:
                print("Файл або папку для видалення не знайдено!")
        except FileNotFoundError:
            print("Файл або папку для видалення не знайдено!")
