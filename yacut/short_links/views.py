from flask import (
    Response,
    flash,
    Blueprint,
    render_template,
    redirect,
    request,
    url_for
)

from . import BASE_URL, ShortLinkService, URLForm, URLMap

bp = Blueprint('short_links', __name__)


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


@bp.route('/get_all_links')
def get_all_links():
    '''Отображает все записи в БД с пагинацией.'''
    page = request.args.get('page', 1, type=int)
    per_page = 8

    pagination = URLMap.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        'all_links.html',
        pagination=pagination,
        url_map=pagination.items
    )


@bp.route('/delete/<short_id>', methods=['GET', 'DELETE'])
def delete_url_map_by_short(short_id: str):
    '''Удаляет запись из БД по короткому идентификатору.'''
    message = ShortLinkService.delete_url_map_by_short(short_id)
    flash(message)
    return redirect(url_for('short_links.get_all_links'))


@bp.route('/<short_link>')
def redirect_by_original_link(short_link: str) -> Response:
    '''Перенаправляет на оригинальную ссылку по короткой.'''
    short_id = short_link.split('/')[-1]
    return redirect(URLMap.get_original_link_by_short(short_id))
