import paramiko
import os
# running on Windows env
# use pem to login ec2 instance from windows desktop

hostname = 'git.xxxxxx.com'
username = 'ec2-user'
private_key = os.sys.path[0] + os.sep + 'ec2-user_for_xxxxx.pem'
key = paramiko.RSAKey.from_private_key_file(private_key)

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname,username=username,pkey=key)
stdin,stdout,stderr = ssh.exec_command('df -h')
print stdout.read()
print stderr.read()
ssh.close()
