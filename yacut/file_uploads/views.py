import asyncio

from flask import Blueprint, render_template
from .services import YandexDiskService
from yacut.short_links import BASE_URL, ShortLinkService
from yacut.file_uploads import FilesForm

bp = Blueprint('file_uploads', __name__, url_prefix='/files')


@bp.route('/', methods=['GET', 'POST'])
async def upload_files():
    '''Инициализирует ассинхронное добавление файлов на ЯндексДиск и
    добавление записей в БД со ссылками на них.'''
    form = FilesForm()
    files_info = []
    if form.validate_on_submit():
        files = form.files.data
        tasks = [
            YandexDiskService.upload_file_to_yadisk(file) for file in files
        ]
        data = await asyncio.gather(*tasks)
        for url, file_name in data:
            short_id = ShortLinkService.create_short_url(url)[0].short
            short_link = f'{BASE_URL}{short_id}'
            files_info.append({'file_name': file_name,
                               'short_link': short_link})
    context = {
        'form': form,
        'files_info': files_info
    }
    return render_template('upload_files.html', context=context)


@bp.route('/<short_code>')
def download_file():
    '''Перенаправляет на оригинальную ссылку по короткой и скачивает файл.'''
    pass
