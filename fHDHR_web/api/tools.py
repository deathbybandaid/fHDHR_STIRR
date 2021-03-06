from flask import Response, request, redirect
import urllib.parse
import json


class API_Tools():
    endpoints = ["/api/tools"]
    endpoint_name = "api_tools"
    endpoint_methods = ["GET", "POST"]

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        method = request.args.get('method', default="get", type=str)

        redirect_url = request.args.get('redirect', default=None, type=str)

        if method == "prettyjson":

            dirty_json_url = request.form.get('url', None)

            try:
                json_url_req = self.fhdhr.web.session.get(dirty_json_url)
                json_url_req.raise_for_status()
                json_resp = json_url_req.json()
            except self.fhdhr.web.exceptions.HTTPError as err:
                self.fhdhr.logger.error('Error while getting stations: %s' % err)
                json_resp = {"error": 'Error while getting stations: %s' % err}

            return_json = json.dumps(json_resp, indent=4)

            return Response(status=200,
                            response=return_json,
                            mimetype='application/json')

        else:
            return "%s Invalid Method" % method

        if redirect_url:
            return redirect(redirect_url + "?retmessage=" + urllib.parse.quote("%s Success" % method))
        else:
            return "%s Success" % method
