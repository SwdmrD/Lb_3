ЛБ 3

Також можна використати SQLite 
для цього внести зміни у setting.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
Для MSSql
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'назва вашої бд',
        'USER': 'ім'я',
        'PASSWORD': 'пароль',
        'HOST': 'хост',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'trusted_connection': 'yes',
        },
    }
}
