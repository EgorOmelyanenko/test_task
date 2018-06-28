import requests


class Requester:
    i_url = None

    def __init__(self, url):
        self.i_url = url

    def send_request(self, resource, id_=None, data=None, method="get"):
        variables = "/{}".format(resource) if not id_ else "/{}/{}".format(resource, id_)

        return Requester._get_method(method)(
            self.i_url + variables,
            params=data or {},
            headers={
                'Content-type': 'application/json',
                'Content-Encoding': 'UTF-8'
            }
        ).json()

    @staticmethod
    def _get_method(method):
        return {
            "get": requests.get,
            "post": requests.get
        }[method]
