

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« OpenID Connect authentication](oidc-realm.md) [SAML authentication
»](saml-realm.md)

## PKI 用户身份验证

您可以将 Elasticsearch 配置为使用公钥基础设施 (PKI) 证书来验证用户身份。在这种情况下，直接连接到 Elasticsearch 的客户端必须提供 X.509 证书。首先，必须接受证书在 SSL/TLS 层上进行身份验证 在弹性搜索上。然后，可以选择通过 PKI 领域进一步验证它们。SeePKI 身份验证，用于直接连接到 Elasticsearch 的客户端。

您还可以使用 PKI 证书向 Kibana 进行身份验证，但这需要一些额外的配置。在 Elasticsearch 上，此配置使 Kibana 能够充当 SSL/TLS 身份验证的代理，并将客户端证书提交给 Elasticsearch 以供 PKI 领域进一步验证。请参阅连接到 Kibana 的客户端的 PKI 身份验证。

### 直接连接到 Elasticsearch 的客户端的 PKI 身份验证

要在 Elasticsearch 中使用 PKI，请配置 PKI 领域，在所需的网络层(传输或 http)上启用客户端身份验证，并将用户证书中"主题"字段中的专有名称 (DN) 映射到角色。您可以在角色映射文件中创建映射或使用角色映射 API。

您可以结合使用 PKI 和用户名/密码身份验证。例如，您可以在传输层上启用 SSL/TLS 并定义 PKI 领域，以要求传输客户端使用 X.509 证书进行身份验证，同时仍使用用户名和密码凭据对 HTTP 流量进行身份验证。

1. 将 'pki' 领域的领域配置添加到 'xpack.security.authc.realms.pki' 命名空间下的 'elasticsearch.yml' 中。您必须显式设置"order"属性。请参阅 PKI 领域设置，了解可以为"pki"领域设置的所有选项。

例如，以下代码片段显示了最基本的"pki"域配置：

    
        xpack:
      security:
        authc:
          realms:
            pki:
              pki1:
                order: 1

使用此配置，接受 Elasticsearch SSL/TLSlayer 信任的任何证书进行身份验证。用户名是从最终实体证书的"主题"字段中的 DN 中提取的公用名 (CN)。此配置不足以允许对 Kibana 进行 PKI 身份验证;需要执行其他步骤。

在 'elasticsearch.yml' 中配置领域时，只有您指定的领域用于身份验证。如果还想使用"本机"或"文件"域，则必须将它们包含在域链中。

2. 可选：如果要使用主题 DN 的 CN 以外的其他内容作为用户名，可以指定正则表达式以提取所需的用户名。正则表达式应用于主题 DN。

例如，以下配置中的正则表达式从主题 DN 中提取电子邮件地址：

    
        xpack:
      security:
        authc:
          realms:
            pki:
              pki1:
                order: 1
                username_pattern: "EMAILADDRESS=(.*?)(?:,|$)"

如果正则表达式过于严格，并且与客户端证书的使用者 DN 不匹配，则领域不会对证书进行身份验证。

3. 可选：如果您希望相同的用户在连接到 Kibana 时也使用证书进行身份验证，则必须将 Elasticsearch PKI 领域配置为允许委派。请参阅连接到 Kibana 的客户端的 PKI 身份验证。  4. 重新启动 Elasticsearch，因为领域配置不会自动重新加载。如果要执行后续步骤，则可能希望最后保持重启。  5. 启用 SSL/TLS。  6. 在所需的网络层(传输或 http)上启用客户端身份验证。

要在客户端直接连接到 Elasticsearch 时使用 PKI，您必须通过客户端身份验证启用 SSL/TLS。也就是说，您必须将"xpack.security.transport.ssl.client_authentication"和"xpack.security.http.ssl.client_authentication"设置为"可选"或"必需"。如果设置值为"可选"，则没有证书的客户端可以使用其他凭据进行身份验证。

当客户端直接连接到 Elasticsearch 并且未经过代理身份验证时，PKI 领域依赖于节点网络接口的 TLS 设置。可以将领域配置为比基础网络连接更严格。也就是说，可以配置节点，以便网络接口接受某些连接，但随后无法通过 PKI 域进行身份验证。但是，反之则不然。PKI 领域无法对网络接口拒绝的连接进行身份验证。

具体而言，这意味着：

    * The transport or http interface must request client certificates by setting `client_authentication` to `optional` or `required`. 
    * The interface must _trust_ the certificate that is presented by the client by configuring either the `truststore` or `certificate_authorities` paths, or by setting `verification_mode` to `none`. 
    * The _protocols_ supported by the interface must be compatible with those used by the client. 

有关这些设置的说明，请参阅常规 TLS 设置。

必须将相关的网络接口(传输或 http)配置为信任要在 PKI 领域中使用的任何证书。但是，可以将 PKI 领域配置为仅信任网络接口接受的证书的 _子集_。当 SSL/TLS 层信任的客户端的证书由不同的 CA 签名，而不是由签署用户证书的证书签名的证书时，这很有用。

要使用自己的信任库配置 PKI 域，请指定"truststore.path"选项。路径必须位于 Elasticsearchconfiguration 目录 ('ES_PATH_CONF') 中。例如：

    
        xpack:
      security:
        authc:
          realms:
            pki:
              pki1:
                order: 1
                truststore:
                  path: "pki1_truststore.jks"

