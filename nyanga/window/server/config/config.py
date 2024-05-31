import pathlib


class Config(object):
    SEND_FILE_MAX_AGE_DEFAULT = 1
    BASEPATH = pathlib.Path.joinpath(pathlib.Path.home(), ".nyanga-read")
    DATABASEPATH = pathlib.Path.joinpath(BASEPATH, "data")

    if not pathlib.Path.exists(BASEPATH):
        pathlib.Path.mkdir(BASEPATH)
        pathlib.Path.mkdir(DATABASEPATH)

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASEPATH}/database.db"
