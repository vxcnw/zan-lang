# System.Security.Cryptography

> 源码: `stdlib/System/Security/Cryptography/Aes.zan`, `stdlib/System/Security/Cryptography/AesGcm.zan`, `stdlib/System/Security/Cryptography/Base64.zan`, `stdlib/System/Security/Cryptography/BigInt.zan`, `stdlib/System/Security/Cryptography/Bits.zan`, `stdlib/System/Security/Cryptography/Hex.zan`, `stdlib/System/Security/Cryptography/Hkdf.zan`, `stdlib/System/Security/Cryptography/Hmac.zan`, `stdlib/System/Security/Cryptography/Jwt.zan`, `stdlib/System/Security/Cryptography/Md5.zan`, `stdlib/System/Security/Cryptography/Otp.zan`, `stdlib/System/Security/Cryptography/Rsa.zan`, `stdlib/System/Security/Cryptography/RsaKey.zan`, `stdlib/System/Security/Cryptography/Sha1.zan`, `stdlib/System/Security/Cryptography/Sha256.zan`, `stdlib/System/Security/Cryptography/Sha512.zan`, `stdlib/System/Security/Cryptography/Sm2.zan`, `stdlib/System/Security/Cryptography/Sm3.zan`, `stdlib/System/Security/Cryptography/Sm4.zan`


## Aes (class)

AES（FIPS-197）分组密码，支持 CBC 与 CTR 模式。支持
128/192/256 位密钥。纯 Zan 实现，面向字节（无 T 表）。S-box 以
十六进制存储并解码一次；逆 S-box 由它派生。

- static string SBOX_HEX()
  - AES S-box（256 字节）的十六进制文本，init 时解码一次。

- static byte[]sbox;

- static byte[]inv;

- static bool ready=false;

- static void init()
  - 惰性解码 S-box 并由它派生逆 S-box（幂等）。

- static int xtime(int x)
  - GF(2^8) 上乘 2（约减多项式 x^8+x^4+x^3+x+1）。

- static int gmul(int a, int b)
  - GF(2^8) 上的乘法（俄罗斯农民乘法）。

- static byte[]expandKey(string key, int keyLen, List<int> nrOut){ init}
  - 将密钥扩展为 (Nr+1)*16 字节轮密钥。返回缓冲区；
    <paramref name="nrOut"/>[0] 接收轮数。

- static void addRoundKey(byte[]st, byte[]rk, int round)
  - 第 `round` 轮密钥异或进 16 字节状态。

- static void encryptBlock(byte[]st, byte[]rk, int nr)
  - 单块加密：SubBytes/ShiftRows/MixColumns 共 nr 轮加首尾轮密钥。

- static void decryptBlock(byte[]st, byte[]rk, int nr)
  - 单块解密（encryptBlock 的逆序）。

- static void shiftRows(byte[]st)
  - 行移位（状态按列主序存放）。

- static void invShiftRows(byte[]st)
  - 逆行移位。

- static void mixColumns(byte[]st)
  - 列混合（系数 2/3，经 xtime 展开）。

- static void invMixColumns(byte[]st)
  - 逆列混合（系数 9/11/13/14，经 gmul）。

- static byte[]EncryptBlockEcb(string key, int keyLen, string in16)
  - 加密单个 16 字节分组（ECB）。用于测试/构建
    其他模式。返回全新的 16 字节缓冲区；输入长度或密钥长度
    不合法时返回 null。

- static byte[]DecryptBlockEcb(string key, int keyLen, string in16)
  - AES-ECB 单块解密（EncryptBlockEcb 的逆）。
    同样只用于测试/构建其他模式；参数不合法返回 null。

- static byte[]EncryptCbc(string key, int keyLen, string iv, string data, int len, List<int> outLen)
  - AES-CBC 加密，PKCS#7 填充。返回密文；
    <paramref name="outLen"/>[0] 接收其长度。keyLen 必须是
    16/24/32（否则返回 null）。

- static byte[]DecryptCbc(string key, int keyLen, string iv, string data, int len, List<int> outLen)
  - AES-CBC 解密，去除 PKCS#7 填充。返回明文；
    <paramref name="outLen"/>[0] 接收其长度（密文长度非 16 整数倍、
    或 PKCS#7 填充不一致时为 -1，并返回 null）。填充校验要求
    最后 padVal 字节全部等于 padVal，而非仅看最后一个字节。

- static byte[]Ctr(string key, int keyLen, string iv, string data, int len)
  - AES-CTR（加密==解密）。<paramref name="iv"/> 是 16 字节的
    初始计数器块。返回恰好 <paramref name="len"/> 字节
    的缓冲区；密钥长度或长度参数不合法时返回 null。


## AesGcm (class)

纯 Zan 实现的 AES-GCM（NIST SP 800-38D）认证加密。
仅支持常见的 96 位 IV 形式（J0 = IV || 0^31 || 1）。
128 位分组以两个 64 位半字（long）表示；GF(2^128)
乘法采用右移算法，约简多项式
R = 0xE1||0^120。

- static long load64(string buf, int off)
  - 从 buf[off..] 读取 8 个大端字节到一个 64 位字

- static void store64(byte[]buf, int off, long v)
  - 64 位字按大端写入 buf 的 off 处。

