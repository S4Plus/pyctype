
import struct
import zlib
from PIL import ImageFile as PillowImageFile

file_or_path = ''
close = False

p = PillowImageFile.Parser()
if hasattr(file_or_path, 'read'):
    file = file_or_path
    file_pos = file.tell()
    file.seek(0)
else:
    file = open(file_or_path, 'rb')
    close = True
try:
    # Most of the time Pillow only needs a small chunk to parse the image
    # and get the dimensions, but with some TIFF files Pillow needs to
    # parse the whole file.
    chunk_size = 1024
    while 1:
        data = file.read(chunk_size)
        if not data:
            break
        try:
            p.feed(data)
        except zlib.error as e:
            # ignore zlib complaining on truncated stream, just feed more
            # data to parser (ticket #19457).
            if e.args[0].startswith("Error -5"):
                pass
            else:
                raise
        except struct.error:
            # Ignore PIL failing on a too short buffer when reads return
            # less bytes than expected. Skip and feed more data to the
            # parser (ticket #24544).
            pass
        except RuntimeError:
            # e.g. "RuntimeError: could not create decoder object" for
            # WebP files. A different chunk_size may work.
            pass
        if p.image:
            v1 = p.image.size
        chunk_size *= 2
    v2 = (None, None)
finally:
    if close:
        file.close()
    else:
        file.seek(file_pos)