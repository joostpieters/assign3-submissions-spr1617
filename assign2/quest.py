import zlib
import base64
exec(zlib.decompress(base64.b64decode('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')))
