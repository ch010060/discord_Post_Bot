# discord_Post_Bot

### Purpose
A discord bot, parse the url link from third party websites and post the message with embedded image thumb into discord channel.

**Install requirements：**
1. Install python3
2. Install pip
```
pip install discord
pip install plurk-oauth
pip install tweepy
pip install requests
pip install bs4
pip install validators
pip install aiofiles
```
3. Fillin the config file with your token => setting.json

### How to use:
```
python bot.py
```

### Support websites:
* Pixiv:    ☑ Single image ☑ Multiple images  ☑ Image for a specific page ☑ Ugoira image
```
https://www.pixiv.net/artworks/12345678
https://www.pixiv.net/artworks/12345678 p2
https://www.pixiv.net/artworks/12345678 all
```
* Twitter:  ☑ Single image ☑ Multiple images ☑ Video
```
https://twitter.com/author/status/123456789012345678980
```
* Plurk:    ☑ Single image ☑ Multiple images
```
https://www.plurk.com/p/abcd12
https://www.plurk.com/p/abcd12 all
```
* EH/EX:    ☑ Gallery cover image thumb	
* Yande:    ☑ Gallery sample image thumb	
* Sankakucomplex:    ☑ Gallery sample image thumb	
* PTT:    ☑ Post top image thumb	

