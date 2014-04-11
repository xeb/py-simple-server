#!/usr/bin/python
import os
import argparse
import urllib, json
import re
import dns.resolver

def get_dns_single(host, port):
    """
    get_dns_single: creates a list of IP addresses from a returned set of
    A records for a given host
    """
    addresslist = ""
    cname = dns.resolver.query(host, 'A')
    for i in cname.response.answer:
        for j in i.items:
            addresslist = "%s:%s,%s" % (j.to_text(), port, addresslist)
    return addresslist[:-1]

def get_dns(host, port):
    """
    get_dns: resolves multiple host names if provides, otherwise single
    """
    if "," not in host:
        return get_dns_single(host, port)
    addresslist = ""
    for i in host.split(","):
        try:
            addresslist = "%s,%s" % (get_dns_single(i, port), addresslist)
        except Exception as e:
            print e
    return addresslist[:-1]

def get_consul(consul_url, service, pattern):
    """
    get_consul: resolves hostnames from within a consul cluster
    """
    response = urllib.urlopen(consul_url)
    data = json.loads(response.read())
    addresslist = ""
    for item in data:
        if item['ServiceName'] != service:
            return addresslist

        match = re.search(pattern, item['ServiceID'], re.IGNORECASE)
        if match == None:
            continue

        addresslist = "%s:%s,%s" % (item['ServiceAddress'], item['ServicePort'], addresslist)
    return addresslist[:-1]

def discover(dns, port, consul_url, service, pattern):
    """
    discover: will try to use DNS if args are provided, otherwise,
    it will try the consul cluster
    """
    print "DNS for backends is %s" % dns
    if dns.strip() != "":
        return get_dns(dns, port)
    else:
        print "Getting from CONSUL %s" % consul_url
        return get_consul(consul_url, service, pattern)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pattern',dest='pattern', default="back", help="The case insensitve pattern to find (not a regex)")
    parser.add_argument('--service',dest='service', default="pysimserv", help="The service to look for")
    parser.add_argument('--consul',dest='consul', default="localhost:8500", help="Main consul host to connect to")
    parser.add_argument('--dns',dest='dns', default="", help="DNS host name (or CSV of hosts) to get backends")
    parser.add_argument('--port',dest='port', default="8040", help="Port to use when using DNS to get backends")
    args = parser.parse_args()
    print discover(args.dns, args.port, args.consul, args.service, args.pattern)
