import base64


def decode_from_b64(_input: str) -> str:
    _bytes = str.encode(_input)
    _decoded_bytes = base64.b64decode(_bytes)
    return str(_decoded_bytes, 'utf8', 'ignore')

def encode_to_b64(_input: str) -> str:
    _bytes = _input.encode('utf8')
    assert _bytes is not None
    _encoded_bytes = base64.b64encode(_bytes)
    return str(_encoded_bytes, 'utf8', 'ignore')
