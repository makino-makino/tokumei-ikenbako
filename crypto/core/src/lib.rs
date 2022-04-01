use rsa_fdh::blind as blind_rsa;
use sha2::Sha256;

use base64;
use pem;
use rand;
use serde::{Deserialize, Serialize};
use serde_json;

use rsa::{RSAPrivateKey, RSAPublicKey};

#[derive(Serialize, Deserialize)]
struct BlindPair {
    blinded_digest: String,
    unblinder: String,
}

pub fn blind(message: &str, pubkey: &str) -> Result<String, String> {
    let mut rng = rand::thread_rng();

    let signer_pub_key = pem::parse(pubkey).map_err(|e| e.to_string())?;
    let signer_pub_key =
        RSAPublicKey::from_pkcs8(&signer_pub_key.contents).map_err(|e| e.to_string())?;

    let digest = blind_rsa::hash_message::<Sha256, _>(&signer_pub_key, message.as_bytes()).unwrap();
    let (blinded_digest, unblinder) = blind_rsa::blind(&mut rng, &signer_pub_key, &digest);

    let blinded_digest = base64::encode(blinded_digest);
    let unblinder = base64::encode(unblinder);

    let blind_pair = BlindPair {
        blinded_digest,
        unblinder,
    };

    let res = serde_json::to_string(&blind_pair).map_err(|e| e.to_string())?;
    return Ok(res);
}

pub fn sign(blinded_digest: &str, signer_priv_key: &str) -> Result<String, String> {
    let mut rng = rand::thread_rng();

    println!("blinded_digest: {}", blinded_digest);
    println!("privkey: {}", signer_priv_key);

    let signer_priv_key = pem::parse(signer_priv_key).map_err(|e| e.to_string())?;
    let signer_priv_key =
        RSAPrivateKey::from_pkcs8(&signer_priv_key.contents).map_err(|e| e.to_string())?;

    let blinded_digest = base64::decode(blinded_digest).map_err(|e| e.to_string())?;
    let blind_signature = blind_rsa::sign(&mut rng, &signer_priv_key, &blinded_digest).unwrap();
    let blind_signature = base64::encode(blind_signature);

    Ok(blind_signature)
}

pub fn unblind(unblinder: &str, blind_signature: &str, pubkey: &str) -> Result<String, String> {
    let signer_pub_key = pem::parse(pubkey).map_err(|e| e.to_string())?;

    let signer_pub_key =
        RSAPublicKey::from_pkcs8(&signer_pub_key.contents).map_err(|e| e.to_string())?;

    let blind_signature = base64::decode(blind_signature).map_err(|e| e.to_string())?;

    let unblinder = base64::decode(unblinder).map_err(|e| e.to_string())?;
    let signature = blind_rsa::unblind(&signer_pub_key, &blind_signature, &unblinder);
    let signature = base64::encode(signature);

    Ok(signature)
}

pub fn verify(message: &str, signature: &str, signer_pub_key: &str) -> Result<String, String> {
    println!("msg: {}", message);

    let signature = base64::decode(signature).map_err(|e| e.to_string())?;
    let signer_pub_key = pem::parse(signer_pub_key).map_err(|e| e.to_string())?;

    let signer_pub_key =
        RSAPublicKey::from_pkcs8(&signer_pub_key.contents).map_err(|e| e.to_string())?;

    let digest = blind_rsa::hash_message::<Sha256, _>(&signer_pub_key, message.as_bytes())
        .map_err(|e| e.to_string())?;

    match blind_rsa::verify(&signer_pub_key, &digest, &signature) {
        Ok(_) => return Ok("valid".to_string()),
        Err(e) => {
            let fomarted_err = format!("{}", e);
            return Err(fomarted_err.to_string());
        }
    };
}

