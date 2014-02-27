import requests
from helpers import api_url


class Job(object):
    """

    """
    def __init__(self, name, color, url=None, views=[], auth=None, verify=True):
        self.name = name
        self.color = color
        self.url = url
        self.views = views
        self.details = None
        self.auth = auth
        self.verify = verify
        self.params = {}

        self.populate_details()
        self.populate_params()

    def populate_details(self):
        try:
            details = requests.get(api_url(self.url),
                                   auth=self.auth,
                                   verify=self.verify).json()
            self.details = details
            return self.details
        except Exception as e:
            print e

    def populate_params(self):
        """
        If this is a parametrized job, then self.params dict will
        hold all the information. We populate it in an ugly way, as
        the response in a dict, of a list of dicts with lists etc...

        'actions' is actually a list of dicts. The way to check if a
        job is parametrized or not is to check if the list is empty.

        That is what we do here...
        """
        if self.details['actions']:
            actions = self.details['actions']
        else:
            return

        #ugly as fuck, but the ugly json responses request ugly loops :)
        for action in actions:
            if "parameterDefinitions" in action.keys():
                params = action['parameterDefinitions']
                for param in params:
                    name = param['name']
                    description = param['description']
                    kind = param['type']
                    default = param['defaultParameterValue']['value']
                    self.params[name] = {
                        'name': name,
                        'description': description,
                        'type': kind,
                        'default': default
                    }

        return self.params

    def build(self, payload=None):
        """
        Build a job withour parameters. Just a post request to /build
        """
        try:
            ret = requests.post(self.url+"/build", auth=self.auth,
                                verify=self.verify)

            print ret.status_code
        except Exception as e:
            print e

    def build_parametrized(self, payload=None):
        try:
            if not payload:
                payload = {}
                for param in self.params.keys():
                    payload['param'] = self.params[param]['default']

            ret = requests.post(self.url+"/buildWithParameters",
                                auth=self.auth, verify=self.verify,
                                data=payload)

            print ret.status_code
        except Exception as e:
            print e


class View(object):
    """

    """
    def __init__(self, name, url, jobs=[], description=None):
        self.name = name
        self.url = url
        self.jobs = jobs
        self.description = description

__author__ = 'Chris Loukas a.k.a.:commixon, <commixon@gmail.com'
