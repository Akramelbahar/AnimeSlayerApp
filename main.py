from flask import Flask, render_template, render_template_string , request
import requests
import json
import base64
import datetime


def getIp() :
    return str(requests.get("http://ip-api.com/json").json()["query"])
ip = getIp()
app = Flask(__name__)

def getPublishedAnimeByLast(page):
    ##THE OUTPUT IS ARRAY OF NEW UPDTAES .
    
    headers = {
        "client-id":"android-app2",
        "client-secret":"7befba6263cc14c90d2f1d6da2c5cf9b251bfbbd",
        "user-agent": "okhttp/3.12.13"
    }
    req = requests.get('https://anslayer.com/anime/public/animes/get-published-animes?json={"_offset":'+f'{page*30}'+',"_limit":30,"_order_by":"latest_first","list_type":"latest_updated_episode_new","just_info":"Yes"}' , headers=headers)
    if req.status_code == 200 :
        return (req.json()["response"]["data"])
    else :
        print("ERROR IN getPublishedAnimeByLast status code not equal to 200")
        exit()

def getPublishedAnimeALL(page):
   
    
    headers = {
        "client-id":"android-app2",
        "client-secret":"7befba6263cc14c90d2f1d6da2c5cf9b251bfbbd",
        "user-agent": "okhttp/3.12.13"
    }
    req = requests.get('https://anslayer.com/anime/public/animes/get-published-animes?json={"_offset":'+f'{page*30}'+',"_limit":30,"_order_by":"latest_first","list_type":"anime_list","just_info":"Yes"}' , headers=headers)
    if req.status_code == 200 :
        return (req.json()["response"]["data"])
    else :
        print("ERROR IN getPublishedAnimeByLast status code not equal to 200")
        exit()


def getPublishedAnimeRatingMal(page):
   
    
    headers = {
        "client-id":"android-app2",
        "client-secret":"7befba6263cc14c90d2f1d6da2c5cf9b251bfbbd",
        "user-agent": "okhttp/3.12.13"
    }
    req = requests.get('https://anslayer.com/anime/public/animes/get-published-animes?json={"_offset":'+f'{page*30}'+',"_limit":30,"_order_by":"latest_first","list_type":"top_anime_mal","just_info":"Yes"}' , headers=headers)
    if req.status_code == 200 :
        return (req.json()["response"]["data"])
    else :
        print("ERROR IN getPublishedAnimeByLast status code not equal to 200")
        exit()


def getPublishedAnimeRating(page):
   
    
    headers = {
        "client-id":"android-app2",
        "client-secret":"7befba6263cc14c90d2f1d6da2c5cf9b251bfbbd",
        "user-agent": "okhttp/3.12.13"
    }
    req = requests.get('https://anslayer.com/anime/public/animes/get-published-animes?json={"_offset":'+f'{page*30}'+',"_limit":30,"_order_by":"latest_first","list_type":"top_anime","just_info":"Yes"}' , headers=headers)
    if req.status_code == 200 :
        return (req.json()["response"]["data"])
    else :
        print(req.text)
        print('https://anslayer.com/anime/public/animes/get-published-animes?json={"_offset":'+f'{page*30}'+',"_limit":30,"_order_by":"latest_first","list_type":"top_anime","just_info":"Yes"}')
        print("ERROR IN getPublishedAnimeByLast status code not equal to 200")
        exit()

def getByName(name):
   
    
    headers = {
        "client-id":"android-app2",
        "client-secret":"7befba6263cc14c90d2f1d6da2c5cf9b251bfbbd",
        "user-agent": "okhttp/3.12.13"
    }
    req = requests.get('https://anslayer.com/anime/public/animes/get-published-animes?json={"_offset":0,"_limit":100,"_order_by":"latest_first","list_type":"top_anime","anime_name":"'+str(name)+'","just_info":"Yes"}' , headers=headers)
    if req.status_code == 200 :
        return (req.json()["response"]["data"])
    else :
        #print(req.text)
        print('https://anslayer.com/anime/public/animes/get-published-animes?json={"_offset":0,"_limit":100,"_order_by":"latest_first","list_type":"top_anime","anime_name":"'+str(name)+'","just_info":"Yes"}' )
        print("ERROR IN getPublishedAnimeByLast status code not equal to 200")
        exit()


def getAnimeDetails(id):
    headers = {
        "client-id":"android-app2",
        "client-secret":"7befba6263cc14c90d2f1d6da2c5cf9b251bfbbd",
        "user-agent": "okhttp/3.12.13"
    }
    req = requests.get("https://anslayer.com/anime/public/anime/get-anime-details?anime_id="+str(id)+"&fetch_episodes=Yes&more_info=No" , headers=headers)
    open("PtrGetAnimeDetails.txt","w").write(str(req.json()))
    return (req.json())


def cardGen(cover, name, epCount, vote,id):
    return f""" 
   
        <a href="/get-anime-details={id}"><div class="anime-card">
            <img src="{cover}" alt="{name}">
            <div class="anime-info">
                <h3>{name}</h3>
                <p>{epCount}</p>
                <p>⭐ {vote}</p>
            </div>
        </div></a>
   
    """

def episodeCardGen(ep, epn, anime_id):
    return f"""
    <form method="post" action="/watch/{anime_id}/">
        <input type="hidden" name="epn" value="{epn}">
        <button type="submit">
            <li>{ep}</li>
        </button>
    </form>
    """
