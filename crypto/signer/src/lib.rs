use crypto_core;
use std::borrow::Borrow;
use std::ffi::CStr;
use std::ffi::CString;
use std::os::raw::c_char;

pub fn to_cstring<T: Borrow<str>, E: std::fmt::Display>(r: Result<T, E>) -> *mut c_char {
    let s = match r {
        Ok(v) => v.borrow().to_owned(),
        Err(e) => format!("err: {}", e),
    };

    let s = CString::new(s.as_bytes()).unwrap();
    s.into_raw()
}

fn from_cstring(str: *mut c_char) -> String {
    unsafe { CStr::from_ptr(str).to_string_lossy().into_owned() }
}

#[no_mangle]
pub extern "C" fn sign(encoded_digest: *mut c_char, signer_priv_key: *mut c_char) -> *mut c_char {
    let signer_priv_key = from_cstring(signer_priv_key);
    let encoded_digest = from_cstring(encoded_digest);

    to_cstring(crypto_core::sign(&encoded_digest, &signer_priv_key).map(|e| e.to_string()))
}

#[no_mangle]
pub extern "C" fn verify(
    message: *mut c_char,
    signature: *mut c_char,
    signer_pub_key: *mut c_char,
) -> *mut c_char {
    let message = from_cstring(message);
    let signature = from_cstring(signature);
    let signer_pub_key = from_cstring(signer_pub_key);

    to_cstring(crypto_core::verify(&message, &signature, &signer_pub_key))
}

