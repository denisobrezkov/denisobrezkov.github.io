AUTHOR = 'Denis Obrezkov'
SITENAME = 'Python, Data, and Knowledge'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Berlin'

#DEFAULT_LANG = 'ru'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Учим Python (tg)', 'https://t.me/learnpythonforfun'),
         ('Учим Python (vk)', 'https://vk.com/learnpythonforfun'),)

# Social widget
SOCIAL = (('Linkedin', 'https://www.linkedin.com/in/denisobrezkov/'),)

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = './notmyidea'

PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = ['i18n_subsites']

I18N_SUBSITES = {
    'ru': {
        'SITENAME': 'Блог о Python, Data, and Knowledge',
        },
    'en': {
        'SITENAME': 'About Python, Data, and Knowledge'
        }

    }

#LANGUAGE_URL = '{lang}/'
#LANGUAGE_SAVE_AS = '{lang}/index.html'
