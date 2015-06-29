from django.conf import settings


class AdminShorcatModelMixin(object):

    @classmethod
    def shortcut_count(cls):
        return cls.objects.count()

    @classmethod
    def shortcut_count_new(cls):
        return 0

    shortcut_class_name = "file2"

class AdminShortcut(object):
    def __init__(self, opts):
        self.shortcut_list = settings.ADMIN_SHORTCUTS
        # define shortcut params
        self.section_title = opts.get('section_name')
        self.title = opts.get('title')
        self.url = opts.get('url')
        self.url_name = opts.get('url_name')
        self.class_name = opts.get('class_name', 'file1')
        self.open_new_window = opts.get('open_new_window', False)
        self.url_extra = opts.get('url_extra', '')


    @property
    def section(self):
        return self.get_or_create_section()

    @property
    def section_shortcut_list(self):
        return self.section['shortcuts']


    def get_shortcut_dict(self):
        s_d = {
                'url': self.url,
                'url_name': self.url_name,
                'title': self.title,
                'class': self.class_name,
                'open_new_window': self.open_new_window,
                'url_extra': self.url_extra,
        }
        return s_d


    # methos
    def add_shortcut(self):
        self.section_shortcut_list.append(self.get_shortcut_dict())

    def get_section(self):
        section = filter(lambda x: x['title'] == self.section_title, self.shortcut_list)
        return section[0] if len(section) else None

    def create_section(self):
        self.shortcut_list.append({
            'title': self.section_title,
            'shortcuts': []
        })
        return self.get_section()

    def get_or_create_section(self):
        section = self.get_section()
        return section if section else self.create_section()


class AdminModelShortcut(AdminShortcut):

    def __init__(self, model, opts):
        model.__bases__+=(AdminShorcatModelMixin, )
        self.model = model
        self.opts = self.get_default_options()
        self.opts.update(opts)
        super(AdminModelShortcut, self).__init__(self.opts)



    def get_default_options(self):
        return {
            'title': self.model_verbose_name_p,
            'url_name': self.change_list_url_pattern,
            'section_name': self.model._meta.app_label,
            'class_name': self.model.shortcut_class_name
        }


    # properties

    @property
    def change_list_url_pattern(self):
        return 'admin:%s_%s_changelist' % (self.app_label, self.model_name.lower())

    @property
    def app_label(self):
        return self.model._meta.app_label
    @property
    def model_name(self):
        return self.model.__name__

    @property
    def model_verbose_name(self):
        return self.model._meta.verbose_name

    @property
    def model_verbose_name_p(self):
        return self.model._meta.verbose_name_plural

    def get_shortcut_dict_with_counters(self): pass
