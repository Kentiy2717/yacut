from flask import (
    Response,
    abort,
    flash,
    Blueprint,
    render_template,
    redirect,
    url_for
)

from . import ShortLinkService, URLForm, URLMap

bp = Blueprint('short_links', __name__)
BASE_URL = 'http://localhost:5000/'


@bp.route('/', methods=['GET', 'POST'])
def index_view():
    '''Отображает форму для создания короткой ссылки и возвращает
    короткую ссылку при успешном добавлении в БД, либо выводит ошибку.'''
    form = URLForm()
    if form.validate_on_submit():
        url_map, error_message = ShortLinkService.create_short_url(
            original_url=form.original_link.data,
            custom_id=form.custom_id.data
        )
        if url_map is None:
            flash(error_message)
            return render_template('index.html', form=form)
        short_link = f'{BASE_URL}{url_map.short}'
        redirect_view = "short_links.redirect_by_original_link"
        flash('Ваша новая ссылка готова:')
        flash('<a href="'
              f'{url_for(redirect_view, short_link=url_map.short)}">'
              f'{short_link}</a></p>')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@bp.route('/<short_link>')
def redirect_by_original_link(short_link: str) -> Response:
    '''Перенаправляет на оригинальную ссылку по короткой.'''
    url_map = URLMap.get_by_short(short_link)
    if url_map is None:
        abort(404)
    return redirect(url_map.original)
