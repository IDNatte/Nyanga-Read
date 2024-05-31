from nyanga.window.server.storage.model.settings import Setting
from nyanga.window.server.helper.constant import constant
from nyanga.window.server.server import create_app


def db_settings_initializer():
    with create_app().app_context():
        constant.DB.create_all()
        check_db_population = Setting.query.count()
        if check_db_population == 0:
            init_lang_settings = Setting(setting_type="language", value="en")
            init_content_settings = Setting(setting_type="content", value="safe")
            constant.DB.session.add(init_lang_settings)
            constant.DB.session.add(init_content_settings)
            constant.DB.session.commit()
