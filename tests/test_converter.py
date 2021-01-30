import os

from tid2org.tid2org import Convertor


working_dir =  os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
test_tiddler = os.path.join(working_dir,
                            'examples/Load testing wiki.muumu.us.tid')

convertor = Convertor()
split_tags = ['Load_Testing', 'Node.js', 'Docker', 'nginx', 'notes.muumu.us',
              'PM2']
with open(test_tiddler, 'r') as f:
    convertor.load(f)


def test_load():
    assert convertor.metadata['created'] == '20200808211749888'
    assert convertor.metadata['creator'] == 'krj'
    assert convertor.metadata['modified'] == '20200816220542594'
    assert convertor.metadata['modifier'] == 'krj'
    assert convertor.metadata['title'] == 'Load testing wiki.muumu.us'
    assert convertor.metadata['tags'] == split_tags
    assert len(convertor.tid_body) == 142

def test_split_tags():
    assert convertor._Convertor__split_tags(
        '[[Load Testing]] Node.js Docker nginx notes.muumu.us PM2') == split_tags

def test_org_header():
    assert convertor.org_header == ['#+TITLE: Load testing wiki.muumu.us',
                                    '#+AUTHOR: krj',
                                    f"#+TAGS: {' '.join(split_tags)}"]

def test_org_body_code_block():
    code_block = """```python
print('Hello world')
```"""
    c = Convertor()
    c.load(code_block.split('\n'))
    assert c.org_body == ['#+BEGIN_SRC python',
                          "print('Hello world')",
                          '#+END_SRC']

def test_org_body_block_quote():
    block_quote = """<<<
Computers are like a bicycle for our minds
<<< Steve Jobs"""
    c = Convertor()
    c.load(block_quote.split('\n'))
    assert c.org_body == ['#+BEGIN_QUOTE',
                          'Computers are like a bicycle for our minds',
                          '#+END_QUOTE']

def test_org_body_formatting():
    c = Convertor()
    c.load(['This line has inline `code`.',
            "This line has ''bold'' text.",
            'This line has //italic// text.',
            'This line has __underscored__ text.',
            'This line has ~~struckthrough~~ text.'])
    assert c.org_body == ['This line has inline ~code~.',
                          'This line has *bold* text.',
                          'This line has /italic/ text.',
                          'This line has _underscored_ text.',
                          'This line has +struckthrough+ text.']

def test_org_body_headers():
    c = Convertor()
    c.load(['! Top level',
            '!! Second level',
            '!!!!!! Sixth level'])
    assert c.org_body == ['* Top level',
                          '** Second level',
                          '****** Sixth level']