- static List<long> gfmul(List<long> X, List<long> Y)
  - GF(2^128) 乘法：X、Y 按 [hi,lo] 表示；返回 [hi,lo]

- static List<long> ghashBlock(List<long> Y, string buf, int off, int avail, List<long> H)
  - Y = (Y xor block) * H，其中 block 是 buf[off..] 处 16 字节，不足补零

- static List<long> ghash(List<long> H, string aad, int aadLen, string data, int dataLen)
  - GHASH：AAD 块、密文块再接长度块，在 GF(2^128) 上逐块累乘 H。

- static void inc32(byte[]ctr)
  - 计数器块的低 32 位（第 12..15 字节，大端）加一。

- static void gctr(string key, int keyLen, string ctr, string data, int dataLen, byte[]outb)
  - GCTR：由 AES(counter) 生成密钥流，与数据异或（原地写入 out）

- static byte[]Encrypt(string key, int keyLen, string iv, string aad, int aadLen, string pt, int ptLen, string tagOut)
  - AES-GCM 加密，使用 96 位（12 字节）IV。密文
    （与明文等长）写入返回值，16 字节 tag 写入
    <paramref name="tagOut"/>。参数不合法（密钥长度、
    长度字段为负、输出缓冲区缺失等）时返回 null。

- static byte[]Decrypt(string key, int keyLen, string iv, string aad, int aadLen, string ct, int ctLen, string tag, List<int> ok)
  - AES-GCM 解密，使用 96 位 IV。校验通过时返回明文
    并将 <paramref name="ok"/>[0] 置 -1（true）；tag/aad/密文被篡改时
    返回 null 并将 <paramref name="ok"/>[0] 置 0。**调用方绝不能
    在 ok != -1 时使用任何返回值**——认证失败不产出明文是 GCM 的
    核心安全性质，API 本身保证这一点，而非依赖调用方检查。


## Base64 (class)

对原始字节缓冲区的标准 Base64（RFC 4648）编解码。

- static string ALPHA()
  - RFC 4648 标准 Base64 字母表（A–Z、a–z、0–9、`+`、`/`）。

- static string Encode(string buf, int len)
  - 将 <paramref name="len"/> 字节编码为 Base64 文本。

- static int dec(int c)
  - 单个 Base64 字符转 6 位值；非法字符返回 -1。

- static byte[]Decode(string s, List<int> outLen)
  - 将 Base64 文本解码为字节缓冲区。
    <paramref name="outLen"/>[0] 接收解码后的字节数；
    遇到非法字符或填充错误时置为 -1 并返回 null。


## BigInt (class)

任意精度非负整数，使用 32 位 limb 存储
以小端序（limb 0 为最低有效位）存放在 List<long> 中。足以支持
RSA 与 SM2 的比较、加减乘、Montgomery 模幂运算和
模逆。每个 limb 取值在 [0, 2^32) 内，两个 limb 的乘积
作为位模式可放入有符号 64 位 long，所有高字
提取均通过 Bits.Shr64 使用逻辑（而非算术）移位。

- List<long> d;

- static BigInt make(List<long> limbs)
  - 由 limb 列表构造并修剪高位零。

- void trim()
  - 去掉高位零 limb（至少保留一位）。

- int count()
  - limb 个数。

- long limb(int i)
  - 第 i 个 limb（越界返回 0；按 32 位无符号解释）。

- bool isZero()
  - 是否为零。

- static BigInt zero()
  - 值 0。

- static BigInt one()
  - 值 1。

- static BigInt FromBytesBE(string buf, int len)
  - 从大端序字节缓冲区构建 BigInt。
    大端序字节缓冲区 → BigInt（RSA/SM2 整数编码的标准字节序）。

- byte[]ToBytesBE(int outLen)
  - 序列化为恰好 <paramref name="outLen"/> 字节的大端序缓冲区
    （左侧补零；过小时截断高位字节）。
    序列化为无符号大端整数（0 ≤ v < 256^outLen）；过小时高位补零，
    过大时静默截断高位——调用方需保证 outLen 足够容纳。

- static int cmp(BigInt a, BigInt b)
  - 比较：a > b 返回 1，a < b 返回 -1，相等返回 0。

- static BigInt add(BigInt a, BigInt b)
  - 无符号加法。

- static BigInt sub(BigInt a, BigInt b)
  - 无符号减法 a - b；要求 a >= b（否则借位下溢）。

- static BigInt mul(BigInt a, BigInt b)
  - 无符号乘法（教科书 O(n²)，limb 基 2^32）。

- static long montInv(long n0)
  - -n[0]^{-1} mod 2^32（Montgomery 参数 n'，Newton 迭代求出）。

- static BigInt montMul(BigInt a, BigInt b, BigInt n, long n0inv)
  - Montgomery 乘积：a * b * R^{-1} mod n，R = 2^(32k)。要求 a、b < n。

- static BigInt pow2mod(int bits, BigInt n)
  - 通过反复翻倍计算 2^(bits) mod n

- int bitLength()
  - 有效位长（0 计为 1 位）。

- int getBit(int idx)
  - 第 idx 位的值（0 起，低位在前）。

- static BigInt ModPow(BigInt g, BigInt exp, BigInt n)
  - 模幂 base^exp mod n（Montgomery 阶梯，n 必须为奇数——RSA/SM2
    的模数均满足）。要求 base < n；返回值已约减到 [0, n)。

