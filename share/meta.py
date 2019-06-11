import logging

logger = logging.getLogger(__name__)


def get_sth_display(target_value, choices):
    for value, display in choices:
        if value == target_value:
            return display
