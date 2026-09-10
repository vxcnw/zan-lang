# System.Net.Tls

> 源码: `stdlib/System/Net/Tls/TlsStream.zan`


## TlsContext (class)

TLS 上下文：封装 OpenSSL 的 SSL_CTX。每个服务器（带
证书 + 私钥）或每个客户端创建一个，再据此为每个连接派生
`TlsStream`。

服务器端：
TlsContext tls = TlsContext.CreateServer("cert.pem", "key.pem");
TlsStream s = await TlsStream.AcceptAsync(tls, clientSock);

客户端：
TlsContext tls = TlsContext.CreateClient();
TlsStream s = await TlsStream.ConnectAsync(tls, sock, "example.com");

- [DllImport("ssl")]static extern string TLS_server_method();

- [DllImport("ssl")]static extern string TLS_client_method();

- [DllImport("ssl")]static extern string SSL_CTX_new(string method);

- [DllImport("ssl")]static extern void SSL_CTX_free(string ctx);

- [DllImport("ssl")]static extern int SSL_CTX_use_certificate_chain_file(string ctx, string file);

- [DllImport("ssl")]static extern int SSL_CTX_use_PrivateKey_file(string ctx, string file, int type);

- [DllImport("ssl")]static extern int SSL_CTX_check_private_key(string ctx);

- [DllImport("ssl")]static extern void SSL_CTX_set_verify(string ctx, int mode, string callback);

- [DllImport("ssl")]static extern int SSL_CTX_set_default_verify_paths(string ctx);

- [DllImport("ssl")]static extern int SSL_CTX_load_verify_locations(string ctx, string file, string path);

- [DllImport("ssl")]static extern string SSL_CTX_get_cert_store(string ctx);

- [DllImport("crypto")]static extern long ERR_get_error();

- [DllImport("crypto")]static extern string d2i_X509(string px, byte[]pp, int len);

- [DllImport("crypto")]static extern int X509_STORE_add_cert(string store, string x);

- [DllImport("crypto")]static extern void X509_free(string x);

- [DllImport("crypto")]static extern string X509_get_issuer_name(string x);

- [DllImport("crypto")]static extern string X509_get_subject_name(string x);

- [DllImport("crypto")]static extern int X509_NAME_oneline(string name, byte[]buf, int size);

- [DllImport("crt", EntryPoint="memcpy")]static extern nint PlatMemCopyIn(byte[]dst, nint src, long n);

- [DllImport("crt", EntryPoint="memcpy")]static extern nint PlatMemCopyOut(nint dst, string src, long n);

- [DllImport("crypt32", EntryPoint="CertOpenSystemStoreA")]static extern nint CertOpenSystemStore(nint prov, string name);

- [DllImport("crypt32")]static extern nint CertEnumCertificatesInStore(nint store, nint prev);

- [DllImport("crypt32")]static extern int CertCloseStore(nint store, int flags);

- [DllImport("crt", EntryPoint="zan_crypto_cert_encoded")]static extern nint CertEncoded(nint cert, nint outLen);

- string ctx;

- bool server;

- string error;

- bool verify;

- string trust;

- List<string> pins;

- bool pinRequired;

- CertPolicyFn certPolicy;

- TlsContext()
  - 内部构造：verify 默认开启；经 CreateServer/CreateClient 使用。

- void SetCertPolicy(CertPolicyFn fn)
  - 设置证书策略（见 `CertPolicyFn`）。
    只影响客户端方向；与 DisableVerify() 互斥的放宽手段：
    校验仍在跑，放行与否由策略逐连接决定。

- bool PolicyActive()
  - 是否已设置证书策略（握手后逐连接裁决校验结果）。

- void AddPin(string spkiSha256Base64)
  - 添加一个可接受的服务器公钥 pin：即
    DER SubjectPublicKeyInfo 的 base64 SHA-256（即由
    `openssl ... -pubkey | openssl pkey -pubin -outform der
    | openssl dgst -sha256 -binary | base64` 命令得到的值）。

- void RequirePinning(bool on)
  - 开关 pin 强制校验。发布构建始终开启，保证
    发布的二进制始终校验配置的 pin；HTTP 客户端中的开发开关
    是唯一可以放宽它的途径。

