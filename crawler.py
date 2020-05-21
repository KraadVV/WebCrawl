import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import re
#put url of corp that you want to know
url = input()

# url, char/corp,
def crawlId(url, type):
    options = Options()
    options.headless = True


    browser = webdriver.Firefox(options=options, executable_path="./geckodriver")
    browser.get(url)
    time.sleep(7)



    if type == 'corp' or type == 'chara':

        browser.execute_script("""var jquery_script = document.createElement('script'); 
    jquery_script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js';
    // jquery_script.onload = function(){var $ = window.jQuery; $("h1").wrap("<i></i>");};
    jquery_script.onload = function(){
      var $ = window.jQuery; 
      $("h1").wrap("<i></i>");
    };
    document.getElementsByTagName('head')[0].appendChild(jquery_script);""")

        '''
        browser.execute_script("""var jquery_script = document.createElement('script'); 
            jquery_script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js';
            // jquery_script.onload = function(){var $ = window.jQuery; $("h1").wrap("<i></i>");};
            jquery_script.onload = function(){
              var $ = window.jQuery; 
              $("h1").wrap("<i></i>");
            };
            document.getElementsByTagName('head')[0].appendChild(jquery_script);""")
        '''
    time.sleep(1)

    if type == 'corp':
        browser.find_element_by_id('charsJoined').click()
        print("loading joined member\n")
        while True:
            try:
                time.sleep(10)
                browser.find_element_by_id('loadMore').click()
                print("loading more\n")
                time.sleep(10)
            except:
                break

    page_source = browser.page_source

    browser.close()

    return(page_source)

a = crawlId(url,'corp')

print(a)

list = []

state = True

while state:
    keyn = '<td class="name">'
    keynidx = a.find(keyn)
    if keynidx == -1:
        break
    a = a[keynidx+18:]

    keyu = "/character/"
    keyuidx = a.find(keyu)

    a = a[keyuidx:]
    keyend = a.find('">')
    url = "https://evewho.com" + a[0:keyend]

    keyc = '</a>'
    keycidx = a.find(keyc)
    cha = a[keyend+2:keycidx]

    if cha not in list and '"' not in cha:
        list.append([cha,url])
    a = a[keycidx:]


print(list)

final = []
for i in range(len(list)):
    charurl = list[i][1]
    chainfo = crawlId(charurl, 'chara')
    movement = []
    while True:
        keyn = '<td class="name">'
        keynidx = chainfo.find(keyn)
        if keynidx == -1:
            break
        chainfo = chainfo[keynidx+18:]

        keyuend = '">'
        corpnameidx = chainfo.find(keyuend)
        corpnameEidx = chainfo.find('</a>')
        corpname = chainfo[corpnameidx+2:corpnameEidx]

        chainfo = chainfo[corpnameEidx:]

        keycd = 'departed">'
        keycdidx = chainfo.find(keycd)
        if keycdidx != -1:
            keycdend ='</span'
            keycdendidx = chainfo.find(keycdend)
            corpDpt = chainfo[keycdidx+10:keycdendidx]
        else:
            corpDpt = '0'

        chainfo = chainfo[keycdendidx+6:]

        keycj = 'joined">'
        keycjidx = chainfo.find(keycj)
        keycjend = '</span>'
        keycjendidx = chainfo.find(keycjend)
        corpJn = chainfo[keycjidx+8:keycjendidx]

        print([i, list[i][0], corpname, corpJn, corpDpt])

        movement.append([i, list[i][0], corpname, corpJn, corpDpt])

        chainfo = chainfo[keycjendidx:]
    movement.reverse()

    for i in range(len(movement)):
        try:
            final.append([movement[0][1], movement[i][2], movement[i+1][2], movement[i+1][3]])
        except:
            break

f = open("corplog.csv", "w")
for i in range(len(final)):
    f.write(final[i][0]+','+final[i][1]+','+final[i][2]+','+final[i][3]+'\n')

f.close()
