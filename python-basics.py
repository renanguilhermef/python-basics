import socket,csv,os.path,nmap
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ping3 import ping

class sendEmail: 
    def __init__(self,hostSMTP,port,myemail,password = None):
        self.hostSMTP = hostSMTP
        self.port = port 
        self.myemail = myemail
        self.password = password 

        self.smtp = smtplib.SMTP(host=hostSMTP, port=port)
        self.smtp.starttls()
        if self.password != None and self.password != "":
            self.smtp.login(myemail,password)

    def sendMSG(self,to,subject,body_message):
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.myemail
            message["To"] = to
            message.attach(MIMEText(body_message,"plain"))
            self.smtp.sendmail(message["From"] , message["To"], message.as_string())
            print ("Email sent successfully!")
        except Exception as ex: 
            print("Error: ", ex)

class domainCheck:

    def __init__(self,hostDomain,smtpServer,smtpPort,emailSender,emailReceiver,emailSenderPass = None):
        self.hostDomain = hostDomain
        self.smtpServer =smtpServer
        self.smtpPort = smtpPort 
        self.emailSender = emailSender 
        self.emailReceiver = emailReceiver
        self.emailSenderPass = emailSenderPass


    def createCSV(self,csvFile,*args):
        if os.path.isfile(csvFile):
            with open(csvFile, 'a', newline='') as file:
                existcsv = csv.writer(file)
                existcsv.writerow(args[1])              
        else:
            with open(csvFile, 'w', newline='') as file:
                newcsv = csv.writer(file)
                newcsv.writerow(args[0])
                newcsv.writerow(args[1])

    def checkSocket(self,port):
        s = socket.socket() 
        msg = None 
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            s.connect((self.hostDomain,port))
        except socket.error as err:
            msg = "Error:" + str(err)
            e = sendEmail(self.smtpServer,self.smtpPort,self.emailSender,self.emailSenderPass)
            e.sendMSG(self.emailReceiver,"Socket failed", "Server: " + self.hostDomain + " port: " + str(port) + " msg: " + msg)   
        else:
            msg = "Success: " + self.hostDomain  + ":" + str(port)   
        finally: 
            self.createCSV("socket_servers.csv",["Server:Port", "MSG", "DateTime"],[self.hostDomain + ":" + str(port), msg, now])
    
    def checkPort(self,port_range,nmap_path = None):
        nmap_path = [nmap_path,]
        portScanner = nmap.PortScanner(nmap_search_path=nmap_path) if nmap_path else nmap.PortScanner()
        portScanner.scan(self.hostDomain,str(port_range))
        if portScanner.all_hosts():
            hostIP = portScanner.all_hosts()[0]
            for protocol in portScanner[hostIP].all_protocols():
                ports  = portScanner[hostIP][protocol].keys()         
                for port in ports:
                    state = portScanner[hostIP][protocol][port]['state']
                    self.createCSV("namp_domains.csv",["Domain:Port-Range", "ScanPortResult"],[self.hostDomain + ":" + str(port_range), "Port: " + str(port) +  " Protocol : " + protocol + " State: " + state])
        else:
            self.createCSV("namp_domains.csv",["Domain:Port-Range", "ScanPortResult"],[self.hostDomain + ":" + str(port_range), "Host domain not found"])

    def checkPing(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pingble = ping(self.hostDomain) 
        status = "Success" if pingble else "Failed" 
        self.createCSV("ping_domains.csv",["Domain", "Ping", "DateTime"],[self.hostDomain,status,now])
        if status == "Failed":
            e = sendEmail(self.smtpServer,self.smtpPort,self.emailSender,self.emailSenderPass)
            e.sendMSG(self.emailReceiver,"Ping failed", "Ping failed for the server domain: " + self.hostDomain)   
