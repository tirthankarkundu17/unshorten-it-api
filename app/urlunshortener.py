from urllib import parse

import requests


def unshorten_url(url: str):
    success = False
    unshortened_url = ""
    try:
        unshortened_url = requests.head(url, allow_redirects=True).url
        success = True
    except:
        print("Unsuccessful")
    return success, unshortened_url


def sanitize_url(url: str):
    allowed = ["sid", "marketplace", "sort"] # Specific for Flipkart
    success = False
    try:
        parse.urlsplit(url)
        allowed_query_params = {}
        query_params = dict(parse.parse_qsl(parse.urlsplit(url).query))
        for k, v in query_params.items():
            if k in allowed:
                allowed_query_params[k] = v

        sanitized_url = url.split("?")[0] + "?" + parse.urlencode(allowed_query_params)
        success = True
    except:
        print("Unsuccessful")

    return success, sanitized_url