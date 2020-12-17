import requests as req


def j(r):
    """Helper function needed because flask test_client() provide json as a property(?), not as a method."""
    return r.json() if callable(r.json) else r.json


def requests(method, url, **kwargs):
    from oka import oka
    from oka.auth import get_token
    headers = {'Authorization': 'Bearer ' + oka.token} if oka.token else {}
    r = getattr(req, method)(url, headers=headers, **kwargs)
    if r.status_code == 401:
        print("Please login before.")
        oka.token = get_token(oka.url)
        r = getattr(req, method)(url, headers=headers, **kwargs)
    if r.ok:
        return r
    # raise Exception(j(r)["errors"]["json"])
