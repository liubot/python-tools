#coding:utf-8
import logging
import logging.config
import os
import yaml


def setup_logger(output_file, config_file):
    '''
        output_file:日志文件名称
        config_file:配置文件yaml路径
    '''
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
    with open(config_file,'r') as fh:
        logging_config = yaml.safe_load(fh)

    logging_config['handlers']['file_handler']['filename'] = output_file
    logging.config.dictConfig(logging_config)




def init():
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(APP_DIR, 'logs', 'server.log')
    config_file = os.path.join(APP_DIR,'logging.yaml')
    setup_logger(output_file,config_file)
    return logging.getLogger("server")


if __name__ == "__main__":
    logger = init()
    logger.info("this is info")
    logger.debug("this is debug")
