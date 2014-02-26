def api_url(url):
    """
    The RESTful API of Jenkins requires that the request must be done in the
    ../api/json route.

    This is a simple function that takes the given url and appends the
    /api/json extension to it
    """
    return url+"/api/json"

__author__ = 'Chris Loukas a.k.a.:commixon, <commixon@gmail.com'
