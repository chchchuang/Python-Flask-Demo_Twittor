import os
import sys

sys.path.insert(0, os.getcwd()) # os.getcwd():返回當前工作目錄; 將當前工作目錄加到系統路徑中, 才能順利 import不在當下工作目錄底下的 module

from twittor import create_app

# Create an application instance that web servers can use. We store it as
# "application" (the wsgi default) and also the much shorter and convenient "app".
application = create_app()
