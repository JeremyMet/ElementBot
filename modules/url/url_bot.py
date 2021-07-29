from modules.module import module ;
import urllib.request
import urllib.parse
import html;
import re ;
from bcolors import bcolors ;
import time;
import json;

# Some Constants
title_regex = re.compile("\\?\"author\\?\":\\?\"");
youtube_url = "https://www.youtube.com/watch?v="
watch_regex = re.compile("watch\?v=([0-9aA-zZ\-])*");

def findTitleOther(url, delay=0):
    ret = "";
    try:
        req = urllib.request.Request(url, data=None, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3)'})
        webpage = urllib.request.urlopen(req, timeout=5).read()
        webpage = html.unescape(webpage.decode(encoding="utf8"))
        ret = webpage.split('<title>')[1].split('</title>')[0]
        ret += '<br>'+url+'<br>';
    except:
        pass
    if ret:
        time.sleep(delay)
    return ret;

def findTitleYouTube(url, delay=0):
    ret = "";
    try:
        if url[-1] == "/":
            url = url[:-1]; # pour éventuellement corriger les urls mal formées.
        tmp_re_search = re.search(watch_regex, url)
        if tmp_re_search:
            video_id = tmp_re_search.group(0);
            video_id = video_id.split("watch?v=")[1];
        else:
            video_id = url.split("/")[-1]
            video_id = video_id.split("?")[0];
        # found on Stackoverflow, looks very nice.
        params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
        api_url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        api_url = api_url + "?" + query_string
        with urllib.request.urlopen(api_url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
        author = data['author_name']
        title = data['title'];
        ret = '<b>{}</b> \u2014 {}<br>{}<br>'.format(author.capitalize(), title.capitalize(), url);
    except:
        pass
    if ret:
        time.sleep(delay)
    return ret


class url_bot(module):

    url_regex = re.compile("(https?|ftp|ssh|mailto):\/\/[\u00C0-\u017Fa-z0-9\/:%_+.,#?!@&=-]+", re.IGNORECASE)

    filter_list = ["https://matrix.to"];

    @classmethod
    # returns True if the URL is allowed
    def filter_out(cls, url):
        for current_url in cls.filter_list:
            if url.find(current_url)>=0:
                return False;
        return True;

    def __init__(self, keyword = "url_bot", is_permanent = False): # <- template ... Here goes your default module name
        super().__init__(keyword, is_permanent) ;
        self.module_name = "url_bot"
        self.whatis = "Get small description from url"
        self.__version__ = "0.0.1"
        self.help = "None"

    @module.login_check_dec
    def process_msg_passive(self, cmd, sender, room):
        if len(cmd)>0 and cmd[0] == ">": # Cette condition permet de ne pas traiter les citations (i.e. lien déjà posté).
            return "";
        reg_match = re.finditer(url_bot.url_regex, cmd);
        ret = "" ;
        for match in reg_match: # si une url valide est trouvée ...
            url = match.group(0) ;
            print("{}>>> current url: {}{}".format(bcolors.OKBLUE,url,bcolors.ENDC))
            if url_bot.filter_out(url): # if this addressed is allowed
                if url.find("youtu") > 0: # not perfect, should be modified with regex.
                    ret += findTitleYouTube(url, delay=1);
                elif url.find("twitter.") > 0:
                    pass # do nothing for now ...
                else:
                    ret+= findTitleOther(url, delay=1);
        if ret != "":
            ret= "<blockquote>"+ret+"</blockquote>"
        return ret;

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=KXatvzWAzLU";
    title = findTitleYouTube(url)
    parsed_url = urllib.parse.urlparse(url);
    print(title)
    print(parsed_url.netloc)
