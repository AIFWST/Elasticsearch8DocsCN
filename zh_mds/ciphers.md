

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Manually configure security](manually-
configure-security.md)

[« Setting passwords for native and built-in users](change-passwords-native-
users.md) [Supported SSL/TLS versions by JDK version »](jdk-tls-
versions.md)

## 启用密码套件以实现更强的加密

TLS 和 SSL 协议使用密码套件来确定用于保护数据的加密强度。您可能希望增加使用 Oracle JVM 时使用的加密强度;IcedTea OpenJDK的发货没有这些限制。成功使用加密通信不需要此步骤。

_Java加密扩展 (JCE) 无限强度管辖权PolicyFiles_允许在需要添加到 Java 安装的单独 JARfile 中使用其他 Java 密码套件。您可以从甲骨文的下载页面下载此JAR文件。The_JCE无限强度管辖权策略 密钥长度大于 128 位的加密(例如 256 位 AES加密)需要文件_。

安装后，JCE 中的所有密码套件都可供使用，但需要配置才能使用它们。要启用具有 Elasticsearch 安全功能的更强密码套件，请配置"cipher_suites"参数。

必须在群集中的所有节点上安装_JCE无限强度管辖权策略Files_，以建立改进的加密强度级别。

[« Setting passwords for native and built-in users](change-passwords-native-
users.md) [Supported SSL/TLS versions by JDK version »](jdk-tls-
versions.md)
