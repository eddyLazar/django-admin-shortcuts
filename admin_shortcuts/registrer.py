from shortcuts import AdminShortcut, AdminModelShortcut

""" Params list

section_name - name of shorctu section
title - title of shortcut
url - url for shortcut link
url_name - url pattern for shortcut link
class_name - css class name for shortcut block
open_new_window
url_extra - extra url params
"""

def reg_shortcut(**kwargs):
    admin_shortcut = AdminShortcut(kwargs)
    admin_shortcut.add_shortcut()

def reg_model(model, **kwargs):
    admin_shortcut = AdminModelShortcut(model, kwargs)
    admin_shortcut.add_shortcut()

def reg_app(app_name, models_list = [], **kwargs):
    from django.apps import apps
    app = apps.get_app_config(app_name)
    for model in app.get_models():
        if (model.__name__.lower() in [m_n.lower() for m_n in models_list]):
            reg_model(model, **kwargs)
