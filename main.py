from flask import Flask,request
from bs4 import BeautifulSoup
import datetime
import urllib
import html


app = Flask(__name__) #initiates Flask app


#default page
page = open("templates/default.html","r").read()


@app.route('/') #route is the 'directory'
def main():
    #returns that page
    return page


@app.route('/cite', methods=['GET'])
def APA():
    error = None
    response = page #this will be returned to the web page
    if request.method == 'GET':

        url=request.args.get('url')
        
        #parse validity of url
        url=parse_url(url)
        print(url)

        #get the content of the URL
        try:
            source = urllib.request.urlopen(url)
        except urllib.error.URLError:
            return response + "Cannot find URL specified."


        #start parsing it with BeautifulSoup
        soup = BeautifulSoup(source, 'html.parser')
        #find all instances of <meta> (for metadata) in the soup
        meta = soup.find_all("meta")

        #find all big headings <h1> in the soup
        #h1 = soup.find_all("h1")

        #find the title
        title = soup.title.string
        print('[TITLE]')
        for i in soup.findAll('meta',{'property':True}):
            if "og:title" in i['property']:
                print(i['content'])

        title = "<br><b>title:</b><br>" + str(title)

        meta_results = ''

        #loop over result and adds to it the response
        for i in meta:
            meta_results+=html.escape(str(i))+"<br>"
        meta_results = "<b>metadata:</b><br>" + meta_results

        #find author
        print("[AUTHOR]")
        for i in soup.findAll('meta',{'name':True}):
            if 'author' in i['name']:
                print(i['content'])

        print("DEBUG:",soup.h1)
        if soup.h1 != "":
            h1 =  "<br><br><b>big headers: </b>" + str(soup.h1.string)

        else:
            h1 = ""

        response += "results for <a href=\"%s\">%s</a>:<br><br>"%(url,url) +  meta_results + title + h1


        return response


    else:
        return response

def parse_url(url):

    if url.startswith("http://")==0 and url.startswith("https://")==0:
        url="http://"+url

    print("[PARSED URL]:",url)
    return url




if __name__ == '__main__':
    app.run()
