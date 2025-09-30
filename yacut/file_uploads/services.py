import os
import urllib
import aiohttp

from aiohttp import FormData
from dotenv import load_dotenv

API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'

load_dotenv()
DISK_TOKEN = os.environ.get('DISK_TOKEN')
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}


class YandexDiskService:

    @staticmethod
    async def _get_url_for_upload_file(file_name: str) -> str:
        '''Асинхронно возвращает адрес ссылки для загрузки файла.'''

        async with aiohttp.ClientSession() as session:
            payload = {
                'path': f'app:/{file_name}',
                'overwrite': 'True'
            }

            async with session.get(url=REQUEST_UPLOAD_URL,
                                   params=payload,
                                   headers=AUTH_HEADERS) as response:
                data = await response.json()
                return data['href']

    @staticmethod
    async def _get_original_link_on_file(location: str) -> str:
        '''Асинхронно загружает файл на ЯндексДиск и возвращает его имя.'''

        async with aiohttp.ClientSession() as session:
            params = {
                'path': location,
                'fields': 'public_url'
            }

            async with session.get(url=DOWNLOAD_LINK_URL,
                                   params=params,
                                   headers=AUTH_HEADERS) as response:
                data = await response.json()
                return data['href']

    @staticmethod
    async def upload_file_to_yadisk(file) -> list:
        '''Асинхронно загружает файл на ЯндексДиск и возвращает его имя.'''

        upload_url = await YandexDiskService._get_url_for_upload_file(
            file.filename
        )

        file.stream.seek(0)

        async with aiohttp.ClientSession() as session:
            data = FormData()
            data.add_field('file',
                           file.stream.read(),
                           filename=file.filename,
                           content_type=file.content_type)

            async with session.put(upload_url,
                                   data=data) as response:
                if response.status in [201, 202]:
                    # Если файл успешно загружен,
                    # то получем ссылку на его скачивание по пути.
                    location = response.headers['Location']
                    location = urllib.parse.unquote(location)
                    location = location.replace('/disk', '')
                    url = await YandexDiskService._get_original_link_on_file(
                        location
                    )
                    return url, file.filename
                else:
                    return (
                        f'Ошибка загрузки {file.filename}: {response.status}'
                    )