- static BigInt ModInverse(BigInt a, BigInt m)
  - 用二进制扩展欧几里得算法求模逆 a^{-1} mod m（m 无需为素数）。
    不可逆（gcd(a,m) ≠ 1）时返回零。

- static BigInt subSigned(BigInt a, bool aneg, BigInt b, bool bneg, List<bool> outNeg)
  - 有符号减法 a(符号 aneg) - b(符号 bneg)；返回绝对值，符号写入 out[0]

- static List<BigInt> divmod(BigInt a, BigInt b)
  - 教科书式长除法：返回 [商, 余数]

- static BigInt mod(BigInt a, BigInt m)
  - a mod m（经 divmod 取余数）。

- static BigInt setBit(BigInt x, int idx)
  - 返回第 idx 位置 1 的副本。


## Bits (class)

哈希/加密原语共用的位操作辅助函数。32 位操作（Rotl32/Rotr32）
存放在 int 中，64 位辅助函数（Shr64/Rotr64）
作用于 long。需要 32 位结果时，调用方用 0xFFFFFFFF 掩码。

- static int Rotl32(int x, int n)
  - 32 位循环左移。

- static int Rotr32(int x, int n)
  - 32 位循环右移。

- static long Shr64(long x, int n)
  - 64 位值的逻辑（无符号）右移。Zan 的 <c>>></c>
    是算术右移，因此需将符号扩展出的高位掩掉。

- static long Rotr64(long x, int n)
  - 64 位循环右移（SHA-512 使用）。


## Hex (class)

对原始字节缓冲区进行小写十六进制编解码
（Zan 字符串当作字节数组使用）。

- static string Encode(string buf, int len)
  - 将 <paramref name="buf"/> 的 <paramref name="len"/> 字节
    编码为小写十六进制字符串。

- static int nibble(int c)
  - 单个十六进制字符转数值（0-9、a-f、A-F）；其余字符返回 0（不报错）。

- static byte[]Decode(string hex)
  - 将十六进制字符串解码为
    <c>hex.Length / 2</c> 字节的缓冲区。


## Hkdf (class)

基于 HMAC-SHA256 的 HKDF（RFC 5869）：先提取后扩展的密钥
派生。用于从单一主密钥派生各用途的子密钥，这样
泄漏的子密钥永远不会暴露主密钥或兄弟子密钥。

- static byte[]Extract(string salt, int saltLen, string ikm, int ikmLen)
  - HKDF-Extract：PRK = HMAC-SHA256(salt, ikm)。返回 32 字节。

- static byte[]Expand(string prk, string info, int infoLen, int outLen)
  - HKDF-Expand：派生 <paramref name="outLen"/> 字节（最多 8160），
    输入为 32 字节 PRK 和 context/info 字符串。

- static byte[]Derive(string salt, int saltLen, string ikm, int ikmLen, string info, int infoLen, int outLen)
  - 一步调用的 HKDF：先 Extract 再 Expand。


## Hmac (class)

基于本命名空间中 SHA/MD5/SM3 原语的 HMAC（RFC 2104）。
所有支持的哈希均使用 64 字节分组。

- static int SHA256=0;

- static int SHA1=1;

- static int SM3=2;

- static int MD5=3;

- static int digestLen(int algo)
  - 返回算法对应的摘要字节数（SHA256/SM3 为 32，SHA1 为 20，MD5 为 16）。

- static byte[]hashOf(int algo, string buf, int len)
  - 按算法编号分发到底层哈希的 `Hash`（未知编号按 SHA-256 处理）。

- static byte[]Compute(int algo, string key, int keyLen, string msg, int msgLen)
  - 按所选算法计算 HMAC（0=SHA256、1=SHA1、
    2=SM3、3=MD5）。摘要长度等于底层哈希的输出
    长度。

- static byte[]Sha256Mac(string key, int keyLen, string msg, int msgLen)
  - 以 SHA-256 计算 HMAC 的便捷封装。


## Jwt (class)

紧凑 JWS 令牌的 JSON Web Token 辅助函数。支持 HS256 和 RS256；
不安全（`none`）令牌及一切未被请求的算法都会被拒绝。解析
使用调用方提供的 Unix 时间戳，因此 exp/nbf 校验结果是确定性的。
预期的 issuer/audience 为空字符串时，仅禁用各自的校验。

- static int maxTokenSize()
  - 令牌总长上限（128 KiB）。

- static int maxHeaderSize()
  - header 段解码后字节上限（8 KiB）。

- static int maxPayloadSize()
  - payload 段解码后字节上限（64 KiB）。

- static string urlAlphabet()
  - Base64Url 字母表（RFC 4648 §5，`-_` 代替 `+/`，无填充）。

- static int urlDigit(int c)
  - Base64Url 字符 -> 6 位值；非法字符返回 -1。

- static string Base64UrlEncode(string bytes, int len)
  - 将恰好 <paramref name="len"/> 字节编码为无填充的 RFC 4648 Base64Url。

- static byte[]Base64UrlDecode(string text, List<int> outLen)
  - 严格解码无填充的 Base64Url。outLen[0] 为字节数，输入格式错误时为 -1。

- static int dotAt(string token, int from)
  - 从 `from` 起第一个 '.' 的下标；没有则 -1。

