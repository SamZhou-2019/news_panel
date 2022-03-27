from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
from flask import Flask, render_template
import re
import requests
from bs4 import BeautifulSoup as bs
app = Flask(__name__)


def bilibili():
    driver = webdriver.Edge()  # 使用 Microsoft Edge 浏览器
    driver.implicitly_wait(5)
    driver.get("https://www.bilibili.com/v/popular/all")
    time.sleep(3)

    for page in range(0, 3):
        time.sleep(3)  # 每次翻页时暂停3秒，等待加载
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # 排行榜每次只加载20项，每次翻页到底就加载20项

    divs = driver.find_elements(By.CSS_SELECTOR, 'div.video-card')
    i = 0
    content_all = []
    for div in divs:
        if(div.text != ''):
            i += 1
            link = div.find_element(By.TAG_NAME, 'a').get_attribute('href')
            content = div.find_element(By.TAG_NAME, 'p.video-name').text
            upname = div.find_element(By.TAG_NAME, 'span.up-name__text').text
            play = div.find_element(By.TAG_NAME, 'span.play-text').text.strip()
            like = div.find_element(By.TAG_NAME, 'span.like-text').text.strip()
            """
            content_one = '<b style="background-color:deeppink;">哔哩</b> <b>' +\
                str(i)+' </b><br><a class="link" href="'+link+'">'+content+'</a><br><i>UP:'+upname+' 播放量' +\
                play+' 点赞数'+like+'</i>'
            """
            content_one = '<b style="background-color:deeppink;">哔哩</b> <b>' +\
                str(i)+' </b><i>UP:'+upname + ' ▶️'+play+' 👍'+like +\
                '</i><br><a class="link" href="'+link+'">'+content+'</a>'

            content_all.append(content_one)
    return content_all[0:min(50, len(content_all))]


def baidu():
    driver = webdriver.Edge()  # 使用 Microsoft Edge 浏览器
    driver.implicitly_wait(5)
    driver.get("https://top.baidu.com/board?tab=realtime")
    time.sleep(3)

    divs = driver.find_elements(
        By.CSS_SELECTOR, 'horizontal_1eKyQ')
    content_all = []
    i = 0
    for div in divs:
        if(div.text != ''):
            link = div.find_elements(
                By.CSS_SELECTOR, 'div.content_1YWBm').find_element(By.TAG_NAME, 'a').get_attribute('href')
            content = div.find_element(
                By.TAG_NAME, 'div.c-single-text-ellipsis').text
            info = div.find_element(
                By.TAG_NAME, 'div.ellipsis_DupbZ').text
            info = re.sub('[<>]|查看更多', '', info)
            hot_index = div.find_element(
                By.TAG_NAME, 'div.hot-index_1Bl1a').text
            content_one = '<b style="background-color:red;">百度</b> <b>' + \
                str(i)+' </b> <i>🔥 '+hot_index+'</i><br><a class="link" href = "'+link + \
                '" >'+content+'<br>'+'</a>'+info
            i += 1

            content_all.append(content_one)
    return content_all[0:min(50, len(content_all))]


def zhihu():
    driver = webdriver.Edge()  # 使用 Microsoft Edge 浏览器
    driver.implicitly_wait(5)
    driver.get("https://www.zhihu.com/knowledge-plan/hot-question/hot/0/hourF")
    time.sleep(3)

    for page in range(0, 3):
        time.sleep(3)  # 每次翻页时暂停3秒，等待加载
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # 排行榜每次只加载20项，每次翻页到底就加载20项

    divs = driver.find_elements(
        By.CSS_SELECTOR, 'div.css-3yxeqs')
    i = 0
    content_all = []
    for div in divs:
        if(div.text != ''):
            i += 1
            link = div.find_element(By.TAG_NAME, 'a').get_attribute('href')
            content = div.find_element(
                By.TAG_NAME, 'div.css-3dzvwq').text
            content = re.sub('新题', '<b style:"color:blue;">【新题】</b> ', content)
            content = re.sub(
                '上升', '<b style:"color:yellow;">【上升】</b> ', content)
            content = re.sub('飙升', '<b style:"color:red;">【飙升】</b> ', content)
            seek = div.find_element(
                By.TAG_NAME, 'div.css-16eyt6t').text
            content_one = '<b style="background-color:blue;">知乎</b> <b>' + \
                str(i)+'</b> <i>❤️ ' + seek + '</i><br><a class="link" href = "'+link+'" >' + \
                content+'</a>'

            content_all.append(content_one)
    return content_all[0:min(50, len(content_all))]


