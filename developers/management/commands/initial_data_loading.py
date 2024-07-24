import os
import shutil
from io import BytesIO
import requests
import json
from django.core.management.base import BaseCommand
from django.test import RequestFactory

from api.v1.views.catalog import APICreateGameInfoView
from api.v1.views.developers import APICreateAllDevelopersView
from developers.models import Developer
from catalog.models import GameInfo


class Command(BaseCommand):
    help = "Load initial data"

    def handle(self, *args, **kwargs):  # noqa
        def delete_all_in_directory(directory: str) -> None:
            try:
                if os.path.exists(directory) and os.path.isdir(directory):
                    shutil.rmtree(directory)
                    print(
                        f"Папка {directory} разом з усіма вкладеними файлами та папками видалена!"
                    )
                    os.makedirs(directory)
                else:
                    print("Зазначена папка не знайдена!")
            except Exception as e:
                print(f"Сталася помилка при видаленні папки: {e}")

        def delete_all_images_for_developers():
            delete_all_in_directory("../cloud_img/developers")

        def delete_all_images_for_catalog():
            delete_all_in_directory("../cloud_img/game_info")

        def delete_all_images_for_gallery():
            delete_all_in_directory("../cloud_img/gallery")

        def get_json_from_url(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                raise Exception(f"Сталася помилка при завантаженні файлу: {e}")
            except json.JSONDecodeError as e:
                raise Exception(f"Сталася помилка при декодуванні JSON: {e}")

        def get_photo_from_url(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                image_file = BytesIO(response.content)
                image_file.name = url.split("/")[-1]
                return {"photo_jpeg": (image_file.name, image_file, "image/jpeg")}
            except requests.exceptions.RequestException as e:
                raise Exception(f"Сталася помилка при завантаженні файлу photo: {e}")

        data_developers_json = os.getenv(
            "DATA_DEVELOPERS_JSON",
            "data_developers.json",
        )
        data_catalog_json = os.getenv("DATA_CATALOG_JSON", "data_catalog.json")
        url_initial_data = os.getenv("URL_INITIAL_DATA", "")
        system_icon_description = os.getenv("IGNORE_GAME_INFO", ".")

        factory = RequestFactory()

        if not Developer.objects.exists():
            delete_all_images_for_developers()
            developers_data = get_json_from_url(data_developers_json)

            for developer in developers_data:
                file = get_photo_from_url(url_initial_data + developer["photo"])

                developer_data = {
                    "name_ua": developer["name_ua"],
                    "name_en": developer["name_en"],
                    "role_ua": developer["role_ua"],
                    "is_active": True,
                }
                developer_data.update(file)
                # response = requests.post(api_url_developer, data=post_data, files=files)

                request = factory.post(
                    "/api/v1/developer/", data=developer_data, format="multipart"
                )

                # Виклик методу post безпосередньо
                response = APICreateAllDevelopersView.as_view()(request)

                if response.status_code == 201:
                    print(f"Розробника {developer['name_en']} успішно створено.")
                else:
                    print(
                        f"Не вдалося створити розробника {developer['name_en']}. Код статусу: {response.status_code}."
                        f"Повідомлення про помилку: {response.status_text}"
                    )
                    break
            print("Всі розробники були оброблені.")

        if not GameInfo.objects.exists():
            delete_all_images_for_catalog()
            delete_all_images_for_gallery()

            data_catalog = get_json_from_url(data_catalog_json)

            for game_info in data_catalog:
                game_info_data = {
                    "name_ua": game_info["name_ua"],
                    "name_en": game_info["name_en"],
                    "description_ua": game_info["description_ua"],
                    "description_en": game_info["description_en"],
                    "members": game_info["members"],
                    "is_team": game_info.get("team", False),
                    "is_active": game_info.get("is_active", False),
                }
                files = get_photo_from_url(url_initial_data + game_info["photo"])
                game_info_data.update(files)
                request = factory.post(
                    "/api/v1/game_info/", data=game_info_data, format="multipart"
                )
                # Виклик методу post безпосередньо
                response = APICreateGameInfoView.as_view()(request)

                # response = requests.post(api_url_game_info, data=post_data, files=files)

                if response.status_code == 201:
                    print(
                        f"Інформація про гру {game_info['name_en']} успішно створена."
                    )
                    if game_info["description_ua"] == system_icon_description:
                        res = GameInfo.objects.filter(
                            description_ua=system_icon_description
                        ).delete()
                        print("Видаляємо екземпляр системного значка з БД. ", res)
                        # Видаляємо інформацію з БД для файлів зображень системного значка
                else:
                    print(
                        f"Не вдалося створити інформацію про гру {game_info['name_en']}. "
                        f"Код статусу: {response.status_code}"
                    )

            print("Всі екземпляри інформації про гру були оброблені.")
