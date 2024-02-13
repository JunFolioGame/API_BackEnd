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
            filename = f"{filename[:-4]}_{int(time.time())}{filename[-4:]}"  # якщо папка вже існує, то напевне там є малюнки

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
            os.remove(photo_url)
            print("Зображення видалено!")
        except FileNotFoundError:
            print("Зображення для видалення не знайдено!")
