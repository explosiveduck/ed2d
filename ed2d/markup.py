from xml.parsers import expat
from html.parser import HTMLParser

class TagStack(object):
    def __init__(self):
        self.tags = []
        self.args = []
        self.data = []
        self.dataAdded = []
        self.stackSize = 0
        self.frameHasData = False

    def push(self, tag, args):
        self.tags.append(tag)
        self.args.append(args)
        self.data.append([])
        self.dataAdded.append(False)
        self.stackSize += 1

    def add_data(self, data):
        self.data[self.stackSize-1].append(data)
        self.dataAdded[-1] = True

    def clear_frame_data(self):
        self.data[self.stackSize-1] = []
        self.dataAdded[-1] = False

    def is_data_added(self, posRel=0):
        pos = -1 - posRel
        return self.dataAdded[pos]

    def pop(self):
        self.dataAdded.pop()
        stackFrame = (self.tags.pop(), self.args.pop(), self.data.pop())
        self.stackSize -= 1
        return stackFrame

    def peek(self, posRel=0):
        pos = -1 - posRel
        return (self.tags[pos], self.args[pos], self.data[pos])

    def path(self):
        return '/'.join(self.tags)


class BaseParser(object):
    def __init__(self, parser, tag, parent, root):
        self.parser = parser
        self.parent = parent
        self.tag = tag
        self.root = root

        if self.parent is None and self.tag is None and self.root is None:
            self.isRoot = True
        else:
            self.isRoot = False

        if self.isRoot:
            self.stack = TagStack()
            self.root = self
        else:
            self.stack = self.root.stack

        self.parsers = {}

        self.set_handlers()

        self.init_data()

    def set_handlers(self):
        pass

    def restore_handlers(self):
        if self.parent is not None:
            self.parent.set_handlers()

    def start(self, tag, attrs):
        if not isinstance(attrs, dict):
            attrs = dict(attrs)

        self.stack.push(tag, attrs)

        tagPath = self.stack.path()

        for parser in self.parsers:
            if parser == tagPath:
                ParserClass = self.parsers[parser]['object']
                parInst = self.switch_parser(ParserClass)
                self.parsers[parser]['instance'] = parInst

    def data(self, data):
        # We need to check if the stack frame has been used
        # previously and clear the previous data if so.
        if self.stack.is_data_added() is True:
            self.stack.clear_frame_data()
        self.stack.add_data(data.strip())
        self.parse()

    def end(self, tag):
        if self.stack.is_data_added() is False:
            self.parse()

        if tag == self.tag:
            self.integrate()
            self.restore_handlers()

        self.stack.pop()

    def switch_parser(self, parser):
        tag, attrs, data = self.stack.peek()
        return parser(self.parser, tag, self, self.root)

    def register_parser(self, stackTree, parser):
        self.parsers[stackTree] = {'object': parser}

    # The following method stubs are what the parsing sub-classes
    # will be implemented within.
    def init_data(self):
        pass

    def parse(self):
        pass

    def integrate(self):
        pass

class XmlParser(BaseParser):
    def set_handlers(self):
        self.parser.StartElementHandler = self.start
        self.parser.CharacterDataHandler = self.data
        self.parser.EndElementHandler = self.end

class HtmlParser(BaseParser):
    def set_handlers(self):
        self.parser.handle_starttag = self.start
        self.parser.handle_data = self.data
        self.parser.handle_endtag = self.end

def parse_html_data(rootParser, htmlData):
    htmlParser = HTMLParser()
    root = rootParser(htmlParser, None, None, None)
    linedData = htmlData.split('\n')
    for line in linedData:
        htmlParser.feed(line.strip())
    return root

def parse_html(rootParser, htmlPath):
    htmlParser = HTMLParser()
    root = rootParser(htmlParser, None, None, None)

    with open(htmlPath, 'rb') as htmlFile:
        for line in htmlFile:
            htmlParser.feed(line.strip())
    
    return root

def parse_xml_data(rootParser, xmlData):
    xmlParser = expat.ParserCreate()
    root = rootParser(xmlParser, None, None, None)
    linedData = xmlData.split('\n')
    for line in linedData:
        xmlParser.Parse(line.strip(), 0)

    xmlParser.Parse(b'',)
    return root

def parse_xml(rootParser, xmlPath):

    xmlParser = expat.ParserCreate()
    root = rootParser(xmlParser, None, None, None)

    with open(xmlPath, 'rb') as xmlFile:
        for line in xmlFile:
            xmlParser.Parse(line.strip(), 0)

    xmlParser.Parse(b'', 1)

    return root
