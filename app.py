import json
import time
import utils
from pync import Notifier as n


def get_private_messages(rc):
    messages = set()
    p = rc.pipeline()
    for i in range(rc.llen('messages')):
        p.rpop('messages')
    for redis_data in p.execute():
        messages.add(redis_data)
    return messages


def get_highlights(rc):
    highlights = set()
    p = rc.pipeline()
    for i in range(rc.llen('highlights')):
        p.rpop('highlights')
    for redis_data in p.execute():
        highlights.add(redis_data)
    return highlights


def main(rc):
    while True:
        highlights = get_highlights(rc=rc)
        messages = get_private_messages(rc=rc)
        for highlight in highlights:
            highlight = json.loads(highlight)
            title = 'IRC Highlight: %s' % highlight.get('channel')
            msg = '%s  - %s' % (highlight.get('message'),
                                highlight.get('sender'))
            n.notify(msg, sound='default', title=title)
        for message in messages:
            message = json.loads(message)
            title = 'IRC Privmsg from %s' % message.get('sender')
            msg = message.get('message')
            n.notify(msg, sound='tink', title=title)
        time.sleep(3)

if __name__ == '__main__':
    rc = utils.get_redis_client()
    main(rc)