- static bool fixedEquals(string actual, int actualLen, string expected, int expectedLen)
  - 常量时间比较（长度差也并入累积差），防签名校验的时序侧信道。

- static bool hasDuplicateKeys(JsonValue node)
  - JSON 树中对象层是否存在重复键（重复键会改变语义，按非法拒绝）。

- static bool readNumericDate(JsonValue node, List<long> result)
  - 读 JWT NumericDate（纯数字串）到 result[0]；非数字或溢出 long 时
    返回 false。

- static JwtToken fail(string error)
  - 构造校验失败的 JwtToken：valid=false，error 为固定文案，无内容。

- static JwtToken parseParts(string token, string algorithm)
  - 拆分三段式令牌并解码：限长、Base64Url、JSON 对象、重复键与
    header.alg 必须恰为 `algorithm`；失败返回带错误文案的 token。

- static string validateClaims(JwtToken token, long now, string issuer, string audience)
  - 按调用方提供的 now 校验 exp/nbf（NumericDate）与 iss/aud
    （空串关闭对应校验）；通过返回 ""，否则返回错误文案。

- static string CreateHs256(string payloadJson, string secret, int secretLen)
  - 由对象形式的 payload JSON 和带字节数的密钥创建 HS256 紧凑 JWT。

- static JwtToken ParseHs256(string token, string secret, int secretLen, long now, string issuer, string audience)
  - 仅解析并校验 HS256，然后对照显式输入验证 exp、nbf、iss 和 aud。

- static string CreateRs256(string payloadJson, RsaKey privateKey)
  - 用 RSA 私钥创建 RS256 紧凑 JWT；密钥无法签名时返回空。

- static JwtToken ParseRs256(string token, RsaKey publicKey, long now, string issuer, string audience)
  - 仅解析并校验 RS256，然后对照显式输入验证 exp、nbf、iss 和 aud。


## JwtToken (class)

已解码的 JWT 及其签名与声明校验结果。

- bool valid;

- string error;

- string headerJson;

- string payloadJson;

- JsonValue header;

- JsonValue payload;

- bool IsValid()
  - 仅当结构、算法、签名、JSON 及所请求的声明全部有效时才为 true。

- string Error()
  - 令牌有效时返回空字符串，否则返回固定的校验错误信息。

- string HeaderJson()
  - 解码后的紧凑 header JSON，解码失败时为空字符串。

- string PayloadJson()
  - 解码后的紧凑 payload JSON，解码失败时为空字符串。

- JsonValue Header()
  - 解析后的 header 对象，解码或 JSON 解析失败时为 null。

- JsonValue Payload()
  - 解析后的声明对象，解码或 JSON 解析失败时为 null。


## Md5 (class)

RFC 1321 MD5。仅供遗留/互操作场景使用；不具有抗碰撞性，
不适合用于新的安全场景。

- static byte[]Hash(string msg, int len)
  - 计算 MD5；返回新分配的 16 字节摘要。

- static void wLE(byte[]b, int o, int v)
  - 按小端序把 32 位字 v 写入 b 偏移 o 处的 4 个字节。


## Otp (class)

HOTP（RFC 4226）和 TOTP（RFC 6238）一次性密码。

- static int SHA1=1;
  - 哈希算法常量：SHA-1（摘要 20 字节）。

- static int SHA256=2;
  - 哈希算法常量：SHA-256（摘要 32 字节）。

- static int SHA512=3;
  - 哈希算法常量：SHA-512（摘要 64 字节）。

- static int MAX_VERIFICATION_WINDOW=1000;
  - 验证窗口上限，防止把校验接口变成穷举放大器。

- static int digestLen(int algorithm)
  - 算法对应的摘要长度（字节）。

- static int blockLen(int algorithm)
  - HMAC 分组长度（字节；SHA-512 为 128，其余 64）。

- static byte[]hash(int algorithm, string buf, int length)
  - 按算法常量分发到对应 Sha*.Hash。

- static byte[]hmac(int algorithm, string key, int keyLen, string message, int messageLen)
  - 通用 HMAC（RFC 2104）；超长密钥先哈希归一化到分组长度。
    本文件内部的独立实现，不经 `Hmac`。

- static int modulus(int digits)
  - 10^digits（动态截断模）。

- static string decimalCode(int number, int digits)
  - 验证码左补零到 `digits` 位。

- static void validate(int digits, int algorithm)
  - 校验位数（6-8）与算法常量，非法即抛 ArgumentException。

- static void validateKey(string key, int keyLen)
  - 校验密钥非空且 keyLen 在 [0, key.Length]，非法即抛 ArgumentException。

- static void validateCode(string code, int digits)
  - 校验验证码非空、长度等于 digits 且全为十进制数字，非法即抛 ArgumentException。

- static void validateWindow(int window, string name)
  - 校验验证窗口在 [0, MAX_VERIFICATION_WINDOW]，非法即抛 ArgumentException。

- static string Hotp(string key, int keyLen, long counter, int digits, int algorithm)
  - 为显式的 64 位计数器生成 HOTP 验证码。
    <paramref name="digits"/> 必须在 6 到 8 之间。

- static string Totp(string key, int keyLen, long unixTime, int period, int digits, int algorithm)
  - 当前 Unix 时间与周期的关系即时生成 TOTP 验证码；
    常用 30 秒周期。digits 6-8。

