import hashlib

import requests
import json

import warnings
warnings.filterwarnings('ignore')

_session_cache = {}

config_file='config.json'
with open(config_file) as f:
    config = json.loads(f.read())

def _get_session(endpoint_uri):
    cache_key = hashlib.md5(endpoint_uri.encode('utf-8')).hexdigest()
    if cache_key not in _session_cache:
        _session_cache[cache_key] = requests.Session()
    return _session_cache[cache_key]


def make_post_request(endpoint_uri, data, *args, **kwargs):
    kwargs.setdefault('timeout', 10)
    for key, val in config.items():
        kwargs[key] = val
    session = _get_session(endpoint_uri)
    response = session.post(endpoint_uri, data=data, *args, **kwargs)
    response.raise_for_status()

    return response.content


def make_get_request(url, path, *args, **kwargs):
    kwargs.setdefault('timeout', 10)
    for key, val in config.items():
        kwargs[key] = val
    session = _get_session(url)
    response = session.get(url + path, *args, **kwargs)
    response.raise_for_status()

    return response.content
