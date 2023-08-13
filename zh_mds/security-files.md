

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Manually configure security](manually-
configure-security.md)

[« Supported SSL/TLS versions by JDK version](jdk-tls-versions.md) [FIPS
140-2 »](fips-140-compliance.md)

## 安全文件

Elasticsearch 安全功能使用以下文件：

* "ES_PATH_CONF/roles.yml"定义集群上使用的角色。请参阅定义角色。  * 'ES_PATH_CONF/elasticsearch-users' 定义了 'file' 领域的用户及其散列密码。请参阅基于文件的用户身份验证。  * 'ES_PATH_CONF/elasticsearch-users_roles' 定义了 'file' 领域的用户角色分配。请参阅基于文件的用户身份验证。  * "ES_PATH_CONF/role_mapping.yml"定义角色的可分辨名称 (DN) 的角色分配。这允许将 LDAP 和 Active Directory 组和用户以及 PKI 用户映射到角色。请参阅将用户和组映射到角色。  * 'ES_PATH_CONF/log4j2.properties' 包含审核信息。请参阅日志文件审核输出。

安全功能使用的任何文件都必须存储在 Elasticsearchconfiguration 目录中。Elasticsearch 以受限的权限运行，并且只允许从目录布局中配置的位置读取以增强安全性。

其中一些文件采用 YAML 格式。编辑这些文件时，请注意 YAML 是缩进级别敏感的，缩进错误可能会导致配置错误。避免使用制表符来设置缩进级别，或者使用自动将制表符扩展到空格的编辑器。

请注意正确转义 YAML 构造，例如"："或带引号的字符串中的前导感叹号。使用"|"或">"字符定义块文本，而不是转义有问题的字符有助于避免问题。

[« Supported SSL/TLS versions by JDK version](jdk-tls-versions.md) [FIPS
140-2 »](fips-140-compliance.md)
