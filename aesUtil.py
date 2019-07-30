from base64 import b64encode, encodebytes
from Crypto.Cipher import AES
import binascii
import re
import hashlib

BS = AES.block_size


def padding_pkcs5(value):
    return str.encode(value + (BS - len(value) % BS) * chr(BS - len(value) % BS))


def padding_zero(value):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)


def aes_ecb_encrypt(key, value):
    # AES/ECB/PKCS5padding
    # key is sha1prng encrypted before
    cryptor = AES.new(bytes.fromhex(key), AES.MODE_ECB)
    padding_value = padding_pkcs5(value)    # padding content with pkcs5
    ciphertext = cryptor.encrypt(padding_value)
    return ''.join(['%02x' % i for i in ciphertext]).upper()


def get_userkey(key, value):
    ''' AES/ECB/PKCS5Padding encrypt '''
    cryptor = AES.new(bytes.fromhex(key), AES.MODE_ECB)
    padding_value = padding_pkcs5(value)
    ciphertext = cryptor.encrypt(padding_value)
    return ''.join(['%02x' % i for i in ciphertext]).upper()


def get_sha1prng_key(key):
    '''[summary]
    encrypt key with SHA1PRNG
    same as java AES crypto key generator SHA1PRNG
    Arguments:
        key {[string]} -- [key]

    Returns:
        [string] -- [hexstring]
    '''
    signature = hashlib.sha1(key.encode()).digest()
    signature = hashlib.sha1(signature).digest()
    return ''.join(['%02x' % i for i in signature]).upper()[:32]

def aes_ecb_decrypt(key:str, value:str) -> str:
    ''' AES/ECB/NoPadding decrypt '''
    key = bytes.fromhex(key)
    cryptor = AES.new(key, AES.MODE_ECB)
    padding_value = padding_zero(value)
    #ciphertext = cryptor.decrypt(padding_value)
    ciphertext = cryptor.decrypt(bytes.fromhex(value))
    return ''.join(['%02x' % i for i in ciphertext]).upper()

def aes_ecb_decrypt_strip(key:str, value:str) -> str:
    ''' AES/ECB/NoPadding decrypt '''
    key = bytes.fromhex(key)
    cryptor = AES.new(key, AES.MODE_ECB)
    # base64_decrypted = base64.decodebytes(value.encode(encoding='utf-8'))
    ciphertext = cryptor.decrypt(bytes.fromhex(value))
    # 去除填充
    # return ''.join(['%02x' % i for i in ciphertext]).upper()
    return deal_control_char(str(ciphertext, "utf-8").strip())

def aes_ecb_decrypt_auto(key:str, value:str) -> str:
    ''' AES/ECB/NoPadding decrypt '''
    key = get_sha1prng_key(key)
    key = bytes.fromhex(key)
    cryptor = AES.new(key, AES.MODE_ECB)
    # base64_decrypted = base64.decodebytes(value.encode(encoding='utf-8'))
    ciphertext = cryptor.decrypt(bytes.fromhex(value))
    # 去除填充
    # return ''.join(['%02x' % i for i in ciphertext]).upper()
    return deal_control_char(str(ciphertext, "utf-8").strip())

def deal_control_char(s):
	temp=re.sub('[\x00-\x09|\x0b-\x0c|\x0e-\x1f]','',s)
	return temp

if __name__ == '__main__':
    key = get_sha1prng_key('b42effGcSYwzVH1e138L1JkM8aR4XXwQ')
    encrypt = aes_ecb_encrypt(key,'13430617013')
    print('加密后:',encrypt)
    decrypt = aes_ecb_decrypt_strip(key,encrypt)
    print('解密后:',decrypt)
    #C33586EE738F2326DEFB42C9046AD2CC
