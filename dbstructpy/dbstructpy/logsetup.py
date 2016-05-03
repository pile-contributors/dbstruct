'''
Prepare the logging to console and file.
'''
import logging

def setup_logging(args, logger):
    '''
    Prepare module logger based on user options.
    '''

    # Set the root logger level.
    if args.debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    if args.logfile and len(args.logfile) > 0:
        logfile = args.logfile
    else:
        logfile = None


    if logfile:
        log_formatter = logging.Formatter('%(asctime)s ' \
                                         '[%(threadName)-12.12s] ' \
                                         '[%(levelname)-5.5s]  ' \
                                         '%(message)s')

        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    log_formatter = logging.Formatter('[%(levelname)-5.5s]  ' \
                                     '%(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)
    console_handler.setLevel(loglevel)

    logger.setLevel(logging.DEBUG)
