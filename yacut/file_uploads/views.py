from flask import Blueprint, request, render_template
from .services import YandexDiskService
from yacut.short_links import ShortLinkService
from yacut.file_uploads import FilesForm

bp = Blueprint('file_uploads', __name__, url_prefix='/files')


@bp.route('/', methods=['GET', 'POST'])
def upload_files():
    '''Инициализирует добавление файлов на ЯндексДиск и
    добавление записей в БД со ссылками на них.'''
    form = FilesForm()
    return render_template('upload_files.html', form=form)


@bp.route('/<short_code>')
def download_file():
    '''Перенаправляет на оригинальную ссылку по короткой и скачивает файл.'''
    pass
