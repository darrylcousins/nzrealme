# -*- coding: utf-8 -*-
"""
Deflate/encode, decode/inflate.

This code comes from this discussion:
http://stackoverflow.com/questions/1089662/python-inflate-and-deflate-implementations

The deflate/encode method is supposed to duplicate this bit of perl code::

    >>> my $xml    = $self->saml_request();
    >>> my $data   = '';
    >>> my $status = rawdeflate \$xml => \$data, Append => 0
    >>>     or die "Can't compress request data: $RawDeflateError\n";
    >>> $data = encode_base64($data);
    >>> $data =~ s{[\r\n]}{}g;
    >>> return $data;

My investigation found that ``rawdeflate`` compresses data to RFC 1951.

To handle the raw deflate and inflate, without header and checksum, the
following things needed to happen:

On deflate/compress: strip the first two bytes (header) and the last four bytes
(checksum).

On inflate/decompress: there is a second argument for window size. If this
value is negative it suppresses headers.::

    >>> xml = '<Header><Body>The content</Body></Header>'
    >>> b64 = deflate_and_base64_encode(xml)
    >>> print(decode_base64_and_inflate(b64))
    <Header><Body>The content</Body></Header>

"""

import zlib
import base64


__all__ = (
    'deflate_and_base64_encode',
    'decode_base64_and_inflate'
    )


def decode_base64_and_inflate(b64string):
    """
    Decode and inflate a compressed string.
    """
    decoded_data = base64.b64decode(b64string)
    return zlib.decompress(decoded_data, -15)

def deflate_and_base64_encode(string_val):
    """
    Deflate and encode a string.
    """
    zlibbed_str = zlib.compress(string_val)
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode(compressed_string)
