from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from urllib.parse import quote
import json
import requests

import util
from recon import recon

server_token = '825046c13f258af3'
webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=c691059157c79978d3dd352cde632618a0003c0af0583405fd2faa33c7666b54'
banner_img = 'https://hackernoon.imgix.net/hn-images/1*74pgSFzS-BUILPTWvAmVVA.jpeg'

def start_recon(host, port, username, password):
    util.connect_to_host({
        'host': host,
        'port': port,
        'username': username,
        'password': password
    })
    url = recon.go(False) # must be remote mode
    data = {
        "msgtype": "actionCard",
        "actionCard": {
            "title": "irtk 信息收集完成",
            "text": f"![banner]({banner_img})\n### irtk 信息收集完成\n\n发布地址：\n{url}",
            "btnOrientation": "0", 
            "singleTitle" : "查看详情",
            "singleURL" : f"dingtalk://dingtalkclient/page/link?url={quote(url)}&pc_slide=true"
        }
    }
    requests.post(webhook_url, json=data)


class MyHTTPServer(BaseHTTPRequestHandler):
    def do_POST(self):
        token = self.headers.get('token')
        if token != server_token:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized')
            return

        post_data = self.rfile.read(int(self.headers.get('Content-Length')))
        json_data = json.loads(post_data.decode('utf-8'))
        content = json_data.get('text', {}).get('content')

        host, port, username, password = content.split()
        port = int(port)
        thread = Thread(target=start_recon, args=(host, port, username, password))
        thread.start()

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        data = {
            "msgtype": "text",
            "text": {
                "content": f"开始对 {username}@{host}:{port} 进行自动化信息收集..."
            }
        }
        self.wfile.write(json.dumps(data).encode('utf-8'))

if __name__ == '__main__':
    server_address = ('', 80)
    httpd = HTTPServer(server_address, MyHTTPServer)
    print("Server started on port 80...")
    httpd.serve_forever()
