

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Security domains](security-domain.md) [File-based user authentication
»](file-realm.md)

## 活动目录用户身份验证

您可以配置 Elastic Stack 安全功能以与 ActiveDirectory 通信以对用户进行身份验证。请参阅配置 Active DirectoryRealm。

安全功能使用LDAP与Active Directory通信，因此"active_directory"领域类似于"ldap"领域。与 LDAP 目录一样，Active Directory 按层次结构存储用户和组。目录的层次结构是从容器构建的，例如_organizational unit_ ('ou')、_organization_ ('o') 和 _domaincomponent_ ('dc')。

条目的路径是唯一标识用户或组的_Distinguished Name_ (DN)。用户名和组名通常具有a_common name_ ('cn') 或_unique ID_ ('uid') 等属性。DN 被指定为字符串，例如"cn=admin，dc=example，dc=com"(空格将被忽略)。

安全功能仅支持 Active Directory 安全组。不能将通讯组映射到角色。

当您使用Active Directory进行身份验证时，用户输入的用户名应与"sAMAccountName"或"userPrincipalName"匹配，而不是通用名称。

Active Directory 领域使用 LDAP 绑定请求对用户进行身份验证。对用户进行身份验证后，领域会搜索以在 Active Directory 中查找用户的哨兵。找到用户后，Active Directoryrealm 就会从 Active Directory 中用户条目的"tokenGroups"属性中检索用户的组成员身份。

### 配置 Active Directoryrealm

要与 Active Directory 集成，请配置"active_directory"领域，并将 Active Directory 用户和组映射到角色映射文件中的角色。

1. 将类型为"active_directory"的领域配置添加到"xpack.security.authc.realms.active_directory"命名空间下的"elasticsearch.yml"。至少，您必须指定活动目录"domain_name"和"顺序"。

有关可以为"active_directory"领域设置的所有选项，请参阅 Active Directory 领域设置。

如果域名未在 DNS 中映射，则绑定到 Active Directory 将失败。如果 Windows DNS 服务器未提供 DNS，请在本地"/etc/hosts"文件中添加域映射。

例如，以下领域配置将 Elasticsearch 配置为连接到"ldaps://example.com:636"，以便通过 ActiveDirectory 对用户进行身份验证：

    
        xpack:
      security:
        authc:
          realms:
            active_directory:
              my_ad:
                order: 0 __domain_name: ad.example.com
                url: ldaps://ad.example.com:636 __

__

|

领域顺序控制在对用户进行身份验证时检查已配置领域时的顺序。   ---|---    __

|

如果未指定 URL，则默认为"ldap：<domain_name>：389"。   在 'elasticsearch.yml' 中配置领域时，只有您指定的领域用于身份验证。如果还想使用"本机"或"文件"域，则必须将它们包含在域链中。

2. 如果要跨林中的多个域对用户进行身份验证，则需要执行额外的步骤。配置和用户身份验证方式存在一些细微差异。

将"domain_name"设置设置为林根域名。

还必须设置"url"设置，因为必须针对全局编录进行身份验证，全局编录使用不同的端口，并且可能不会在每个域控制器上运行。

例如，以下领域配置将 Elasticsearch 配置为连接到全局编录端口上的特定域控制器，并将域名设置为林根：

    
        xpack:
      security:
        authc:
          realms:
            active_directory:
              my_ad:
                order: 0
                domain_name: example.com __url: ldaps://dc1.ad.example.com:3269, ldaps://dc2.ad.example.com:3269 __load_balance:
                  type: "round_robin" __

__

|

"domain_name"设置为林中根域的名称。   ---|---    __

|

此示例中使用的"url"值具有两个不同域控制器的 URL，这两个域控制器也是全局编录服务器。端口 3268 是与全局编录进行未加密通信的默认端口;端口 3269 是 SSL 连接的默认端口。连接到的服务器可以位于林的任何域中，只要它们也是全局编录服务器。   __

