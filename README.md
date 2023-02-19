# python-basics

Install requirements:

    pip install -r requirements.txt
    
Class sendEmail:

Init:

    hostSMP = Inform your host smtp of your email #Required
    port = Inform your host smtp port #Required
    myemail = Inform my email to be sender #Required
    password = Inform your email if required #Optional
    
Function sendMSG:

    to = Inform who is going to receive email #Required
    subject = Inform email subject #Required
    body_message = Inform email message #Required
    
How to use class example:
  
  With passsword:
  
    e = sendEmail(<SMTP_SERVER>,<SMTP_PORT>,<MY_EMAIL>,<MY_PASSWORD>)
    e.sendMSG(<EMAIL_DESTINATION>,<MY_SUBJECT>, <MY_BODY_MESSAGE>) 
  
  With no password:
    
    e = sendEmail(<SMTP_SERVER>,<SMTP_PORT>,<MY_EMAIL>)
    e.sendMSG(<EMAIL_DESTINATION>,<MY_SUBJECT>, <MY_BODY_MESSAGE>)   
    
Class domainCheck:

Init:

    hostDomain = Inform hostdomain to check #Required
    smtpServer = Inform  smtp server #Required
    smtpPort = Inform  smtp server port #Required 
    emailSender = Inform sender email  #Required
    emailReceiver = Inform email receiver #Required 
    emailSenderPass = Inform sender email password #Optional 
    
Function checkSocket:
    
    port = Inform which port to check server socker #Required 
    
Function checkPort:
  It is required to install nmap in your machine 
  
    port_range: inform a port or a range port. Example : 22, "22-90" #Required
    nmap_path: Inform nmap path install location #Optional
    
Function checkPing:
  No extra parameters needed 
  

How to use class example:

    for domain in ['186.202.153.153', 'www.google.com.br', 'minhacasa.edu.br']:
      s = domainCheck(domain,<SMTP_SERVER>,<SMTP_PORT>,<MY_EMAIL>,<MY_PASSWORD>)
      s.checkSocket(22)
      s.checkPort("22-100",r"C:\Program Files (x86)\Nmap\nmap.exe")
      s.checkPing()

  
    
