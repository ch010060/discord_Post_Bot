import discord
from discord.ext import commands
from core.classes import Cog_Extension
from plurk_oauth import PlurkAPI
import json,random
import requests
import re
from pathlib import Path
import tweepy

from bs4 import BeautifulSoup



class Event(Cog_Extension):
   #以下pixiv
   p1=re.compile('www\.pixiv\.net\/member_illust\.php')
   p2=re.compile('www\.pixiv\.net\/artworks')
   p3=re.compile('www\.pixiv\.net\/en\/artworks')
   #以下twitter
   p4=re.compile('twitter\.com\/(\w{0,60})\/status')
   p5=re.compile('t\.co\/')
   #以下plurk
   p6=re.compile('www\.plurk\.com\/p')
   with open('setting.json','r',encoding='utf8') as jfile:
      jdata=json.load(jfile)
   
   #twitter oauth
   auth = tweepy.OAuthHandler(jdata['consumer_key'], jdata['consumer_secret'])
   auth.set_access_token(jdata['access_token'], jdata['access_token_secret'])
   api = tweepy.API(auth)
   
   #plurk oauth
   plurk = PlurkAPI(jdata['plurk_consumer_key'], jdata['plurk_consumer_secret'])
   plurk.authorize(jdata['plurk_access_token'], jdata['plurk_access_token_secret'])

   @commands.Cog.listener()
   async def on_message(self,msg):
      k=False
      chr={}
      strf=''
      askNum=1
      twitterMedia=None
      print(msg.author,msg.content)
      a=self.p1.search(msg.content)
      if a==None:
         a=self.p2.search(msg.content)
         if a==None:
            a=self.p3.search(msg.content)
      if a!=None:
         k=True
         strf = re.search('\d{3,9}', msg.content[a.start():]).group()

      for i in range(len(msg.embeds)):
         chr=msg.embeds[i].to_dict()

      if k and msg.author!=self.bot.user:
         colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
         uId,uName,illustTitle,illustComment,pageCount=self.pixive(strf)
         if pageCount>1:
            askpage = re.search('p\d{1,2}', msg.content[a.start():])
            allpage = re.search('all', msg.content[a.start():])
            if askpage:
               if int(askpage.group()[1:])<pageCount+1:
                  askNum=int(askpage.group()[1:])
                  embed=discord.Embed(title=illustTitle,url="https://www.pixiv.net/artworks/"+strf, color=colonn)
                  embed.set_image(url="https://pixiv.cat/"+strf+"-"+str(askNum)+".jpg")
                  embed.set_author(name=uName, url="https://www.pixiv.net/users/"+uId)
                  await msg.channel.send(embed=embed)
            elif allpage:
               for c in range(1,pageCount+1):
                  await msg.channel.send("https://pixiv.cat/"+strf+"-"+str(c)+".jpg")
            else:
                  embed=discord.Embed(title=illustTitle,url="https://www.pixiv.net/artworks/"+strf, color=colonn)
                  embed.set_image(url="https://pixiv.cat/"+strf+"-1.jpg")
                  embed.set_author(name=uName, url="https://www.pixiv.net/users/"+uId)
                  await msg.channel.send(embed=embed)
         else:
            embed=discord.Embed(title=illustTitle,url="https://www.pixiv.net/artworks/"+strf, color=colonn)
            embed.set_image(url="https://pixiv.cat/"+strf+".jpg")
            embed.set_author(name=uName, url="https://www.pixiv.net/users/"+uId)
            await msg.channel.send(embed=embed)
         try:
            await msg.edit(suppress=True)
         except:
            print('沒有關閉embed的權限')
      #以下twitter
      a=self.p4.search(msg.content)
      if a!=None:
         strf = re.search('\d{15,20}', msg.content[a.start():]).group()
         status = self.api.get_status(strf, tweet_mode="extended")
         try:
            twitterMedia=status.extended_entities['media']
            k=True
         except AttributeError:  #twitter沒圖片
            pass
         if k and msg.author!=self.bot.user:
            if len(status.extended_entities['media'])==1:
               try:
                  twitterMedia=status.extended_entities['media'][0]['video_info']
                  await msg.channel.send(twitterMedia['variants'][0]['url'])
               except KeyError:  #twitter沒影片
                  pass
                  
            else:
               colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
               uId=status.user.screen_name
               uName=status.user.name
               illustTitle=status.full_text
               a=self.p5.search(illustTitle)
               illustTitle=illustTitle[:a.start()-9]
               embed=discord.Embed(title=illustTitle,url="https://twitter.com/"+uId+"/status/"+strf, color=colonn)
               embed.set_image(url=twitterMedia[0]['media_url_https'])
               embed.set_author(name=uName, url="https://twitter.com/"+uId)
               await msg.channel.send(embed=embed)
               for i in range(1,len(status.extended_entities['media'])):
                  await msg.channel.send(twitterMedia[i]['media_url_https'])
               try:
                  await msg.edit(suppress=True)
               except:
                  print('沒有關閉embed的權限')
      #以下plurk
      a=self.p6.search(msg.content)
      if a!=None:
         url = re.search("(?P<url>https?://www.plurk.com/p/[^\s]{6})", msg.content).group("url")
         plurk_id = int((url.rsplit('/', 1)[-1]), 36)
         json_object_string = self.plurk.callAPI('/APP/Timeline/getPlurk', options={'plurk_id': plurk_id})
         owner_id = json_object_string['plurk']['owner_id']
         nick_name = json_object_string['plurk_users'][str(owner_id)]['nick_name']
         if json_object_string:
             content_string = json_object_string['plurk']['content']
             try:
                 image_url = re.search("(?P<url>https?://images.plurk.com/[^\s]+.(?:png|jpg|gif))", content_string).group("url")
                 colonn = random.randint(0,255)*65536+random.randint(0,255)*256+random.randint(0,255)
                 embed=discord.Embed(title='plurk',url=url, color=colonn)
                 embed.set_image(url=image_url)
                 embed.set_author(name=nick_name, url="https://www.plurk.com/"+nick_name)
                 await msg.channel.send(embed=embed)
                 allpage = re.search('all', msg.content[a.start():])
                 if allpage:
                    image_urls = re.findall("(?P<url>https?://images.plurk.com/(?!mx_)[^\s]+.(?:png|jpg|gif))", content_string, re.DOTALL)
                    image_urls_dedupe = []
                    for index in range(len(image_urls)):
                        if image_urls[index] not in image_urls_dedupe:
                            image_urls_dedupe.append(image_urls[index])
                    list_len = len(image_urls_dedupe)
                    if list_len > 1:
                        for index in range(1, list_len):
                            await msg.channel.send(image_urls_dedupe[index])
                 """
                 try:
                    await msg.edit(suppress=True)
                 except:
                    print('沒有關閉embed的權限')
                 """
             except AttributeError:  #plurk沒圖片
                 print("image url not found")
                 pass
         else:
             print("plurk not found")
             pass
            
   def pixive(self,strf):
      r =  requests.get("https://www.pixiv.net/artworks/"+strf,headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'})
      soup = BeautifulSoup(r.text, 'html.parser')
      content2=soup.find_all('meta')
      str1=content2[25].get('content')
      str1=str1.replace('false','\"false\"').replace('true','\"true\"').replace('null','\"null\"')

      jdata=json.loads(str1)
      return jdata['illust'][strf]['userId'],jdata['illust'][strf]['userName'],jdata['illust'][strf]['illustTitle'],jdata['illust'][strf]['illustComment'],jdata['illust'][strf]['pageCount']
      

def setup(bot):
   bot.add_cog(Event(bot))