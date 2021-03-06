import os

from tworg.tworg import Convertor


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

def test_multiple_split_tags():
    c = Convertor()
    with open(os.path.join(working_dir,
                           'examples/Ansible for DevOps_ Server and configuration management for humans.tid'),
              'r') as f:
        c.load(f)
    tags = ['Ansible', 'Books', 'read', 'to_read', 'Read_in_2020',
            'in_digital_library']
    assert c.metadata['tags'] == tags

def test_split_tags():
    assert convertor._Convertor__split_tags(
        '[[Load Testing]] Node.js Docker nginx notes.muumu.us PM2') == split_tags

def test_org_header():
    assert convertor.org_header == ['#+TITLE: Load testing wiki.muumu.us',
                                    '#+AUTHOR: krj',
                                    f"#+TAGS: {' '.join(split_tags)}"]

def test_ignore_color_header():
    c = Convertor()
    c.load(['color: green',
            'something'])
    assert c.tid_body == ['something']

def test_org_header_missing_fields():
    header_mappings = [(['title: A title\n', 'tags: One Two Three'],
                        ['#+TITLE: A title',
                         '#+TAGS: One Two Three']),
                       (['creator: Me', 'tags: One Two Three'],
                        ['#+AUTHOR: Me', '#+TAGS: One Two Three']),
                       (['No header here.'],
                        [])]
    for tid, org in header_mappings:
        c = Convertor()
        c.load(tid)
        assert c.org_header == org


def test_org_body_code_block():
    code_block = """```python
print('Hello world')
```"""
    c = Convertor()
    c.load(code_block.split('\n'))
    assert c.org_body == ['#+BEGIN_SRC python\n',
                          "print('Hello world')",
                          '#+END_SRC\n']

def test_org_body_block_quote():
    block_quote = """<<<
Computers are like a bicycle for our minds
<<< Steve Jobs"""
    c = Convertor()
    c.load(block_quote.split('\n'))
    assert c.org_body == ['#+BEGIN_QUOTE\n',
                          'Computers are like a bicycle for our minds',
                          '#+END_QUOTE\n']

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

def test_org_body_unordered_lists():
    c = Convertor()
    c.load(['* Item one',
            '* Item two',
            '** Nested item 1',
            '*** Nested item 2'])
    assert c.org_body == ['- Item one',
                          '- Item two',
                          '\t- Nested item 1',
                          '\t\t- Nested item 2']

def test_fmt_links():
    translations = [('[[Tiddler Title]]',
                     '[[roam:Tiddler Title][Tiddler Title]]'),
                    ('[[Displayed Link Title|Tiddler Title]]',
                     '[[roam:Tiddler Title][Displayed Link Title]]'),
                    ('[[TW5|https://tiddlywiki.com/]]',
                     '[[https://tiddlywiki.com/][TW5]]'),
                    ('[[Mail me|mailto:me@where.net]]',
                     '[[mailto:me@where.net][Mail me]]'),
                    ('[[Open file|file:///users/me/index.html]]',
                     '[[file:/users/me/index.html][Open file]]'),
                    ('[[Link one]] and then [[Another link|http://google.com]]',
                     '[[roam:Link one][Link one]] and then [[http://google.com][Another link]]')]
    c = Convertor()
    for tid, org in translations:
        assert c._Convertor__fmt_links(tid) == org
