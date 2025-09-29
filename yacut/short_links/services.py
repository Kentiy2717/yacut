import secrets
import string
import logging

from sqlite3 import IntegrityError

from yacut import db
from . import URLMap

logger = logging.getLogger(__name__)


class ShortLinkService:

    @staticmethod
    def create_short_url(original_url: str,
                         custom_id: str = None) -> tuple[URLMap | None,
                                                         str | None]:
        '''Генерирует уникальную короткую ссылку,
        проверяет, что ссылки, переданной пользователем, еще нет в БД
        и делает запись в БД.
        Возвращает созданный объект и сообщение об ошибке.
        '''

        if custom_id:
            if URLMap.query.filter_by(short=custom_id).first():
                return None, 'Такое мнение уже было оставлено ранее!'
            short_id = custom_id
        else:
            short_id = ShortLinkService.generate_unique_short_id()

        try:
            url_map = URLMap(original=original_url, short=short_id)
            db.session.add(url_map)
            db.session.commit()
            return url_map, None
        except IntegrityError:
            db.session.rollback()
            return None, 'Ошибка при создании ссылки'

    @staticmethod
    def generate_unique_short_id(length: int = 6) -> str:
        '''Генерирует уникальный short_id
        с защитой от крайних случаев (100 попыток).'''

        alphabet = string.ascii_letters + string.digits
        MAX_ATTEMPTS_FOR_GENERATE_UNIQUE_SHORT_ID = 100
        for _ in range(MAX_ATTEMPTS_FOR_GENERATE_UNIQUE_SHORT_ID):
            short_id = ''.join(secrets.choice(alphabet) for _ in range(length))
            if not URLMap.query.filter_by(short=short_id).first():
                return short_id

        # Если не удалось за разумное количество попыток
        logger.error('Не удалось сгенерировать уникальный short_id '
                     f'за {MAX_ATTEMPTS_FOR_GENERATE_UNIQUE_SHORT_ID} попыток')
        raise RuntimeError('Не удалось создать уникальную короткую ссылку')
