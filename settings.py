import os
from os import environ

import dj_database_url

import otree.settings

ROOT_URLCONF = 'tiered_disclosure.urls'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# the environment variable OTREE_PRODUCTION controls whether Django runs in
# DEBUG mode. If OTREE_PRODUCTION==1, then DEBUG=False
if environ.get('OTREE_PRODUCTION') not in {None, '', '0'}:
    DEBUG = False
else:
    DEBUG = True

# don't share this with anybody.
SECRET_KEY = 'q8_x3%@k(nmeh@_4jsq5z-qr(8n)2i35%6vl0v2d!7p(cu&b(1'


DATABASES = {
    'default': dj_database_url.config(
        # Rather than hardcoding the DB parameters here,
        # it's recommended to set the DATABASE_URL environment variable.
        # This will allow you to use SQLite locally, and postgres/mysql
        # on the server
        # Examples:
        # export DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
        # export DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/NAME
    
        # fall back to SQLite if the DATABASE_URL env var is missing
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
    )
}

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = 'DEMO'

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'cfpbrules'


# setting for integration with AWS Mturk
AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')


# e.g. EUR, CAD, GBP, CHF, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True



# e.g. en, de, fr, it, ja, zh-hans
# see: https://docs.djangoproject.com/en/1.9/topics/i18n/#term-language-code
LANGUAGE_CODE = 'en'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

# SENTRY_DSN = ''

DEMO_PAGE_INTRO_TEXT = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            oTree on GitHub
        </a>.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Here are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish.
</p>
"""

ROOMS = [
    {
        'name': 'econ101',
        'display_name': 'Econ 101 class',
        'participant_label_file': '_rooms/econ101.txt',
    },
    {
        'name': 'live_demo',
        'display_name': 'Room for live demo (no participant labels)',
    },
]


mturk_hit_settings = {
    'keywords': ['bonus', 'study'],
    'title': 'Title for your experiment',
    'description': 'Description for your experiment',
    'frame_height': 500,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 60,
    'expiration_hours': 7*24, # 7 days
    #'grant_qualification_id': 'YOUR_QUALIFICATION_ID_HERE',# to prevent retakes
    'qualification_requirements': []
}


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': (1.00/550),
    'participation_fee': 5.00,
    'num_bots': 12,
    'doc': "",
    'mturk_hit_settings': mturk_hit_settings,
}

ROOMS=[
    {
        'name': 'Gettysburg',
        'display_name': 'Gettysburg Econ Lab',
        'participant_label_file': 'tiered_disclosure/participant_labels.txt',
        'use_secure_urls': True,
    }
]


SESSION_CONFIGS = [
    # {
    #     'name': 'sophistication_scale3',
    #     'display_name': "sophistication scale3",
    #     'num_demo_participants': 1,
    #     'app_sequence': [
    #         'sophistication_scale3',
    #     ],
    # },
    # {
    #     'name': 'peg_turning_task',
    #     'display_name': "pegtask",
    #     'num_demo_participants': 1,
    #     'app_sequence': [
    #         'peg_turning_task',
    #     ],
    # },
    {
        'name': 'tiered_disclosure_v125',
        'display_name': "Tiered Disclosure",
        'use_browser_bots' : False,
        'app_sequence': [
            'tiered_disclosure',
            'survey'
        ],
        'participation_fee': 10,
        'real_world_currency_per_point': (1.00/700), #TODO: CHANGE
        'num_demo_participants': 12,
        'experimenter_present': True, # set false to show "Next" button on ALL pages. 
        'treatmentorder': '1,2,3,4',
        'doc': """
        Specify treatmentorder with no spaces, and numbers separated by commas. Treatments are as follows:\n\n
        Treatment 1: Truncation, 3 products, 2 shown dimensions, 3 total dimensions\n\n
        Treatment 2: Truncation, 6 products, 2 shown dimensions, 3 total dimensions\n\n
        Treatment 3: ASL, 2 products, 2 representatives, 3 total dimensions\n\n
        Treatment 4: ASL, 6 products, 2 representatives, 3 total dimensions\n\n
        """
    },
]

# anything you put after the below line will override
# oTree's default settings. Use with caution.
otree.settings.augment_settings(globals())
