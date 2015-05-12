import utils
from pushbullet import Pushbullet

conf = utils.parse_config()
api_key = conf.get('pushbullet_api_key') 
pb = Pushbullet(api_key)


def get_device_name(d):
    # Instead of using str we have to do this for reasons I don't understand
    nn = d.__dict__.get('nickname')
    return nn


def get_devices(notifiable_devices=conf.get('pushbullet_devices')):
    reachable_devices = pb.devices
    devices_to_notify = []
 
    if type(notifiable_devices) == str:
        devices_to_notify = [d for d in reachable_devices 
                             if notifiable_devices in get_device_name(d)]
    else:
        for nd in notifiable_devices:
            d = [d for d in reachable_devices 
                 if nd == get_device_name(d)]
            devices_to_notify.extend(d)
    return devices_to_notify


def pb_notify(msg):
    if utils.boolify(conf.get('pushbullet_notify')):
        notify(msg)


def notify(msg):
    devices = get_devices()
    title = None
    txt = None

    if 'channel' in msg:
        title = '%s in %s: %s' % (msg.get('sender'),
                                  msg.get('channel'), 
                                  msg.get('message'))
        txt = '%s  - %s' % (msg.get('message'),
                            msg.get('sender'))
    else:
        title = 'PM from %s' % msg.get('sender')
        txt = msg.get('message')

    for d in devices:
        d.push_note(title, txt)
