#!C:\Users\ingov\PycharmProjects\appium-framework\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'uiautomator2==2.9.2','console_scripts','uiautomator2'
__requires__ = 'uiautomator2==2.9.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('uiautomator2==2.9.2', 'console_scripts', 'uiautomator2')()
    )
