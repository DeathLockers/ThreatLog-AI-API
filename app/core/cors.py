from . import getenv

domains_list = getenv("DOMAINS_ORIGINS_LIST")

DOMAINS_ORIGINS_LIST = domains_list.split(",")