def weibo():
    driver = webdriver.Edge()  # 使用 Microsoft Edge 浏览器
    driver.implicitly_wait(5)
    driver.get("https://s.weibo.com/top/summary")
    time.sleep(5)

    divs = driver.find_element(
        By.CSS_SELECTOR, 'div.data tbody').find_elements(By.CSS_SELECTOR, 'tr')
    i = 0
    content_all = []
    for div in divs:
        if(div.text != ''):
            try:
                if div.find_element(By.TAG_NAME, 'td.td-01').text == '•':
                    continue
                else:
                    hot_index = div.find_element(By.TAG_NAME, 'span').text
            except(NoSuchElementException):
                hot_index = 'NEWS'
            topic = div.find_element(By.TAG_NAME, 'a').text
            link = div.find_element(By.TAG_NAME, 'a').get_attribute('href')

            content_one = '<b style="background-color:orange;">微博</b> <b>' + \
                str(i)+' </b> <i>🔥 '+hot_index+'</i><br><a class="link" href = "' + \
                link+'" >'+topic+'</a>'
            i += 1

            content_all.append(content_one)
    return content_all[0:min(51, len(content_all))]


def weather():
    w = []
    city = ['北京','上海','广州','深圳']
    for i in city:
        url = 'http://wthrcdn.etouch.cn/WeatherApi?city=' + i
        r = requests.get(url, timeout=3)
        soup = bs(r.text, "html.parser")

        city = soup.find("city").text.strip()
        temper_now = soup.find("wendu").text.strip()
        water = soup.find("shidu").text.strip()
        wind = soup.find("fengxiang").text.strip() + \
            soup.find("fengli").text.strip()
        sun = soup.find("sunrise_1").text.strip() + '-' + \
            soup.find("sunset_1").text.strip()
        now = '<b style="background-color:green;">' + city + '</b> 🌡️' + temper_now + '℃ 💧' +\
            water + ' 🪁' + wind + ' ☀' + sun

        day1_date = soup.find("forecast").find_all(
            'weather')[0].find('date').text.strip()
        day1_day = soup.find("forecast").find_all('weather')[
            0].find('day').find('type').text.strip()
        day1_night = soup.find("forecast").find_all('weather')[
            0].find('night').find('type').text.strip()
        day1_wind = soup.find("forecast").find_all('weather')[0].find("fengxiang").text.strip() +\
            soup.find("forecast").find_all('weather')[
            0].find("fengli").text.strip()
        day1_high = soup.find("forecast").find_all('weather')[
            0].find('high').text.strip().split(' ')[1]
        day1_low = soup.find("forecast").find_all('weather')[
            0].find('low').text.strip().split(' ')[1]
        if day1_day == day1_night:
            day1 = '<b style="background-color:green;">' + city + '</b> <b>今天 ' + day1_date + '</b> ' + day1_day +\
                ' ' + day1_wind + ' ' + day1_low + '-' + day1_high
        else:
            day1 = '<b style="background-color:green;">' + city + '</b> <b>今天 ' + day1_date + '</b> ' + day1_day + '转' + day1_night +\
                ' ' + day1_wind + ' ' + day1_low + '-' + day1_high

        day2_date = soup.find("forecast").find_all(
            'weather')[1].find('date').text.strip()
        day2_day = soup.find("forecast").find_all('weather')[
            1].find('day').find('type').text.strip()
        day2_night = soup.find("forecast").find_all('weather')[
            1].find('night').find('type').text.strip()
        day2_wind = soup.find("forecast").find_all('weather')[1].find("fengxiang").text.strip() +\
            soup.find("forecast").find_all('weather')[
            1].find("fengli").text.strip()
        day2_high = soup.find("forecast").find_all('weather')[
            1].find('high').text.strip().split(' ')[1]
        day2_low = soup.find("forecast").find_all('weather')[
            1].find('low').text.strip().split(' ')[1]
        if day2_day == day2_night:
            day2 = '<b style="background-color:green;">' + city + '</b> <b>明天 ' + day2_date + '</b> ' + day2_day +\
                ' ' + day2_wind + ' ' + day2_low + '-' + day2_high
        else:
            day2 = '<b style="background-color:green;">' + city + '</b> <b>明天 ' + day2_date + '</b> ' + day2_day + '转' + day2_night +\
                ' ' + day2_wind + ' ' + day2_low + '-' + day2_high

        day3_date = soup.find("forecast").find_all(
            'weather')[2].find('date').text.strip()
        day3_day = soup.find("forecast").find_all('weather')[
            2].find('day').find('type').text.strip()
        day3_night = soup.find("forecast").find_all('weather')[
            2].find('night').find('type').text.strip()
        day3_wind = soup.find("forecast").find_all('weather')[2].find("fengxiang").text.strip() +\
            soup.find("forecast").find_all('weather')[
            2].find("fengli").text.strip()
        day3_high = soup.find("forecast").find_all('weather')[
            2].find('high').text.strip().split(' ')[1]
        day3_low = soup.find("forecast").find_all('weather')[
            2].find('low').text.strip().split(' ')[1]
        if day3_day == day3_night:
            day3 = '<b style="background-color:green;">' + city + '</b> <b>后天 ' + day3_date + '</b> ' + day3_day +\
                ' ' + day3_wind + ' ' + day3_low + '-' + day3_high
        else:
            day3 = '<b style="background-color:green;">' + city + '</b> <b>后天 ' + day3_date + '</b> ' + day3_day + '转' + day3_night +\
                ' ' + day3_wind + ' ' + day3_low + '-' + day3_high

        # w = w + '<b style="background-color:green;">天气</b> ' + \
        #     now + '   ' + day1 + '   ' + day3 + '   '
        w.append(now)
        w.append(day1)
        w.append(day2)
        w.append(day3)
    return str(w)  # 把w换成列表，[now,day1,day2]，然后返回str(w)传给页面


