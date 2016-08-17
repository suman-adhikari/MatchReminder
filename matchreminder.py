import urllib2
from bs4 import BeautifulSoup
import re
import datetime
import time
import webbrowser

url = 'http://www.chelseafc.com/matches/fixtures---results.html'
page = urllib2.urlopen(url)
soup  = BeautifulSoup(page,'lxml')
fileurl = 'Nextmatch.html'


def monthToNum(mth):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(mth)+1


def remove_all_whitespace(teams):
    pattern = re.compile(r'\s+')
    teams = re.sub(pattern, '', teams)
    return teams.replace("Vs", " Vs ")

def timeLeft(date_time):
    _time,_date= date_time.split(',')

    _day,_gate,_month = _date.strip().split(' ')
    _month = monthToNum(_month)

    _time =_time.replace(' ','')
    space,_hour,_min = _time.split(':')

    matchdate = datetime.datetime(datetime.date.today().year,int(_month),int(_gate),int(_hour),int(_min),00)
    interval = datetime.timedelta(seconds=0, minutes=45, hours=4, days=0)
    matchdate = matchdate + interval  #adding hour/min to date

    today = datetime.datetime.today();

    remaining_time = matchdate-today
    #print str(remaining_time)[:-7]
    return str(remaining_time)[:-7]

def getImages(div):
    site_url = "http://www.chelseafc.com"
    images = div.find_all("img")
    img1 = site_url + images[0]["src"]
    img2 = site_url + images[1]["src"]
    return [img1,img2]

def nextmatch(soup):
    div = soup.find("div", class_="next-match")
    images = getImages(div);
    date_time = div.find("span",class_="match-date-time").string
    match_time_left = timeLeft(date_time)
    teams = div.find("p",class_='match-teams').text
    match = remove_all_whitespace(teams)
    webfile(match_time_left,match,images)



def webfile(match_time,Teams,images):
    file = open(fileurl, 'w')

    txt = '<!doctype html>' \
          '<html lang="en">' \
          '<head><meta charset="UTF-8"><title>Next Match</title>' \
          '<link rel="stylesheet" href="style.css"/>' \
          '<link href="https://fonts.googleapis.com/css?family=Bungee+Hairline|Monoton" rel="stylesheet">'\
          '<link href="https://fonts.googleapis.com/css?family=Bungee+Hairline|Changa|Monoton" rel="stylesheet">'\
          '</head >' \
          '<body>' \
          '<div id="abc">chelsea  next  match</div>'\
          '<div id="container">' \
          '<span><img src="'+images[0]+'"></span>'\
          '<span>'+ Teams +' <br>' + match_time +' </span>'\
          '<span><img src="'+ images[1] +'"></span>'\
          '</div>' \
          '</body>' \
          '</html>'

    file.write(txt)

    webbrowser.open_new(fileurl)

nextmatch(soup)




