openssl genrsa -out pkcs1_priv.key
openssl rsa -in pkcs1_priv.key -pubout -out pub.key

openssl pkcs8 -topk8 -in pkcs1_priv.key -out priv.key -nocrypt

sed -i -z 's/\n//g' priv.key
sed -i -z 's/\n//g' pub.key

