#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests

class AddApi:

    def __init__(self, ip):
        self.ip = "http://" + ip

    def add(self, name, uris, upstream_url):
        ip = self.ip + ":8001/apis/"
        upstream_url = self.ip + upstream_url
        try:
            data = requests.post(ip, data={"name":name, "uris":uris, "upstream_url":upstream_url})
            print(name, "---", data)
        except:
            print(name, "failed...")

    def run(self, data):
        for row in data:
            self.add(row["name"], row["uris"], row["upstream_url"])

if __name__ == "__main__":
    ip = "10.16.89.129"
    a = AddApi(ip)
    data = [
            # main
            {"name":"home", "uris":"/home", "upstream_url":":8082/home"},
            {"name":"sendjson", "uris":"/sendjson", "upstream_url":":8082/sendjosn"},
            {"name":"theoption", "uris":"/theoption", "upstream_url":":8082/theoption"},
            {"name":"applys", "uris":"/applys", "upstream_url":":8082/applys"},
            {"name":"logs", "uris":"/logs", "upstream_url":":8082/logs"},
            {"name":"apply", "uris":"/apply", "upstream_url":":8082/apply"},
            {"name":"results", "uris":"/results", "upstream_url":":8082/results"},
            {"name":"add", "uris":"/add", "upstream_url":":8082/add"},
            {"name":"addbox", "uris":"/addbox", "upstream_url":":8082/addbox"},
            {"name":"home", "uris":"/home", "upstream_url":":8082/home"},
            # login
            {"name":"login", "uris":"/login", "upstream_url":":8081/login"},
            {"name":"register", "uris":"/register", "upstream_url":":8081/register"}
            ]
    a.run(data)