def it():
    url = 'https://www.ithome.com/rss/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    r = requests.get(url, headers=headers, timeout=5)

    soup = bs(r.text, "html.parser")
    all = ''
    for i in soup.find_all('item'):
        all = all + '<b style="background-color:blueviolet;">IT之家</b> <a style="color:white;" href="' +\
            i.find('link').text.strip() + '">' + \
            i.find('title').text.strip() + '</a> '
    return all


def news():
    urls = {'国内': 'http://www.xinhuanet.com/politics/news_politics.xml',
            '地方': 'http://www.xinhuanet.com/local/news_province.xml',
            '国际': 'http://www.xinhuanet.com/world/news_world.xml'}

    all = ''
    for i in ['国内', '地方', '国际']:
        url = urls[i]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        r = requests.get(url, headers=headers, timeout=5)
        r.encoding = 'utf-8'

        soup = bs(r.text, "html.parser")
        for j in soup.find_all('item'):
            title = j.find('title').text.strip()
            desc = j.find('description').text.strip()
            all = all + '<b style="background-color:cyan;">新华社-' + i + \
                '</b> <b>' + title + '</b> ' + desc + ' '

    return all


@app.route('/')
def hello_world():
    b = bilibili()
    ba = baidu()
    z = zhihu()
    w = weibo()
    i = it()
    we = weather()
    n = news()
    return render_template('main.html',
                           # bili=re.sub('\n', '', b),
                           # baidu=re.sub('\n', '', ba),
                           # weibo=re.sub('\n', '', w),
                           # zhihu=re.sub('\n', '', z),
                           hot=str(b + ba + z + w),
                           weather=re.sub('\n', '', we),
                           it=re.sub('\n', '', i),
                           news=re.sub('\n', '', n))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
