import datetime
import hashlib
import json
import os
import random
import time
import traceback
from typing import Union
import pytz


def getCountryDetail(country_code: str) -> dict:
    dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir, "res", "countries.json"), "rb") as f:
        ListCountry = json.load(f)
        f.close()

    LISTtzname = pytz.country_timezones[country_code]
    countries = [
        _country for _country in ListCountry if _country["iso"] == country_code.lower()]
    country = random.choice(countries)
    tzname = random.choice(LISTtzname)
    timezone = pytz.timezone(tzname)
    abbr = timezone.localize(datetime.datetime.now(), is_dst=False)
    date = datetime.datetime.now(timezone)
    offset = date.strftime("%z")
    tzname = tzname.split("/")
    tzname = "/".join(tzname[:2])
    return {
        "region": country["iso"].upper(),
        "network": country["network"],
        "mcc": country["mcc"],
        "mnc": country["mnc"],
        "locale": country["locale"].replace("_", "-"),
        "_locale": country["locale"],
        "language": country["locale"].split("_")[0],
        "tz_name": tzname,
        "timezone_name": date.strftime("%Z"),
        "tz_offset": round(date.utcoffset().total_seconds()),
        "tz_abbr": abbr.tzname(),
        "utc_offset": "GMT"+offset[0:3]+":"+offset[3:],
        "timezone": round(date.utcoffset().total_seconds()/3600, 2),
    }


def getUNIX(add: bool = False, addRandom: int = 0) -> int:
    if add:
        return int(round((time.time() * 1000)) + addRandom)
    else:
        return int(round(time.time()))


def getDateTime(fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    my_zone = datetime.datetime.now()
    return str(my_zone.strftime(fmt))


def toHexStr(num: int) -> str:
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return tmp_string


def json_encode(data: dict) -> str:
    return json.dumps(data, separators=(",", ":"), indent=None,)


def trace_id(device_id: Union[str, int] = "") -> str:
    if device_id == "":
        device_id = str(round(time.time()*1000)).zfill(9)
    e = toHexStr(round(time.time()*1000) % 4294967295)
    e = e.zfill(8)
    if type(device_id) == int:
        r = "01"
    else:
        device_id = device_id.replace("-", "")
        r = int(device_id)
    e2 = toHexStr(r)
    r = 22 - len(e2) - 4
    c = str(len(e2)).zfill(2)
    seed = toHexStr(round(random.random() * pow(10, 12)))[0:r]
    c = c+e2+seed
    e3 = e+c
    e3_1 = e3[0:16]
    res = f"00-{e3}-{e3_1}-01"
    return res


def parseCookie(cookies: dict) -> dict:
    dict = {}
    for k, v in cookies.items():
        dict[k] = v
    return dict


def say_my_name() -> str:
    stack = traceback.extract_stack()
    return stack[-2][2]


def parseHeader(headers: dict) -> dict:
    dict = {}
    to_store = ["x-tt-logid", "x-tt-trace-host", "x-tt-trace-tag", "x-tt-token-sign", "x-tt-trace-id", "x-tt-token",
                "x-tt-store-idc", "x-tt-store-idc", "x-tt-cmpl-token", "x-tt-multi-sids", "x-tt-store-region", "x-ms-token", "x-ss-etag"]
    for k, v in headers.items():
        if k.lower() in to_store:
            dict[k.lower()] = v
    return dict


def md5stub(body) -> str:
    try:
        return (hashlib.md5(body).hexdigest()).upper()
    except:
        return (hashlib.md5(body.encode()).hexdigest()).upper()
