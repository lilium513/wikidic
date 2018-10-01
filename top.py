from flask import Flask, render_template, request,abort
import re
from bs4 import BeautifulSoup
import urllib
import requests
import json
app = Flask(__name__)

@app.route('/hello', methods=['POST','GET']) #Methodを明示する必要あり
def hello():
    if request.method == 'POST':
        # wiki = "post"
        url = request.form['dicUrl']
        print(url)
        wiki,title = makeWiki(url)
        print(wiki)
        date = {"wiki":wiki,"active":True,"title":title}
        return json.dumps(date)
    else:
        url = ""
    return render_template('top.html', title='flask test') 

@app.route('/report', methods=['GET']) #Methodを明示する必要あり
def report():

    return render_template('report.html') 


@app.errorhandler(404)
def error_handler(error):
    '''
     Description
      - abort(404) した時にレスポンスをレンダリングするハンドラ
    '''
    date = {"active":False}
    return json.dumps(date)


def makeWiki(url):
    if "wikipedia" not in url:
        print("abort")
        abort(404)
    url=url.split("/")
    title = url[-1]
    body = "/".join(url[:-1])
    if title[0] != "%":
        title = urllib.parse.quote(url[-1])
    
    html = requests.get(body + "/" + title)
    soup = BeautifulSoup(html.text, "html.parser")
    charcters = soup.findAll("dt")
    result = ""
    for charcter in charcters:
        before_split = charcter.text
        before_split = re.sub(r"\[.*?\]","",before_split)
        after_split = before_split.split(" / ")
        for fullname in after_split:
            fullname = fullname[:-1]
            fullname_and_yomi = fullname.split("（")
            if len(fullname_and_yomi)>1: #読みがあるものだったら
                kanjis,yomis = fullname_and_yomi[0].split(" "),fullname_and_yomi[1].split(" ")
                if len(kanjis) == len(yomis):
                    for kanji,yomi in zip(kanjis,yomis):
                        if kanji != yomi:
                            result += yomi + "\t" + kanji +"\t" + "名詞" + "\t"+"\n"
    title = urllib.parse.unquote(title) 
    return result,title

    #読み 文字 品詞 説明


## おまじない
if __name__ == "__main__":
    app.run(debug=False)