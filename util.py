import json
import csv
import requests
import feedparser
import dateutil
import subprocess
from io import StringIO
from dateutil.parser import isoparse
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup
from collections import defaultdict
from wmo_codes import wmo_codes
from typing import List, Dict, TypeVar, TypedDict, Callable
from dataclasses import dataclass, asdict, field, is_dataclass
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from argparse import ArgumentParser

K = TypeVar("K")
T = TypeVar("T")


def filter_dict_keys(d: dict, condition: Callable):
    return {k: v for k, v in d.items() if condition(k)}


def json_from_url(url, **params):
    req = requests.PreparedRequest()
    req.prepare_url(url, params)

    return json.loads(requests.get(req.url).content)


def run(prog, *args, **kwargs):
    named_args = [f"-{'-' if len(k) > 1 else ''}{k.replace('_', '-')}={v}"
                  for k, v in kwargs.items()]
    proc = subprocess.run([prog, *args, *named_args], stdout=subprocess.PIPE)

    return proc.stdout.decode("UTF-8")


def csv_from_subprocess(prog, *args, **kwargs):
    return list(csv.reader(StringIO(run(prog, *args, **kwargs))))


def parse_html(html):
    # https://stackoverflow.com/a/66690657
    elem = BeautifulSoup(html, features="html.parser")
    text = ""
    for e in elem.descendants:
        if isinstance(e, str):
            text += e#.strip()
        elif e.name in ["br", "p", "h1", "h2", "h3", "h4", "tr", "th", "div"]:
            if not text.endswith("\n\n"):
                text += "\n"
        elif e.name == "li":
            text += "\n- "
    return text.strip()


def transpose_dict_lists(d: Dict[K, List[T]]) -> List[Dict[K, T]]:
    """ "Transpose" a dictionary of lists, returning a list of dictionaries,
    each n-th item in the list containing the n-th item in the original list at
    dict[k] for each k in the dict. Consumes the original lists. """
    l = []

    while any(d.values()):
        l.append({k: d[k].pop(0) for k in d if d[k]})

    return l


def asdictify(d) -> dict:
    if is_dataclass(d):
        return asdictify(asdict(d))

    if isinstance(d, list):
        return list(map(asdictify, d))

    if isinstance(d, dict):
        return {k: asdictify(v) for k, v in d.items()}

    return d


def seriablize(d) -> dict:
    if isinstance(d, list):
        return list(map(seriablize, d))

    if isinstance(d, dict):
        return {seriablize(k): seriablize(v) for k, v in d.items()}

    if isinstance(d, datetime) or isinstance(d, date):
        return d.isoformat()

    if not hasattr(d, "__hash__"):
        return str(d)

    return d


def dashify_arg(a):
    if "=" not in a:
        return a

    if len(a.split("=")[0]) == 1:
        return f"-{a}"

    return f"--{a}"
