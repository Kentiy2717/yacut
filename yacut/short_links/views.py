from flask import (
    Response,
    flash,
    Blueprint,
    render_template,
    redirect
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
        flash('Ваша новая ссылка готова:')
        flash(f'<a href="{short_link}">{short_link}</a></p>')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@bp.route('/<short_link>')
def redirect_by_original_link(short_link: str) -> Response:
    '''Перенаправляет на оригинальную ссылку по короткой.'''
    short_id = short_link.split('/')[-1]
    return redirect(URLMap.get_original_link_by_short(short_id))
