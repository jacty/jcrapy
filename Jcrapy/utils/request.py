import hashlib
import weakref

from w3lib.url import canonicalize_url

from Jcrapy.utils.python import to_bytes

_fingerprint_cache = weakref.WeakKeyDictionary()

def request_fingerprint(request, include_headers=None, keep_fragments=False):
    """
    Return the request fingerprint.

    The request fingerprint is a hash that uniquely identifies the resource the
    request points to. For example, take the following two urls:

    http://www.example.com/query?id=111&cat=222
    http://www.example.com/query?cat=222&id=111

    Even though those are two different URLs both point to the same resource
    and are equivalent (i.e. they should return the same response).

    Another example are cookies used to store session ids. Suppose the
    following page is only accessible to authenticated users:

    http://www.example.com/members/offers.html

    Lot of sites use a cookie to store the session id, which adds a random
    component to the HTTP Request and thus should be ignored when calculating
    the fingerprint.

    For this reason, request headers are ignored by default when calculating
    the fingeprint. If you want to include specific headers use the
    include_headers argument, which is a list of Request headers to include.

    Also, servers usually ignore fragments in urls when handling requests,
    so they are also ignored by default when calculating the fingerprint.
    If you want to include them, set the keep_fragments argument to True
    (for instance when handling requests with a headless browser).

    """
    if include_headers:
        print('include_headers in request.py is True')    
    cache = _fingerprint_cache.setdefault(request, {})
    cache_key = (include_headers, keep_fragments)
    if cache_key not in cache:
        fp = hashlib.sha1()
        fp.update(to_bytes(request.method))
        fp.update(to_bytes(canonicalize_url(request.url, keep_fragments=keep_fragments)))
        fp.update(request.body or b'')
        if include_headers:
            print('include_headers')

        cache[cache_key] = fp.hexdigest()
    return cache[cache_key]
