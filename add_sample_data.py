import requests
import json
import sys
import uuid

def create_secret(manager_host,tenant_name,manager_username,mananger_password,secret_name,secret_value):
    try:
        print secret_value
        resp = requests.put('http://'+manager_host+'/api/v3.1/secrets/'+secret_name,
                            json.dumps(dict(
                            value = secret_value,
                            update_if_exists = False,
                            visibility = 'tenant',
                            is_hidden_value = False
                            )),headers={'Tenant':tenant_name,'Content-Type':'application/json'},
                            auth=(manager_username, manager_password))
        print('response content {}'.format(resp.content))
        if resp.status_code==200:
            print('secret was updated successfully')
    except Exception as e:
        print ('Exception happned {}'.format(getattr(e, 'message', repr(e))))

def populate_pool(manager_host,tenant_name,manager_username,mananger_password,pool_id,pool_ips):
    ips_dict = []
    for ip in ips:
        ips_dict.append( { 'id' : str(uuid.uuid4()) , 'ip_address': ip , 'status': 'RELEASED' })
    try:
        create_secret(manager_host,tenant_name,manager_username,mananger_password,pool_id,json.dumps(ips_dict))
    except Exception as e:
        print ('Exception happned {}'.format(getattr(e, 'message', repr(e))))


if __name__=='__main__':
    if len(sys.argv)<8:
        print ('missing parameter : usage '+sys.argv[0]+' manager_host tenant_name manager_username \
               manager_password pool_id first_ip second_ip third_ip')
        sys.exit(1)
    manager_host=sys.argv[1]
    tenant_name=sys.argv[2]
    manager_username=sys.argv[3]
    manager_password=sys.argv[4]
    pool_id=sys.argv[5]
    ips=[sys.argv[6],sys.argv[7],sys.argv[8]]
    populate_pool(manager_host,tenant_name,manager_username,manager_password,pool_id,ips)
