import re
import requests
import json

import util
from config import config

vt_api = "https://www.virustotal.com/api/v3"
headers = {
    "accept": "application/json",
    "x-apikey": config['ti']['ak'],
}

def search(target):
    target_type = get_target_type(target)
    if target_type == 'file':
        endpoint = f"/files/{get_file_hash(target)}"
        attr = request(endpoint)
        print_hash_info(attr)
    elif target_type == 'ip':
        endpoint = f"/ip_addresses/{target}"
        attr = request(endpoint)
        print_ip_info(attr)
    elif target_type == 'hash':
        endpoint = f"/files/{target}"
        attr = request(endpoint)
        print_hash_info(attr)
    elif target_type == 'domain':
        endpoint = f"/domains/{target}"
        attr = request(endpoint)
        print_domain_info(attr)

def get_target_type(target):
    if re.match(r'^[a-zA-Z]:[\\/].*', target) or re.match(r'^[\\/].*', target):
        return 'file'
    elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
        return 'ip'
    elif re.match(r'^[a-fA-F0-9]{32,}$', target):
        return 'hash'
    
    return 'domain'

def get_file_hash(filename):
    command = f"sha256sum {filename} | cut -d' ' -f1"
    return util.exec_cmd(command)

def request(endpoint):
    response = requests.get(vt_api + endpoint, headers=headers)
    res = response.json()
    return res['data']['attributes']

def print_hash_info(attr):
    print('YARA:', json.dumps(attr['crowdsourced_yara_results'][0] if 'crowdsourced_yara_results' in attr else 'Unknown', indent=2))
    print('Names:', attr['names'])
    print('Meaningful Name:', attr['meaningful_name'] if 'meaningful_name' in attr else 'Unknown')
    print('Threat Classification:', json.dumps(attr['popular_threat_classification'] if 'popular_threat_classification' in attr else 'Unknown', indent=2))
    print('Sandbox Verdicts:', json.dumps(attr['sandbox_verdicts'] if 'sandbox_verdicts' in attr else 'Unknown', indent=2))
    print('Last Analysis Stats:', json.dumps(attr['last_analysis_stats'], indent=2))
    print('Reputation:', attr['reputation'])

def print_ip_info(attr):
    print('Regional Internet Registry:', attr['regional_internet_registry'])
    print('Network:', attr['network'])
    print('Tags:', attr['tags'])
    print('Country:', attr['country'])
    print('AS Owner:', attr['as_owner'])
    print('Last Analysis Stats:', json.dumps(attr['last_analysis_stats'], indent=2))
    print('Reputation:', attr['reputation'])

def print_domain_info(attr):
    print('Last DNS Records:', json.dumps(attr['last_dns_records'], indent=2))
    print('Tags:', attr['tags'])
    print('Registrar:', attr['registrar'] if 'registrar' in attr else 'Unknown')
    print('Last Analysis Stats:', json.dumps(attr['last_analysis_stats'], indent=2))
    print('Reputation:', attr['reputation'])
