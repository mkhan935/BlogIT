from django.apps import AppConfig


class ArticlesAppConfig(AppConfig):
    name = 'blogIT.apps.articles'
    label = 'articles'
    verbose_name = 'Articles'

    def ready(self):
        import blogIT.apps.articles.signals

default_app_config = 'blogIT.apps.articles.ArticlesAppConfig'
