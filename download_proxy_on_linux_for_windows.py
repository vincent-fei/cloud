import paramiko
import os
# running on Windows env
# use pem to login ec2 instance from windows desktop

#download information
object_url = r"http://dldir1.qq.com/music/clntupate/QQMusic_Setup_1152.exe"
object_name = os.path.basename(object_url)

# login information
hostname = '10.127.x.x'
username = 'wangfei'
password = 'xxxxxxxxxxxxx'

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=hostname,username=username,password=password)
print "Now begin to download through remote linux server"
command = "wget -O " + object_name + " " + object_url
ssh.exec_command(command)
ssh.close()

t = paramiko.Transport((hostname, 22))
t.connect(username=username,password=password)
sftp = paramiko.SFTPClient.from_transport(t)

remote_path = '/home/' + username + '/' + object_name
local_path = r"E:\Download" + os.sep + object_name

print "Now download to local desktop from remote linux"
sftp.get(remote_path, local_path)
t.close
print object_name + ' download to ' + local_path
