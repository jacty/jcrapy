from urllib.parse import urlparse, urlunparse

from Jcrapy.utils.python import to_bytes

def _parsed_url_args(parsed):
    # Assume parsed is urlparse-d from Request.url,
    # which was passed via safe_url_string and is ascii-only.
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    path = to_bytes(path, encoding="ascii")
    host = to_bytes(parsed.hostname, encoding="ascii")
    port = parsed.port
    scheme = to_bytes(parsed.scheme, encoding="ascii")
    netloc = to_bytes(parsed.netloc, encoding="ascii")
    if port is None:
        port = 443 if scheme == b'https' else 80
    return scheme, netloc, host, port, path

def _parse(url):
    """ Return tuple of (scheme, netloc, host, port, path),
    all in bytes except for port which is int.
    Assume url is from Request.url, which was passed via safe_url_string and is ascii-only.
    """
    url = url.strip()
    parsed = urlparse(url)
    return _parsed_url_args(parsed)