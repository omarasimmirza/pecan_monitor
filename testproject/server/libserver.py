import paramiko 
import smtplib, ssl
from email.message import EmailMessage
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

class SystemCheck:
    def __init__(self, ip=None, port=None, user=None, password=None, mail=None):
        self.ip = ip 
        self.port = port 
        self.user = user 
        self.password = password 
        self.mail = mail
        self.alert = []
    
    def __repr__(self):
        return f'alerts: {self.alert}'

    def print_self(self):
        print(self.ip)
        print(self.port)
        print(self.user)
        print(self.password)
        print(self.mail)

    def upload_file(self):
        client_file = "info_client.py"
        client_lib = "libclient.py"
        path_file = r"C:\Users\Administrator\Desktop\pecan-tutorial\test-project\testproject\client\info_client.py"
        path_lib = r"C:\Users\Administrator\Desktop\pecan-tutorial\test-project\testproject\client\libclient.py"
        try:
            client = paramiko.Transport((self.ip, self.port))
            client.banner_timeout = 10
            client.connect(username=self.user, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(client)
            sftp.mkdir('upload')
            sftp.chdir('upload')
            sftp.put(path_file, client_file)
            sftp.put(path_lib, client_lib)
            sftp.close()
            client.close()
        except Exception as e:
            print(e)

    def decrypt_data(self, key, data):
        decrypt = Fernet(key.encode())
        return decrypt.decrypt(data.encode()).decode()

    def convert_time(self, time):
        day = time // (24 * 3600)
        time = time % (24 * 3600)
        hour = time // 3600
        time %= 3600
        minutes = time // 60
        time %= 60
        seconds = time
        print(f"{day} day(s) {hour} hour(s) {minutes} minute(s) {seconds} second(s)")

    def ssh_connect(self):
        out_list = []
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.ip, self.port, self.user, self.password)
        self.upload_file()       
        stdin, stdout, stderr = client.exec_command("cd upload/;python3 info_client.py")

        for lines in stdout.readlines():
            out_list.append(lines)

        for lines in stderr.readlines():
            print(lines)

        result_str = self.decrypt_data(out_list[0], out_list[1])
        result_list = result_str.split(':', -1)
        client.exec_command('sudo rm -rf upload/')
        client.close()
        return result_list

    def email_user(self, machine):
        load_dotenv()
        sender_email = str(os.environ.get('email_app_sender'))  # Enter your address
        receiver_email = str(self.mail)  # Enter receiver address
        password = str(os.environ.get('email_app_pass'))
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"

        message = "[ALERT]\n\n"
        for alerts in self.alert:
            for key, val in alerts.items():
                if (val == 'cpu'):
                    alerts['limit'] = float(alerts['limit'][:-1])
                    print(alerts['limit'])
                    if (alerts['limit'] < float(machine.cpu_usage)):
                        message += f'{val} usage is over the limit: {alerts["limit"]}%\nIt is at {machine.cpu_usage[:5]}%\n'
                elif (val == 'memory'):
                    print(alerts['limit'])
                    alerts["limit"] = float(alerts["limit"][:-1])
                    if (alerts["limit"] < float(machine.memory_usage)):
                        message += f'{val} usage is over the limit: {alerts["limit"]}%\nIt is at {machine.memory_usage[:5]}%\n'

        print(message)
        if message != "[ALERT]\n\n":
            print(message)
            msg = EmailMessage()
            msg.set_content(message)
            msg['Subject'] = 'Python Crossover Project'
            msg['From'] = sender_email
            msg['To'] = receiver_email
            context = ssl.create_default_context()
            
            with smtplib.SMTP(smtp_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, msg.as_string())