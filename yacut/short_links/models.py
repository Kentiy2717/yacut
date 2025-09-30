from datetime import datetime

from flask import abort

from yacut import db
from . import BASE_URL


class URLMap(db.Model):
    '''Модель для хранения оригинальных ссылок и
    соответствующих им коротких'''

    __tablename__ = 'url_maps'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    original = db.Column(
        db.String(2048),
        nullable=False
    )
    short = db.Column(
        db.String(16),
        unique=True,
        index=True
    )
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        '''Сериализация модели в словарь.'''
        return dict(
            url=self.original,
            short_link=f'{BASE_URL}{self.short}'
        )

    def from_dict(self, data):
        '''Десериализация json в модель.'''
        self.original = data['url']
        if 'custom_id' in data and data['custom_id']:
            self.short = data['custom_id']
        else:
            from .services import ShortLinkService
            self.short = ShortLinkService.generate_unique_short_id()

    @classmethod
    def get_url_map_by_short_id(cls, short_id: str):
        '''Возвращает объект соответствующий короткому идентификатору.'''
        return cls.query.filter_by(short=short_id).first()

    @classmethod
    def get_original_link_by_short(cls, short_id: str) -> str:
        '''Возвращает оригинальную ссылку соответствующую
        короткому идентификатору.'''
        url_map = cls.query.filter_by(short=short_id).first()
        if url_map is None:
            abort(404)
        return url_map.original
