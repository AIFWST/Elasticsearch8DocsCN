

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« File-based user authentication](file-realm.md) [Native user
authentication »](native-realm.md)

## LDAP 用户身份验证

您可以将弹性堆栈安全功能配置为与轻量级目录访问协议 (LDAP) 服务器通信以对用户进行身份验证。请参阅配置 LDAP 域。

LDAP 按层次结构存储用户和组，类似于文件夹在文件系统中的分组方式。LDAP 目录的层次结构是从容器构建的，例如_organizational unit_ ('ou')、_organization_ ('o')、and_domain component_ ('dc')。

条目的路径是唯一标识用户或组的_Distinguished Name_ (DN)。用户名和组名通常具有a_common name_ ('cn') 或_unique ID_ ('uid') 等属性。DN 被指定为字符串，例如"cn=admin，dc=example，dc=com"(空格将被忽略)。

"ldap"领域支持两种操作模式，一种是用户搜索模式，另一种是具有用户 DN 特定模板的模式。

### 将 LDAP 组映射到角色

领域认证过程的一个组成部分是解析与经过身份验证的用户关联的角色。角色定义用户在群集中拥有的权限。

由于使用"ldap"领域时，用户在LDAP服务器中进行外部管理，因此期望他们的角色也在那里进行管理。事实上，LDAP 支持组的概念，组通常表示组织中不同系统的用户角色。

"ldap"领域使您能够通过 LDAP 组或其他元数据将 LDAP 用户映射到角色。可以通过添加角色映射 API 或使用存储在每个节点上的文件来配置此角色映射。当用户使用 LDAP 进行身份验证时，该用户的权限是由用户映射到的角色定义的所有权限的联合。

### 配置 LDAP 领域

要与 LDAP 集成，请配置"ldap"域并将 LDAP 组映射到用户角色。

1. 确定要使用的模式。"ldap"领域支持两种操作模式：用户搜索模式和具有用户 DN 特定模板的模式。

LDAP 用户搜索是最常见的操作模式。在此模式下，具有搜索 LDAP 目录权限的特定用户用于根据提供的用户名和 LDAP 属性搜索身份验证用户的 DN。找到后，通过尝试使用找到的 DN 和提供的密码绑定到 LDAP 服务器来对用户进行身份验证。

如果您的 LDAP 环境对用户使用了一些特定的标准命名条件，那么您可以使用用户 DN 模板来配置领域。此方法的优点是不必执行搜索即可查找用户 DN。但是，可能需要多个绑定操作才能找到正确的用户 DN。

