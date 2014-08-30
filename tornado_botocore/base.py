import botocore.session
import botocore.response

from functools import partial
from tornado.httpclient import AsyncHTTPClient, HTTPRequest


class Botocore(object):

    def __init__(self, service, operation, region_name, session=None):
        self.session = session or botocore.session.get_session()
        self.service = self.session.get_service(service)
        self.operation = self.service.get_operation(operation)
        self.http_client = AsyncHTTPClient()
        self.operation.call = self.operation_call
        self.endpoint = self.service.get_endpoint(region_name)
        self.endpoint.make_request = self.make_request

    def operation_call(self, endpoint, callback, **kwargs):
        event = self.session.create_event('before-parameter-build',
            self.service.endpoint_prefix, self.operation.name)
        self.session.emit(event,
            operation=self.operation, endpoint=endpoint, params=kwargs)
        params = self.operation.build_parameters(**kwargs)
        event = self.session.create_event('before-call',
            self.service.endpoint_prefix, self.operation.name)
        self.session.emit(event,
            operation=self.operation, endpoint=endpoint, params=params)
        request = endpoint.make_request(self.operation, params)
        request = HTTPRequest(
            url=request.url, headers=request.headers,
            method=request.method, body=request.body)
        self.http_client.fetch(request, partial(
            self.prepare_response, callback=callback))

    def make_request(self, operation, params):
        do_auth = (getattr(self.service, 'signature_version', None) and
            getattr(operation, 'signature_version', True) and self.endpoint.auth)
        if do_auth:
            signer = self.endpoint.auth
        else:
            signer = None
        request = self.endpoint._create_request_object(operation, params)
        prepared_request = self.endpoint.prepare_request(request, signer)
        return prepared_request

    def prepare_response(self, http_response, callback):
        http_response.content = http_response.body
        http_response.encoding = 'utf-8'
        response = botocore.response.get_response(
            session=self.session, operation=self.operation,
            http_response=http_response)
        event = self.session.create_event('after-call',
            self.service.endpoint_prefix, self.operation.name)
        self.session.emit(event, operation=self.operation,
            http_response=response[0], parsed=response[1])
        callback(response)

    def call(self, callback, **kwargs):
        self.operation.call(endpoint=self.endpoint, callback=callback)
