import configparser, time, re, os
from tools import log as lo, listdir_fullpath


class Text:
    def __init__(self, text, path):
        self.text = text
        self.path = path

    def __del__(self):
        # with open(self.path + ".edit", "w") as f:
        with open(self.path, "w") as f:
            f.write( self.text )

    def get_val(self):
        return self.text

    def set_val(self, text):
        self.text = text


class UpdateNum:
    def __init__(self, template, koef):
        self.template = template
        self.koef     = koef
        left, right   = self.template[0], self.template[-1]
        self.pattern  = re.compile( "\{0}{1}\{2}".format( left, r"(\d+(?:\.\d+)?)", right ) )


    def __change(self, *args):
        match = args[0]
        full = match.group(0)
        number_str = match.group(1)

        if "." in number_str:
            number = int( float( number_str ) * KOEF )
        else:
            number = int( int( number_str ) * KOEF )
        number_str = full[0] + str(number) + full[-1]

        return number_str

    def run(self, *args):
        text = args[0]
        result = re.sub( self.pattern, self.__change ,text.get_val() )
        text.set_val( result )
        return text



config = configparser.RawConfigParser()
config.read('setting.conf')

args = config['site']

#load config
PATH_DIR = args['dir']
KOEF = float(args['koef'])
VAL  = args['va']


log = lo( "updBot", "main.log")

values = VAL.split("\n")

handlers = [ UpdateNum(v, KOEF) for v in values ]

def script():

    dir_list = listdir_fullpath( PATH_DIR )
    # dir_list = filter( lambda path : not re.search(r"edit", path), dir_list )

    for path in dir_list:
        log.info( "Path: %s handle", path )
        with open(path) as f:
            data = f.read()

        text = Text( data, path )
        for handler in handlers:
            text = handler.run( text )

    log.info("=== Done ===")


script()