from flask import Blueprint, request, jsonify

from yacut import db
from yacut.short_links import URLMap
from . import APIValidator

bp = Blueprint('api', __name__, url_prefix='/api/id')


@bp.route('/', methods=['POST'])
def create_short_link():
    '''Создает короткую ссылку и добавляет в БД.'''
    data = request.get_json(force=True, silent=True)
    APIValidator.validate_create_request(data)
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@bp.route('/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    '''Отдает оригинальную ссылку по короткому идентификатору.'''
    url_map = URLMap.get_url_map_by_short_id(short_id)
    if url_map is None:
        from yacut.shared.error_handlers import InvalidAPIUsage
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.original}), 200