import os
import logging

import pytest
from Crypto.PublicKey import RSA

from signer import sign, verify


@pytest.fixture
def server_privkey():
    return os.environ["PRIVKEY"]


@pytest.fixture
def server_pubkey():
    return os.environ["PUBKEY"]


@pytest.fixture
def client_pubkey():
    return "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhwSND/S1prq8Rlt9oujIAlI9aj4lyhfIMT9/xYn/X1jN4vYkh74UqtAiSS9wNgyvpAp0lKJEJqbDR6p9WwZa972MeP9ni4OfhYLtjyz6ykkSWUxOToTX3GMPgOXwQV+EapZRUhzGs4GECoDap4mcgyhIpkPPuzpfaQkrdPslYD3eCWDkX1MN2DjVTWK+m/wjJ4oBSoMDq4IsZduHUiRrr6uaCGGg5qFRglcp+synxjKfTzKVTKCs4lOzxMSjsbMW6n4AUt6zuBegdva1ztDN7+Oq1U9K+0sIijf41148Bntyjq+LJbMkhEpbfwDX3rPQ3a75HsF53PMdNxlG3xJw1QIDAQAB"


@pytest.fixture
def unblind_signature():
    return "myuhms+Uhd8MnGG9t1Ivy3B4nm8SMkpHzhO3pU/45yk2bxwAK+B2Huz1oo1dapLs7zFWLfFMOLAoitv2rLNHH+KpIZ9bDITtj4m0/HBXYfY4y/SZf7vZ9+Y0kA4+3ghkWieIfUJjT0Mjc6DELQzggmUwSiGnSd/qu16GwIJXJPhVz0aiRk4F6Lm2C50DhrGhAc7DAy4u1q99GwBDCM6p5sVwAYYcq9mTaP4FkpI8R72RbF1H0RQGCHjRoFhqtm+Vn2gbZ9YksAX54jT/VFU5OL29sX4w9EFOoq2iUvZVSOOwSm03Qa98OmC+R+BwdXjS9Kue2q/uG9A9cvkM2HWiHQ=="


@pytest.fixture
def signature():
    return "KpIj2JZSGic11FBvRgKd0rCtsXH039bZ3LxHEpWkuoXB6jZElDnVPmDt8ne2UyRq5DEPjqeXDcvcQstbh+4xCd9hAQCFBNp5JbrvZxTAfmPQ4oiWiIjKEClL4J3JJ0cNHO/9sZFTTefnPVFvqPnYvpnDyH/a602xrIz/2mzPpKp+R9YqDSL8kuMyzX+a+rTm9v6qAhjDHA10gZMfyGCHb9AQUhXQWMYxwca5K0tkI9D9qQNPwpKl/RL5OkXd1yadtHloWdXHk768Tq5wbGkXl/g5Bv5cjP5YK/+TQWBWeST8iUYXRHFGam2wqFaGOU0lI9rbH5KMpkowJftlsZfxDw=="


@pytest.fixture
def message():
    return """{"votes":[true,true,true,true,true,true,true],"free":"o"}"""


@pytest.fixture
def blind_digest():
    return "XnjZnl8y2s1lE+7f8uwI9Rf1falOsabbjvvoKwCb8un3w+6YIX0eBGP0ujqdYgxD4b1yzq3/KR8Hm6Szr5FWAYKvg6w+i2/kznH0ldM4xRYZIGiZKL/WwZTklflib8xvjIPlZ1MRqaDsj+xKkmqFKFvmLsTRFXjQtJAr4q/a/TI9KGfPrOcifk9nRvzHRZrqxkTXS7s55j2vsCuJ0KzKD7RKa6iGEqdRrWu0zdhj7bVBVIoCy8ZI3vrkoRdY96Xi9Z2ZQ98ZeaN5yHdrTiyh+CpoLvvkYvuRPb9dkHhWsRFRMKXgz8kT10Bxy88T2S2PW5cvxdMbCEw3OnA4NoVuug=="


def test_sign(blind_digest, server_privkey):
    sign(blind_digest, server_privkey)


def test_verify(unblind_signature, client_pubkey, server_pubkey):
    results = (
        verify(client_pubkey, unblind_signature, server_pubkey),
        not verify('invalid'+client_pubkey, unblind_signature, server_pubkey),
        not verify(client_pubkey, 'invalid'+unblind_signature, server_pubkey),
        not verify(client_pubkey, unblind_signature,
                   server_pubkey.replace('QAB', 'QAC')),
    )

    try:
        assert all(results)
    except AssertionError as e:
        print("verify results:")
        for r in results:
            print(r)
        raise e
