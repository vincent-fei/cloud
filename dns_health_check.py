#!/usr/bin/env python
# DNS check 
# 
import os, httplib, dns.resolver

appdomain = 'baidu.com'
iplist = []

def get_iplist(domain=''):
    try:
        A = dns.resolver.query(domain, 'A')
    except Exception,e:
        print "DNS resolver error:" + str(e)
        return
    for i in A.response.answer:
        for j in i.items:
            iplist.append(j.address)
    return True

def check(ip):
    checkurl = ip + ":80"
    getcontent = ""
    httplib.socket.setdefaulttimeout(5)
    conn = httplib.HTTPConnection(checkurl)
    try:
        conn.request("GET", "/", headers={"host":appdomain})
        r = conn.getresponse()
        getcontent = r.read(6)
    finally:
        if getcontent == "<html>":
            print ip + "\t[OK]"
        else:
            print ip + "[Error]"

if __name__ == "__main__":
    if get_iplist(appdomain) and len(iplist) > 0:
        for ip in iplist:
            check(ip)
    else:
        print "DNS resolver error"
