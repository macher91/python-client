from __future__ import unicode_literals
from coreapi.document import Document, Link, Array, Object, Error
import json


def _to_plaintext(node, indent=0, base_url=None):
    if isinstance(node, Document):
        head_indent = '    ' * indent
        body_indent = '    ' * (indent + 1)

        body = '\n'.join([
            body_indent + str(key) + ': ' +
            _to_plaintext(value, indent + 1, base_url=base_url)
            for key, value in node.data.items()
        ] + [
            body_indent + str(key) + '(' + _fields_to_plaintext(value) + ')'
            for key, value in node.links.items()
        ])

        head = '<%s %s>' % (
            node.title.strip() or 'Document',
            json.dumps(node.url)
        )
        return head if (not body) else head + '\n' + body

    elif isinstance(node, Object):
        head_indent = '    ' * indent
        body_indent = '    ' * (indent + 1)

        body = '\n'.join([
            body_indent + str(key) + ': ' +
            _to_plaintext(value, indent + 1, base_url=base_url)
            for key, value in node.data.items()
        ] + [
            body_indent + str(key) + '(' + _fields_to_plaintext(value) + ')'
            for key, value in node.links.items()
        ])

        return '{}' if (not body) else '{\n' + body + '\n' + head_indent + '}'

    elif isinstance(node, Array):
        head_indent = '    ' * indent
        body_indent = '    ' * (indent + 1)

        body = ',\n'.join([
            body_indent + _to_plaintext(value, indent + 1, base_url=base_url)
            for value in node
        ])

        return '[]' if (not body) else '[\n' + body + '\n' + head_indent + ']'

    elif isinstance(node, Link):
        return 'link(%s)' % _fields_to_plaintext(node)

    elif isinstance(node, Error):
        return '<Error>' + ''.join([
            '\n    * %s' % repr(message) for message in node.messages
        ])

    return json.dumps(node)


def _fields_to_plaintext(link):
    return ', '.join([
        field.name for field in link.fields if field.required
    ] + [
        '[%s]' % field.name for field in link.fields if not field.required
    ])


class PlainTextCodec(object):
    """
    A plaintext representation of a Document, intended for readability.
    """

    def dump(self, node):
        return _to_plaintext(node)
