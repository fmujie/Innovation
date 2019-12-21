import requests
import json
import time


class Device():
    DeviceID = ''  # 设备ID
    ApiKey = ''  # APIKey管理中的默认APIKEY
    def __init__(self):
        self.DEVICEID = self.DeviceID
        self.APIKEY = self.ApiKey
        self.url = 'http://api.heclouds.com/devices/%s/datapoints' % (self.DEVICEID)
        self.headers = {"api-key": self.APIKEY, "Connection": "close"}

    def upload_point(self, DataStreamName, VALUE):
        dict = {"datastreams": [{"id": "id", "datapoints": [{"value": 0}]}]}
        dict['datastreams'][0]['id'] = DataStreamName
        dict['datastreams'][0]['datapoints'][0]['value'] = VALUE
        if "succ" in requests.post(self.url, headers=self.headers, data=json.dumps(dict)).text:
            print("Value:", VALUE, " has been uploaded to ", DataStreamName, " at ", time.ctime())

    def get_point(self, DataStreamName):
        data = json.loads(requests.get(self.url, headers=self.headers, ).text)
        for i in data['data']['datastreams']:
            if i["id"] == DataStreamName:
                return int(i['datapoints'][0]['value'])
        else:
            return "Not found DataStreamName - %s " % DataStreamName


if __name__ == "__main__":
    DataStreamName = 'temperature'  # 数据流名称，没有则新建数据流
    device = Device()
    device.upload_point(DataStreamName, 52)  # 向数据流中添加新数据
    print(device.get_point(DataStreamName))  # 查询数据流中的最新数据
