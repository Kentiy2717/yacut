from datetime import datetime

from yacut import db


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
            id=self.id,
            original=self.original,
            short=self.short,
            timestamp=self.timestamp,
        )

    def from_dict(self, data):
        '''Деериализация json в модель.'''
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])

    @classmethod
    def get_by_short(cls, short_link: str):
        '''Возвращает объект соответствующий короткой ссылке.'''
        # Пока не использую, но скорее всего будет нужна в файлах.
        return cls.query.filter_by(short=short_link).first()
