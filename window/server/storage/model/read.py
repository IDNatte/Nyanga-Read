from sqlalchemy_serializer import SerializerMixin

from server.helper.database.id_rand import random_id_generator
from server.helper.constant.constant import DB

import datetime


class Read(DB.Model, SerializerMixin):
    __tablename__ = "nyanga_read_manga"

    id = DB.Column(
        DB.String(200), primary_key=True, nullable=False, default=random_id_generator
    )
    manga = DB.Column(DB.String(200), nullable=False)
    chapter = DB.Column(DB.String(200), nullable=False)
    chapter_number = DB.Column(DB.String(50), nullable=False)
    readed_at = DB.Column(DB.DateTime, default=datetime.datetime.utcnow)
