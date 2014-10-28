import json
import requests
import re

def search(arg):

# arg contains a dict with one key:value
#
# locus is AGI identifier and is mandatory

    if not ('locus' in arg):
        return

    locus = arg['locus']
    locus = locus.upper()
    p = re.compile('AT[1-5MC]G[0-9]{5,5}', re.IGNORECASE)
    if not p.search(locus):
        return

    # Construct Intermine serialized query
    display_fields = 'Gene.computationalDescription Gene.curatorSummary Gene.symbol Gene.briefDescription Gene.name'

    query_body = '<query model="genomic" view="' + display_fields + '" '
    query_body = query_body + 'sortOrder="Gene.computationalDescription ASC" >'
    query_body = query_body + '<constraint path="Gene.primaryIdentifier" op="=" value="' + locus
    query_body = query_body + '" code="A" /></query>'

    payload = {'format':'json', 'start':0, 'query':query_body }
    
    # Eating some of our own puppy chow here. Note that we only support unauth calls to api.araport.org in the 
    # 0.3 release of ADAMA services 
    r = requests.get('https://api.araport.org/intermine/v0.4/query/results', params=payload)

    if r.ok:
        r_json = r.json()
        if (('results' in r_json) and (len(r_json['results']) > 0)):
            record = { 'class': 'locus_property',
                'locus': locus,
                'properties': [ {'type': 'computational_description', 'value': r_json['results'][0][0] },
                                {'type': 'curator_summary', 'value': r_json['results'][0][1]},
                                {'type': 'brief_description', 'value': r_json['results'][0][3]},
                                {'type': 'name', 'value': r_json['results'][0][4]} ] }
            print json.dumps(record, indent=3)
            print '---'


def list(arg):
    pass
