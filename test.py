# import paramiko
# from time import sleep

# ssh = paramiko.SSHClient()


# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# ssh.connect('192.168.1.1' , port=22 , username='admin' , password='admin')

# print('connection successfull')

# # channel = ssh.invoke_shell()

# def exec ():
#     while True:

#         command = input('enter your command:')

#         print('command executing...')

#         stdin, stdout, stderr = ssh.exec_command(command)

#         output = stdout.readlines()
#         output = "".join(output)

#         print('success...')
#         print(output)
#         if command == 'exit':
#             return False


# if __name__ == '__main__':
#     exec()

devices = {
    'device1': {
        'device_type': 'linux',
        'ip': '192.168.2.204',
        'username': 'hoopad',
        'password': 'P@ssw0rd'
    },
    'device2': {
        'device_type': 'linux',
        'ip': '192.168.2.205',
        'username': 'ranjbar',
        'password': 'Gitl@b1399'
    },
    'device3': {
        'device_type': 'linux',
        'ip': '192.168.2.210',
        'username': 'hoopad',
        'password': 'P@ssw0rd'
    },
    'device4': {
        'device_type': 'linux',
        'ip': '192.168.2.211',
        'username': 'hoopad',
        'password': 'P@ssw0rd'
    },
    'device5': {
        'device_type': 'linux',
        'ip': '192.168.2.212',
        'username': 'hoopad',
        'password': 'P@ssw0rd'
    },
}

from netmiko import ConnectHandler
import time
import concurrent.futures

device = {}
output = []

def connection(dev):
    for k,v in dev.values():
        device['device_type'] = v['device_type']
        device['ip'] = v['ip']
        device['username'] = v['username']
        device['password'] = v['password']
        conn = ConnectHandler(**device)
        return conn

with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(connection, devices)
        print(results)

# for i in devices:
#     try:
#         device['device_type'] = 'linux'
#         device['ip'] = devices[i]['ip']
#         device['username'] = devices[i]['username']
#         device['password'] = devices[i]['password']
#         print(devices[i] , 'connecting')
#         conn = ConnectHandler(**device)
#         conn.enable()
#         print(devices[i] , 'successfull')
#         # output.append(conn.send_command('hostname'))
#     except:
#         print('error...')

# print(output)
