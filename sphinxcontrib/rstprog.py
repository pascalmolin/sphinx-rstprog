from sphinx.errors import ExtensionError
from sphinx.parsers import RSTParser
from sphinx.util import logging
logger = logging.getLogger(__name__)
logger.info('loading extension %s'%__name__)

import re

__version__ = '0.0.1'

class progtorst:

    commentstart = '/**'
    commentend   = '**/'
    codedirective = '.. code::'
    indent = '   '

    start = re.compile(' *%s *$' % re.escape(commentstart))
    end   = re.compile(' *%s *$' % re.escape(commentend))

    def __init__(self):
        pass

    def run(self, lines):
        self.buffer = []
        self.out = []
        self.iw = 0
        self.parse = self.parse_prog
        if isinstance(lines, str):
            lines = lines.split('\n')
        for l in lines:
            logger.info('[%s] %s'%(self.parse.__name__,l))
            self.parse(l)

        return self.out

    def write(self,l,flush=False):
        # buffer by default, remove empty lines
        if self.buffer or l:
            self.buffer.append(self.iw*self.indent + l)
        if flush:
            if self.buffer:
                self.out += self.buffer
                self.buffer = []
            
    def start_text(self):
        self.parse = self.parse_text
        self.iw = 0
        self.write('')

    def end_text(self):
        self.iw = 0
        self.write('',flush=True)

    def start_prog(self):
        self.parse = self.parse_prog
        self.write('',flush=True)
        self.iw = 1

    def end_prog(self):
        # manual flush
        if any( [ l.strip() != '' for l in self.buffer ]):
            self.out += ['', self.codedirective, self.indent ]
            self.out += [ self.indent + l for l in self.buffer ]
            self.buffer = []

    def parse_text(self,l):
        if self.start.match(l):
            raise SyntaxError('illegal start comment %s' % l)
        elif self.end.match(l):
            self.end_text()
            self.start_prog()
        else:
            self.write(l)

    def parse_prog(self,l):
        if self.start.match(l):
            self.end_prog()
            self.start_text()
        elif self.end.match(l):
            raise SyntaxError('illegal end comment %s' % l)
        else:
            self.write(l)

class GPparser(RSTParser):

    supported = ('gp', 'gpdocument')

    def __init__(self,*args,**kwargs):
        self.codeparser = progtorst()
        super().__init__(*args,**kwargs)

    def parse(self, inputstring, document):
        # inputstring is str of list(str)

        lines = self.codeparser.run(inputstring)

        super().parse(lines, document)

def setup(app):

    # type: (Sphinx) -> Dict[str, Any]
    app.add_source_parser(GPparser)
    app.add_source_suffix('.gp','gpdocument')

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
