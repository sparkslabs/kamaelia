aesmod so far has 3 functions
generate_key
enc_aes
and dec_aes

generate_key takes 2 parameters a string variable that should have enough
memory to hold the key generated and an int param that specifies the
keylength.
when the function returns, the first param will have the key.

both enc_aes and dec_aes will take input_file name output file name and key as
parameters.

please see aesint.h and keygen.h for proptotypes
