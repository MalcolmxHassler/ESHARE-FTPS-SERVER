import os
import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import TLS_FTPHandler,ThrottledDTPHandler
import configparser

config = configparser.ConfigParser()
config.read('eshare.conf')

username=config['credentials']['username']
password=config['credentials']['password']
ip_address=config['network']['ip_address']
port=int(config['network']['port'])
read_limit=int(config['setting']['read_limit'])
write_limit=int(config['setting']['write_limit'])
max_con=int(config['setting']['max_con'])
max_con_per_ip=int(config['setting']['max_con_per_ip'])
certificate=config['security']['certificate']
key=config['security']['key']
banner=config['setting']['banner']
directory=config['directory']['folder']

def ftps():
    authorizer = DummyAuthorizer()
    
    authorizer.add_user(username,password,directory, perm='elradfmwMT')
    authorizer.add_anonymous(os.getcwd())

    handler = TLS_FTPHandler
    
    #certificate
    handler.certfile = certificate
    handler.keyfile = key
    
    #IP address and port
    address = (ip_address, port)
    server = FTPServer(address, handler)
    
    #banner
    handler.banner = banner

    #connection limits
    server.max_cons = max_con
    server.max_cons_per_ip = max_con_per_ip

    #limit speed
    dtp_handler = ThrottledDTPHandler
    dtp_handler.read_limit = read_limit  # 50 Kb/sec (30 * 1024)
    dtp_handler.write_limit = write_limit  # 50 Kb/sec (30 * 1024)

    handler.dtp_handler=dtp_handler

    #logs
    logging.basicConfig(filename='/var/log/eshare.log', level=logging.INFO)

    handler.authorizer = authorizer
    

    #start ftp server
    server.serve_forever()

if __name__ == '__main__':
    ftps()
    
    
