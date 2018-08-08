import email
from email.message import Message
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

from data import dataInstance


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type == 'text/plain' or content_type == 'text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))


def message_to_display(message):
    print_info(message)
    result = ''
    if message.is_multipart():
        for sub_message in message.get_payload():
            result += message_to_display(sub_message)
    else:
        result = f"Content-type: {message.get_content_type()}\n" \
                 f"{message.get_payload()}\n" + "*" * 76 + '\n'
    return result


class CrazySrvHandler:
    dao = dataInstance

    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        mail_from = envelope.mail_from
        rcpt_tos = envelope.rcpt_tos
        # message = Parser().parsestr(envelope.content)
        message = email.message_from_bytes(envelope.content)
        content = message_to_display(message)
        subject = message['Subject']

        obj = {
            "from": mail_from,
            "to": rcpt_tos,
            "subject": subject,
            "content": content
        }

        self.dao.store_msg(obj)

        print(self.dao.read_from(obj['from']))

        return '250 Message accepted for delivery'
