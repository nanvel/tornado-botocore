from tornado.ioloop import IOLoop
from tornado_botocore import Botocore


def on_response(response):
    print response
    # {u'Reservations': [], 'ResponseMetadata': {'RequestId': 'ad5d87c9-ec3c-4eab-86c4-851332d4c397'}}


if __name__ == '__main__':
    ec2 = Botocore(
        service='ec2', operation='DescribeInstances',
        region_name='us-east-1')
    ec2.call(callback=on_response)
    IOLoop.instance().start()
