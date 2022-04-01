cd /crypto/signer \
    && cargo build --release

cd /crypto/sender \
    && wasm-pack build --target web \
    && sed -i -e "s/input = new URL('sender_bg.wasm', import.meta.url);//g" pkg/sender.js
