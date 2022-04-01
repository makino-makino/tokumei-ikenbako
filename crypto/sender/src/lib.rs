use std::borrow::Borrow;
use wasm_bindgen::prelude::wasm_bindgen;

pub fn to_string<T: Borrow<str>, E: std::fmt::Display>(r: Result<T, E>) -> String {
    match r {
        Ok(v) => v.borrow().to_owned(),
        Err(e) => format!("err: {}", e),
    }
}

#[wasm_bindgen]
pub fn blind(message: &str, pubkey: &str) -> String {
    to_string(crypto_core::blind(message, pubkey))
}

#[wasm_bindgen]
pub fn unblind(blind_signature: &str, pubkey: &str, unblinder: &str) -> String {
    to_string(crypto_core::unblind(blind_signature, pubkey, unblinder).map(|e| e))
}

#[wasm_bindgen]
pub fn verify(message: &str, signature: &str, signer_pub_key: &str) -> String {
    to_string(crypto_core::verify(message, signature, signer_pub_key).map(|e| e))
}

#[test]
fn test_blind() {
    let pubkey = "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwXTUY0OErUu7aTzUcTDRdrG2jWy0zA4TP0fmqMNoPxJPv2yoIFJ33S3CCrbEvzR9rJw7J5R6LqJW1p8onUs1FegN5jQUGCMCdQm0qkvASbF74gzlB18Qgbw0EAVlPkT0yu37WzD4ER3O7GcuL1fvohEAzHAZF4CbffIM0ngEdIM+b2bR8rz6JIUGXY01oXcadUEx0yTzS/sIFWuGoSmn4a8Dt+xLDWAAFgWZV1PcvaWeQDNEl/PXjso9sFvBS0dp+WZmhvwA3YrIQee+zXR8bft0and+5dBqExxgxfYmipBTgXr+8/U6w1AEQeLKg7jTmU1rNfgDYxdMe0KmXy6x8wIDAQAB-----END PUBLIC KEY-----";

    let res = crypto_core::blind("aaaaa", pubkey).unwrap();
    println!("----- blind -----\n{}", res);
}

#[test]
fn test_unblind_and_verify() {
    let pubkey = "-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwXTUY0OErUu7aTzUcTDRdrG2jWy0zA4TP0fmqMNoPxJPv2yoIFJ33S3CCrbEvzR9rJw7J5R6LqJW1p8onUs1FegN5jQUGCMCdQm0qkvASbF74gzlB18Qgbw0EAVlPkT0yu37WzD4ER3O7GcuL1fvohEAzHAZF4CbffIM0ngEdIM+b2bR8rz6JIUGXY01oXcadUEx0yTzS/sIFWuGoSmn4a8Dt+xLDWAAFgWZV1PcvaWeQDNEl/PXjso9sFvBS0dp+WZmhvwA3YrIQee+zXR8bft0and+5dBqExxgxfYmipBTgXr+8/U6w1AEQeLKg7jTmU1rNfgDYxdMe0KmXy6x8wIDAQAB-----END PUBLIC KEY-----";

    let blinded_signature = "EfjSYZqSWYJ6pHGXpgUTuYqdS/kdHEw2XbEGGBr5qAldcR+xVY5I0lp0mAG0MVqvdd8d54pMMC93RESSwXWbjUxtrwylDY3ZXyOwlnCmlgK2Ybegdt8HT2zKo/GXE084zMh32kCk2eELzH6o7a5iwCPeYkfOUOGcH3gqmfqijIDJmPpYJWflIRhoShbCa0RvjLekSkmoD6lYpZvSxhjn6X1exQqUj5DkOTvYHiaFk4C+IW5sWAcf0AjQzwDQIDw6oiSCWHT6zIlZv5MWQxPPLMC35MpW5Dpn8hv1OLehzblhvlaCcQIfzZizN79CDp4Cn/J94E3ZT1zyIAZ//a+DqA==";

    let unblinder = "mYw9HF1Aej31EJNvDGcrPy2H6rM0ko5ucgPmMYSGeYPvkoYB9+s9tW01LwVcshO70Tur+z+0mcn3wcD18rArWYm3pHzubH20AoAC/ZykGZn7oYGLaJBkN7zc1gD0iT2HpqGoIz9lOTY7/UKr4C5bAsJuUVYgnsr0dNVwuYh+dF5qF9V9bZIOPPK8tJ6kNV2PBfBX7PmRbgirlnvX0wsqqxip8QR4cz2S8Z/z096PsgHz47Kh4MaOw6/MEfMgplUYu/lFOoryR/i/K189m+leps8GwJJOPKkEWM3KKdbCrrVYcJ6kHAnXEdh80tzHzLzmenmZdG1kzn6mZwAJ63FldA==";

    let res = crypto_core::unblind(blinded_signature, pubkey, unblinder).unwrap();
    println!("----- unblind -----\n{}", res);

    // todo: 
}
