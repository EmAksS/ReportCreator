from os import environ

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False

FRONTEND_PORT = environ.get('FRONTEND_PORT', 3000)

# Хосты для связи фронта и бека (CORS)
# CORS_ALLOWED_ORIGINS = [
#     f'http://localhost:{FRONTEND_PORT}', # React server
#     f'http://127.0.0.1:{FRONTEND_PORT}',
#     f"http://26.213.134.143:{FRONTEND_PORT}",
#     f"http://26.135.149.127:{FRONTEND_PORT}",
#     f"http://26.135.149.127:8000",
#     f"http://26.146.126.232:{FRONTEND_PORT}",
#     f"http://26.146.126.232:8000",
#     f"http://26.213.134.143:8000",
#     f"https://26.63.43.26:{FRONTEND_PORT}",
#     f"https://26.63.43.26:8000",
# ]

CORS_ALLOW_ALL_ORIGINS = True

CORS_ORIGIN_WHITELIST = [
    f'http://localhost:{FRONTEND_PORT}', # React server
    f'http://127.0.0.1:{FRONTEND_PORT}',
    f"http://26.213.134.143:{FRONTEND_PORT}",
    f"http://26.135.149.127:{FRONTEND_PORT}",
    f"http://26.135.149.127:8000",
    f"http://26.146.126.232:{FRONTEND_PORT}",
    f"http://26.146.126.232:8000",
    f"http://26.213.134.143:8000",
    f"https://26.63.43.26:{FRONTEND_PORT}",
    f"https://26.63.43.26:8000",
]

CSRF_TRUSTED_ORIGINS = [
    f'http://localhost:{FRONTEND_PORT}', # React server
    f'http://127.0.0.1:{FRONTEND_PORT}',
    f"http://26.213.134.143:{FRONTEND_PORT}",
    f"http://26.135.149.127:{FRONTEND_PORT}",
    f"http://26.135.149.127:8000",
    f"http://26.146.126.232:{FRONTEND_PORT}",
    f"http://26.146.126.232:8000",
    f"http://26.213.134.143:8000",
    f"https://26.63.43.26:{FRONTEND_PORT}",
    f"https://26.63.43.26:8000",
]