- bool PinningActive()
  - 当握手必须满足至少一个已配置的
    pin 时为 true。

- bool PinMatches(string got)
  - `got`（base64 的 SPKI SHA-256）与任一 pin 匹配时为 true。

- static TlsContext CreateServer(string certFile, string keyFile)
  - 从 PEM 证书链
    和 PEM 私钥创建服务器端 TLS 上下文。失败（路径错误/私钥
    不匹配）时返回 null；原因见 LastError()。

- static TlsContext CreateClient()
  - 创建客户端 TLS 上下文。证书校验
    使用系统默认信任库；如需自签名开发服务器，可调用
    DisableVerify()。

- static TlsContext CreateClientWithCertificate(string certFile, string keyFile)
  - 创建带 PEM 证书链和对应 PEM 私钥的
    客户端 TLS 上下文，用于双向 TLS 认证。

- void DisableVerify()
  - 禁用对端证书校验（仅限开发）。
    0 = SSL_VERIFY_NONE。

- static nint PtrAt(nint ptr, int off)
  - 从结构体的 ptr + off 处读取一个原生指针宽度的字段。

- static int IntAt(nint ptr, int off)
  - 从结构体的 ptr + off 处读取一个小端序 32 位字段。

- static void LoadSystemRootsWindows(string sslctx)
  - 枚举 Windows "ROOT" 证书库，把所有受信任的
    根证书（包括本地安装的代理/MITM CA）加入支撑 sslctx 的
    OpenSSL X509_STORE，使校验结果与系统信任一致。

- static string LoadSystemRootsUnix(string sslctx)
  - 随包分发的 OpenSSL 是 CI 上的构建产物，编译期 OPENSSLDIR 指向构建机的
    目录（macOS 那份是 /opt/homebrew/etc/openssl@3，Linux 那份是
    /usr/lib/ssl）。这些目录在用户机器上通常不存在，于是
    SSL_CTX_set_default_verify_paths 一张根证书都装不进来，所有 https
    请求都在链校验处失败。按 curl 的做法探测本机的系统 CA 包，
    装上第一个存在的，返回其路径；都没有则返回 ""。

- string TrustHint()
  - 链校验失败时补充的定位提示：本机一个系统 CA
    信任库都没装上时点名该原因，否则为 ""。

- static byte[]PemBodyToDer(string pem, int expectedLen)
  - 从 PEM 字符串中抽出 base64 正文（BEGIN/END 标记之间）并解码为 DER。

- bool AddTrustedCert(string pemFile)
  - 把 PEM 格式的 CA（或自签名）证书加入本上下文的信任库，
    使其签发的对端证书在链校验中被接受。返回 true 表示成功。
    用于私有 CA 与测试（自签名开发服务器）。

- string Handle()
  - 底层 OpenSSL SSL_CTX 指针（interop 传递用，勿手工释放）。

- bool IsServer()
  - 是否为服务器端上下文。

- void Free()
  - 释放底层的 SSL_CTX。


## TlsStream (class)

非阻塞套接字上的一条 TLS 连接，由 OpenSSL 内存
BIO 驱动，因此所有套接字 IO 都经过协程 reactor（await
Socket.ReadReady / Socket.SendAsync），TLS 不会阻塞线程。

加密字节在 socket <-> rbio/wbio 间流动；SSL_read/SSL_write 使
明文出入 SSL 引擎。WANT_READ 时向 rbio 灌入一次套接字读取；
wbio 中待发的字节则在每次引擎步骤后
刷回套接字。

- [DllImport("crt", EntryPoint="zan_monotonic_us")]static extern long MonotonicUs();

- [DllImport("ssl")]static extern string SSL_new(string ctx);

- [DllImport("ssl")]static extern void SSL_free(string ssl);

- [DllImport("ssl")]static extern void SSL_set_bio(string ssl, string rbio, string wbio);

- [DllImport("ssl")]static extern void SSL_set_accept_state(string ssl);

- [DllImport("ssl")]static extern void SSL_set_connect_state(string ssl);