- static bool fixedTimeEquals(string expected, string supplied)
  - 校验失败恒定时间比较（长度差参与累积，不提前返回），
    防止按比较耗时逐位猜码。

- static bool VerifyHotp(string key, int keyLen, long counter, int digits, int algorithm, string code, int lookAhead)
  - 以恒定时间校验当前计数器及其后
    <paramref name="lookAhead"/> 个计数器的 HOTP。

- static bool VerifyTotp(string key, int keyLen, long unixTime, int period, int digits, int algorithm, string code, int window)
  - 以恒定时间在对称漂移窗口内校验 TOTP。
    窗口为 1 时校验前、当前、后三个时间段。


## Rsa (class)

RSA（RFC 8017 / PKCS#1）：原始公/私钥运算以及 PKCS#1
v1.5 和 OAEP 加密填充。大整数运算来自 BigInt；哈希
（OAEP 的 MGF1 用）来自本命名空间。所有缓冲区都显式携带长度，
因为 String.Length 基于 strlen，对二进制数据不安全。

- static int hLen(int algo)
  - 哈希分发：0=SHA-256，1=SHA-1，2=SM3

- static byte[]hashOf(int algo, string buf, int len)
  - 按算法常量分发到对应摘要函数（0=SHA-256，1=SHA-1，2=SM3）。

- static byte[]ModExp(string msg, int mLen, string n, int nLen, string exp, int eLen)
  - 原始 RSA：base^exp mod n。返回 k 字节大端序缓冲区，
    其中 k = <paramref name="nLen"/>。

- static byte[]mgf1(string seed, int seedLen, int maskLen, int algo)
  - MGF1 掩码生成（RFC 8017）

- static byte[]EncryptOaep(string msg, int mLen, string n, int k, string e, int eLen, int algo, string seed)
  - RSA-OAEP 加密（RFC 8017 §7.1.1）。<paramref name="seed"/> 必须
    提供 hLen 个全新随机字节。label 为空。返回 k 字节密文；
    若消息对 k 而言过长（mLen > k - 2*hLen - 2）或 k 过小
    （k < 2*hLen + 2），返回 null，绝不写入越界。

- static byte[]DecryptOaep(string cph, string n, int k, string d, int dLen, int algo, List<int> outLen)
  - RSA-OAEP 解密（RFC 8017 §7.1.2）。返回恢复出的消息；
    <paramref name="outLen"/>[0] 接收其长度，编码结构非法（Y!=0、
    lHash 不符、缺 0x01 分隔符、k 过小）时为 -1。所有失败路径走
    同一条返回，不因错误位置不同而泄露 padding oracle。

- static byte[]EncryptPkcs1(string msg, int mLen, string n, int k, string e, int eLen, string rnd)
  - RSA PKCS#1 v1.5 type-2 加密。<paramref name="rnd"/> 提供
    填充串所需的 (k - mLen - 3) 个非零随机字节。若消息过长
    （mLen > k - 11）或随机数不足，返回 null。

- static byte[]DecryptPkcs1(string cph, string n, int k, string d, int dLen, List<int> outLen)
  - RSA PKCS#1 v1.5 解密。<paramref name="outLen"/>[0] 接收
    消息长度（填充错误时为 -1）。

- static byte[]sha256DigestInfo()
  - SHA-256 的 DigestInfo 前缀（RFC 8017 §9.2 注 1）

- static byte[]emsaPkcs1Sha256(string msg, int mLen, int k)
  - 将 SHA-256(msg) 按 EMSA-PKCS1-v1_5 编码为 k 字节

- static byte[]SignPkcs1Sha256(string msg, int mLen, string n, int k, string d, int dLen)
  - 对 SHA-256(msg) 计算 RSASSA-PKCS1-v1_5 签名。返回
    k 字节的签名（k = 模数字节数）。

- static bool VerifyPkcs1Sha256(string msg, int mLen, string sig, string n, int k, string e, int eLen)
  - 校验 RSASSA-PKCS1-v1_5 SHA-256 签名。


## RsaKey (class)

RSA 密钥材料，从 PEM（PKCS#1、PKCS#8 或 SubjectPublicKeyInfo）加载。
现有 `Rsa` 原语使用模数/指数的字节
缓冲区；本类提供可复用的 PEM/DER 解码层，供
签名 HTTP 协议和数据库客户端使用。

- byte[]modulus;

- byte[]publicExponent;

- byte[]privateExponent;

- int modulusLength;

- int publicExponentLength;

- int privateExponentLength;

- RsaKey()

- int ModulusLength()
  - 模数长度（字节），即签名/密文长度。

- bool HasPrivateKey()
  - 是否含私钥指数（public key 时为 false，不能 Sign/Decrypt）。

- static int Find(string hay, string needle, int from)
  - 从 `from` 起查找子串首次出现，找不到返回 -1。

- static byte[]PemToDer(string pem, List<int> outLen)
  - 剥掉 PEM 封装（BEGIN/END 行与软换行）后按 Base64 解码为 DER；
    找不到 PEM 边界时返回 null 且 outLen[0] = 0。

- static int ReadLength(string der, List<int> cursor)
  - 读 DER TLV 的长度字段（短/长形式），cursor 前移过它。

- static int Enter(string der, List<int> cursor, int tag)
  - 期望 `tag` 并进入其内容，返回内容结束下标；tag 不符返回 -1。

