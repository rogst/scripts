#!/usr/bin/python

import requests
import socket

API_URL = "https://api.linode.com/api/"
API_KEY = "<enter secret Linode API key>"
DNS_DOMAIN = "<domain name>"  # e.g. example.com
DNS_RECORD = "<record name>"  # e.g. www


def get_external_ip():
    return requests.get("http://myip.steneteg.org").text


def get_domain_ip():
    return socket.gethostbyname(DNS_DOMAIN)


def update_dns_record(new_value):
    try:
        data = {"api_key": API_KEY, "action": "domainList"}
        resp = requests.post(API_URL, data=data).json()
        domain = [item for item in resp["DATA"]
                  if item["DOMAIN"] == DNS_DOMAIN][0]

        data = {"api_key": API_KEY,
                "action": "domainResourceList",
                "DomainID": str(domain["DOMAINID"])}
        resp = requests.post(API_URL, data=data).json()
        resource = [item for item in resp["DATA"]
                    if item["NAME"] == DNS_RECORD][0]

        data = {"api_key": API_KEY,
                "action": "domainResourceSave",
                "DomainID": str(domain["DOMAINID"]),
                "ResourceID": str(resource["RESOURCEID"]),
                "Name": DNS_RECORD,
                "Type": resource["TYPE"],
                "Target": new_value}
        resp = requests.post(API_URL, data=data).json()
        if len(resp["DATA"]["ERRORARRAY"]) == 0:
            return True
        else:
            print(resp["DATA"]["ERRORARRAY"])
            return False
    except Exception as ex:
        print(str(ex))
        return False


if __name__ == "__main__":
    if get_domain_ip() != get_external_ip():
        if update_dns_record(get_external_ip()) is True:
            print("DNS updated successfully")
        else:
            print("DNS update failed")
    else:
        print("DNS is already up to date")
