'''
First lets go over what this directory is all about
Django's built- in authentication only works with traditional HTML request-response cycle.
This means the client would fill out a form, click submit and the browser makes a request
to the server which includes the data the user had typed, server processes data, then
responds with html or redirects to a new page

we dont want to do this, we want the server to return JSON and the client should decide
what to next. Same like the HTML cycle but when the request is sent, the server responds to that
request rather than control browser's behavior,  we can still use parts of the the built in authentication

'''
from django.apps import AppConfig


class AuthenticationAppConfig(AppConfig):
    name = 'blogIT.apps.authentication'
    label = 'authentication'
    verbose_name = 'Authentication'

    def ready(self):
        import blogIT.apps.authentication.signals

# This is how you register a custom app config with Django. Django is smart
# enough to look for the `default_app_config` property of each registered app
# and use the correct app config based on that value.
default_app_config = 'blogIT.apps.authentication.AuthenticationAppConfig'
