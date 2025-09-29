from flask_wtf import FlaskForm
from flask_wtf.file import DataRequired, MultipleFileField
from wtforms import SubmitField


class FilesForm(FlaskForm):
    files = MultipleFileField(
        'Файл не выбран',
        validators=[DataRequired(message='Файл не выбран')]
    )
    submit = SubmitField('Загрузить')
