# resource_pool_secrets_plugin
A plugin that uses cfy secrets to allocate_ip/unallocate_ip for a node to install cloudify agent


**Note: before using any cfy command we must check if we set the profile first

command is : 
```
cfy profiles use [cloudify_server_ip] -u [cloudify_username] -p [cloudify_password] -t [cloudify_tenant]
```

Installation Steps to Simulate the Environment:
------------------------------------------------
in order to create the environment that will hold 3 servers 
and that is done by using the ``` openstack_server_create_blueprint ``` and make sure that the deployment of ``` openstack-example-network ``` is installed on the environment

using the following command :

navigate the plugin direcoty 

```
cfy install ./openstack_server_create_blueprint/openstack-resource-pool-env-setup.yaml -d resource-pool-deployment -b resource-pool-blueprint 
```

Plugin Installation Steps:
--------------------------
first we have to install cloudify-common 

``` pip install -r dev-requirements.txt ```
 
then we want to create the wagon file (used when we try to upload the plugin to the local environment)

``` pip install wagon ```

**Note: You might get dependancies error in case that happens ( sudo yum install -y python-devel )

navigate to the plugin directory

``` wagon create . ```

the above command will generate a wagon file that we will use to upload the plugin 

using the following command : ``` cfy plugins upload -y plugin.yaml [wagon_file_name from the previous step] ```

if we want to use it in the testing blueprint we need to modify the import of ``` test_plugin.yaml ```
by changing the github link with : ``` plugin: [uploaded_plugin_name] ```
and we can get the name using the following command ``` cfy plugins list ```

Plugin Testing Steps:
---------------------

before testing the plugin we need to check the servers on the openstack if they are up and what is their ips and call a script to add them to cfy secrets resource

using the following script : ``` add_sample_data.py ``` 

we can get the IPs using the following command :

``` cfy deployments outputs resource-pool-deployment ```

we can test the plugin using the following command :

navigate to plugin directory

```
cfy install ./test_plugin.yaml -d resource-pool-plugin-test-deployment -b resource-pool-plugin-blueprint -i manager_host_ip= [cfy host] -i manager_tenant = [ cfy tenant ] -i manager_username = [ cfy username ] -i manager_password [ cfy password ] -i ip_pool_id= [the id of pool passed to add_sample_data.py]
```
