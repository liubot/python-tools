#coding:utf-8
import logging
import logging.config
import os
import yaml
from pprint import pprint


def setup_logger(log_root_path, config_file):
    '''
        log_root_path:日志目录名称
        config_file:配置文件yaml路径
    '''
    if not os.path.exists(os.path.dirname(log_root_path)):
        os.makedirs(os.path.dirname(log_root_path))

    with open(config_file,'r') as fh:
        logging_config = yaml.safe_load(fh)

    #设置handler的filepath
    for handler in logging_config['handlers']:
        if logging_config['handlers'][handler].get("filename"):
            log_name = logging_config['handlers'][handler]['filename']
            logging_config['handlers'][handler]['filename'] = os.path.join(log_root_path,log_name)

    logging.config.dictConfig(logging_config)



def init():
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    log_root_path = os.path.join(APP_DIR, 'logs')
    config_file = os.path.join(APP_DIR,'logging.yaml')
    setup_logger(log_root_path,config_file)
    return logging.getLogger("server"),logging.getLogger("cron")

server_logger, cron_logger = init()
if __name__ == "__main__":

    cron_del_logger = logging.getLogger("cron.delete")
    other = logging.getLogger("other")
    server_logger.info("this is info")
    server_logger.debug("this is debug")
    cron_logger.info("this is cron")
    cron_del_logger.info("this is cron delete")
    other.info("this is other")
