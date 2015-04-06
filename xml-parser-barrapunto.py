#!/usr/bin/python
# -*- coding: utf-8 -*-


from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys


class CounterHandler(ContentHandler):

    def __init__(self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""
        self.theContent_title = ""
        self.theContent_link = ""
        self.fich = open("barrapunto.html", "w")
        self.cod_html = ('<meta http-equiv="Content-Type" content="text/html;'
                         + 'charset=UTF-8" /\n>')
        self.fich.write(self.cod_html.encode('utf-8'))

    def startElement(self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement(self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                self.theContent_title = self.theContent
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                self.theContent_link = self.theContent
                self.inContent = False
                self.theContent = ""

                if (self.theContent_title) and (self.theContent_link):
                    self.theContent = ("<li><a href=" + self.theContent_link +
                                       ">" + self.theContent_title +
                                       "</a></li>\n")
                    self.fich.write(self.theContent.encode('utf-8'))
                    self.theContent = ""

    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

# --- Main prog

if len(sys.argv) < 2:
    print "Usage: python xml-parser-jokes.py <document>"
    print
    print " <document>: file name of the document to parse"
    sys.exit(1)

# Load parser and driver

JokeParser = make_parser()
JokeHandler = CounterHandler()
JokeParser.setContentHandler(JokeHandler)

# Ready, set, go!

xmlFile = open(sys.argv[1], "r")
JokeParser.parse(xmlFile)

print "Parse complete"
