class Job(object):
    """

    """
    def __init__(self, name, color, url=None, views=[], details=None):
        self.name = name
        self.color = color
        self.url = url
        self.views = views
        self.details = details


class View(object):
    """

    """
    def __init__(self, name, url, jobs=[], property=[], description=None):
        self.name = name
        self.url = url
        self.jobs = jobs
        self.property = property
        self.description = description

__author__ = 'Chris Loukas a.k.a.:commixon, <commixon@gmail.com'
