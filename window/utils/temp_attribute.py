class NyangaTemporaryAttr:
    __manga_id = None

    @classmethod
    def set_openmanga_id(cls, value):
        cls.__manga_id = value

    @classmethod
    def get_openmanga_id(cls):
        return cls.__manga_id
