import sys
import codecs

ENCODING = 'utf8'

def process(handle):
    with codecs.getreader(ENCODING)(sys.stdin.buffer, 'strict') as stream:
        content = stream.read()
    ret = handle(content)
    with codecs.getwriter(ENCODING)(sys.stdout.buffer, 'strict') as stream:
        stream.write(ret)
