import base64

from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import pytest


@pytest.fixture
def pubkey():
    key = b"MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt79uopDMVUIgoy8s5xPX5Qscb5qKAwnv1UUq1w/Bvut6w7b4tWwqeG9CQoEHmh+U0OoxKqBurnxowLm1Uotnl8Gm5q30yMW77FmPhxMhBHZ7osoZ7UB6oYB9Cn7UCTPPFY/OUiXSXzrFO75q7isZduXcplz1suX/butPnEsML5EJVEfdq/qpzDtqr5nH2G2OLaYyxBt64pNM6HUbdcAa0Xv8M6xn01Spvc6xS8SL4juZ70hfdRuYW11PBHbv1jfx4yva2OdxJ8H3xF1td7SzwVCIOXGRMmUVzYVeMW9uOXFCygHhKT3pqJ0QjLzA0MZ9/TyitByeP4ZBqUZ8zjWoBQIDAQAB"
    return base64.b64decode(key)


@pytest.fixture
def signature():
    sig = b'eFOs98lfT3wQiB6W7lCnmsV6aZoSNzGXNcIzvLOlgi78NXBYYYpZxJ3VtkG41hsODqqCYfkJXPTPre5Y3G48p3o6IdYAe1gMrnddzUV0y8XJwi2372LW1bjAWVjayXouPcDSgiWj1wDuG6KDM03edwHdf2LARi7YJWe2sv9aJHD9Cm8bC3O7UgC9ufue/Kpv54AvpFFR/CMXqmOYV0OpBODbXF/D1fSk9H3XBIQay/4dLNWZXVZSepgo/dDDzcMTiDEmUgrkEmt3xXjGbAFj4+nS6Vfgb8KeJtKOR+sZ74eBk8GPq0PAA4zDNwO6/+AnI8gf6nbsb4xXfvkWYvpbSQ=='
    return base64.b64decode(sig)


@pytest.fixture
def message():
    return b'hello'


def test_crypto_processes(pubkey, message, signature):
    key = RSA.import_key(pubkey)
    h = SHA256.new(message)
    pkcs1_15.new(key).verify(h, signature)
