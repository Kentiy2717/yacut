import re

from yacut.short_links import URLMap


class APIValidator:

    @staticmethod
    def validate_create_request(data):
        '''Валидация запроса на создание короткой ссылки.'''

        from yacut.error_handlers import InvalidAPIUsage

        if not data:
            raise InvalidAPIUsage('Отсутствует тело запроса')
        if 'custom_id' in data and data['custom_id']:
            if APIValidator._validate_custom_id(
                data['custom_id']
            ):
                raise InvalidAPIUsage(
                    'Указано недопустимое имя для короткой ссылки'
                )
            if URLMap.get_url_map_by_short(short_id=data['custom_id']):
                raise InvalidAPIUsage(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
        if 'url' not in data:
            raise InvalidAPIUsage('"url" является обязательным полем!')
        return URLMap.from_dict

    @staticmethod
    def _validate_custom_id(custom_id: str) -> str | None:
        '''Валидация уникального короткого идентификатора.'''

        if len(custom_id) > 16:
            return 'Короткий идентификатор не более 16 символов'
        if not re.match(r'^[a-zA-Z0-9]+$', custom_id):
            return 'Разрешены только латинские буквы и цифры'
        return None