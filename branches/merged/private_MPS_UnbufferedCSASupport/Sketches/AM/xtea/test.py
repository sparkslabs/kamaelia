import xtea
text = 'hello678'
key = '1234567890123456'
enc = xtea.xtea_encrypt(key,text).encode('hex')
print "encrypted text ",enc
dec = xtea.xtea_decrypt(key,enc.decode('hex'))
print "decrypted text ",dec

