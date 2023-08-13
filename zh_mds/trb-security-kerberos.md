

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Troubleshooting security](security-
troubleshooting.md)

[« Common SSL/TLS exceptions](trb-security-ssl.md) [Common SAML issues
»](trb-security-saml.md)

## 常见科贝罗斯例外

**Symptoms:**

* 由于 GSS 协商失败或服务登录失败(在服务器或 Elasticsearch http 客户端中)，用户身份验证失败。下面列出了一些常见的异常，并提供了一些提示来帮助解决这些问题。

**Resolution:**

"在 GSS-API 级别未指定故障(机制级别：校验和失败)"

    

当您在 HTTP 客户端看到此错误消息时，它可能与不正确的密码有关。

当您在 Elasticsearch 服务器日志中看到此错误消息时，它可能与 Elasticsearch 服务密钥表有关。密钥表文件存在，但无法以用户身份登录。请检查密钥表到期时间。还要检查密钥表是否包含最新的凭据;如果没有，请更换它们。

您可以使用"klist"或"ktab"等工具在密钥表中列出主体并验证它们。您可以使用"kinit"来查看是否可以使用密钥表获取初始票证。请在 Kerberos 环境中查看工具及其文档。

Kerberos 依赖于正确的主机名解析，因此请检查您的 DNS 基础结构。不正确的 DNS 设置、DNS SRV 记录或"krb5.conf"中 KDCservers 的配置可能会导致主机名解析出现问题。

"在 GSS-API 级别未指定故障(机制级别：请求是重放 (34))"

"在 GSS-API 级别未指定的故障(机制级别：时钟偏差太大(37))"

    

为了防止重播攻击，Kerberos V5 设置了计算机时钟同步的最大容差，通常为 5 分钟。请检查域内计算机上的时间是否同步。

"gss_init_sec_context() 失败：请求了不受支持的机制"

"找不到以下凭据：1.2.840.113554.1.2.2 用法：接受"

    

当使用"curl"测试Elasticsearch Kerberos设置时，您通常会在客户端看到此错误消息。例如，当您在客户端上使用旧版本的 curl 时，会出现这些消息，因此缺少 KerberosSpnego 支持。Elasticsearch 中的 Kerberos 领域仅支持 Spengo 机制(Oid 1.3.6.1.5.5.2);它尚不支持Kerberosmechanism(Oid 1.2.840.113554.1.2.2)。

确保：

* 您已经安装了 curl 版本 7.49 或更高版本，因为旧版本的 curl 已知存在 Kerberos 错误。  * 计算机上安装的 curl 在调用命令 'curl -V' 时列出了"GSS-API"、"Kerberos"和"SPNEGO"功能。如果没有，您将需要使用此支持编译"curl"版本。

要下载最新的 curl 版本，请访问<https://curl.haxx.se/download.html>

由于 Kerberos 日志本质上通常是神秘的，并且许多事情可能会出错，因为它依赖于 DNS 和 NTP 等外部服务。您可能需要启用其他调试日志来确定问题的根本原因。

Elasticsearch 使用 JAAS(Java Authentication and Authorization Service)Kerberos 登录模块来提供 Kerberos 支持。要启用调试日志，请使用以下 Kerberos 领域设置：

    
    
    xpack.security.authc.realms.kerberos.<realm-name>.krb.debug: true

有关详细信息，请参阅 Kerberos 领域设置。

有时，您可能需要在 SPNEGOGSS 上下文协商期间更深入地了解问题，或者查看 Kerberos 消息交换。要在 JVM 上启用 Kerberos/SPNEGO 调试日志记录，请添加以下 JVM 系统属性：

`-Dsun.security.krb5.debug=true`

`-Dsun.security.spnego.debug=true`

有关 JVM 系统属性的更多信息，请参阅设置 JVM选项。

[« Common SSL/TLS exceptions](trb-security-ssl.md) [Common SAML issues
»](trb-security-saml.md)