如果信任库受密码保护，则应通过将适当的"secure_password"设置添加到 Elasticsearchkey 库来配置密码。例如，以下命令为上述示例域添加密码：

    
        bin/elasticsearch-keystore add \
    xpack.security.authc.realms.pki.pki1.truststore.secure_password

当证书文件采用 PEM 格式时，"certificate_authorities"选项可用作"truststore.path"设置的替代方法。设置接受列表。这两个选项是排他性的，它们不能同时使用。

7. 映射 PKI 用户的角色。

您可以通过角色映射 API 或使用存储在每个节点上的文件来映射 PKI 用户的角色。这两个配置选项将合并在一起。当用户针对 PKI 领域进行身份验证时，该用户的权限是用户映射到的角色定义的所有权限的联合。

您可以通过证书中的可分辨名称来标识用户。例如，以下映射配置使用角色映射 API 将"John Doe"映射到"用户"角色：

    
        PUT /_security/role_mapping/users
    {
      "roles" : [ "user" ],
      "rules" : { "field" : {
        "dn" : "cn=John Doe,ou=example,o=com" __} },
      "enabled": true
    }

__

|

PKI 用户的可分辨名称 (DN)。   ---|--- 或者，使用角色映射文件。例如：

    
        user: __- "cn=John Doe,ou=example,o=com" __

__

|

角色的名称。   ---|---    __

|

PKI 用户的可分辨名称 (DN)。   文件的路径默认为"ES_PATH_CONF/role_mapping.yml"。您可以使用"files.role_mapping"领域设置(例如"xpack.security.authc.realms.pki.pki1.files.role_mapping")指定不同的路径(必须在"ES_PATH_CONF"内)。

PKI 用户的可分辨名称遵循 X.500 命名约定，该约定将最具体的字段(如"cn"或"uid")放在名称的开头，将最一般的字段(如"o"或"dc")放在名称的末尾。某些工具(如 _openssl_)可能会以不同的格式打印出主题名称。

确定证书的正确 DN 的一种方法是使用身份验证 API(使用相关的 PKI 证书作为身份验证方式)并检查结果中的元数据字段。用户的可分辨名称将填充在"pki_dn"键下。您还可以使用身份验证 API 来验证您的角色映射。

有关更多信息，请参阅将用户和组映射到角色。

PKI 领域支持授权领域作为角色映射的替代方法。

### 连接到 Kibana 的客户端的 PKI 身份验证

默认情况下，PKI 领域依赖于节点的网络接口来执行 SSL/TLS 握手并提取客户端证书。此行为要求客户端直接连接到 Elasticsearch，以便它们的 SSLconnection 由 Elasticsearch 节点终止。如果 SSL/TLS 身份验证由 Kibana 执行，则必须将 PKI 领域配置为允许委派。

具体来说，当提供 X.509 证书的客户端连接到 Kibana 时，Kibana 会执行 SSL/TLS 身份验证。然后，Kibana 转发客户端的证书链(通过调用 Elasticsearch API)，让已配置为委派的 PKI 领域进一步验证它们。

要允许特定 Elasticsearch PKI 领域的身份验证委派，请首先为通常的情况配置领域，如直接连接到 Elasticsearch 的客户端的 PKIauthentication 部分所述。在这种情况下，启用 TLS 时，必须加密 HTTP 客户端通信。

您还必须显式配置"信任库"(或等效地配置"certificate_authorities")，即使它与您在网络层上配置的信任配置相同。"xpack.security.authc.token.enabled"和"delegate.enabled"设置也必须为"true"。例如：

    
    
    xpack:
      security:
        authc:
          token.enabled: true
          realms:
            pki:
              pki1:
                order: 1
                delegation.enabled: true
                truststore:
                  path: "pki1_truststore.jks"

重新启动 Elasticsearch 后，此领域可以验证委托的 PKI身份验证。然后，您必须将 Kibana 配置为允许 PKI 证书身份验证。

对于直接连接到 Elasticsearch 的客户端，带有"delegate.enabled"的 PKI 领域仍然保持不变。直接身份验证的用户和通过委派到 Kibana 进行 PKI 身份验证的用户都遵循相同的角色映射规则或授权域配置。

但是，如果使用角色映射 API，则可以区分通过委派进行身份验证的用户和直接进行身份验证的用户。前者在用户的元数据中具有额外的字段"pki_delegated_by_user"和"pki_delegated_by_realm"。在将身份验证委托给 Kibana 的常见设置中，这些字段的值分别为"kibana"和"保留"。例如，以下角色映射规则通过连接到 Elasticsearch(而不是通过 Kibana)将"role_for_pki1_direct"角色分配给已通过"pki1"领域直接进行身份验证的所有用户：

    
    
    PUT /_security/role_mapping/direct_pki_only
    {
      "roles" : [ "role_for_pki1_direct" ],
      "rules" : {
        "all": [
          {
            "field": {"realm.name": "pki1"}
          },
          {
            "field": {
              "metadata.pki_delegated_by_user": null __}
          }
        ]
      },
      "enabled": true
    }

__

|

如果设置了此元数据字段(即，它不是 ** 'null')，则用户已在委派方案中进行身份验证。   ---|--- « OpenID Connect 身份验证 SAML 身份验证»