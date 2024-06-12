import sys
import logging

if '--debug' in sys.argv: 
    logging.basicConfig(
        level = logging.DEBUG,
        format = "%(relativeCreated)d " +
            "%(filename)s:%(lineno)d %(levelname)s: " + 
            "%(message)s"
    ) 
    print('设置日志格式为 --debug 方案。')
else:
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s [maxkbent:%(filename)s:%(lineno)d]" + 
            " %(levelname)s: %(message)s"
    )
logging.getLogger('elasticsearch').setLevel(logging.ERROR)
logging.getLogger('werkzeug').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)