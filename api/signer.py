import subprocess
from ctypes import cdll, c_char_p
import logging

LIBRARY_PATH = "../crypto/signer/target/release/libsigner.so"

ffi = cdll.LoadLibrary(LIBRARY_PATH)
ffi.sign.argtypes = (c_char_p, c_char_p)
ffi.sign.restype = c_char_p

ffi.verify.argtypes = (c_char_p, c_char_p, c_char_p)
ffi.verify.restype = c_char_p


FFI_ERROR_PREFIX = 'err: '


def sign(blind_digest, privkey):
    logging.debug("privkey: %s", privkey)
    logging.debug("blind_digest: %s", blind_digest)

    result = ffi.sign(blind_digest.encode('utf-8'), privkey.encode('utf-8'))
    return result.decode('utf-8')


def verify(message, signature, pubkey):
    logging.debug("message: %s", message)
    logging.debug("signature: %s", signature)
    logging.debug("pubkey: %s", pubkey)

    out = None
    try:
        out = ffi.verify(message.encode('utf-8'),
                         signature.encode('utf-8'), pubkey.encode('utf-8'))
    except Exception as e:
        logging.error('exception: %s', e)
        return VerifyResult.from_error(str(e))

    result = VerifyResult(out)

    logging.debug('verify result: %s', result)

    return result


class VerifyResult():
    def __init__(self, ffi_output=b'', error_message=''):
        self.raw_out: str = ffi_output.decode('utf-8')
        self.ok = self.raw_out == 'valid' or bool(error_message)

        if not self.ok and self.raw_out.startswith(FFI_ERROR_PREFIX):
            self.error_message = error_message or self.raw_out.strip(
                FFI_ERROR_PREFIX)

    @classmethod
    def from_error(cls, error_message):
        return cls(error_message=error_message)

    def __str__(self):
        return 'OK' if self.ok else self.raw_out

    def __bool__(self):
        return self.ok
    __nonzero__ = __bool__


if __name__ == '__main__':
    privkey = "-----BEGIN PRIVATE KEY-----MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC2JGn7NrLWiyU/r8vFoCRyMX2hWIso5Ed0EEf6uQ5aNqb2/Xs6J3mgWJnvsmfk7hpp5If0hT9oVyk5CkRRDLq7OJHvqNN/VUTTcAxvU21jhAp5Uj7EE8/xo+ivLko5E0dZsxyLviLn3B3n+Ham+cFOwKDljTNwNb2WTzmvbtGqgroIkoCCkan6mIbqgPIKETPumKmRZxxS+r9OdhF6gYLF9zM/unx+VDeWYi8142uq2SrduoaF2eI4uW3Ry4FQZ/j0+u/WWW6sQQ/P+Wg8FLZQk1F6gad8ELpnS8NRpHj5k9+3wxWSOxX8j7GCodvvM5KRoRYfN2DRCUoGF2RUrKD1AgMBAAECggEAIPHpMYUtR90XObPEedSDgxwsixiG4ziXLAkd293JGMw12wryVQx61WPxRAfS/veKU4kAhlvroiXR0P1oafiRdfe/fcfdqXR05IGp3iEK8isZ8ePMco7a1+w71CPdTQGNsE3TZftYOPP5fNHWNFGMg4AYGi02Fp/B0QQ3fOHgjqSUdV8ygrzN9n1BXVBU7/5RnBRsqEwIbVFN+K05ApaLagu+JlZT1X+QsWHFi6fOQgXDhGydepLCyUC5ULbu4mj8Gogm2p4usU04Td8R3oRVc3DPPC2IddDcqH/MfPYK4byrfJXFndOGPvYUvrs1I1CkhnXOb7/VDvUC2ebviDFaaQKBgQDfEZN2Bl4loihtLcNx5UKY9WZY+wl3veDXA7F7peeqjywAEancs1MzxCHIHEQG/9QdbXbMVSmZhb8I7k6e66PdHmalHxhkEvmthUWK43GrbC+zcPUPSGM4xZoM+/mG3H4cspc9byb43t5xPDUN7tXT/Q3/I3jCu2JTA4ckNtwc2wKBgQDRCBuX8ODJ8XwRY44R9BozQqpqks8i4+7GFZKTVFRvSZm9m+99+i7LZFFFVg//QaxunepzgIu2y7HRqJyNiQHRuxqA0apQzBMhQ5bjZu3aIg/aZgzci8LgUpl1ygQZCNZqZ+yxZv7GdkXAic5K0MXta4jrlbgI7Mp5Fcnhi1+6bwKBgFphyrfVmKvy6iJimoA5fiRvugpvnMRxoPo9utn4vMc0v4U/ou2TkzC0VWO5YC7d1VofEjV0hCh6Mo8xz5VAsOJVAQ4CbWWO8q9GAoll4pasfR9ds01/7QQBvItqRQ5JpKeIDRONR+MqmkKTPIPqs6TzMYqhGrr8JbixAz6/I6xlAoGACIQaC7Cml9OcyGCT8ytMvfXjV4AvrC45Fhze4d23qukGuHDX6vv8WBD4Nqjw8edNDRyl5prAFmxqDC6gYivIxTCoPcNM+wm1Zc+JIC6bVh25I56wu3N+NwFmeyQF0rdHdQJS5E9b5d3/rX5vxyCGT8vnwiFRZBuxjAlVNjklZ0UCgYBtDBcfm1azdyxm2MTiVLW1VbFRtboLmjQJEodot92qnxnVBSSBBzBqtLJk4Vu7cKQtRJsP9M+NyVamfqKYkPru92sH4p/qI8el4Y8nQvKuLJGWpBBuEyG4IE7Qd+Tssj2FmEyYrKocN4D3Yhl7hTk18rPublcIjSjw332rDumFfQ==-----END PRIVATE KEY-----"
    digest = "gArKIqO4wSBpI4pdPqFtO7s4Yc1kiczjtbcf0RdbZggwVxCEPc2x6f0hbmvCLdIwWmgogf68XSD70P7/NFmDaDgrasyctQRWqPm9GG1mwJ8zeDaMapKXl77nk+4yeoG2CyRrSgh+HafTqZUh5rpu2aSaVmMidrfSo7elkEZGx7L4yiBLEUYU2qvJecruXDG3l+2kWOyBTw679n2lRECFwequH1KbSSehJbl/uoGW8/h8tL/9CR6NYzUl2EqymA7868a2LCa6i0c7Mj/qlyDGtdNjwNgrMrVKlYpdhXeNkPn+5NG2FL+uvamG2BjFbfR4+BVLUcv7m9J75QibnvQJWA=="

    result = sign(digest, privkey)

    msg = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqZTlqi9WIyfMTBuxRBt6MC5QB9Od85BViK14ztz+GVfbdkYeKx+Ivt2f+NZSVAprBeMeHdZziKPltXIvqAqcB9b1i/4Zwil5PtCdKAhiWG+pyx27qx83co/2S8lDeSEpkkI/4hA5Aa7xfXNPoD34U3aB7wI8tSEIPvK0o86oc7jMl5LfGbCVKHkVWlFyw1TQjh5Kl2TNcr26wvIOUIe4zVNIam9KzpiNMvWN4TPJTq9BERj17pGUVmRPFC+OIo2tqV6XVWnmlR42Ifx4eqgcIdrvkoniSMR46B0aoAi0bUhEm8xmb2AYdKIzzjXpfWhdQ5nYHsg1RY10qyJcaofXbwIDAQAB"
