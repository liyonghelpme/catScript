import urllib
import urllib2

u = 'http://192.168.3.120:9100/login'
data = {
'uid':2,
}
req = urllib2.urlopen(u, urllib.urlencode(data))
con = req.read()
import json
print con
