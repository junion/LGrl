import logging
import logging.handlers
 
class TlsSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        """
        Emit a record.
 
        Format the record and send it to the specified addressees.
        """
        try:
            import smtplib
            import string # for tls add this line
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                            self.fromaddr,
                            string.join(self.toaddrs, ","),
                            self.getSubject(record),
                            formatdate(), msg)
            if self.username:
                smtp.ehlo() # for tls add this line
                smtp.starttls() # for tls add this line
                smtp.ehlo() # for tls add this line
                smtp.login(self.username, self.password)
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()
#        except (KeyboardInterrupt, SystemExit):
#            raise
        except:
            pass
#            self.handleError(record)
 
#logger = logging.getLogger()
# 
#gm = TlsSMTPHandler(("smtp.gmail.com", 587), 'junion.sjlee@gmail.com', ['junion.sjlee@gmail.com'], 'Error found!', ('junion.sjlee@gmail.com', 'w1dPtnsla'))
#gm.setLevel(logging.ERROR)
# 
#logger.addHandler(gm)

def sendMail(subject,text=None):
    import os
    import smtplib
    import mimetypes
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email.MIMEAudio import MIMEAudio
    from email.MIMEImage import MIMEImage
    from email.Encoders import encode_base64
    
    gmailUser = 'letsgoreport@gmail.com'
    gmailPassword = 'letsgo!@#'
    recipient = 'letsgoreport@gmail.com'
    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = subject
    if text == None:
        text = subject
    msg.attach(MIMEText(text))
    mailServer = smtplib.SMTP('smtp.gmail.com',587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser,gmailPassword)
    mailServer.sendmail(gmailUser,recipient,msg.as_string())
    mailServer.close()
    print('Sent email to %s' % recipient)
    
#sendMail('x','y')