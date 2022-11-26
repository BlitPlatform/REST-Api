import base64


def decode_from_b64(_input: str) -> bytes:
    _bytes = str.encode(_input)
    return base64.b64decode(_bytes)
