import http.client
import datetime
import time
import json
import numpy as np
from api.helpers.response_format import timerange_total_array_format

class TimerangeTotalHelper(object):
    def __init__(self):
        self.current_datetime = time.mktime(datetime.datetime.now(datetime.timezone.utc).timetuple())
        self.furthest_datatime= time.mktime(datetime.datetime(2018, 1, 1, 0, 0).timetuple())

    def get_api_from_countly(self):
        conn = http.client.HTTPConnection("207.148.79.97")
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"method\"\r\n\r\nviews\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"api_key\"\r\n\r\n76e0e145aa7343c0b23ac8a1156a0e7e\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"app_id\"\r\n\r\n5c2c39560e66a35b7e802993\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'cache-control': "no-cache",
            'postman-token': "fb3e7a8a-0177-e4f5-198f-5894279d462c"
            }
        conn.request("POST", "/o", payload, headers)
        res = conn.getresponse()
        data = res.read()
        return data
    
    def post_process(self, total_dict, number, page, start_time, end_time):
        if len(total_dict) == 0:
            return timerange_total_array_format([], [], start_time, end_time)
        total_dict = sorted(total_dict.items(), key=lambda x:x[1], reverse=True)[:number]
        total_dict = np.array(total_dict)
        views = list(total_dict[:, 0])
        viewcounts = list(map(int, total_dict[:, 1])) #Parse integer
        return timerange_total_array_format(views, viewcounts, start_time, end_time)

    def parse_json(self, data):
        json_data = json.loads(data.decode("utf-8"))
        return json_data

    def get_timerange_total(self, number, start_time, end_time, page):
        data = self.get_api_from_countly()
        json_data = self.parse_json(data)
        start_time = max(int(start_time), self.furthest_datatime)
        end_time = min(int(end_time), self.current_datetime)
        if start_time > end_time:
          start_time = end_time
        return self.get_timerange_total_process(json_data, number, page, start_time, end_time)

    def get_timerange_total_process(self, json_data, number, page, start_time, end_time):
        total_dict = {}
        for year in json_data:
            if str.isdigit(year): 
                for month in json_data[year]:
                    if str.isdigit(month):
                        for day in json_data[year][month]:
                            if str.isdigit(day):
                                for hour in json_data[year][month][day]:
                                    if str.isdigit(hour):
                                        dt = time.mktime(datetime.datetime(int(year), int(month), int(day), int(hour), 0, 0).timetuple())
                                        if dt >= start_time and dt <= end_time:
                                            for page in json_data[year][month][day][hour]:
                                                if 't' in json_data[year][month][day][hour][page]:
                                                    if page in total_dict:
                                                        total_dict[page] += json_data[year][month][day][hour][page]['t']
                                                    else:
                                                        total_dict[page] = json_data[year][month][day][hour][page]['t']
        result = self.post_process(total_dict, number, page, start_time, end_time)
        return result
