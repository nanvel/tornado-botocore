Tornado botocore
================

This module lets you use botocore with tornado's AsyncHTTPClient, so you can write asynchronous code in tornado for interacting with Amazon Web Services.

Installation
------------

Requirements:

    - `botocore <https://github.com/boto/botocore>`__ (use v0.60.0 with tornado-botocore==0.0.3 and v0.65.0 with tornado-botocore>=0.1.0, and I am not guarantee that all will work with botocore versions > 0.65.0)
    - `tornado <https://github.com/tornadoweb/tornado>`__

.. code-block:: bash

    pip install tornado-botocore


Example
-------

A Simple EC2 Example from `botocore docs <http://botocore.readthedocs.org/en/latest/tutorial/ec2_examples.html>`__:

.. code-block:: python

    import botocore.session


    if __name__ == '__main__':
        session = botocore.session.get_session()
        ec2 = session.get_service('ec2')
        operation = ec2.get_operation('DescribeInstances')
        endpoint = ec2.get_endpoint('us-east-1')
        http_response, response_data = operation.call(endpoint)
        print response_data


Using tornado-botocore:

.. code-block:: python

    from tornado.ioloop import IOLoop
    from tornado_botocore import Botocore


    def on_response(response):
        print response


    if __name__ == '__main__':
        ec2 = Botocore(
            service='ec2', operation='DescribeInstances',
            region_name='us-east-1')
        ec2.call(callback=on_response)
        IOLoop.instance().start()


If a callback is not specified, it works synchronously:

.. code-block:: python

    from tornado_botocore import Botocore


    if __name__ == '__main__':
        ec2 = Botocore(
            service='ec2', operation='DescribeInstances',
            region_name='us-east-1')
        print ec2.call()


Another example - deactivate SNS endpoint:

.. code-block:: python

    from tornado import gen
    from tornado.ioloop import IOLoop
    from tornado_botocore import Botocore


    def on_response(response):
        print response
        # {'ResponseMetadata': {'RequestId': '056eb19e-3d2e-53e7-b897-fd176c3bb7f2'}}


    if __name__ == '__main__':
        sns_operation = Botocore(
            service='sns', operation='SetEndpointAttributes',
            region_name='us-west-2')
        sns_operation.call(
            callback=on_response,
            endpoint_arn='arn:aws:sns:us-west-2:...',
            attributes={'Enabled': 'false'})
        IOLoop.instance().start()

Send email using SES service and tonado.gen:

.. code-block:: python

    @gen.coroutine
    def send(self, ...):
        ses_send_email = Botocore(
            service='ses', operation='SendEmail',
            region_name='us-east-1')
        source = 'example@mail.com'
        message = {
            'Subject': {
                'Data': 'Example subject'.decode('utf-8'),
            },
            'Body': {
                'Html': {
                    'Data': '<html>Example content</html>'.decode('utf-8'),
                },
                'Text': {
                    'Data': 'Example content'.decode('utf-8'),
                }
            }
        }
        destination = {
            'ToAddresses': ['target@mail.com'],
        }
        res = yield gen.Task(ses_send_email.call,
            source=source, message=message, destination=destination)
        raise gen.Return(res)


Contribute
----------

If you want to contribute to this project, please perform the following steps:

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    $ virtualenv .env --no-site-packages
    $ source .env/bin/activate
    $ pip install -r requirements.txt

    $ git co -b feature_branch master
    # Implement your feature
    $ git add . && git commit
    $ git push -u origin feature_branch
    # Send us a pull request for your feature branch
