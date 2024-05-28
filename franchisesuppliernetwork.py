import requests
from requests import Session
from bs4 import BeautifulSoup as bs
from lxml import html
import pandas as pd
s = Session()
s.headers['user-agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:10Gecko/20100101 Firefox/104.0'


def Every_Post_Page(url):
    r = s.get(url)
    tree = tree = html.fromstring(r.text)
    Post_Image = ''.join(tree.xpath('//img[@class ="attachment-post-thumbnail size-post-thumbnail wp-post-image"]/@src'))
    Post_detials = ''.join(tree.xpath('//div[@class ="col-sm-12"]//p//text()')).strip()
    Post_Publish_time = ''.join(tree.xpath('//a//time[@class = "entry-date published"]//text()'))
    Post_Publish_By = ''.join(tree.xpath('//div[@class="post_info"]//span[@class = "author vcard"]//text()'))

    return  {
        'Post_Image':Post_Image,
        'Post_detials':Post_detials,
        'Post_Publish_time':Post_Publish_time,
        'Post_Publish_By':Post_Publish_By
    }
    

All_Data =[]
def listpage():    
    Page = 1
    while True:
        url = f'https://franchisesuppliernetwork.com/resources/page/{Page}/?resource_type=all'
        r = s.get(url)
        tree = tree = html.fromstring(r.text)
        All_Posts = tree.xpath('//div[@class = "news-container blogpage"]//div[@class = "single-news Post" or @class ="single-news Podcast"]')
        if All_Posts:
            for posts in All_Posts:
                Image = ''.join(posts.xpath('.//img/@src'))
                InCetgoary = ''.join(posts.xpath('.//div[@class="lncategory"]//text()'))
                Heading = ''.join(posts.xpath('.//h3//text()'))
                Post_link = ''.join(posts.xpath('.//a/@href'))
                
                detail = Every_Post_Page(Post_link)

                data = {
                    'main_Url':url,
                    'Page':Page,
                    'Image':Image,
                    'InCetgoary':InCetgoary,
                    'Heading':Heading,
                    'Post_link':Post_link,
                    'Post_Image':detail['Post_Image'],
                    'Post_detials':detail['Post_detials'],
                    'Post_Publish_time':detail['Post_Publish_time'],
                    'Post_Publish_By':detail['Post_Publish_By']

                }
             

                All_Data.append(data)
                print(All_Data)
        else:
            break
        Page += 1
        

listpage()
df = pd.DataFrame(All_Data)
df.to_excel('All_franchisesuppliernetwork.xlsx',index=False)
