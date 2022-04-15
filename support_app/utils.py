from enum import Enum


class EmailType(int, Enum):
    TICKET_CREATION = 1,
    TICKET_STATUS_UPDATE = 2,
    TICKET_NEW_MESSAGE = 3


prepared_mails = {
    EmailType.TICKET_CREATION: 'You created a new ticket! Ticket id: {}, Ticket body: {}',
    EmailType.TICKET_STATUS_UPDATE: 'Your ticket (id: {}) has been set to {} status',
    EmailType.TICKET_NEW_MESSAGE: 'Your ticket (id: {}) has new support answer: {}'
}


def get_prepared_email(email_type: EmailType, *args):
    return prepared_mails[email_type].format(*args)
