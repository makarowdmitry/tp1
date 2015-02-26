def get_setting(setting):
    import settings
    return getattr(settings, setting)


ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_AUTO_SIGNUP = True
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_REDIRECT_URL='/'
SOCIALACCOUNT_QUERY_EMAIL = True

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email'],
        'METHOD': 'oauth2'
    },
    'google': {
       'SCOPE': ['https://www.googleapis.com/auth/userinfo.profile','https://www.googleapis.com/auth/userinfo.email'],
       'AUTH_PARAMS': {'access_type': 'online'}
    }
}


ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = False


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

TEMPLATE_CONTEXT_PROCESSORS = get_setting('TEMPLATE_CONTEXT_PROCESSORS') + (
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)

ACCOUNT_SIGNUP_FORM_CLASS = 'item.forms.SignupForm'
