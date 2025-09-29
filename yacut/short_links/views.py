from flask import (
    abort,
    flash,
    Blueprint,
    request,
    render_template,
    redirect
)
from . import ShortLinkService, URLForm

bp = Blueprint('short_links', __name__)
BASE_URL = 'http://localhost:5000/'


@bp.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        url_map, error_message = ShortLinkService.create_short_url(
            original_url=form.original_link,
            custom_id=form.custom_id
        )
        if url_map is None:
            flash(error_message)
            return render_template('index.html', form=form)
        short_link = f'{BASE_URL}{url_map.short}'
        flash('Ваша новая ссылка готова:'
              f'<a href="{short_link}">{short_link}</a></p>')
        return render_template('index.html', form=form)
    return render_template('index.html', None)