#!python
# run docker on docker hosts with python from windows desktop
# wangfei

import docker

docker_host = 'tcp://54.xx.xx.xx:2375'
docker_image = "wangfeib12/tomcat_prod_v1"
client_version = '1.15'
docker_command = "/opt/tomcat/bin/startup.sh"
docker_volumes = ['/data']
docker_name = "tomcat1"
docker_ports = [8080,22]
port_bindings = {8080:8080,22:2222}

# make connection
docker_client = docker.Client(
        base_url = docker_host, 
        version = client_version, 
        timeout = 10)

# create docker container        
docker_client.create_container(
        image = docker_image,
        stdin_open = True, tty = True,
        command = docker_command,
        volumes = docker_volumes,
        ports = docker_ports,
        name = docker_name)

# start docker container
docker_client.start(
        container = docker_name, 
        binds={docker_volumes[0]:{'bind': docker_volumes[0],'ro': False}},
        port_bindings = port_bindings, lxc_conf=None,
        publish_all_ports=True, links=None, privileged=False,
        dns=None, dns_search=None, volumes_from=None, network_mode=None,
        restart_policy=None, cap_add=None, cap_drop=None)