- static byte[]ReadIntegerSafe(string der, List<int> cursor, List<int> outLen)
  - 读 DER INTEGER，去掉前导 0x00 符号字节；非 INTEGER 返回 null。

- static RsaKey ParsePkcs1Private(string der, int offset)
  - 解析 PKCS#1 RSAPrivateKey（读 version/n/e/d；CRT 分量不读取）。
    结构不符返回 null。

- static int SkipElement(string der, List<int> cursor)
  - 跳过一个 DER 元素（标签+长度+内容），cursor 停在其末尾。

- static RsaKey ParseSpkiPublic(string der, int offset)
  - 解析 SubjectPublicKeyInfo：跳过 AlgorithmIdentifier，取 BIT STRING
    内的 PKCS#1 公钥。结构不符返回 null。

- static RsaKey ParseCertificatePublic(string der)
  - 解析 X.509 证书：定位 tbsCertificate 的 SubjectPublicKeyInfo 并取其
    RSA 公钥。结构不符返回 null。

- static RsaKey ParsePkcs1Public(string der, int offset)
  - 解析 PKCS#1 RSAPublicKey（n, e）；结构不符返回 null。

- static RsaKey FromPrivatePem(string pem)
  - 从 PEM 私钥加载：支持 PKCS#1（BEGIN RSA PRIVATE KEY）与
    PKCS#8（BEGIN PRIVATE KEY）。解析失败返回 null。

- static RsaKey FromPublicPem(string pem)
  - 从 PEM 公钥加载：支持 SubjectPublicKeyInfo（BEGIN PUBLIC KEY）、
    PKCS#1 公钥及 X.509 证书（BEGIN CERTIFICATE，取其 SubjectPublicKeyInfo）。
    解析失败或非 RSA 密钥返回 null。

- string SignSha256(string message)
  - RSA PKCS#1 v1.5 SHA-256 签名，返回 Base64。无私钥时返回空串。

- bool VerifySha256(string message, string signatureBase64)
  - 校验 PKCS#1 v1.5 SHA-256 签名（Base64 编码，长度须等于模数长度）。

- string EncryptOaepSha1(string plaintext)
  - RSA-OAEP(SHA-1) 公钥加密，返回 Base64 密文（长度=模数长度）。
    输出上限约 modLen - 42 字节，超长会失败——常规做法是用本方法
    包一个对称密钥再加密正文。


## Sha1 (class)

FIPS 180-4 SHA-1。仅供遗留/互操作场景（如 HMAC-SHA1）使用；
不建议用于新的安全场景。

- [DllImport("crt", EntryPoint="fopen")]static extern nint PlatFopen(string path, string mode);

- [DllImport("crt", EntryPoint="fread")]static extern long PlatFread(byte[]buf, long size, long count, nint fp);

- [DllImport("crt", EntryPoint="fclose")]static extern int PlatFclose(nint fp);

- static byte[]Hash(string msg, int len)
  - 计算 SHA-1；返回 20 字节摘要。

- static byte[]HashBytes(byte[]data, int len)
  - 对字节缓冲区的前 <paramref name="len"/> 字节计算 SHA-1。

- static byte[]HashFile(string path)
  - 流式计算文件的 SHA-1（不把文件整体读入内存），返回
    20 字节摘要；打开失败返回 null。

- static string HashFileHex(string path)
  - 流式计算文件的 SHA-1 并返回小写十六进制串；失败返回空串。

- static string ToHex(byte[]digest)
  - 把摘要编码为小写十六进制串。

- static bool VerifyFile(string path, string expectedHex)
  - 按十六进制摘要校验文件（大小写不敏感）。

- static int[]NewState()
  - 初始链接变量 h0..h4（FIPS 180-4 §5.3.1）。

- static byte[]Finish(int[]h, byte[]tail, int tailLen, long totalBytes)
  - 追加 FIPS 填充（0x80、零、64 位大端比特长度）并返回摘要；
    tail 保存最后一个不完整块（tailLen < 64）。

- static void Block(int[]h, byte[]m, int off)
  - 单个 64 字节块的压缩函数，原地更新 h[0..4]。

- static void wBE(byte[]b, int o, int v)
  - 32 位整数按大端写入 b 的 o 处。


## Sha256 (class)

FIPS 180-4 SHA-256。纯 Zan 实现，直接操作原始字节缓冲区。

- static byte[]Hash(string msg, int len)
  - 对 <paramref name="len"/> 字节计算 SHA-256；返回
    新分配的 32 字节摘要（由调用方释放）。

- static void wBE(byte[]buf, int off, int v)
  - 按大端序把 32 位字 v 写入 buf 偏移 off 处的 4 个字节。


## Sha512 (class)

纯 Zan 实现的 SHA-512（FIPS 180-4）。操作以 Zan 有符号 64 位 long
存放的 64 位数据；加法按 mod 2^64 回绕，所有右移都使用
逻辑位移辅助函数 Bits.Shr64 / Bits.Rotr64。消息长度限制为
64 位比特数（128 位长度字段的高 64 位始终为零）。