|

提供了负载平衡设置，以指示选择要连接到的服务器时的所需行为。   在此配置中，用户需要使用其完整的用户主体名称 (UPN) 或下层登录名称。UPN 通常是用户名与"@<DOMAIN_NAME"(如"johndoe@ad.example.com")的串联。下层登录名是 NetBIOS 域名，后跟"\"和用户名，如"AD\johndoe"。使用下层登录名需要连接到常规 LDAP 端口(389 或 636)，以便查询配置容器以从 NetBIOS 名称检索域名。

3. (可选)配置 Elasticsearch 应如何与多个 Active Directory 服务器交互。

"load_balance.type"设置可以在领域级别使用。支持两种操作模式：故障转移和负载平衡。请参阅活动目录领域设置。

4. (可选)要保护密码，请加密 Elasticsearch 和 Active Directory 服务器之间的通信。  5. 重新启动弹性搜索。  6. (可选)配置绑定用户。

Active Directory 领域使用 LDAP 绑定请求对用户进行身份验证。默认情况下，所有 LDAP 操作都由 Elasticsearch 进行身份验证的用户运行。在某些情况下，普通用户可能无法访问 Active Directory 中的所有必要项目，因此需要_bind user_。可以配置绑定用户，并用于执行除 LDAP 绑定请求之外的所有操作，LDAP 绑定请求是验证用户提供的凭据所必需的。

使用绑定用户使运行方式功能能够与 ActiveDirectory 领域一起使用，并能够维护一组与 Active Directory 的池连接。这些池连接减少了每个用户身份验证必须创建和销毁的资源数。

以下示例显示了通过"bind_dn"和"secure_bind_password"设置的用户绑定用户的配置：

    
        xpack:
      security:
        authc:
          realms:
            active_directory:
              my_ad:
                order: 0
                domain_name: ad.example.com
                url: ldaps://ad.example.com:636
                bind_dn: es_svc_user@ad.example.com __

__

|

这是执行所有活动目录搜索请求的用户。如果未配置绑定用户，所有请求都将以使用 Elasticsearch 进行身份验证的用户身份运行。   ---|--- 应通过将适当的"secure_bind_password"设置添加到 Elasticsearch 密钥库来配置"bind_dn"用户的密码。例如，以下命令为上述示例领域添加密码：

    
        bin/elasticsearch-keystore add  \
    xpack.security.authc.realms.active_directory.my_ad.secure_bind_password

配置绑定用户时，默认情况下启用连接池。可以使用"user_search.pool.enabled"设置禁用连接池。

7. 将活动目录用户和组映射到角色。

领域认证过程的一个组成部分是解析与经过身份验证的用户关联的角色。角色定义用户在群集中拥有的权限。

由于使用"active_directory"领域，用户在Active Directory服务器中进行外部管理，因此期望他们的角色也在那里进行管理。事实上，Active Directory 支持组的概念，组通常表示组织中不同系统的用户角色。

"active_directory"领域使您能够通过其 Active Directory 组或其他元数据将 Active Directory 用户映射到角色。可以通过角色映射 API 或使用存储在每个节点上的文件来配置此角色映射。当用户针对 Active Directory 领域进行身份验证时，该用户的权限是用户所定义的角色所定义的所有权限的并集。

在映射定义中，您可以使用组的可分辨名称指定组。例如，以下映射配置将 ActiveDirectory "管理员"组映射到"监视"和"用户"角色，将"用户"组映射到"用户"角色，并将"John Doe"用户映射到"用户"角色。

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

"管理员"组的活动目录可分辨名称 (DN)。   ---|--- PUT /_security/role_mapping/basic_users { "roles" ： [ "user" ]， "rules" ： { "any"： [ { "field" ： { "groups" ： "cn=users，dc=example，dc=com" __} }， { "field" ： { "dn" ： "cn=John Doe，cn=contractors，dc=example，dc=com" __} } ] }， "enabled"： true }

