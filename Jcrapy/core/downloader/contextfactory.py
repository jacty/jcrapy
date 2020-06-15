from OpenSSL import SSL
from twisted.internet.ssl import optionsForClientTLS, CertificateOptions,platformTrust, AcceptableCiphers
from twisted.web.client import BrowserLikePolicyForHTTPS

from Jcrapy.core.downloader.tls import DEFAULT_CIPHERS

class JcrapyClientContextFactory(BrowserLikePolicyForHTTPS):
    """
    Non-peer-certificate verifying HTTPS context factory

    Default OpenSSL method is TLS_METHOD (also called SSLv23_METHOD)
    which allows TLS protocol negotiation

    'A TLS/SSL connection established with [this method] may
     understand the SSLv3, TLSv1, TLSv1.1 and TLSv1.2 protocols.'
    """
    def __init__(self, method=SSL.SSLv23_METHOD, tls_verbose_logging=False, tls_ciphers=None, *args, **kwargs):   
        super(JcrapyClientContextFactory, self).__init__(*args, **kwargs)
        self._ssl_method = method
        self.tls_verbose_logging = tls_verbose_logging
        if tls_ciphers:
            self.tls_ciphers = AcceptableCiphers.fromOpenSSLCipherString(tls_ciphers)
        else:
            self.tls_ciphers = DEFAULT_CIPHERS