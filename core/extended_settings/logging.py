import os

LOG_HANDLER = os.environ.get("LOG_HANDLER")
LOG_FORMATTER = os.environ.get("LOG_FORMATTER")
LOG_LEVEL = os.environ.get("LOG_LEVEL")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": LOG_FORMATTER},
    },
    "loggers": {
        "": {
            "handlers": [LOG_HANDLER],
            "level": LOG_LEVEL,
            "propagate": True,
        },
    },
    "root": {
        "handlers": [LOG_HANDLER],
        "level": LOG_LEVEL,
        "propagate": True,
    },
}
