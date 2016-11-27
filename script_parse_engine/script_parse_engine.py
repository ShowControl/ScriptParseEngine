"""Script Parse Engine parses the stream of text
for tags and maps it into a data-structure"""

__author__ = 'bapril'
__version__ = '0.0.1'
import Tkinter as tk
import re
import json

class ScriptParseEngine(object):
    """ScriptParseEngine Class"""
    def __init__(self, source):
        self.source = source
        self.input = ""
        self.current_tag_name = None
        self.tag = None
        self.output = []
        if type(source).__name__ == 'instance':
            self.source_type = str(source.__class__)
        elif type(source).__name__ == 'file':
            self.source_type = 'file'
        else:
            print "Unknown source: %s" % type(source).__name__

    def update(self):
        """Pull a new version of the text and re-parse"""
        #erase what we have there
        self.output = []
        if self.source_type == 'file':
            self.input = self.source.read()
        elif self.source_type == 'Tkinter.Text':
            self.input = self.source.get("1.0", tk.END)
        else:
            print "Don't know source object type: %s" % self.source_type
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
        self.tag = {}
        self.tag['type'] = self.input[1:end]
        self.current_tag_name = self.tag['type']

        self.input = self.input[end:]
        #TODO take non-data tags
        options = {
            '{' : self.parse_json_tag,
            '(' : self.parse_text_tag,
        }
        options[self.input[0]]()

    def parse_json_tag(self):
        """Parse the JSON tag"""
        string = self.map_json_string("", 0)
        try:
            self.tag = json.loads(string)
            self.tag['type'] = self.current_tag_name
            self.output.append(self.tag)
        except ValueError:
            print "ERROR Parsing JSON"
            self.tag['type'] = 'invalid'
            self.tag['error'] = 'Unable to parse JSON'
            self.tag['text'] = string
            self.output.append(self.tag)

    def map_json_string(self, output, level):
        """Deal with multi-layered json"""
        if len(self.input) < 1:
            return output
        if self.input[0] == "}":
            level = level - 1
        elif self.input[0] == "{":
            level = level + 1
        output = output + self.input[0]
        self.input = self.input[1:]
        if level == 0:
            return output
        else:
            return self.map_json_string(output, level)

    def parse_text_tag(self):
        """Found a text tag, parse it"""
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
