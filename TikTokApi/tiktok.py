import json
import logging
import os
from typing import Union
from urllib.parse import urlencode
import uuid

import requests

from TikTokApi.helpers.gorgon import Gorgon
from TikTokApi.helpers.tt_encrypt import TTEncrypt
from TikTokApi.helpers.x_gorgon import XGorgon
from TikTokApi.utils import (getDateTime, getUNIX, parseCookie, parseHeader,
                             trace_id)
from TikTokApi.helpers.argus import Argus
from TikTokApi.helpers.ladon import Ladon


class TikTok:
    device = {
        "headers": {},
        "cookies": {},
        "proxies": None,
        "interest_list": [],
        "gecko_packages": [],
    }
    api = None
    debug = False

    logger = logging.getLogger("TikTokApi")

    def __init__(self, **kwargs):
        self.request = requests.Session()
        self.debug = kwargs.get("debug", False)
        self.device["proxies"] = kwargs.get("proxies", None)
        self.request.proxies = self.device["proxies"]
        self.data = {}
        self.tt = TTEncrypt()
        self.xg = XGorgon()
        self.argus = Argus()
        self.ladon = Ladon()
        """
        Contact https://t.me/sovitt

        """

    