#[test]
fn test() {
    let message = "hello";

    let pubkey = "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtiRp+zay1oslP6/LxaAkcjF9oViLKORHdBBH+rkOWjam9v17Oid5oFiZ77Jn5O4aaeSH9IU/aFcpOQpEUQy6uziR76jTf1VE03AMb1NtY4QKeVI+xBPP8aPory5KORNHWbMci74i59wd5/h2pvnBTsCg5Y0zcDW9lk85r27RqoK6CJKAgpGp+piG6oDyChEz7pipkWccUvq/TnYReoGCxfczP7p8flQ3lmIvNeNrqtkq3bqGhdniOLlt0cuBUGf49Prv1llurEEPz/loPBS2UJNReoGnfBC6Z0vDUaR4+ZPft8MVkjsV/I+xgqHb7zOSkaEWHzdg0QlKBhdkVKyg9QIDAQAB-----END PUBLIC KEY-----";
    let privkey = "-----BEGIN PRIVATE KEY-----MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC2JGn7NrLWiyU/r8vFoCRyMX2hWIso5Ed0EEf6uQ5aNqb2/Xs6J3mgWJnvsmfk7hpp5If0hT9oVyk5CkRRDLq7OJHvqNN/VUTTcAxvU21jhAp5Uj7EE8/xo+ivLko5E0dZsxyLviLn3B3n+Ham+cFOwKDljTNwNb2WTzmvbtGqgroIkoCCkan6mIbqgPIKETPumKmRZxxS+r9OdhF6gYLF9zM/unx+VDeWYi8142uq2SrduoaF2eI4uW3Ry4FQZ/j0+u/WWW6sQQ/P+Wg8FLZQk1F6gad8ELpnS8NRpHj5k9+3wxWSOxX8j7GCodvvM5KRoRYfN2DRCUoGF2RUrKD1AgMBAAECggEAIPHpMYUtR90XObPEedSDgxwsixiG4ziXLAkd293JGMw12wryVQx61WPxRAfS/veKU4kAhlvroiXR0P1oafiRdfe/fcfdqXR05IGp3iEK8isZ8ePMco7a1+w71CPdTQGNsE3TZftYOPP5fNHWNFGMg4AYGi02Fp/B0QQ3fOHgjqSUdV8ygrzN9n1BXVBU7/5RnBRsqEwIbVFN+K05ApaLagu+JlZT1X+QsWHFi6fOQgXDhGydepLCyUC5ULbu4mj8Gogm2p4usU04Td8R3oRVc3DPPC2IddDcqH/MfPYK4byrfJXFndOGPvYUvrs1I1CkhnXOb7/VDvUC2ebviDFaaQKBgQDfEZN2Bl4loihtLcNx5UKY9WZY+wl3veDXA7F7peeqjywAEancs1MzxCHIHEQG/9QdbXbMVSmZhb8I7k6e66PdHmalHxhkEvmthUWK43GrbC+zcPUPSGM4xZoM+/mG3H4cspc9byb43t5xPDUN7tXT/Q3/I3jCu2JTA4ckNtwc2wKBgQDRCBuX8ODJ8XwRY44R9BozQqpqks8i4+7GFZKTVFRvSZm9m+99+i7LZFFFVg//QaxunepzgIu2y7HRqJyNiQHRuxqA0apQzBMhQ5bjZu3aIg/aZgzci8LgUpl1ygQZCNZqZ+yxZv7GdkXAic5K0MXta4jrlbgI7Mp5Fcnhi1+6bwKBgFphyrfVmKvy6iJimoA5fiRvugpvnMRxoPo9utn4vMc0v4U/ou2TkzC0VWO5YC7d1VofEjV0hCh6Mo8xz5VAsOJVAQ4CbWWO8q9GAoll4pasfR9ds01/7QQBvItqRQ5JpKeIDRONR+MqmkKTPIPqs6TzMYqhGrr8JbixAz6/I6xlAoGACIQaC7Cml9OcyGCT8ytMvfXjV4AvrC45Fhze4d23qukGuHDX6vv8WBD4Nqjw8edNDRyl5prAFmxqDC6gYivIxTCoPcNM+wm1Zc+JIC6bVh25I56wu3N+NwFmeyQF0rdHdQJS5E9b5d3/rX5vxyCGT8vnwiFRZBuxjAlVNjklZ0UCgYBtDBcfm1azdyxm2MTiVLW1VbFRtboLmjQJEodot92qnxnVBSSBBzBqtLJk4Vu7cKQtRJsP9M+NyVamfqKYkPru92sH4p/qI8el4Y8nQvKuLJGWpBBuEyG4IE7Qd+Tssj2FmEyYrKocN4D3Yhl7hTk18rPublcIjSjw332rDumFfQ==-----END PRIVATE KEY-----";

    let blind_pair = blind(message, pubkey).unwrap();
    let blind_pair: BlindPair = serde_json::from_str(&blind_pair).unwrap();

    let blind_signature = sign(&blind_pair.blinded_digest, privkey).unwrap();
    let signature = unblind(&blind_pair.unblinder, &blind_signature, pubkey).unwrap();

    let res = verify(message, &signature, pubkey).unwrap();
    println!("res: {}", &res);
}
