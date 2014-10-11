import botocore.session
import botocore.response
import botocore.parsers

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
        request_dict = self.operation.build_parameters(**kwargs)
        event = self.session.create_event('before-call',
            self.service.endpoint_prefix, self.operation.name)
        self.session.emit(event,
            operation=self.operation, endpoint=endpoint, params=request_dict)
        request = endpoint.make_request(
            operation_model=self.operation.model, request_dict=request_dict)
        request = HTTPRequest(
            url=request.url, headers=request.headers,
            method=request.method, body=request.body)
        self.http_client.fetch(request, partial(
            self.prepare_response, callback=callback))

    def make_request(self, operation_model, request_dict):
        do_auth = self.endpoint._signature_version and self.endpoint.auth
        if do_auth:
            signer = self.endpoint.auth
        else:
            signer = None
        request = self.endpoint._create_request_object(request_dict)
        prepared_request = self.endpoint.prepare_request(request, signer)
        return prepared_request

    def prepare_response(self, http_response, callback):
        operation_model = self.operation.model
        protocol = operation_model.metadata['protocol']
        response_dict = {
            'headers': http_response.headers,
            'status_code': http_response.code,
        }
        if response_dict['status_code'] >= 300:
            response_dict['body'] = http_response.body
        elif operation_model.has_streaming_output:
            response_dict['body'] = botocore.response.StreamingBody(
                http_response.body, response_dict['headers'].get('content-length'))
        else:
            response_dict['body'] = http_response.body
        parser = botocore.parsers.create_parser(protocol)
        parsed = parser.parse(
            response_dict, operation_model.output_shape)
        event = self.session.create_event('after-call',
            self.service.endpoint_prefix, self.operation.name)
        self.session.emit(event, operation=self.operation,
            http_response=http_response, parsed=parsed)
        callback(parsed)

    def call(self, callback, **kwargs):
        self.operation_call(endpoint=self.endpoint, callback=callback, **kwargs)
