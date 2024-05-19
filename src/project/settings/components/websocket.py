# pylint: disable=E0602,C0114

ASGI_APPLICATION = "project.asgi.application"

REDIS_HOST = env("REDIS_HOST")  # noqa: F821 # type: ignore
REDIS_PORT = env("REDIS_PORT")  # noqa: F821 # type: ignore

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}
