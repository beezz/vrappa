#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Miscellaneous helpfull classes based on :class:`vrappa.VrappaBase`.
"""

import pprint
import smtplib
import datetime
import traceback
from email.MIMEText import MIMEText

from . import VrappaBase


SMTP_CONF_DEFAULT = {
    'host': 'localhost',
    'port': 25,
    'login': None,
    'password': None,
    'tls': False,
}

MAIL_CONF_DEFAULT = {
    'sender': 'root@localhost',
    'msg_fmt': (
        u"[{timestamp}][{app}]\n"
        u"Arguments: {args}\n"
        u"Keyword arguments: {kwargs}\n\n"
        u"{exc_tb}\n"
    ),
    'subject_fmt': u"[{app}]: {exc_str}",
    'recipients': [
        'root@localhost',
    ],
}


class EmailOnException(VrappaBase):

    def __init__(
        self,
        app_str=None,
        smtp_conf=None,
        mail_conf=None,
        catch=(Exception, ),
        **kwargs
    ):
        self.app_str = app_str
        self.smtp_conf = smtp_conf or SMTP_CONF_DEFAULT
        self.mail_conf = mail_conf or MAIL_CONF_DEFAULT
        super(EmailOnException, self).__init__(catch=catch, **kwargs)

    def get_subject_fmt(self, exc, args=None, kwargs=None):
        return self.mail_conf['subject_fmt']

    def get_msg_fmt(self, exc, args=None, kwargs=None):
        return self.mail_conf['msg_fmt']

    def get_fmt_dict(self, exc, args=None, kwargs=None):
        return {
            'timestamp': datetime.datetime.isoformat(
                datetime.datetime.utcnow()
            ),
            'app': self.app_str,
            'exc_str': str(exc),
            'exc_tb': traceback.format_exc(limit=30),
            'args': pprint.pformat(args),
            'kwargs': pprint.pformat(kwargs),
        }

    def get_recipients(self, exc, args=None, kwargs=None):
        return self.mail_conf['recipients']

    def get_to_field(self, exc, args=None, kwargs=None):
        return ','.join(self.mail_conf['recipients'])

    def get_from_field(self, exc, args=None, kwargs=None):
        return self.mail_conf['sender']

    def build_message(self, exc, args=None, kwargs=None):
        fmt_dict = self.get_fmt_dict(exc, args=args, kwargs=kwargs)
        msg = MIMEText(
            self.get_msg_fmt(exc, args=args, kwargs=kwargs).format(**fmt_dict)
        )
        msg['Subject'] = self.get_subject_fmt(
            exc, args=None, kwargs=None,
        ).format(**fmt_dict)
        msg['To'] = self.get_to_field(exc, args=args, kwargs=kwargs)
        msg['From'] = self.get_from_field(exc, args=args, kwargs=kwargs)
        return msg

    def get_server_connection(self, exc, args=None, kwargs=None):
        session = smtplib.SMTP(
            self.smtp_conf.get('host', 'localhost'),
            self.smtp_conf.get('port', 25),
        )
        is_tls = self.smtp_conf.get('tls')
        if is_tls:
            session.ehlo()
            session.starttls()
            session.ehlo()
        if self.smtp_conf.get('login') and self.smtp_conf.get('password'):
            session.login(
                self.smtp_conf.get('login'),
                self.smtp_conf.get('password'),
            )
        return session

    def action(self, exc, args=None, kwargs=None):
        msg = self.build_message(exc, args=args, kwargs=kwargs)
        try:
            server = self.get_server_connection(
                exc, args=args, kwargs=kwargs,
            )
            server.sendmail(
                self.get_from_field(exc, args=args, kwargs=kwargs),
                self.get_recipients(exc, args=args, kwargs=kwargs),
                msg.as_string(),
            )
        finally:
            server.quit()
