import os
import re
import SimpleHTTPServer
import SocketServer
import StringIO
import json

from os.path import isfile, join
from ast_serializer import serialize

TESTS_FOLDER = "../../tests"
SKIP_FILES = ['Math.py', '.*.pyc']


def is_valid(file_name):
    return not any(map(lambda e: re.match(e, file_name), SKIP_FILES))


def serialize_ast(file_name):
    import compiler

    output = StringIO.StringIO()
    tree = compiler.parseFile(os.path.join(TESTS_FOLDER, file_name))
    serialize(tree, 0, '', output.write)
    return output.getvalue()


def serialize_ast2(file_name):
    import ast
    from ast_serializer2 import serialize

    data = open(join(TESTS_FOLDER, file_name)).read()
    output = StringIO.StringIO()
    tree = ast.parse(data)
    serialize(tree, 0, '', output.write)
    return output.getvalue()


class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def write_json(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-length", len(data))
        self.end_headers()

        self.wfile.write(data)

    def do_GET(self):
        if self.path.startswith('/ast'):
            file_name = self.path.split('/')[-1]
            data = serialize_ast2(file_name)
            self.write_json(data)
        elif self.path == '/files':
            files = filter(lambda e: is_valid(e) and isfile(join(TESTS_FOLDER, e)), os.listdir(TESTS_FOLDER))
            self.write_json(json.dumps(files))
        else:
            self.path = '/html/' + self.path
            return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

server = SocketServer.TCPServer(('127.0.0.1', 8080), RequestHandler)
server.serve_forever()