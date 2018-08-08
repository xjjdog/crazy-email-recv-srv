import email
from email.message import Message
from data import dataInstance


def message_to_display(message: Message):
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
        message: Message = email.message_from_bytes(envelope.content)
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
