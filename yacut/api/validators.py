import re

from yacut.short_links import URLMap


# Надо еще поправить.
class APIValidator:

    @staticmethod
    def validate_create_request(data):
        '''Валидация запроса на создание короткой ссылки.'''
        errors = []

        if not data:
            return ['Отсутствует тело запроса']
        if 'url' not in data:
            return ['"url" является обязательным полем!']

        if 'custom_id' in data and data['custom_id']:
            custom_id_error = APIValidator._validate_custom_id(
                data['custom_id']
            )
            if custom_id_error:
                errors.append('Указано недопустимое имя для короткой ссылки')

        return errors

    @staticmethod
    def _validate_custom_id(custom_id: str) -> str | None:
        '''Валидация уникального короткого идентификатора.'''
        if URLMap.query.filter_by(short=custom_id).first():
            return 'Предложенный вариант короткой ссылки уже существует.'
        if len(custom_id) > 16:
            return 'Короткий идентификатор не более 16 символов'
        if not re.match(r'^[a-zA-Z0-9]+$', custom_id):
            return 'Разрешены только латинские буквы и цифры'
        return None