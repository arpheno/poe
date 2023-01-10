from lxml import etree
import base64

import logging

import clipboard

logger= logging.getLogger(__name__)
import zlib


def _fetch_xml_from_import_code(import_code: str) -> bytes:
    """Decodes and unzips a Path Of Building import code.
    :raises: :class:`TypeError`, :class:`ValueError`
    :return: Decompressed XML build document."""
    try:
        base64_decode = base64.urlsafe_b64decode(import_code)
        decompressed_xml = zlib.decompress(base64_decode)
    except (TypeError, ValueError):
        logger.exception("Error while decoding.")
    except zlib.error:
        logger.exception("Error while decompressing.")
    else:
        return decompressed_xml

if __name__ == '__main__':
    text = clipboard.paste()

    xml_pob=_fetch_xml_from_import_code(text)

    root = etree.fromstring(xml_pob)
    print(etree.tostring(root, pretty_print=True).decode())