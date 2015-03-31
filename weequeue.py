import weechat
import json
import utils

SCRIPT_NAME = 'weequeue'
SCRIPT_AUTHOR = 'Evan Gray <evanscottgray@gmail.com>'
SCRIPT_VERSION = '0.0.1'
SCRIPT_LICENSE = 'MIT'
SCRIPT_DESC = 'Pop notifications onto a redis list to be scooped up later.'

weechat.register(SCRIPT_NAME, SCRIPT_AUTHOR, SCRIPT_VERSION, SCRIPT_LICENSE,
                 SCRIPT_DESC, '', '')

r = utils.get_redis_client()


def add_highlight(message, sender, channel):
    hl = {'sender': sender, 'channel': channel, 'message': message}
    r.lpush('highlights', json.dumps(hl))


def add_message(message, sender):
    msg = {'sender': sender, 'message': message}
    r.lpush('messages', json.dumps(msg))


DEFAULT_OPTIONS = {'show_highlights': 'on',
                   'show_private_message': 'on',
                   'show_message_text': 'on',
                   'sound': 'off',
                   }

for key, val in DEFAULT_OPTIONS.items():
        if not weechat.config_is_set_plugin(key):
                weechat.config_set_plugin(key, val)

weechat.hook_print('', 'irc_privmsg', '', 1, 'notify', '')


def notify(data, buffer, date, tags, displayed, highlight, prefix, message):
    if weechat.config_get_plugin('show_highlights') == 'on' and int(highlight):
        channel = weechat.buffer_get_string(buffer, 'localvar_channel')
        if weechat.config_get_plugin('show_message_text') == 'on':
            add_highlight(message, sender=prefix, channel=channel)
        else:
            add_highlight('New Highlight', channel=channel)
    elif (weechat.config_get_plugin('show_private_message') == 'on'
          and 'notify_private' in tags):
        if weechat.config_get_plugin('show_message_text') == 'on':
            add_message(message, sender=prefix)
        else:
            add_message('New Private Message', sender=prefix)
    return weechat.WEECHAT_RC_OK
