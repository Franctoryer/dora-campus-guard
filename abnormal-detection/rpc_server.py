from xmlrpc.server import SimpleXMLRPCServer

from detect import is_sensitive

if __name__ == '__main__':
    PORT = 8008
    server = SimpleXMLRPCServer(("localhost", PORT))
    server.register_function(is_sensitive, "is_sensitive")
    print(f"异常预警 RPC 服务正在监听 {PORT} 端口 ...")
    server.serve_forever()