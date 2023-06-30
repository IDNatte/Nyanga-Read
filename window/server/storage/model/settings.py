from sqlalchemy_serializer import SerializerMixin

from server.helper.constant.constant import DB


class Setting(DB.Model, SerializerMixin):
    __tablename__ = "nyanga_setting"

    id = DB.Column(DB.Integer, primary_key=True)
    setting_type = DB.Column(DB.String(50), nullable=False, unique=True)
    value = DB.Column(DB.String(200), nullable=False)
