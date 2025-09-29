from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    URLField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp
)


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 2048)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16),
            Optional(),
            Regexp(
                r'^[a-zA-Z0-9]*$',
                message='Можно использовать только латинские буквы и цифры'
            )
        ]
    )
    submit = SubmitField('Создать')
