# -*- coding: utf-8 -*-
"""
 html page layout - wrapper 
 
"""
import json
from htmlform import htmlelement


class head(object):
    """
        html <head> object containing css styling, <link src's>, <scripts>
    """
    def __init__(self, title, **kw):
        self.title = title
        self.links = kw['links'] if 'links' in kw else []
        self.style_sheets = kw['style'] if 'style' in kw else []
        self.scripts = kw['scripts'] if 'scripts' in kw else []
    def add_link(self, link):
        self.links.append(link)
    def add_style_sheet(self, sheet):
        """
            add a .css 
        """
        self.add_link('<link rel="stylesheet" type="text/css" href="%s">'%(sheet))
    def add_script(self, script):
        self.scripts.append('<script src="%s"></script>'%(script))
    def html(self):
        headHtml = ['<head>']
        headHtml.append('<title>%s</title>'%(self.title))
        for link in self.links:
            headHtml.append(link)
        for script in self.scripts:
            headHtml.append(script)
        headHtml.append('</head>')
        return headHtml
class body(htmlelement):
    def __init__(self, **kw):
        self.scripts = kw['scripts'] if 'scripts' in kw else []
        self.initParamItems({})
    def html(self):
        toReturn = self.getChildHtml(['<body>'])
        for script in self.scripts:
            toReturn.append(script)
        toReturn.append('</body>')
        return toReturn
        
class page(htmlelement):
    """
        webpage - an object which contains html elements: head, body,scripts
    """
    def __init__(self, pageName, **kw):
        self.pageName = pageName
        try:
            self.load()
        except Exception as e:
            print(repr(e))
            self.head = head(self.pageName)
            self.body = body()
    def load(self):
        try:
            config = open('config/%s_config.json'%(self.pageName),'r')
            cfg = self.pageName
        except:
            cfg = 'default_web_page'
            config = open('config/webpage_config.json','r')
            pass
        js_config = json.load(config)
        print (js_config)
        self.head = head(self.pageName, 
                        links=js_config[cfg]['head']['links'], 
                        style=js_config[cfg]['head']['style_sheets'],
                        scripts=js_config[cfg]['head']['scripts'])
        self.body = body(scripts=js_config[cfg]['body']['scripts'])
        config.close()

    def save(self):
        webpage = {
            self.pageName: {
                "head": {
                    "title": self.head.title,
                    "style_sheets": self.head.style_sheets,
                    "links": self.head.links,
                    "scripts": self.head.scripts
                },
                "body": {
                    "scripts": self.body.scripts
                }
            }
        }
        with open('config/%s_config.json'%(self.pageName), 'w+') as config:
            json.dump(webpage, config)
    def htmlrender(self, content):
        if content is not None:
            self.body.items = [content]
        self.items = [self.head, self.body]
        toRender = self.getChildHtml(['<html>'])
        toRender.append('</html>')
        return '\n'.join(toRender)

        
        
        
        
        
        
        
        
        