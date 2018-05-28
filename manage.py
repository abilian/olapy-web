from __future__ import absolute_import, division, print_function

import imp
import sys

from olapy_web.cli import app

if __name__ == '__main__':
    try:
        imp.reload(sys)
        sys.setdefaultencoding("UTF8")  # type: ignore
    except Exception:
        pass

    app.run(host='127.0.0.1', port=5000)
