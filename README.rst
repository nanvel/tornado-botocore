Tornado botocore
================

This module lets you use botocore with tornado's AsyncHTTPClient, so you can write asynchronous code in tornado for interacting with Amazon Web Services.

For async file upload to S3 see: https://gist.github.com/nanvel/c489761a11ec2db184c5

See also: https://github.com/qudos-com/botocore-tornado

Another option is aiohttp and aiobotocore: https://github.com/aio-libs/aiobotocore

Installation
------------

Requirements:
    - `botocore <https://github.com/boto/botocore>`__ (v1.2.0)
    - `tornado <https://github.com/tornadoweb/tornado>`__

Versions:
    - tornado-botocore==0.0.3 (botocore==0.60.0)
    - tornado-botocore==0.1.0 (botocore==0.65.0)
    - tornado-botocore==1.0.0 (botocore==1.2.0)

.. code-block:: bash

    pip install tornado-botocore


Example
-------

A Simple EC2 Example from `botocore docs <http://botocore.readthedocs.org/en/latest/tutorial/ec2_examples.html>`__:

.. code-block:: python

    import botocore.session


    if __name__ == '__main__':
        session = botocore.session.get_session()
        client = session.create_client('ec2', region_name='us-west-2')

        for reservation in client.describe_instances()['Reservations']:
            for instance in reservation['Instances']:
                print instance['InstanceId']


Using tornado-botocore:

.. code-block:: python

    from tornado.ioloop import IOLoop
    from tornado_botocore import Botocore


    def on_response(response):
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                print instance['InstanceId']


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
            Endpoint='arn:aws:sns:us-west-2:...',
            Attributes={'Enabled': 'false'})
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
            Source=source, Message=message, Destination=destination)
        raise gen.Return(res)

Usage
-----

Session: I think it makes sense to keep one global session object instead of create one for every request.

Credentials: You can specify credentials once on session object creation (pass to get_session method).

Testing: endpoint_url argument is useful for testing (use DynamoDBLocal).

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
