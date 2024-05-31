class NyangaTemporaryAttr:
    __manga_id = None
    __my_manga = None

    @classmethod
    def set_openbookmark(cls, value):
        cls.__my_manga = value

    @classmethod
    def get_openbookmark(cls):
        return cls.__my_manga

    @classmethod
    def set_openmanga_id(cls, value):
        cls.__manga_id = value

    @classmethod
    def get_openmanga_id(cls):
        return cls.__manga_id
