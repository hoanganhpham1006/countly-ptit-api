import http.client
import datetime
import json
import numpy as np
from api.helpers.response_format import total_array_format

class TotalHelper(object):
    def __init__(self):
        self.current_datetime = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)

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
    
    def post_process(self, total_dict, number, page, total_type):
        if len(total_dict) == 0:
            return total_array_format([], [], total_type)
        total_dict = sorted(total_dict.items(), key=lambda x:x[1], reverse=True)[:number]
        total_dict = np.array(total_dict)
        views = list(total_dict[:, 0])
        viewcounts = list(map(int, total_dict[:, 1])) #Parse integer
        return total_array_format(views, viewcounts, total_type)

    def parse_json(self, data):
        json_data = json.loads(data.decode("utf-8"))
        pages = json_data['meta']['views']
        return json_data, pages

    def get_total(self, number, total_type, page):
        data = self.get_api_from_countly()
        json_data, pages = self.parse_json(data)

        if total_type == 'all':
            return self.get_total_all(json_data, pages, number, page, total_type)
        elif total_type == 'general':
            return self.get_total_general(json_data, pages, number, page, total_type)
        elif total_type == 'year':
            return self.get_total_year(json_data, pages, number, page, total_type)
        elif total_type == 'month':
            return self.get_total_month(json_data, pages, number, page, total_type)
        elif total_type == 'day':
            return self.get_total_day(json_data, pages, number, page, total_type)
    
    def get_total_general(self, json_data, pages, number, page, total_type):
        total_dict = {}
        for p in pages:
            for year in range(2018, self.current_datetime.year + 1):
                if (p in json_data[str(year)]):
                    if ('u' in json_data[str(year)][p]):
                        if p in total_dict:
                            total_dict[p] += json_data[str(year)][p]['u']
                        else:
                            total_dict[p] = json_data[str(year)][p]['u']
        
        result = self.post_process(total_dict, number, page, total_type)
        return result

    def get_total_year(self, json_data, pages, number, page, total_type):  
        year = self.current_datetime.year
        total_dict = {}
        for p in pages:
                if (p in json_data[str(year)]):
                    if ('u' in json_data[str(year)][p]):
                        total_dict[p] = json_data[str(year)][p]['u']
        
        result = self.post_process(total_dict, number, page, total_type)
        return result
    
    def get_total_month(self, json_data, pages, number, page, total_type):  
        year = self.current_datetime.year
        month = self.current_datetime.month
        total_dict = {}
        for p in pages:
                if (p in json_data[str(year)][str(month)]):
                    if ('u' in json_data[str(year)][str(month)][p]):
                        total_dict[p] = json_data[str(year)][str(month)][p]['u']
        
        result = self.post_process(total_dict, number, page, total_type)
        return result
    
    def get_total_day(self, json_data, pages, number, page, total_type):  
        year = self.current_datetime.year
        month = self.current_datetime.month
        day = self.current_datetime.day
        total_dict = {}
        for p in pages:
                if (p in json_data[str(year)][str(month)][str(day)]):
                    if ('t' in json_data[str(year)][str(month)][str(day)][p]):
                        total_dict[p] = json_data[str(year)][str(month)][str(day)][p]['t']
        
        result = self.post_process(total_dict, number, page, total_type)
        return result

    def get_total_all(self, json_data, pages, number, page, total_type):  
        result = []
        result.append(self.get_total_general(json_data, pages, number, page, 'general')[0])
        result.append(self.get_total_year(json_data, pages, number, page, 'year')[0])
        result.append(self.get_total_month(json_data, pages, number, page, 'month')[0])
        result.append(self.get_total_day(json_data, pages, number, page, 'day')[0])
        return result
