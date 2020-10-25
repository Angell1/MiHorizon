import time
import consul
import json


class Consul(object):
    def __init__(self, host, port):
        '''初始化，连接consul服务器'''
        self._consul = consul.Consul(host, port)

    def registerserver(self,server_name, ip, port):
        print(f"开始注册服务{server_name}")
        # 健康检查ip端口，检查时间：5,超时时间：30，注销时间：30s
        check = consul.Check.tcp(ip, port,  "5s", "30s", "30s")
        # 注册服务部分
        self._consul.agent.service.register(server_name, f"{server_name}-{ip}-{port}",
                                 address=ip, port=port, check=check)
        print(f"注册服务{server_name}成功")


    def unregisterserver(self,server_name, ip, port):
        print(f"退出服务{server_name}")
        self._consul.agent.service.deregister(f'{server_name}-{ip}-{port}')


    def GetService(self, name):
        services = self._consul.agent.services()
        service = services.get(name)
        if not service:
            return None, None
        addr = "{0}:{1}".format(service['Address'], service['Port'])
        return service, addr
