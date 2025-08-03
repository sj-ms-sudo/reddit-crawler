import requests
from requests.auth import HTTPBasicAuth
import argparse
def getToken():
    auth = HTTPBasicAuth('erglCaUSGQdinGQuLi7ANg','EBsM-iPGsgWk24LXdRw57CfyxaTbgQ')
    data = {'grant_type':'password','username':'Shot-Hippo1134','password':'Reddit@123'}
    headers = {'User-Agent': 'red_crawl/0.1 by Shot-Hippo1134'}
    res = requests.post('https://www.reddit.com/api/v1/access_token',auth=auth,data=data,headers=headers)
    return res.json()["access_token"]
def crawlprint(url,keyword,save=None): 
    TOKEN = getToken()
    headers = {'Authorization':f'Bearer {TOKEN}','User-Agent': 'red_crawl/0.1 by Shot-Hippo1134'}
    response = requests.get(url,headers=headers)
    try:
        posts = response.json()['data']['children']
    except Exception as e:
        print(" Failed to fetch posts. Reason:", e)
        return
    flag = 0
    for post in posts:
        title = post['data']['title']
        matched = [kw for kw in keyword if kw in title.lower()]
        if matched:
            if not save:
                print(f"matched keywords    :   {','.join(matched)}")
                print(f"title   :   {title}")
                print(f"url     :   {post['data']['url']}")
                print(f"score   :   {post['data']['score']}")
                print(f"ups :   {post['data']['ups']}")
                print(f"downs   :   {post['data']['downs']}")
            else:
                flag+=1
                with open (save,'a')as file:
                    file.write(f"matched keywords    :   {','.join(matched)}\n")
                    file.write(f"title   :   {title}\n")
                    file.write(f"url     :   {post['data']['url']}\n")
                    file.write(f"score   :   {post['data']['score']}\n")
                    file.write(f"ups :   {post['data']['ups']}\n")
                    file.write(f"downs   :   {post['data']['downs']}\n\n")
    if flag!=0:
        print(f"{flag} items saved to {str(save)}")
if __name__ =="__main__":
    parser = argparse.ArgumentParser(description="Reddit Crawler")
    parser.add_argument("subreddit",help = "The name of the subreddit")
    parser.add_argument("-k",nargs= '+',help = "Give the keywords")
    parser.add_argument("-s",type=str,help = "Specify file name to save")
    args = parser.parse_args()
    url =  f'https://oauth.reddit.com/r/{args.subreddit}/new'
    if args.s:
        crawlprint(url,args.k,args.s)
    else:
        crawlprint(url,args.k)