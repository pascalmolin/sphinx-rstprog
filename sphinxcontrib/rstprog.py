from sphinx.errors import ExtensionError
from sphinx.parsers import RSTParser
from sphinx.util import logging
logger = logging.getLogger(__name__)
logger.info('loading extension %s'%__name__)

import re

__version__ = '0.0.1'
DEBUG = False

class IllegalDelimiter(ExtensionError):
    category = 'RstProg error'
    def __init__(self, message, line, number, document):
        message += " '%s' -- %s line %d"%(line, document, number+1)
        super().__init__(message)

class progtorst:

    commentstart = '/**'
    commentend   = '**/'
    codedirective = '.. code::'
    indent = '   '

    start = re.compile(' *%s *$' % re.escape(commentstart))
    end   = re.compile(' *%s *$' % re.escape(commentend))

    def __init__(self):
        pass

    def run(self, lines, document):
        self.buffer = []
        self.out = []
        self.document = document
        self.parse = self.parse_prog
        if isinstance(lines, str):
            lines = lines.split('\n')
        try:
            for i,l in enumerate(lines):
                if DEBUG:
                    logger.info('[%s:%d] %s'%(self.parse.__name__,i,l))
                self.parse(l,i)
        except IllegalDelimiter as e:
            logger.error(e)
            return self.out

        return self.out

    def write(self,l,flush=False):
        # buffer by default, remove empty lines
        if self.buffer or l:
            self.buffer.append(l)
        if flush:
            if self.buffer:
                self.out += self.buffer
                self.buffer = []
            
    def start_text(self):
        self.parse = self.parse_text
        self.write('')

    def end_text(self):
        self.write('',flush=True)

    def start_prog(self):
        self.parse = self.parse_prog
        self.write('',flush=True)

    def end_prog(self):
        # manual flush
        if any( [ l.strip() != '' for l in self.buffer ]):
            self.out += ['', self.codedirective, self.indent ]
            self.out += [ self.indent + l for l in self.buffer ]
            self.out += ['']
            self.buffer = []

    def parse_text(self,l,i):
        if self.start.match(l):
            raise IllegalDelimiter('unexpected start comment',l,i,self.document)
        elif self.end.match(l):
            self.end_text()
            self.start_prog()
        else:
            self.write(l)

    def parse_prog(self,l,i):
        if self.start.match(l):
            self.end_prog()
            self.start_text()
        elif self.end.match(l):
            raise IllegalDelimiter('unexpected end comment',l,i,self.document)
        else:
            self.write(l)

class GPparser(RSTParser):

    supported = ('gp', 'gpdocument')

    def __init__(self,*args,**kwargs):
        self.codeparser = progtorst()
        super().__init__(*args,**kwargs)

    def parse(self, inputstring, document):
        # inputstring is str of list(str)

        lines = self.codeparser.run(inputstring, document)
        if DEBUG:
            logger.info('\n###'.join(lines))

        super().parse(lines, document)


def config_inited(app, config):
    global DEBUG
    DEBUG = config.rstprog_debug

def setup(app):

    # type: (Sphinx) -> Dict[str, Any]
    app.add_source_parser(GPparser)
    app.add_source_suffix('.gp','gpdocument')

    app.add_config_value('rstprog_debug', DEBUG, '')
    app.connect('config-inited', config_inited)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
