import sys
from nbs.app import AppContext

if __name__ == "__main__":
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
