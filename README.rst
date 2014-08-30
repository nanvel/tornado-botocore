Tornado botocore
================

This module allows to use botocore with tornado AsyncHTTPClient, so we can write asynchronous code in tornado for interacting with amazon web services.

`http://nanvel.name/weblog/tornado-botocore/ <http://nanvel.name/weblog/tornado-botocore/>`__

Installation
------------

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
        http_response, response_data = response
        print response_data


    if __name__ == '__main__':
        ec2 = Botocore(
            service='ec2', operation='DescribeInstances',
            region_name='us-east-1')
        ec2.call(callback=on_response)
        IOLoop.instance().start()


Contribute
----------

If you want to contribute to this project, please perform the following steps

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