- static string KHEX="428a2f98d728ae227137449123ef65cdb5c0fbcfec4d3b2fe9b5dba58189dbbc3956c25bf348b53859f111f1b605d019923f82a4af194f9bab1c5ed5da6d8118d807aa98a303024212835b0145706fbe243185be4ee4b28c550c7dc3d5ffb4e272be5d74f27b896f80deb1fe3b1696b19bdc06a725c71235c19bf174cf692694e49b69c19ef14ad2efbe4786384f25e30fc19dc68b8cd5b5240ca1cc77ac9c652de92c6f592b02754a7484aa6ea6e4835cb0a9dcbd41fbd476f988da831153b5983e5152ee66dfaba831c66d2db43210b00327c898fb213fbf597fc7beef0ee4c6e00bf33da88fc2d5a79147930aa72506ca6351e003826f142929670a0e6e7027b70a8546d22ffc2e1b21385c26c9264d2c6dfc5ac42aed53380d139d95b3df650a73548baf63de766a0abb3c77b2a881c2c92e47edaee692722c851482353ba2bfe8a14cf10364a81a664bbc423001c24b8b70d0f89791c76c51a30654be30d192e819d6ef5218d69906245565a910f40e35855771202a106aa07032bbd1b819a4c116b8d2d0c81e376c085141ab532748774cdf8eeb9934b0bcb5e19b48a8391c0cb3c5c95a634ed8aa4ae3418acb5b9cca4f7763e373682e6ff3d6b2b8a3748f82ee5defb2fc78a5636f43172f6084c87814a1f0ab728cc702081a6439ec90befffa23631e28a4506cebde82bde9bef9a3f7b2c67915c67178f2e372532bca273eceea26619cd186b8c721c0c207eada7dd6cde0eb1ef57d4f7fee6ed17806f067aa72176fba0a637dc5a2c898a6113f9804bef90dae1b710b35131c471b28db77f523047d8432caab7b40c724933c9ebe0a15c9bebc431d67c49c100d4c4cc5d4becb3e42b6597f299cfc657e2a5fcb6fab3ad6faec6c44198c4a475817";

- static string HHEX="6a09e667f3bcc908bb67ae8584caa73b3c6ef372fe94f82ba54ff53a5f1d36f1510e527fade682d19b05688c2b3e6c1f1f83d9abfb41bd6b5be0cd19137e2179";

- static List<long> K;

- static List<long> H0;

- static bool ready=false;

- static long word64(string h, int idx)
  - 把十六进制串中第 idx 个 64 位字（16 个 hex 字符）解析为 long。

- static void init()
  - 惰性装载 80 个轮常量 K 与初始哈希 H0（幂等）。

- static long s0(long x)
  - 消息调度 σ0(x) = ROTR1 ^ ROTR8 ^ SHR7。

- static long s1(long x)
  - 消息调度 σ1(x) = ROTR19 ^ ROTR61 ^ SHR6。

- static long bigS0(long x)
  - 压缩函数 Σ0(a) = ROTR28 ^ ROTR34 ^ ROTR39。

- static long bigS1(long x)
  - 压缩函数 Σ1(e) = ROTR14 ^ ROTR18 ^ ROTR41。

- static byte[]Hash(string msg, int len){ init}
  - 对 <paramref name="msg"/> 的前
    <paramref name="len"/> 字节计算 64 字节 SHA-512 摘要。


## Sm2 (class)

SM2 公钥密码（GB/T 32918 / GM/T 0003），基于
标准 256 位素数曲线，构建于 BigInt 之上。提供密钥派生
（d*G）、SM2 数字签名（用 ZA 用户哈希签名/验签）以及
C1C3C2 形式的 SM2 公钥加密。点以 Jacobian 坐标存储，
因此每次标量乘法只需一次模逆。

- static string PHEX="FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF";

- static string AHEX="FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC";

- static string BHEX="28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93";

- static string NHEX="FFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123";

- static string GXHEX="32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7";

- static string GYHEX="BC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0";

- static BigInt P;

- static BigInt A;

- static BigInt B;

- static BigInt N;

- static BigInt GX;

- static BigInt GY;

- static bool ready=false;

- static BigInt hb(string h)
  - 十六进制串 -> 大端字节 -> BigInt。

- static void init()
  - 惰性装载 SM2 推荐曲线参数（幂等）。

- static BigInt fromInt(int v)
  - 小整数 -> BigInt（大端 4 字节）。

- static BigInt fadd(BigInt x, BigInt y)
  - (x + y) mod P。

- static BigInt fsub(BigInt x, BigInt y)
  - (x - y) mod P。

- static BigInt fmul(BigInt x, BigInt y)
  - (x * y) mod P。

- static BigInt fsqr(BigInt x)
  - x² mod P。

- static BigInt finv(BigInt x)
  - 模逆 x⁻¹ mod P。

- static BigInt nmod(BigInt x)
  - x mod N。

- static BigInt nsub(BigInt x, BigInt y)
  - (x - y) mod N。

- static BigInt nmul(BigInt x, BigInt y)
  - (x * y) mod N。

- static BigInt ninv(BigInt x)
  - 模逆 x⁻¹ mod N。

- static List<BigInt> pt(BigInt x, BigInt y, BigInt z)
  - 构造 Jacobian 点 [X, Y, Z]。

- static List<BigInt> inf()
  - 无穷远点（Z = 0）。

- static bool isInf(List<BigInt> Pt)
  - 是否无穷远点。

