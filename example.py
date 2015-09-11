from tornado.ioloop import IOLoop
from tornado_botocore import Botocore


def on_response(response):
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print instance['InstanceId']
    # i-279e5123
    # ...


if __name__ == '__main__':
    ec2 = Botocore(
        service='ec2', operation='DescribeInstances',
        region_name='us-east-1')
    ec2.call(callback=on_response)
    IOLoop.instance().start()
