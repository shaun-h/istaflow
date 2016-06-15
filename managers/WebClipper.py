#!/usr/bin/env python3
# modified scripts from
# https://forum.omz-software.com/topic/2271/beta-suggestion-safariviewcontroller/2

from __future__ import absolute_import
from __future__ import print_function
import uuid, six.moves.BaseHTTPServer, select, types, clipboard, console, webbrowser
import urllib
from six.moves.SimpleHTTPServer import SimpleHTTPRequestHandler
try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO

from objc_util import *

SFSafariViewController = ObjCClass('SFSafariViewController')

global mobile_config_str
mobile_config_str = ''

global base_mobileconfig
base_mobileconfig = ''

global keep_running
keep_running = True

# The Icon key contains a base64 encoded green version of the Pythonista low-res
# icon (for shortness)

base_mobileconfig = """
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
<key>PayloadContent</key><array><dict>
<key>FullScreen</key><true/>
<key>Icon</key><data>
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
</data>
<key>IsRemovable</key><true/>
<key>Label</key><string>%s</string>
<key>PayloadDescription</key><string>Configures Web Clip</string>
<key>PayloadDisplayName</key><string>Web Clip (Pythonista)</string>
<key>PayloadIdentifier</key><string>co.hevey.profile.%s</string>
<key>PayloadOrganization</key><string>Pythonista</string>
<key>PayloadType</key><string>com.apple.webClip.managed</string>
<key>PayloadUUID</key><string>%s</string>
<key>PayloadVersion</key><integer>1</integer>
<key>Precomposed</key><true/>
<key>URL</key><string>pythonista3://%s?action=run&amp;args=%s</string>
</dict></array>
<key>PayloadDescription</key><string>Pythonista Web Clip</string>
<key>PayloadDisplayName</key><string>%s</string>
<key>PayloadIdentifier</key><string>co.hevey.profile.%s</string>
<key>PayloadOrganization</key><string>Pythonista homescreen webclip</string>
<key>PayloadRemovalDisallowed</key><false/>
<key>PayloadType</key><string>Configuration</string>
<key>PayloadUUID</key><string>%s</string>
<key>PayloadVersion</key><integer>1</integer>
</dict></plist>
"""

class MobileConfigHTTPRequestHandler(SimpleHTTPRequestHandler):
    def offer_generic(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Last-Modified", self.date_time_string())
        self.end_headers()
        f = StringIO()
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write('<html><body><a href="\webclip.mobileconfig">Something odd happened, click here instead</a></body></html>\n')
        f.seek(0)
        self.wfile.write(bytes(f.getvalue(), 'utf-8'))
        #self.copyfile(f, self.wfile)
        f.close()
    def offer_mobileconfig(self):
        global mobile_config_str
        if mobile_config_str:
            mobileconfig = mobile_config_str
        else:
            mobileconfig = ' '
        self.send_response(200)
        self.send_header("Last-Modified", self.date_time_string())
        self.send_header("Content-type", "application/x-apple-aspen-config")
        self.send_header("Content-Length", len(mobileconfig))
        self.end_headers()
        f = StringIO()
        f.write(mobileconfig)
        f.seek(0)
        self.wfile.write(bytes(f.getvalue(),'utf-8'))
        #self.copyfile(f, self.wfile)
        f.close()
        global keep_running
        keep_running = False
    def do_GET(self):
        if (self.path.lower().endswith('.mobileconfig')):
            return self.offer_mobileconfig()
        return self.offer_generic()

class NicerHTTPServer(six.moves.BaseHTTPServer.HTTPServer):
    def serve_forever(self, poll_interval=0.5):
        # More limited form of serve forever - shutdown after mobileconfig download
        # Works in a single thread
        global keep_running
        while keep_running:
            self._handle_request_noblock()

def serve_it_up(port, icon_label, arg):
    global mobile_config_str
    global base_mobileconfig
    ip = '127.0.0.1'
    icon_label = icon_label # 'Istaflow'
    UUID1 = str(uuid.uuid4()).upper()
    script_name = 'istaflow/istaflow.py'
    arg_str = arg# '%22Show%20Battery%20Details.flow%22'
    payload_name = 'Pythonista - %s' % script_name
    UUID2 = str(uuid.uuid4()).upper()
    mobile_config_str = base_mobileconfig % (icon_label, UUID1, UUID1, script_name, arg_str, payload_name, UUID2, UUID2)
    my_httpd = NicerHTTPServer((ip, port), MobileConfigHTTPRequestHandler)
    #print("Serving HTTP on %s:%s ..." % (ip,port))
    my_httpd.serve_forever()
    #print("\n*** Webclip installed! ***")

def save(icon_label, flow_name):
	port = 8000
	flow = '"'+flow_name+'"'
	flow = flow.replace('"','%22')
	flow = flow.replace(' ','%20')
	#urllib.parse.urlencode('"'+flow_name+'"')
	
	clipboard.set('http://127.0.0.1:%s/webclip.mobileconfig' % port)
	console.alert(title='Message', message='If safari doesn\'t open, open Safari and paste url in clipboard to url and install profile',button1='Ok',hide_cancel_button=True)
	webbrowser.open('safari-http://127.0.0.1:%s/webclip.mobileconfig' % port)
	serve_it_up(port, icon_label, flow)

