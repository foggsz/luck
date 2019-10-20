const buf = Buffer.from([0x62, 0x75, 0x66, 0x66, 0x65, 0x72]);
const crypto = require('crypto')

let passwrod = "abcdefghabcdefghabcdefghabcdefgh"
const algorithm = 'AES-256-ECB';
let data = "abcdefghabcdefgh"
let iv = Buffer.alloc(0)
let cipher = crypto.createCipheriv(algorithm, passwrod, iv)
let encryped = cipher.update(data, 'utf8', 'hex')
encryped =encryped+cipher.final('hex')
console.log(encryped)

//256 128 192 的意思是密钥的位数  字节长度=位数/8
// cbc的模式下需要使用初始向量，初始向量 用来与cbc第一个加密分组混淆密码，n个加密组需要和N-1个加密组混淆生成，初始向量位16个字节

let decipher = crypto.createDecipheriv(algorithm, passwrod, iv)
let decryped = decipher.update(encryped, 'hex', 'utf8')
decryped = decryped + W .final('utf8')
console.log(decryped)