__

|

"用户"组的活动目录可分辨名称 (DN)。   ---|---    __

|

用户"John Doe"的活动目录可分辨名称 (DN)。   或者，通过角色映射文件进行配置：

    
        monitoring: __- "cn=admins,dc=example,dc=com" __user:
      - "cn=users,dc=example,dc=com" __- "cn=admins,dc=example,dc=com"
      - "cn=John Doe,cn=contractors,dc=example,dc=com" __

__

|

角色的名称。   ---|---    __

|

"管理员"组的活动目录可分辨名称 (DN)。   __

|

"用户"组的活动目录可分辨名称 (DN)。   __

|

用户"John Doe"的活动目录可分辨名称 (DN)。   有关更多信息，请参阅将用户和组映射到角色。

8. (可选)在 Active Directory 域中配置"元数据"设置，以在用户的元数据中包含额外的属性。

默认情况下，"ldap_dn"和"ldap_groups"填充在用户的元数据中。有关详细信息，请参阅 Active Directory 领域中的用户元数据。

### Active Directoryrealms 中的用户元数据

当用户通过 Active Directory 领域进行身份验证时，以下属性将填充到用户的 _metadata_ 中：

Field

|

描述 ---|--- 'ldap_dn'

|

用户的可分辨名称。   "ldap_groups"

|

为用户解析的每个组的可分辨名称(无论这些组是否映射到角色)。   此元数据在身份验证 API 中返回，可与角色中的模板化查询一起使用。

通过在 Active Directory 领域配置"元数据"设置，可以从 Active Directory 服务器中提取其他元数据。

### 负载平衡和故障转移

可以在领域级别使用"load_balance.type"设置来配置安全功能应如何与多个 Active Directory 服务器交互。支持两种操作模式：故障转移和负载平衡。

请参阅负载平衡和故障转移。

### 加密 Elasticsearch 和 ActiveDirectory 之间的通信

为了保护发送用于身份验证的用户凭据，强烈建议对 Elasticsearch 和 ActiveDirectory 服务器之间的通信进行加密。通过 SSL/TLS 进行连接可确保在 Elasticsearch 传输用户凭据之前对 Active Directory 服务器的身份进行身份验证，并且用户名和密码在传输过程中被加密。

通过 SSL/TLS 连接到 Active Directory 服务器的客户机和节点需要在其密钥库或信任库中安装 Active Directory 服务器的证书或服务器的根 CA 证书。

1. 在 'elasticsearch.yml' 文件中为 'xpack.security.authc.realms' 命名空间创建领域配置。请参阅配置 Active Directory 领域。  2. 在领域配置中设置"url"属性以指定 LDAPS 协议和安全端口号。例如，"网址：ldaps://ad.example.com:636"。  3. 将每个节点配置为信任由签署 Active Directory 服务器证书的证书颁发机构 (CA) 签名的证书。

以下示例演示如何信任位于配置目录中的 CA 证书('cacert.pem')：

    
        xpack:
      security:
        authc:
          realms:
            active_directory:
              ad_realm:
                order: 0
                domain_name: ad.example.com
                url: ldaps://ad.example.com:636
                ssl:
                  certificate_authorities: [ "ES_PATH_CONF/cacert.pem" ]

CA 证书必须是 PEM 编码的证书。

有关这些设置的详细信息，请参阅活动目录领域设置。

4. 重新启动弹性搜索。

默认情况下，当您配置 Elasticsearch 以使用 SSL/TLS 连接到 Active Directory 时，它会尝试使用证书中的值验证领域配置中通过 'url' 属性指定的主机名或 IP 地址。如果证书和领域配置中的值不匹配，Elasticsearch 将不允许连接到 Active Directoryserver。这样做是为了防止中间人攻击。如有必要，可以通过将"ssl.verification_mode"属性设置为"证书"来禁用此行为。

[« Security domains](security-domain.md) [File-based user authentication
»](file-realm.md)