2. 要使用用户搜索配置"ldap"域，请执行以下操作：

    1. Add a realm configuration to `elasticsearch.yml` under the `xpack.security.authc.realms.ldap` namespace. At a minimum, you must specify the `url` and `order` of the LDAP server, and set `user_search.base_dn` to the container DN where the users are searched for. See [LDAP realm settings](security-settings.html#ref-ldap-settings "LDAP realm settings") for all of the options you can set for an `ldap` realm.

例如，以下代码片段显示了配置了用户搜索的 LDAP 域：

        
                xpack:
          security:
            authc:
              realms:
                ldap:
                  ldap1:
                    order: 0
                    url: "ldaps://ldap.example.com:636"
                    bind_dn: "cn=ldapuser, ou=users, o=services, dc=example, dc=com"
                    user_search:
                      base_dn: "dc=example,dc=com"
                      filter: "(cn={0})"
                    group_search:
                      base_dn: "dc=example,dc=com"
                    files:
                      role_mapping: "ES_PATH_CONF/role_mapping.yml"
                    unmapped_groups_as_roles: false

"bind_dn"用户的密码应通过向 Elasticsearch 密钥库添加适当的"secure_bind_password"设置来配置。例如，以下命令为上述示例领域添加密码：

        
                bin/elasticsearch-keystore add \
        xpack.security.authc.realms.ldap.ldap1.secure_bind_password

在 'elasticsearch.yml' 中配置领域时，只有您指定的领域用于身份验证。如果还想使用"本机"或"文件"域，则必须将它们包含在域链中。

3. 要使用用户 DN 模板配置"ldap"域，请执行以下操作：

    1. Add a realm configuration to `elasticsearch.yml` in the `xpack.security.authc.realms.ldap` namespace. At a minimum, you must specify the `url` and `order` of the LDAP server, and specify at least one template with the `user_dn_templates` option. See [LDAP realm settings](security-settings.html#ref-ldap-settings "LDAP realm settings") for all of the options you can set for an `ldap` realm.

例如，以下代码片段显示了使用用户 DN 模板配置的 LDAP 域：

        
                xpack:
          security:
            authc:
              realms:
                ldap:
                  ldap1:
                    order: 0
                    url: "ldaps://ldap.example.com:636"
                    user_dn_templates:
                      - "cn={0}, ou=users, o=marketing, dc=example, dc=com"
                      - "cn={0}, ou=users, o=engineering, dc=example, dc=com"
                    group_search:
                      base_dn: "dc=example,dc=com"
                    files:
                      role_mapping: "/mnt/elasticsearch/group_to_role_mapping.yml"
                    unmapped_groups_as_roles: false

模板模式下不使用"bind_dn"设置。所有 LDAP 操作都以身份验证用户身份运行。

4. (可选)配置安全功能与多个 LDAP 服务器的交互方式。

"load_balance.type"设置可以在领域级别使用。Elasticsearch安全功能支持故障转移和负载平衡操作模式。请参阅 LDAP 领域设置。

5. (可选)要保护密码，请加密 Elasticsearch 和 LDAP 服务器之间的通信。  6. 重新启动弹性搜索。  7. 将 LDAP 组映射到角色。

"ldap"领域使您能够通过 LDAP 组或其他元数据将 LDAP 用户映射到角色。可以通过添加角色映射 API 或使用存储在每个节点上的文件来配置此角色映射。当用户使用 LDAP 进行身份验证时，该用户的权限是由用户映射到的角色定义的所有权限的联合。

在映射定义中，您可以使用组的可分辨名称指定组。例如，以下映射配置将 LDAP"管理员"组映射到"监控"和"用户"角色，并将"用户"组映射到"用户"角色。

通过角色映射 API 配置：

    
        PUT /_security/role_mapping/admins
    {
      "roles" : [ "monitoring" , "user" ],
      "rules" : { "field" : {
        "groups" : "cn=admins,dc=example,dc=com" __} },
      "enabled": true
    }

__

|

"管理员"组的 LDAP 可分辨名称 (DN)。   ---|--- PUT /_security/role_mapping/basic_users { "roles" ： [ "user" ]， "rules" ： { "field" ： { "groups" ： "cn=users，dc=example，dc=com" __} }， "enabled"： true }

__

|

"用户"组的 LDAP 可分辨名称 (DN)。   ---|---或者，通过角色映射文件进行配置：

    
        monitoring: __- "cn=admins,dc=example,dc=com" __user:
      - "cn=users,dc=example,dc=com" __- "cn=admins,dc=example,dc=com"

__

|

映射角色的名称。   ---|---    __

|

"管理员"组的 LDAP 可分辨名称 (DN)。   __

|

"用户"组的 LDAP 可分辨名称 (DN)。   有关更多信息，请参阅将 LDAP 组映射到角色和将用户和组映射到角色。

LDAP 域支持授权域作为角色映射的替代方法。

8. (可选)在 LDAP 领域上配置"元数据"设置，以在用户的元数据中包含额外的字段。

默认情况下，"ldap_dn"和"ldap_groups"填充在用户的元数据中。有关更多信息，请参阅 LDAP 领域中的用户元数据。

下面的示例将用户的公用名 ('cn') 作为其元数据中的附加字段包含在内。

    
        xpack:
      security:
        authc:
          realms:
            ldap:
              ldap1:
                order: 0
                metadata: cn

9. 设置 SSL 以加密 Elasticsearch 和 LDAP 之间的通信。请参阅加密 Elasticsearch 和 LDAP 之间的通信。

### LDAP领域中的用户元数据

当用户通过 LDAP 领域进行身份验证时，以下属性将填充到用户的 _metadata_ 中：

Field

|

描述 ---|--- 'ldap_dn'

|

用户的可分辨名称。   "ldap_groups"

|

为用户解析的每个组的可分辨名称(无论这些组是否映射到角色)。   此元数据在身份验证 API 中返回，并可与角色中的模板化查询一起使用。

通过在 LDAP 域上配置"元数据"设置，可以将其他字段包含在用户的元数据中。此元数据可用于角色映射 API 或模板化角色查询。

### 负载平衡和故障转移

可以在领域级别使用"load_balance.type"设置来配置安全功能应如何与多个 LDAP 服务器交互。安全功能支持故障转移和负载平衡操作模式。

请参阅负载平衡和故障转移。

### 加密 Elasticsearch 和 LDAP 之间的通信

为了保护在 LDAP 领域中发送用于身份验证的用户凭据，强烈建议对 Elasticsearch 和 LDAP 服务器之间的通信进行加密。通过 SSL/TLS 进行连接可确保在 Elasticsearch 传输用户凭据之前对 LDAP 服务器的身份进行身份验证，并且连接的内容已加密。通过 TLS 连接到 LDAP 服务器的客户机和节点需要在其密钥库或信任库中安装 LDAP 服务器的证书或服务器的根 CA 证书。

有关更多信息，请参阅 LDAP 用户身份验证。

1. 在每个节点上配置领域的 TLS 设置，以信任由签署 LDAP 服务器证书的 CA 签名的证书。以下示例演示了如何信任位于 Elasticsearch 配置目录中的 CA 证书 'cacert.pem'： xpack： security： authc： realms： ldap： ldap1： order： 0 url： "ldaps://ldap.example.com:636" ssl： certificate_authorities： [ "cacert.pem" ]

在上面的示例中，CA 证书必须采用 PEM 编码。

还支持 PKCS#12 和 JKS 文件 - 请参阅 LDAP 领域设置中"ssl.truststore.path"的说明。

您还可以指定单个服务器证书而不是 CA 证书，但仅当您具有单个 LDAP 服务器或证书是自签名证书时，才建议这样做。

2. 在领域配置中设置"url"属性以指定 LDAPS 协议和安全端口号。例如，"网址：ldaps://ldap.example.com:636"。  3. 重新启动弹性搜索。

默认情况下，当您将 Elasticsearch 配置为使用 SSL/TLS 连接到 LDAP 服务器时，它会尝试使用证书中的值验证领域配置中通过"url"属性指定的主机名或 IP 地址。如果证书和领域配置中的值不匹配，Elasticsearch 将不允许连接到 LDAP 服务器。这样做是为了防止中间人攻击。如有必要，可以通过将"ssl.verification_mode"属性设置为"证书"来禁用此行为。

[« File-based user authentication](file-realm.md) [Native user
authentication »](native-realm.md)
