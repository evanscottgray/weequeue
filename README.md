# weequeue
remote weechat notifications with redis and osx notification center.

## up and running
optionally start a redis instance:
```
# be sure to change up myport and mypass
docker run -d -p $MYPORT:6379 --name redis dockerfile/redis redis-server /etc/redis/redis.conf --requirepass $MYPASS
```

on your weechat instance:
```
# in your python plugins directory $HOME/.weechat/python/
git clone https://github.com/evanscottgray/weequeue && cd weequeue
# install deps
pip install -r requirements.txt
# make a config
cp config.ini.example config.ini
# edit config and fill in redis settings, should be self explanatory
vim config.ini
```

in weechat to load the plugin:
```
/python load weequeue/weequeue.py
```

on your mac:
```
brew install terminal-notifier
git clone https://github.com/evanscottgray/weequeue && cd weequeue
# copy your config.ini from your weechat instance to config.ini here
make_a_config
# install deps
pip install -r requirements.txt
python app.py
```

You should start seeing notifications pop up. For some reason this must be run
 outside of tmux/screen.
