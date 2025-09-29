from flask import Blueprint, request, jsonify
from yacut.short_links import ShortLinkService

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/id/', methods=['POST'])
def create_short_link():
    pass


@bp.route('/id/<short_id>/', methods=['GET'])
def get_original_link(short_id):
    '''Отдает оригинальную ссылку по короткому идентификатору.'''
    pass