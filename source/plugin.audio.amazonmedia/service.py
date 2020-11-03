#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import xbmc
import threading
#from resources.lib.configs import *
from time import time
from resources.lib.proxy import ProxyTCPD

class AmazonMediaProxy():
    freqCheck = 60
    freqExport = 86400  # 24 * 60 * 60 seconds
    lastCheck = 0
    def __init__(self):
        #from resources.lib.common import Settings
        #self._s = Settings()
        #self.proxy = ProxyTCPD(self._s)
        self.proxy = ProxyTCPD()
        self.log('Bound to 127.0.0.1:{}'.format(self.proxy.port))
        self.proxy_thread = threading.Thread(target=self.proxy.serve_forever)

    def log(self, msg, level=xbmc.LOGINFO):
        log_message = '[{}] {}'.format('AM Proxy', msg)
        xbmc.log(log_message, level)

    def run(self):
        def _start_servers():
            self.proxy.server_activate()
            self.proxy.timeout = 1
            self.proxy_thread.start()
            self.log('Proxy Server started')

        def _stop_servers():
            self.proxy.server_close()
            self.proxy.shutdown()
            self.proxy_thread.join()
            self.log('Proxy Server stopped')

        #from time import time
        monitor = xbmc.Monitor()

        _start_servers()

        while not monitor.abortRequested():
            if monitor.waitForAbort(1):
                break

        _stop_servers()

if __name__ == '__main__':
    AmazonMediaProxy().run()
