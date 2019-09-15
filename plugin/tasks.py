import requests
import json

# ctx is imported and used in operations
from cloudify import ctx

# put the operation decorator on any function that is a task
from cloudify.decorators import operation
from cloudify.exceptions import NonRecoverableError

def get_secret(manager_host,tenant_name,manager_username,mananger_password,secret_name):
    value = None
    try:
        resp = requests.get('http://'+manager_host+'/api/v3.1/secrets/'+secret_name,
                            headers={'Tenant':tenant_name},auth=(manager_username, manager_password))
        ctx.logger.debug('response content {}'.format(resp.content))
        value = json.loads(resp.content)
    except Exception as e:
        raise NonRecoverableError('Exception happned {}'.format(getattr(e, 'message', repr(e))))
    return value;

def update_secret(manager_host,tenant_name,manager_username,mananger_password,secret_name,secret_value):
    try:
        resp = requests.patch('http://'+manager_host+'/api/v3.1/secrets/'+secret_name,
                            json.dumps(dict(
                            value = secret_value,
                            visibility = 'tenant',
                            is_hidden_value = false
                            )),headers={'Tenant':tenant_name,'Content-Type':'application/json'},
                            auth=(manager_username, manager_password))
        ctx.logger.debug('response content {}'.format(resp.content))
        if resp.status_code==200:
            ctx.logger.info('secret was updated successfully')
    except Exception as e:
        raise NonRecoverableError('Exception happned {}'.format(getattr(e, 'message', repr(e))))

@operation
def allocate_ip(manager_host,manager_tenant,manager_username,manager_password,pool_id,**kwargs):
    if pool_id == '':
        ctx.logger.error('pool_id was not provided')
        return;
    try:
        secret = get_secret(manager_host,manager_tenant,manager_username,manager_password,pool_id)
        if not secret:
            ip_to_allocate=''
            ip_addresses = json.loads(secret['value'])
            for ip in ip_addresses:
                if ip['status']=='RELEASED':
                    ip['status']='ALLOCATED'
                    ip_to_allocate=ip['ip_address']
                    ip_to_allocate=result['ip_address']
                    ctx.instance.runtime_properties['ip'] = ip_to_allocate   
                    ctx.instance.runtime_properties['ip_id'] = result['id']
                    ctx.logger.info('ip {} is allocated'.format(ip_to_allocate))
                    secret['value']=ip_addresses
                    secret=json.loads(secret)
                    break;
        if ip_to_allocate == '':
            raise NonRecoverableError('no ips found to allocate')
        else:
            update_secret(manager_host,tenant_name,manager_username,manager_password,pool_id,secret)
    except Exception as e:
        raise NonRecoverableError('Exception happned {}'.format(getattr(e, 'message', repr(e))))


@operation
def unallocate_ip(manager_host,manager_tenant,manager_username,manager_password,pool_id,resource_id,**kwargs):
    if pool_id == '':
        ctx.logger.error('pool_id was not provided')
        return;
    if resource_id == '':
        ctx.logger.error('resource_id was not provided')
        return;
    try:
        secret = get_secret(manager_host,manager_tenant,manager_username,manager_password,pool_id)
        if not secret:
            ip_to_releasee=''
            ip_addresses = json.loads(secret['value'])
            for ip in ip_addresses:
                if ip['id']==resource_id:
                    ip['status']='RELEASED'
                    ip_to_release=ip['ip_address']
                    ctx.logger.info('ip {} is released'.format(ip_to_release))
                    secret['value']=ip_addresses
                    secret=json.loads(secret)
                    break;
        if ip_to_release == '':
            raise NonRecoverableError('no id mapped to ip to release')
        else:
            update_secret(manager_host,tenant_name,manager_username,manager_password,pool_id,secret)
    except Exception as e:
        raise NonRecoverableError('Exception happned {}'.format(getattr(e, 'message', repr(e))))
