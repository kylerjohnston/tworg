import re

class Convertor:
    """ Converts a TiddlyWiki Tiddler (.tid) file to an Emacs org-mode file """
    def __init__(self):
        self.metadata = {
            'created': None,
            'creator': None,
            'modified': None,
            'modifier': None,
            'tags': [],
            'title': None,
        }
        self.tid_body = []

    def load(self, fp):
        """ Read an iterative object containing TiddlyWiki WikiText strings """
        keywords_regex = '|'.join(self.metadata.keys())
        for line in fp:
            metadata_match = re.match(rf"^({keywords_regex}|type): (.*)", line)
            if metadata_match:
                key, value = metadata_match.groups()
                if key == 'tags':
                    self.metadata['tags'] = self.__split_tags(value)
                elif key == 'type':
                    pass
                else:
                    self.metadata[key] = value
            else:
                self.tid_body.append(line)

    @property
    def org_header(self):
        """ Return org-formatted header metadata as a list of lines """
        return [f"#+TITLE: {self.metadata['title']}",
                f"#+AUTHOR: {self.metadata['creator']}",
                f"#+TAGS: {' '.join(self.metadata['tags'])}"]

    @property
    def org_body(self):
        """ Represent self.tid_body in org-mode formatting """
        org_body = []
        multiline_tmp = []
        multiline_type = None
        for line in self.tid_body:
            if len(multiline_tmp) > 0:
                if multiline_type == 'code' and line.startswith('```'):
                    multiline_tmp.append('#+END_SRC')
                    org_body += multiline_tmp
                    multiline_tmp = []
                elif multiline_type == 'quote' and line.startswith('<<<'):
                    # TODO: What to do with quote attribution? Does org-mode
                    # have an attribute for that?
                    multiline_tmp.append('#+END_QUOTE')
                    org_body += multiline_tmp
                    multiline_tmp = []
                else:
                    multiline_tmp.append(line)
            elif line.startswith('```'):
                match = re.match(r'^```(\w*)', line)
                lang = match.groups()[0]
                multiline_tmp.append(f'#+BEGIN_SRC {lang}')
                multiline_type = 'code'
            elif line.startswith('<<<'):
                multiline_tmp.append('#+BEGIN_QUOTE')
                multiline_type = 'quote'
            elif line.startswith('!'):
                match = re.match(r'^(!+).+', line).groups()[0]
                org_body.append(self.__org_fmt(
                    line.replace(match, '*' * len(match))))
            elif line.startswith('*'):
                match = re.match(r'^(\*+).+', line).groups()[0]
                org_body.append(self.__org_fmt(
                    line.replace(match, '\t' * (len(match) - 1) + '-')))
            else:
                org_body.append(self.__org_fmt(line))
        return org_body

    def __str__(self):
        return '\n'.join(self.org_header) + '\n'.join(self.org_body)

    def __org_fmt(self, string):
        """ Given a string in WikiText formatting, return it with
        org formatting """
        return (string.replace('`', '~')
                .replace("''", '*')
                .replace('//', '/')
                .replace('__', '_')
                .replace('~~', '+'))

    def __split_tags(self, tags):
        """ Given a string of tags from a .tid file, split it into a list of
        tags. Tags are separated by spaces, but can also contain spaces if
        they are enclosed by brackets. E.g. an example tag string could look
        like:

        [[Load Testing]] Node.js Docker nginx notes.muumu.us PM2

        This method will convert spaces within a tag to underscores. So, in the
        example above, [[Load Testing]] will become Load_Testing.
        """
        split = tags.split(' ')
        tags = []

        tmp = []

        for tag in split:
            if len(tmp) > 0:
                if tag.endswith(']]'):
                    tmp.append(tag.strip(']]'))
                    tags.append('_'.join(tmp))
                    tmp = []
                else:
                    tags.append(tmp)
            elif tag.startswith('[['):
                tmp.append(tag.strip('[['))
            else:
                tags.append(tag)

        return tags
