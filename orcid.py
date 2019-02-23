import requests
import xml.dom.minidom

r = requests.get('https://pub.sandbox.orcid.org/v3.0_rc1/0000-0002-9227-8514')

dom = xml.dom.minidom.parseString(r.text)
eles = dom.documentElement
creditName = eles.getElementsByTagName("personal-details:credit-name")[0].firstChild.data
print(creditName)