- [DllImport("ssl")]static extern int SSL_do_handshake(string ssl);

- [DllImport("ssl")]static extern int SSL_read(string ssl, string buf, int num);

- [DllImport("ssl")]static extern int SSL_write(string ssl, string buf, int num);

- [DllImport("ssl")]static extern int SSL_get_error(string ssl, int ret);

- [DllImport("ssl")]static extern int SSL_set_verify(string ssl, int mode, string callback);

- [DllImport("ssl")]static extern int SSL_shutdown(string ssl);

- [DllImport("ssl")]static extern int SSL_ctrl(string ssl, int cmd, int larg, string parg);

- [DllImport("ssl")]static extern string SSL_get0_param(string ssl);

- [DllImport("ssl")]static extern long SSL_get_verify_result(string ssl);

- [DllImport("crypto")]static extern int X509_VERIFY_PARAM_set1_host(string param, string name, long len);

- [DllImport("crypto")]static extern int X509_VERIFY_PARAM_set1_ip_asc(string param, string ipasc);

- [DllImport("crypto")]static extern void X509_VERIFY_PARAM_set_hostflags(string param, long flags);

- [DllImport("crypto")]static extern string X509_VERIFY_PARAM_get0_name(string param);

- [DllImport("crypto")]static extern string BIO_new(string method);

- [DllImport("crypto")]static extern string BIO_s_mem();

- [DllImport("crypto")]static extern int BIO_write(string bio, string data, int dlen);

- [DllImport("crypto")]static extern int BIO_read(string bio, string data, int dlen);

- [DllImport("crypto")]static extern int BIO_ctrl_pending(string bio);

- [DllImport("ssl")]static extern string SSL_get1_peer_certificate(string ssl);

- [DllImport("crypto")]static extern string X509_get_X509_PUBKEY(string x);

- [DllImport("crypto")]static extern int i2d_X509_PUBKEY(string pubkey, byte[]pp);

- [DllImport("crypto")]static extern void X509_free(string x);

- [DllImport("crypto", EntryPoint="CRYPTO_free")]static extern void OpenSslFree(nint p, string file, int line);

- [DllImport("crt", EntryPoint="memcpy")]static extern nint PlatMemCopyIn(byte[]dst, nint src, long n);

- string ssl;

- string rbio;

- string wbio;

- nint sock;

- bool open;

- HttpDeadlineToken watch;

- byte[]scratch;

- static int SCRATCH=17408;

- static string lastError="";

- static int Norm(int v)
  - C 的 `int` 返回值是零扩展的（C 的 -1 读到为 4294967295）；
    将其折回有符号 32 位，错误检查才能正常工作。

- static string LastError()
  - 最近一次失败的原因文本（CreateServer/CreateClient/
    ConnectAsync 失败后可读）；成功操作会先清空它。

- static void SetLastError(string error)
  - 更新 LastError 报告的原因文本。

- TlsStream()
  - 内部构造：经 Setup() 使用。

- static TlsStream Setup(TlsContext ctx, nint sock)
  - 把 ctx 包装到套接字上（分配 SSL 与内存 BIO 对、
    SCRATCH 暂存缓冲）；不执行握手。失败返回 null。

- static async TlsStream AcceptAsync(TlsContext ctx, nint sock)
  - 服务器端：包装已接受的套接字并执行 TLS 握手。
    默认 30 秒握手预算；握手失败或超时返回 null，原因见
    `LastError`。

- static async TlsStream AcceptAsync(TlsContext ctx, nint sock, int timeoutMs)
  - 服务器端 TLS 握手，timeoutMs 为握手阶段预算；<= 0
    表示不设握手截止时间。

- static async TlsStream ConnectAsync(TlsContext ctx, nint sock, string host)
  - 客户端：包装已连接的套接字，发送
    <paramref name="host"/> 的 SNI 并执行 TLS 握手。握手失败时
    返回 null。
    客户端 TLS 握手；timeoutMs 为握手阶段预算，<= 0 表示不设
    握手截止时间。保留三参数入口供非 HTTP 调用方使用。

