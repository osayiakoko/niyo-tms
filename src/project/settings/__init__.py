import os
from pathlib import Path
from split_settings.tools import optional, include

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

env = environ.Env(DJANGO_ENV=(str, "production"))

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))


include(
    "components/common.py",  # standard django settings
    "components/logging.py",
    "components/rest_framework.py",
    "components/websocket.py",
    "components/custom.py",
    f'environments/{env("DJANGO_ENV")}.py',
    optional("environments/local.py"),
)