- static List<BigInt> jdouble(List<BigInt> Pt)
  - Jacobian 倍点（本曲线 a ≡ -3 (mod P) 的倍点公式）。

- static List<BigInt> jadd(List<BigInt> Pa, List<BigInt> Qa)
  - Jacobian 点加；X 相同且 Y 相同回退为倍点，Y 相反回退为无穷远点。

- static List<BigInt> scalarMul(BigInt k, List<BigInt> Pt)
  - 二进制阶梯标量乘 k*Pt（从无穷远点开始，高位在前）。

- static List<BigInt> toAffine(List<BigInt> Pt)
  - 返回仿射坐标 [x, y]；若为无穷远点（Z==0）则返回类似 null 的 inf()

- static List<BigInt> gPoint()
  - 基点 G（仿射，Z = 1）。

- static List<BigInt> PublicKey(BigInt d){ init}
  - 从私钥标量派生公钥点（d*G）。
    返回仿射坐标 [x, y]，各 32 字节 BigInt。

- static void writeBE32(string dst, int off, BigInt v)
  - 把 v 的大端 32 字节写入 dst 的 off 处（Zan string 按字节写入）。

- static BigInt computeE(string id, int idLen, string msg, int msgLen, BigInt px, BigInt py){ init}
  - SM2 签名使用的基于 SM3 的 ZA||M 摘要 e（默认 id
    "1234567812345678" 由调用方以字节形式提供）。

- static void Sign(BigInt e, BigInt d, BigInt k, string outSig){ init}
  - SM2 签名。e 为 ZA||M 摘要；k 为每次签名使用的秘密数，
    取值 [1, n-1]。将 r 写入 out[0..31]，s 写入 out[32..63]。

- static bool Verify(BigInt e, BigInt px, BigInt py, BigInt r, BigInt s){ init}
  - 用公钥 (px,py) 校验摘要 e 上的 SM2 签名 (r,s)。
    有效时返回 true。

- static byte[]kdf(string z, int zLen, int klen)
  - GB/T 32918.4 中的 KDF

- static byte[]Encrypt(string msg, int msgLen, BigInt px, BigInt py, BigInt k, List<int> outLen){ init}
  - SM2 公钥加密（C1C3C2，C1 带 0x04 前缀）。
    k 为每条消息的秘密数。outLen[0] 接收密文长度。

- static byte[]Decrypt(string cph, int cphLen, BigInt d, List<int> outLen){ init}
  - 对 C1C3C2 密文（C1 带 0x04 前缀）进行 SM2 解密。返回
    明文；outLen[0] 接收其长度（C3 校验失败时为 -1）。

- static byte[]sliceBE(string src, int off)
  - 从 src 的 off 起读 32 字节（供 BigInt.FromBytesBE）。


## Sm3 (class)

GM/T 0004-2012 SM3（中国国家密码哈希），256 位
输出。纯 Zan 实现，直接操作原始字节缓冲区。

- static int p0(int x)
  - 布尔置换 P0(x) = x ^ ROTL9(x) ^ ROTL17(x)。

- static int p1(int x)
  - 布尔置换 P1(x) = x ^ ROTL15(x) ^ ROTL23(x)。

- static byte[]Hash(string msg, int len)
  - 计算 SM3；返回新分配的 32 字节摘要。

- static void wBE(byte[]b, int o, int v)
  - 按大端序把 32 位字 v 写入 b 偏移 o 处的 4 个字节。


## Sm4 (class)

GB/T 32907-2016 SM4（中国国家分组密码）：128 位分组，
128 位密钥，32 轮。提供单分组 ECB 以及 CBC、CTR 模式。
纯 Zan 实现；S 盒以十六进制存储，只解码一次。

- static string SBOX_HEX()
  - SM4 S 盒（256 字节）的十六进制文本，init 时解码一次。

- static byte[]sbox;

- static bool ready=false;

- static void init()
  - 惰性解码 S 盒（幂等）。

- static int tau(int a)
  - 非线性变换 τ：32 位字逐字节过 S 盒。

- static int lTrans(int b)
  - 轮函数线性变换 L：B ^ B<<<2 ^ B<<<10 ^ B<<<18 ^ B<<<24。

- static int lpTrans(int b)
  - 密钥扩展线性变换 L'：B ^ B<<<13 ^ B<<<23。

- static List<int> ckTable()
  - CK[i] byte j = ((4i + j) * 7) mod 256 (GB/T 32907-2016).

- static List<int> keySchedule(string key, bool forDecrypt){ init}
  - 派生 32 个轮密钥。若 <paramref name="forDecrypt"/> 为真，则
    顺序反转。

- static void cryptBlock(string in16, string out16, List<int> rk)
  - 32 轮迭代并把 X32..X35 反序写出（加/解密共用，区别只在轮密钥顺序）。

- static byte[]EncryptBlock(string key, string in16)
  - 加密单个 16 字节分组。返回新的 16 字节缓冲区。

- static byte[]DecryptBlock(string key, string in16)
  - 解密单个 16 字节分组。返回新的 16 字节缓冲区。

- static byte[]EncryptCbc(string key, string iv, string data, int len, List<int> outLen)
  - 带 PKCS#7 填充的 SM4-CBC 加密。

- static byte[]DecryptCbc(string key, string iv, string data, int len, List<int> outLen)
  - SM4-CBC 解密，去除 PKCS#7 填充。