- static async TlsStream ConnectAsync(TlsContext ctx, nint sock, string host, int timeoutMs)
  - 带握手预算的客户端 TLS 握手：timeoutMs <= 0 表示不设截止。
    失败（Setup 失败、主机名校验参数出错、握手失败、证书链/主机名
    校验不通过且无策略放行、pin 不匹配）返回 null，原因见 LastError。

- static bool IsIpLiteral(string host)
  - host 是否为 IP 字面量（IPv4 点分十进制或 IPv6 含冒号）：
    是则主机名校验走 set1_ip_asc，否则走 set1_host。

- static string PeerCertText(string ssl)
  - 对端证书的可读文本："issuer=... subject=..."；无对端证书
    时返回 ""。证书策略回调与错误报告共用。

- static string NameText(string name)
  - X509_NAME → 单行可读文本（X509_NAME_oneline 形式）。

- static string SpkiPinOf(string ssl)
  - 对端证书 DER
    SubjectPublicKeyInfo 的 base64 SHA-256（即通过 TlsContext.AddPin 固定的值），
    没有对端证书/编码时返回 ""。

- async int FlushOutAsync()
  - 把 wbio 中待发的加密输出字节刷到套接字。
    必须保证 BIO 中读出的每一块都完整发出；否则截断的 TLS
    记录会导致握手/数据损坏。Socket.SendAsync 在内部已经循环
    重发，因此其返回值应等于请求发送的字节数；若不相等则
    视为连接已不可用。

- async int PumpInAsync()
  - 从套接字读一块加密字节灌入 rbio。返回字节数，
    对端关闭为 0，出错为 -1；无可读数据时挂起等待。

- async int HandshakeAsync(int timeoutMs)
  - 驱动 TLS 握手直至完成。成功返回 1。
    整个握手有 30 秒硬截止：对端每 30 秒滴一字节的慢速攻击
    此前会无限循环 WANT_READ，钉死一个协程 + SSL + BIO + 17KB
    暂存缓冲——面向公网的服务器这样被逐个耗干。超时返回 -2，
    调用方照常关闭连接。
    
    截止检查是墙钟轮询，仅在本协程被唤醒时执行；完全静默的
    对端不会唤醒任何东西，所以另外武装进程级 HttpDeadline
    扫描器（每秒唤醒，超时 shutdown 套接字）——被 shutdown
    唤醒的 PumpInAsync 读到 0 按对端关闭返回 -1，走正常清理。
    await ReadReady 自身没有计时能力，这是唯一能让"静默对端"
    也吃到期满的办法。

- int EndHandshakeWatch(int result)
  - 握手结束时释放 deadline 槽位（服务器的连接循环随后会按
    每请求节奏重新 Arm）。result 原样返回。

- async string RecvAsync(int max)
  - 接收解密后的应用字节（最多
    <paramref name="max"/>，最多一个暂存缓冲区）。正常关闭或出错时
    返回 ""。

- async int RecvIntoAsync(string buf, int max)
  - 接收解密后的字节到调用方提供的缓冲区
    （二进制安全：返回字节数，不做 NUL 截断）。
    正常关闭返回 0，出错返回 -1。

- async int SendAsync(string data, int len)
  - 加密并发送 <paramref name="len"/> 字节。成功返回
    明文字节数，失败返回 -1。

- async int SendStringAsync(string data)
  - 发送整个字符串（其 .Length 个字节）。

- void Close()
  - 发送 TLS close_notify 并释放 SSL 引擎与 BIO 所有权；
    底层套接字仍归调用方所有（且必须由其关闭）。Close 后继续
    调用安全：所有方法按未打开处理。


## bool (delegate)

证书策略：客户端握手后若链/主机名校验不通过（verify_result
!= 0），以 (verifyResult, 对端证书文本) 调用；返回 true 放行
本次连接，false 拒绝。证书文本形如
"issuer=/CN=GlobalSign.../O=Alibaba subject=/CN=example.com"。
典型用途：老系统缺根证书时按已知签发者放行（.NET
ServerCertificateValidationCallback 的对应物）。

`delegate bool CertPolicyFn(long verifyResult, string certText);`
