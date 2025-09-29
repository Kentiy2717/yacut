from flask import Blueprint, request, jsonify, render_template
# from .services import YandexDiskService
from yacut.short_links import ShortLinkService

bp = Blueprint('file_uploads', __name__, url_prefix='/files')


@bp.route('/', methods=['GET', 'POST'])
def upload_files():
    '''Инициализирует добавление файлов на ЯндексДиск и
    добавление записей в БД со ссылками на них.'''
    pass


@bp.route('/<short_code>')
def download_file():
    '''Перенаправляет на оригинальную ссылку по короткой и скачивает файл.'''
    pass
