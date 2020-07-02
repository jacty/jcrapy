"""
Module containing all HTTP related classes

Use this module (instead of the more specific ones) when importing Headers,
Request and Response outside this module.
"""
from Jcrapy.https.headers import Headers

from Jcrapy.https.request import Request
from Jcrapy.https.response import Response
from Jcrapy.https.response.html import HtmlResponse