app = Flask(__name__)
def getYear():
    return datetime.datetime.now().year
@app.route("/",)
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 30
    total = 3000
    total_pages = (total + per_page - 1) // per_page

    card_html = ""
    for card in getPublishedAnimeByLast(page) :
        card_html= card_html + cardGen(card["anime_cover_image_url"],card["anime_name"],card["latest_episode_name"],card["anime_rating"],card["anime_id"])
    return render_template('index.html',year=getYear(),maintitle="اخر التحديثات" ,card_html=card_html , page = page , total_pages = total_pages)
    return getPublishedAnimeByLast(page)


@app.route("/AnimeList",)
def AnimeList():
    page = request.args.get('page', 1, type=int)
    per_page = 30
    total = 3000
    total_pages = (total + per_page - 1) // per_page
    
    card_html = ""
   # return getPublishedAnimeALL(page) 
    for card in getPublishedAnimeALL(page) :
        card_html= card_html + cardGen(card["anime_cover_image_url"],card["anime_name"],"",card["anime_rating"],card["anime_id"])
    return render_template('index.html',year=getYear(),maintitle="لائحة الانمي" ,card_html=card_html , page = page , total_pages = total_pages)


@app.route("/top_anime_mal",)
def RatingMal():
    page = request.args.get('page', 1, type=int)
    per_page = 30
    total = 3000
    total_pages = (total + per_page - 1) // per_page

    card_html = ""
   #return getPublishedAnimeRatingMal(page) 
    for card in getPublishedAnimeRatingMal(page) :
        card_html= card_html + cardGen(card["anime_cover_image_url"],card["anime_name"],"","",card["anime_id"])
    return render_template('index.html',year=getYear(),maintitle="التقييم العالمي" ,card_html=card_html , page = page , total_pages = total_pages)


@app.route("/top_anime",)
def TopRating():
    page = request.args.get('page', 1, type=int)
    per_page = 30
    total = 3000
    total_pages = (total + per_page - 1) // per_page

    card_html = ""
    #return getPublishedAnimeRating(page)
    for card in getPublishedAnimeRating(page) :
        card_html= card_html + cardGen(card["anime_cover_image_url"],card["anime_name"],"",card["anime_rating"],card["anime_id"])
    return render_template('index.html',year=getYear(),maintitle="التقييم العربي" ,card_html=card_html , page = page , total_pages = total_pages)

@app.route("/search",)
def search():
    psearch = request.args.get('n', 1, type=str)
    per_page = 100
    page = -1
    total = 100
    total_pages = (total + per_page - 1) // per_page

    card_html = ""
    #return getPublishedAnimeRating(page)
    try : 
        for card in getByName(psearch) :
            card_html= card_html + cardGen(card["anime_cover_image_url"],card["anime_name"],"",card["anime_rating"],card["anime_id"])
        return render_template('index.html',year=getYear(),maintitle=f"result for : {psearch}" ,card_html=card_html , page = page , total_pages = total_pages)
    except : 
        return TopRating()

@app.route("/get-anime-details=<id>")
def getAnimeDetailsFlask(id):
    episodeCard = ""
    anime =  getAnimeDetails(id)
    eps = []
    for ep in anime["response"]["episodes"]["data"]:
        for url in ep["episode_urls"]:
            if url["episode_server_name"] == "muilt" :
                n = url["episode_url"].split("f?n=")[1]
                eps.append({"ep_number":ep["episode_number"] , "name":n})
    
    for ep in eps :
        episodeCard = episodeCard + episodeCardGen(ep["ep_number"],ep["name"],anime["response"]["anime_id"])
    

    return render_template(
        "get-anime-details.html" ,
        anime_name=anime["response"]["anime_name"] , 
        cover = anime["response"]["anime_cover_image_url"]  ,
        season = anime["response"]["anime_season"] +" "+ anime["response"]["anime_release_year"],
        ep_count = anime["response"]["episodes"]["count"],
        age_rating = anime["response"]["anime_age_rating"],
        anime_rating =anime["response"]["anime_rating"],
        genres = anime["response"]["anime_genres"],
        episodeCard = episodeCard
        
        )       
def UrlGen(name):
    data = {
                "n":name ,
                "inf" : {"a":base64.b64encode((str(base64.b64encode((name+":"+getIp() + str(base64.b64encode((name+":"+getIp()).encode("utf-8")))).encode("utf-8"))) + name+":"+getIp() + str(base64.b64encode((name+":"+getIp()).encode("utf-8")))).encode("utf-8")),
                         "b" : getIp()
                         }
            }
    headers = {
                "user-agent":"Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36",
                "content-type" : "application/x-www-form-urlencoded"
            }
    urls = requests.post("https://anslayer.com/la/public/api/fw" , headers=headers , data=data)
    try :
                return [i.replace("http://ok.ru/video/","https://ok.ru/videoembed/").replace("streamtape.to/v/","streamtape.to/e/") for i in urls.json() ]
    except :
                print(urls.text + "an error happened please check at MultiUrl(An empty array will be returned)")
                return []
    
@app.route('/watch/<id>/', methods=['POST'])
def watch(id):
    ep_name = request.form["epn"]
    urls = UrlGen(ep_name)
    l=len(urls)
    
    return render_template("/watchPage.html" , video_sources=urls , l = l,second= getAnimeDetailsFlask(id))
if __name__ == "__main__":
    app.run(debug=True , host="0.0.0.0")
