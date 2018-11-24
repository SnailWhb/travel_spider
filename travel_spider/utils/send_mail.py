#!/usr/bin/env python  
# encoding: utf-8  

""" 
@version: v1.0 
@author: whb
@license: Apache Licence  
@contact: 1223934389@qq.com 
@software: PyCharm 
@file: send_mail.py 
@time: 18-11-22 下午5:04 
"""
import smtplib
import os
from contextlib import contextmanager
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage



def send_mail(jokes):
    """发送电子邮件"""
    sender = 'xiongneng@winhong.com'
    receiver = ['xiadan@winhong.com', 'xiongneng@winhong.com']
    subject = '每日笑话'
    smtpserver = 'smtp.263.net'
    username = 'xiongneng@winhong.com'
    password = '******'
    msg_root = MIMEMultipart('related')
    msg_root['Subject'] = subject

    msg_text_str = """
        <h1>笑话网祝你笑口常开。</h1>
        <div class="listbox">
            <ul>
        """
    for idx, (content, img_url) in enumerate(jokes, 1):
        msg_text_str = "\n".join([msg_text_str, '<li>'])
        msg_text_str = "\n".join([msg_text_str, '<p>%s</p>' % content])
        if img_url:
            msg_text_str = "\n".join([msg_text_str, '<p><img src="cid:image%s"/></p>' % idx])
        msg_text_str = "\n".join([msg_text_str, '</li>'])
    msg_text_str = "\n".join([msg_text_str, '</ul>'])
    msg_text_str = "\n".join([msg_text_str, '</div>'])

    msg_text = MIMEText(msg_text_str, 'html', 'utf-8')
    msg_root.attach(msg_text)

    for idx, (_, img_url) in enumerate(jokes, start=1):
        if img_url:
            with open(os.path.join( os.path.basename(img_url)), 'rb') as fp:
                msg_image = MIMEImage(fp.read())
                msg_image.add_header('Content-ID', '<image%s>' % idx)
                msg_root.attach(msg_image)
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg_root.as_string())
    smtp.quit()


@contextmanager
def session_scope(Session):
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()





if __name__ == '__main__':
    pass 