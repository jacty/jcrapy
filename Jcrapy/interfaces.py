from zope.interface import Interface

class ISpiderLoader(Interface):

    def from_settings(settings):
        """Return an instance of the class for the given settings"""