

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Thread pools](modules-threadpool.md) [Advanced configuration »](advanced-
configuration.md)

## 弹性搜索中的观察程序设置

您可以配置观察程序设置以设置观察程序并通过电子邮件、Slack 和寻呼程序发送通知。

所有这些设置都可以添加到"elasticsearch.yml"配置文件中，但安全设置除外，您可以将其添加到Elasticsearch密钥库中。有关创建和更新 Elasticsearch 密钥库的更多信息，请参阅安全设置。还可以使用群集更新设置 API 跨群集更新动态设置。

### 常规观察程序设置

`xpack.watcher.enabled`

     ([Static](settings.html#static-cluster-setting)) Set to `false` to disable Watcher on the node. 

"xpack.watcher.encrypt_sensitive_data"！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Static](settings.html#static-cluster-setting)) Set to `true` to encrypt sensitive data. If this setting is enabled, you must also specify the `xpack.watcher.encryption_key` setting. For more information, see [_Encrypting sensitive data in Watcher_](encrypting-data.html "Encrypting sensitive data in Watcher"). 
`xpack.watcher.encryption_key`

     ([Secure](secure-settings.html "Secure settings")) Specifies the path to a file that contains a key for encrypting sensitive data. If `xpack.watcher.encrypt_sensitive_data` is set to `true`, this setting is required. For more information, see [_Encrypting sensitive data in Watcher_](encrypting-data.html "Encrypting sensitive data in Watcher"). 
`xpack.http.proxy.host`

     ([Static](settings.html#static-cluster-setting)) Specifies the address of the proxy server to use to connect to HTTP services. 
`xpack.http.proxy.port`

     ([Static](settings.html#static-cluster-setting)) Specifies the port number to use to connect to the proxy server. 
`xpack.http.proxy.scheme`

     ([Static](settings.html#static-cluster-setting)) Protocol used to communicate with the proxy server. Valid values are `http` and `https`. Defaults to the protocol used in the request. 
`xpack.http.default_connection_timeout`

     ([Static](settings.html#static-cluster-setting)) The maximum period to wait until abortion of the request, when a connection is being initiated. 
`xpack.http.default_read_timeout`

     ([Static](settings.html#static-cluster-setting)) The maximum period of inactivity between two data packets, before the request is aborted. 
`xpack.http.tcp.keep_alive`

     ([Static](settings.html#static-cluster-setting)) Whether to enable TCP keepalives on HTTP connections. Defaults to `true`. 
`xpack.http.connection_pool_ttl`

     ([Static](settings.html#static-cluster-setting)) The time-to-live of connections in the connection pool. If a connection is not re-used within this timeout, it is closed. By default, the time-to-live is infinite meaning that connections never expire. 
`xpack.http.max_response_size`

     ([Static](settings.html#static-cluster-setting)) Specifies the maximum size an HTTP response is allowed to have, defaults to `10mb`, the maximum configurable value is `50mb`. 
`xpack.http.whitelist`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A list of URLs, that the internal HTTP client is allowed to connect to. This client is used in the HTTP input, the webhook, the slack, pagerduty, and jira actions. This setting can be updated dynamically. It defaults to `*` allowing everything. Note: If you configure this setting and you are using one of the slack/pagerduty actions, you have to ensure that the corresponding endpoints are explicitly allowed as well. 

### Watcher HTTP TLS/SSLsettings

您可以配置以下 TLS/SSL 设置。

`xpack.http.ssl.supported_protocols`

    

(静态)支持的协议版本。有效协议："SSLv2Hello"、"SSLv3"、"TLSv1"、"TLSv1.1"、"TLSv1.2"、"TLSv1.3"。如果 JVM 的 SSL 提供程序支持 TLSv1.3，则缺省值为 'TLSv1.3，TLSv1.2，TLSv1.1'。否则，默认值为"TLSv1.2，TLSv1.1"。

Elasticsearch 依赖于 JDK 的 SSL 和 TLS 实现。有关详细信息，请查看 JDK 版本支持的 SSL/TLS 版本。

如果"xpack.security.fips_mode.enabled"为"true"，则不能使用"SSLv2Hello"或"SSLv3"。请参阅 FIPS 140-2。

`xpack.http.ssl.verification_mode`

    

(静态)定义如何验证 TLS 连接中另一方提供的证书：

有效值

`full`

     Validates that the provided certificate: has an issue date that's within the `not_before` and `not_after` dates; chains to a trusted Certificate Authority (CA); has a `hostname` or IP address that matches the names within the certificate. 
`certificate`

     Validates the provided certificate and verifies that it's signed by a trusted authority (CA), but doesn't check the certificate `hostname`. 
`none`

    

不执行证书验证。

将证书验证设置为"无"会禁用SSL / TLS的许多安全优势，这是非常危险的。仅当 ElasticSupport 指示在尝试解决 TLS 错误时作为临时诊断机制时，才设置此值。

默认为"full"。

`xpack.http.ssl.cipher_suites`

    

(静态)支持的密码套件因您使用的 Java 版本而异。例如，对于版本 12，默认值为"TLS_AES_256_GCM_SHA384"、"TLS_AES_128_GCM_SHA256"、"TLS_CHACHA20_POLY1305_SHA256"、"TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384"、"TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256"、"TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"、"TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"、"TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256"、""、""、"TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256"、"TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384"、"TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256"、"TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384"、"TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256"、"TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA"、"TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA"、"TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA"、""TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA"、"TLS_RSA_WITH_AES_256_GCM_SHA384"、"TLS_RSA_WITH_AES_128_GCM_SHA256"、"TLS_RSA_WITH_AES_256_CBC_SHA256"、"TLS_RSA_WITH_AES_128_CBC_SHA256"、"TLS_RSA_WITH_AES_256_CBC_SHA"、"TLS_RSA_WITH_AES_128_CBC_SHA"。

有关更多信息，请参阅 Oracle 的 Java 加密体系结构文档。

#### 观察程序 HTTP TLS/SSL 密钥和受信任的证书设置

以下设置用于指定通过 SSL/TLS 连接进行通信时应使用的私钥、证书和受信任证书。私钥和证书是可选的，如果服务器要求客户端身份验证以进行 PKI 身份验证，则会使用私钥和证书。

#### PEM 编码文件

使用 PEM 编码文件时，请使用以下设置：

`xpack.http.ssl.key`

    

(静态)包含私钥的 PEM 编码文件的路径。

如果需要 HTTP 客户端身份验证，它将使用此文件。您不能同时使用此设置和"ssl.keystore.path"。

`xpack.http.ssl.key_passphrase`

    

(静态)用于解密私钥的密码短语。由于密钥可能未加密，因此此值是可选的。

您不能同时使用此设置和"ssl.secure_key_passphrase"。

`xpack.http.ssl.secure_key_passphrase`

     ([Secure](secure-settings.html "Secure settings")) The passphrase that is used to decrypt the private key. Since the key might not be encrypted, this value is optional. 
`xpack.http.ssl.certificate`

    

(静态)指定与密钥关联的 PEM 编码证书(或证书链)的路径。

仅当设置了"ssl.key"时，才能使用此设置。

`xpack.http.ssl.certificate_authorities`

    

(静态)应信任的 PEM 编码证书文件的路径列表。

此设置和"ssl.truststore.path"不能同时使用。

#### Java 密钥库文件

使用 Java 密钥库文件 (JKS) 时，其中包含应信任的私钥、证书和证书，请使用以下设置：

`xpack.http.ssl.keystore.path`

    

(静态)包含私钥和证书的密钥库文件的路径。

它必须是 Java 密钥库 (jks) 或 PKCS#12 文件。不能同时使用此设置和"ssl.key"。

`xpack.http.ssl.keystore.password`

     ([Static](settings.html#static-cluster-setting)) The password for the keystore. 
`xpack.http.ssl.keystore.secure_password`

     ([Secure](secure-settings.html "Secure settings")) The password for the keystore. 
`xpack.http.ssl.keystore.key_password`

    

(静态)密钥库中密钥的密码。缺省值为密钥库密码。

您不能同时使用此设置和"ssl.keystore.secure_password"。

`xpack.http.ssl.keystore.secure_key_password`

     ([Secure](secure-settings.html "Secure settings")) The password for the key in the keystore. The default is the keystore password. 
`xpack.http.ssl.truststore.path`

    

(静态)包含要信任的证书的密钥库的路径。它必须是 Java 密钥库 (jks) 或 PKCS#12 文件。

您不能同时使用此设置和"ssl.certificate_authorities"。

`xpack.http.ssl.truststore.password`

    

(静态)信任库的密码。

您不能同时使用此设置和"ssl.truststore.secure_password"。

`xpack.http.ssl.truststore.secure_password`

     ([Secure](secure-settings.html "Secure settings")) Password for the truststore. 

#### PKCS#12文件

Elasticsearch 可以配置为使用 PKCS#12 容器文件(".p12"或".pfx"文件)，其中包含应信任的私钥、证书和证书。

PKCS#12 文件的配置方式与 Java 密钥库文件的配置方式相同：

`xpack.http.ssl.keystore.path`

    

(静态)包含私钥和证书的密钥库文件的路径。

它必须是 Java 密钥库 (jks) 或 PKCS#12 文件。不能同时使用此设置和"ssl.key"。

`xpack.http.ssl.keystore.type`

     ([Static](settings.html#static-cluster-setting)) The format of the keystore file. It must be either `jks` or `PKCS12`. If the keystore path ends in ".p12", ".pfx", or ".pkcs12", this setting defaults to `PKCS12`. Otherwise, it defaults to `jks`. 
`xpack.http.ssl.keystore.password`

     ([Static](settings.html#static-cluster-setting)) The password for the keystore. 
`xpack.http.ssl.keystore.secure_password`

     ([Secure](secure-settings.html "Secure settings")) The password for the keystore. 
`xpack.http.ssl.keystore.key_password`

    

(静态)密钥库中密钥的密码。缺省值为密钥库密码。

您不能同时使用此设置和"ssl.keystore.secure_password"。

`xpack.http.ssl.keystore.secure_key_password`

     ([Secure](secure-settings.html "Secure settings")) The password for the key in the keystore. The default is the keystore password. 
`xpack.http.ssl.truststore.path`

    

(静态)包含要信任的证书的密钥库的路径。它必须是 Java 密钥库 (jks) 或 PKCS#12 文件。

您不能同时使用此设置和"ssl.certificate_authorities"。

`xpack.http.ssl.truststore.type`

     ([Static](settings.html#static-cluster-setting)) Set this to `PKCS12` to indicate that the truststore is a PKCS#12 file. 
`xpack.http.ssl.truststore.password`

    

(静态)信任库的密码。

您不能同时使用此设置和"ssl.truststore.secure_password"。

`xpack.http.ssl.truststore.secure_password`

     ([Secure](secure-settings.html "Secure settings")) Password for the truststore. 

### 电子邮件通知设置

您可以在"elasticsearch.yml"中配置以下电子邮件通知设置。有关通过电子邮件发送通知的详细信息，请参阅配置电子邮件操作。

`xpack.notification.email.default_account`

    

(动态)要使用的默认电子邮件帐户。

如果配置多个电子邮件帐户，则必须配置此设置或指定要在"电子邮件"操作中使用的电子邮件帐户。请参阅配置电子邮件帐户。

`xpack.notification.email.account`

     Specifies account information for sending notifications via email. You can specify the following email account attributes: 
`xpack.notification.email.account.domain_allowlist`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Specifies domains to which emails are allowed to be sent. Emails with recipients (`To:`, `Cc:`, or `Bcc:`) outside of these domains will be rejected and an error thrown. This setting defaults to `["*"]` which means all domains are allowed. Simple globbing is supported, such as `*.company.com` in the list of allowed domains. 

`profile`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The [email profile](actions-email.html#configuring-email "Configuring email accounts") to use to build the MIME messages that are sent from the account. Valid values: `standard`, `gmail` and `outlook`. Defaults to `standard`. 
`email_defaults.*`

     ([Dynamic](settings.html#dynamic-cluster-setting)) An optional set of email attributes to use as defaults for the emails sent from the account. See [Email action attributes](actions-email.html#email-action-attributes "Email action attributes") for the supported attributes. 
`smtp.auth`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Set to `true` to attempt to authenticate the user using the AUTH command. Defaults to `false`. 
`smtp.host`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The SMTP server to connect to. Required. 
`smtp.port`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The SMTP server port to connect to. Defaults to 25. 
`smtp.user`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The user name for SMTP. Required. 
`smtp.secure_password`

     ([Secure](secure-settings.html "Secure settings"), [reloadable](secure-settings.html#reloadable-secure-settings "Reloadable secure settings")) The password for the specified SMTP user. 
`smtp.starttls.enable`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Set to `true` to enable the use of the `STARTTLS` command (if supported by the server) to switch the connection to a TLS-protected connection before issuing any login commands. Note that an appropriate trust store must be configured so that the client will trust the server's certificate. Defaults to `false`. 
`smtp.starttls.required`

     ([Dynamic](settings.html#dynamic-cluster-setting)) If `true`, then `STARTTLS` will be required. If that command fails, the connection will fail. Defaults to `false`. 
`smtp.ssl.trust`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A list of SMTP server hosts that are assumed trusted and for which certificate verification is disabled. If set to "*", all hosts are trusted. If set to a whitespace separated list of hosts, those hosts are trusted. Otherwise, trust depends on the certificate the server presents. 
`smtp.timeout`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The socket read timeout. Default is two minutes. 
`smtp.connection_timeout`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The socket connection timeout. Default is two minutes. 
`smtp.write_timeout`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The socket write timeout. Default is two minutes. 
`smtp.local_address`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A configurable local address when sending emails. Not configured by default. 
`smtp.local_port`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A configurable local port when sending emails. Not configured by default. 
`smtp.send_partial`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Send an email, despite one of the receiver addresses being invalid. 
`smtp.wait_on_quit`

     ([Dynamic](settings.html#dynamic-cluster-setting)) If set to false the QUIT command is sent and the connection closed. If set to true, the QUIT command is sent and a reply is waited for. True by default. 

`xpack.notification.email.html.sanitization.allow`

    

指定电子邮件通知中允许的 HTML 元素。有关详细信息，请参阅配置 HTML 清理选项。您可以指定单个 HTML 元素和以下 HTML 功能组：

`_tables`

     ([Static](settings.html#static-cluster-setting)) All table related elements: `<table>`, `<th>`, `<tr>`, `<td>`, `<caption>`, `<col>`, `<colgroup>`, `<thead>`, `<tbody>`, and `<tfoot>`. 
`_blocks`

     ([Static](settings.html#static-cluster-setting)) The following block elements: `<p>`, `<div>`, `<h1>`, `<h2>`, `<h3>`, `<h4>`, `<h5>`, `<h6>`, `<ul>`, `<ol>`, `<li>`, and `<blockquote>`. 
`_formatting`

     ([Static](settings.html#static-cluster-setting)) The following inline formatting elements: `<b>`, `<i>`, `<s>`, `<u>`, `<o>`, `<sup>`, `<sub>`, `<ins>`, `<del>`, `<strong>`, `<strike>`, `<tt>`, `<code>`, `<big>`, `<small>`, `<hr>`, `<br>`, `<span>`, and `<em>`. 
`_links`

     ([Static](settings.html#static-cluster-setting)) The `<a>` element with an `href` attribute that points to a URL using the following protocols: `http`, `https` and `mailto`. 
`_styles`

     ([Static](settings.html#static-cluster-setting)) The `style` attribute on all elements. Note that CSS attributes are also sanitized to prevent XSS attacks. 
`img`

`img:all`

     ([Static](settings.html#static-cluster-setting)) All images (external and embedded). 
`img:embedded`

     ([Static](settings.html#static-cluster-setting)) Only embedded images. Embedded images can only use the `cid:` URL protocol in their `src` attribute. 

`xpack.notification.email.html.sanitization.disallow`

     ([Static](settings.html#static-cluster-setting)) Specifies the HTML elements that are NOT allowed in email notifications. You can specify individual HTML elements and [HTML feature groups](notification-settings.html#html-feature-groups). 
`xpack.notification.email.html.sanitization.enabled`

     ([Static](settings.html#static-cluster-setting)) Set to `false` to completely disable HTML sanitation. Not recommended. Defaults to `true`. 
`xpack.notification.reporting.warning.kbn-csv-contains-formulas.text`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Specifies a custom message, which is sent if the formula verification criteria for CSV files from Kibana's [`xpack.reporting.csv.checkForFormulas`](/guide/en/kibana/8.9/reporting-settings-kb.html#reporting-csv-settings) is `true`. Use `%s` in the message as a placeholder for the filename. Defaults to `Warning: The attachment [%s] contains characters which spreadsheet applications may interpret as formulas. Please ensure that the attachment is safe prior to opening.`

### 观察程序电子邮件 TLS/SSLsettings

您可以配置以下 TLS/SSL 设置。

`xpack.notification.email.ssl.supported_protocols`

    

(静态)支持的协议版本。有效协议："SSLv2Hello"、"SSLv3"、"TLSv1"、"TLSv1.1"、"TLSv1.2"、"TLSv1.3"。如果 JVM 的 SSL 提供程序支持 TLSv1.3，则缺省值为 'TLSv1.3，TLSv1.2，TLSv1.1'。否则，默认值为"TLSv1.2，TLSv1.1"。

Elasticsearch 依赖于 JDK 的 SSL 和 TLS 实现。有关详细信息，请查看 JDK 版本支持的 SSL/TLS 版本。

如果"xpack.security.fips_mode.enabled"为"true"，则不能使用"SSLv2Hello"或"SSLv3"。请参阅 FIPS 140-2。

`xpack.notification.email.ssl.verification_mode`

    

(静态)定义如何验证 TLS 连接中另一方提供的证书：

有效值

`full`

     Validates that the provided certificate: has an issue date that's within the `not_before` and `not_after` dates; chains to a trusted Certificate Authority (CA); has a `hostname` or IP address that matches the names within the certificate. 
`certificate`

     Validates the provided certificate and verifies that it's signed by a trusted authority (CA), but doesn't check the certificate `hostname`. 
`none`

    

不执行证书验证。

将证书验证设置为"无"会禁用SSL / TLS的许多安全优势，这是非常危险的。仅当 ElasticSupport 指示在尝试解决 TLS 错误时作为临时诊断机制时，才设置此值。

默认为"full"。

`xpack.notification.email.ssl.cipher_suites`

    

(静态)支持的密码套件因您使用的 Java 版本而异。例如，对于版本 12，默认值为"TLS_AES_256_GCM_SHA384"、"TLS_AES_128_GCM_SHA256"、"TLS_CHACHA20_POLY1305_SHA256"、"TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384"、"TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256"、"TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"、"TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"、"TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256"、""、""、"TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256"、"TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384"、"TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256"、"TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384"、"TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256"、"TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA"、"TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA"、"TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA"、""TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA"、"TLS_RSA_WITH_AES_256_GCM_SHA384"、"TLS_RSA_WITH_AES_128_GCM_SHA256"、"TLS_RSA_WITH_AES_256_CBC_SHA256"、"TLS_RSA_WITH_AES_128_CBC_SHA256"、"TLS_RSA_WITH_AES_256_CBC_SHA"、"TLS_RSA_WITH_AES_128_CBC_SHA"。

有关更多信息，请参阅 Oracle 的 Java 加密体系结构文档。

#### 观察程序电子邮件 TLS/SSL 密钥和受信任的证书设置

以下设置用于指定通过 SSL/TLS 连接进行通信时应使用的私钥、证书和受信任证书。私钥和证书是可选的，如果服务器要求客户端身份验证以进行 PKI 身份验证，则会使用私钥和证书。

#### PEM 编码文件

使用 PEM 编码文件时，请使用以下设置：

`xpack.notification.email.ssl.key`

    

(静态)包含私钥的 PEM 编码文件的路径。

如果需要 HTTP 客户端身份验证，它将使用此文件。您不能同时使用此设置和"ssl.keystore.path"。

`xpack.notification.email.ssl.key_passphrase`

    

(静态)用于解密私钥的密码短语。由于密钥可能未加密，因此此值是可选的。

您不能同时使用此设置和"ssl.secure_key_passphrase"。

`xpack.notification.email.ssl.secure_key_passphrase`

     ([Secure](secure-settings.html "Secure settings")) The passphrase that is used to decrypt the private key. Since the key might not be encrypted, this value is optional. 
`xpack.notification.email.ssl.certificate`

    

(静态)指定与密钥关联的 PEM 编码证书(或证书链)的路径。

仅当设置了"ssl.key"时，才能使用此设置。

`xpack.notification.email.ssl.certificate_authorities`

    

(静态)应信任的 PEM 编码证书文件的路径列表。

此设置和"ssl.truststore.path"不能同时使用。

#### Java 密钥库文件

使用 Java 密钥库文件 (JKS) 时，其中包含应信任的私钥、证书和证书，请使用以下设置：

`xpack.notification.email.ssl.keystore.path`

    

(静态)包含私钥和证书的密钥库文件的路径。

它必须是 Java 密钥库 (jks) 或 PKCS#12 文件。不能同时使用此设置和"ssl.key"。

`xpack.notification.email.ssl.keystore.password`

     ([Static](settings.html#static-cluster-setting)) The password for the keystore. 
`xpack.notification.email.ssl.keystore.secure_password`

     ([Secure](secure-settings.html "Secure settings")) The password for the keystore. 
`xpack.notification.email.ssl.keystore.key_password`

    

(静态)密钥库中密钥的密码。缺省值为密钥库密码。

您不能同时使用此设置和"ssl.keystore.secure_password"。

`xpack.notification.email.ssl.keystore.secure_key_password`

     ([Secure](secure-settings.html "Secure settings")) The password for the key in the keystore. The default is the keystore password. 
`xpack.notification.email.ssl.truststore.path`

    

(静态)包含要信任的证书的密钥库的路径。它必须是 Java 密钥库 (jks) 或 PKCS#12 文件。

您不能同时使用此设置和"ssl.certificate_authorities"。

`xpack.notification.email.ssl.truststore.password`

    

(静态)信任库的密码。

您不能同时使用此设置和"ssl.truststore.secure_password"。

`xpack.notification.email.ssl.truststore.secure_password`

     ([Secure](secure-settings.html "Secure settings")) Password for the truststore. 

#### PKCS#12文件

Elasticsearch 可以配置为使用 PKCS#12 容器文件(".p12"或".pfx"文件)，其中包含应信任的私钥、证书和证书。

PKCS#12 文件的配置方式与 Java 密钥库文件的配置方式相同：

`xpack.notification.email.ssl.keystore.path`

    

(静态)包含私钥和证书的密钥库文件的路径。

它必须是 Java 密钥库 (jks) 或 PKCS#12 文件。不能同时使用此设置和"ssl.key"。

`xpack.notification.email.ssl.keystore.type`

     ([Static](settings.html#static-cluster-setting)) The format of the keystore file. It must be either `jks` or `PKCS12`. If the keystore path ends in ".p12", ".pfx", or ".pkcs12", this setting defaults to `PKCS12`. Otherwise, it defaults to `jks`. 
`xpack.notification.email.ssl.keystore.password`

     ([Static](settings.html#static-cluster-setting)) The password for the keystore. 
`xpack.notification.email.ssl.keystore.secure_password`

     ([Secure](secure-settings.html "Secure settings")) The password for the keystore. 
`xpack.notification.email.ssl.keystore.key_password`

    

(静态)密钥库中密钥的密码。缺省值为密钥库密码。

您不能同时使用此设置和"ssl.keystore.secure_password"。

`xpack.notification.email.ssl.keystore.secure_key_password`

     ([Secure](secure-settings.html "Secure settings")) The password for the key in the keystore. The default is the keystore password. 
`xpack.notification.email.ssl.truststore.path`

    

(静态)包含要信任的证书的密钥库的路径。它必须是 Java 密钥库 (jks) 或 PKCS#12 文件。

您不能同时使用此设置和"ssl.certificate_authorities"。

`xpack.notification.email.ssl.truststore.type`

     ([Static](settings.html#static-cluster-setting)) Set this to `PKCS12` to indicate that the truststore is a PKCS#12 file. 
`xpack.notification.email.ssl.truststore.password`

    

(静态)信任库的密码。

您不能同时使用此设置和"ssl.truststore.secure_password"。

`xpack.notification.email.ssl.truststore.secure_password`

     ([Secure](secure-settings.html "Secure settings")) Password for the truststore. 

### 松弛通知设置

您可以在"elasticsearch.yml"中配置以下Slack通知设置。有关通过 Slack 发送通知的更多信息，请参阅配置 Slack 操作。

`xpack.notification.slack.default_account`

    

(动态)默认的 Slack 帐户可供使用。

如果配置多个 Slack 帐户，则必须配置此设置或指定要在"松弛"操作中使用的 Slack 帐户。请参阅配置 Slack 帐户。

`xpack.notification.slack.account`

    

指定用于通过 Slack 发送通知的帐户信息。您可以指定以下 Slack 帐户属性：

`secure_url`

     ([Secure](secure-settings.html "Secure settings"), [reloadable](secure-settings.html#reloadable-secure-settings "Reloadable secure settings")) The Incoming Webhook URL to use to post messages to Slack. Required. 
`message_defaults`

    

松弛消息属性的默认值。

`from`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The sender name to display in the Slack message. Defaults to the watch ID. 
`to`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The default Slack channels or groups you want to send messages to. 
`icon`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The icon to display in the Slack messages. Overrides the incoming webhook's configured icon. Accepts a public URL to an image. 
`text`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The default message content. 
`attachment`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Default message attachments. Slack message attachments enable you to create more richly-formatted messages. Specified as an array as defined in the [ Slack attachments documentation](https://api.slack.com/docs/attachments). 

### Jira 通知设置

您可以在"elasticsearch.yml"中配置以下 Jira 通知设置。有关在 Jira 中使用通知创建事务的更多信息，请参阅配置 Jira 操作。

`xpack.notification.jira.default_account`

    

(动态)要使用的默认 Jira 帐户。

如果配置多个 Jira 帐户，则必须配置此设置或指定要在"jira"操作中使用的 Jira 帐户。请参阅配置 Jira 帐户。

`xpack.notification.jira.account`

    

指定用于在 Jira 中使用通知创建事务的帐户信息。您可以指定以下 Jira 账户属性：

`allow_http`

     ([Dynamic](settings.html#dynamic-cluster-setting)) If `false`, Watcher rejects URL settings that use a HTTP protocol. Defaults to `false`. 
`secure_url`

     ([Secure](secure-settings.html "Secure settings"), [reloadable](secure-settings.html#reloadable-secure-settings "Reloadable secure settings")) The URL of the Jira Software server. Required. 
`secure_user`

     ([Secure](secure-settings.html "Secure settings"), [reloadable](secure-settings.html#reloadable-secure-settings "Reloadable secure settings")) The name of the user to connect to the Jira Software server. Required. 
`secure_password`

     ([Secure](secure-settings.html "Secure settings"), [reloadable](secure-settings.html#reloadable-secure-settings "Reloadable secure settings")) The password of the user to connect to the Jira Software server. Required. 
`issue_defaults`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Default fields values for the issue created in Jira. See [Jira action attributes](actions-jira.html#jira-action-attributes "Jira action attributes") for more information. Optional. 

### 寻呼机值班通知设置

您可以在"elasticsearch.yml"中配置以下PagerDuty通知设置。有关通过寻呼程序值线发送通知的详细信息，请参阅配置寻呼机值操作。

`xpack.notification.pagerduty.default_account`

    

(动态)默认寻呼机值班帐户使用。

如果配置多个寻呼机帐户，则必须配置此设置或指定要在"寻呼值"操作中使用的寻呼机帐户。请参阅配置寻呼机值班帐户。

`xpack.notification.pagerduty.account`

    

指定用于通过寻呼机发送通知的帐户信息。您可以指定以下寻呼机帐户属性：

`name`

     ([Static](settings.html#static-cluster-setting)) A name for the PagerDuty account associated with the API key you are using to access PagerDuty. Required. 
`secure_service_api_key`

     ([Secure](secure-settings.html "Secure settings"), [reloadable](secure-settings.html#reloadable-secure-settings "Reloadable secure settings")) The [ PagerDuty API key](https://developer.pagerduty.com/documentation/rest/authentication) to use to access PagerDuty. Required. 

`event_defaults`

    

寻呼值空事件属性的默认值。自选。

`description`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A string that contains the default description for PagerDuty events. If no default is configured, each PagerDuty action must specify a `description`. 
`incident_key`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A string that contains the default incident key to use when sending PagerDuty events. 
`client`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A string that specifies the default monitoring client. 
`client_url`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The URL of the default monitoring client. 
`event_type`

     ([Dynamic](settings.html#dynamic-cluster-setting)) The default event type. Valid values: `trigger`,`resolve`, `acknowledge`. 
`attach_payload`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Whether or not to provide the watch payload as context for the event by default. Valid values: `true`, `false`. 

[« Thread pools](modules-threadpool.md) [Advanced configuration »](advanced-
configuration.md)
