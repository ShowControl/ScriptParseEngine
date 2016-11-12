"""Script Parse Engine parses the stream of text
for tags and maps it into a data-structure"""

__author__ = 'bapril'
__version__ = '0.0.1'
import Tkinter as tk
import re

class ScriptParseEngine(object):
    """ScriptParseEngine Class"""
    def __init__(self, source):
        self.source = source
        self.input = ""
        self.current_tag_name = None
        self.tag = None
        self.output = []

    def update(self):
        """Pull a new version of the text and re-parse"""
        #TODO Reflection on source and target should drive action.
        #erase what we have there
        self.output = []
        self.input = self.source.get("1.0", tk.END)
        self.parse_text()
        return self.output

    def parse_text(self):
        """Walk the text looking for the next tag"""
        while True:
            try:
                index = self.input.index('#')
                if index > 0:
                    self.output.append({'text':self.input[0:index]})
                    self.input = self.input[index:]
                else:
                    self.parse_tag()
            except ValueError:
                #No more hashes, take the whole thing.
                self.output.append({'text':self.input})
                return

    def parse_tag(self):
        """Parse the the tag we found"""
        pattern = '^#([a-z]*|#|_)'
        match = re.search(pattern, self.input)
        end = match.end()
        self.current_tag_name = self.input[1:end]
        self.input = self.input[end:]
        options = {
            '{' : self.parse_json_tag,
            '(' : self.parse_text_tag,
            '_' : self.parse_char_tag,
        }
        options[self.input[0]]()

    def parse_char_tag(self):
        """We found a character tag, parse it."""
        self.input = self.input[1:] #Strip the _
        self.tag = {}
        self.tag['name'] = 'character'
        #index_close = self.input.index(' ')

    def parse_json_tag(self):
        """Parse the JSON tag"""
        self.tag = {}

    def parse_text_tag(self):
        """Found a text tag, parse it"""
        self.tag = {}
        self.tag['name'] = self.current_tag_name
        self.tag['text'] = ""
        self.input = self.input[1:] #Strip the (
        while True:
            index_close = self.input.index(')')
            if self.input[index_close - 1] == "\\":
                self.tag['text'] = self.tag['text']+self.input[0:index_close - 1] + ")"
                self.input = self.input[index_close + 1:]
            else:
                self.tag['text'] = self.tag['text']+self.input[0:index_close]
                self.input = self.input[index_close + 1:]
                self.output.append(self.tag)
                return
