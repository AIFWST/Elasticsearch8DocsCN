

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« SAML authentication](saml-realm.md) [JWT authentication »](jwt-auth-
realm.md)

## Kerberosauthentication

您可以配置 Elastic Stack 安全功能以支持 Kerberos V5 身份验证，这是一种在 Elasticsearch 中对用户进行身份验证的行业标准协议。

不能使用 Kerberos 领域在传输网络层上进行身份验证。

要使用 Kerberos 对用户进行身份验证，您需要配置 Kerberos 领域并将用户映射到角色。有关领域设置的详细信息，请参阅Kerberosrealm 设置。

### 关键概念

在设置 Kerberos 领域时，会遇到一些术语和概念：

_kdc_

     Key Distribution Center. A service that issues Kerberos tickets. 
_principal_

    

Kerberos 主体是 Kerberos 可以向其分配票证的唯一标识。它可用于标识服务器提供的用户或服务。

Kerberos V5 主体名称的格式为"primary/instance@REALM"，其中"primary"是用户名。

"instance"是一个可选字符串，用于限定主字符串，由斜杠("/")与主字符串分隔。对于用户，通常不使用它;对于服务主机，它是主机的完全限定域名。

"REALM"是Kerberos领域。通常是大写的域名。典型用户主体的示例是"user@ES.DOMAIN.LOCAL"。非典型服务主体的一个示例是"HTTP/es.domain.local@ES"。域。本地'。

_realm_

     Realms define the administrative boundary within which the authentication server has authority to authenticate users and services. 
_keytab_

     A file that stores pairs of principals and encryption keys. 

对此文件具有读取权限的任何人都可以使用网络中的凭据访问其他服务，因此使用适当的文件权限保护它非常重要。

_krb5.conf_

     A file that contains Kerberos configuration information such as the default realm name, the location of Key distribution centers (KDC), realms information, mappings from domain names to Kerberos realms, and default configurations for realm session key encryption types. 
_ticket granting ticket (TGT)_

     A TGT is an authentication ticket generated by the Kerberos authentication server. It contains an encrypted authenticator. 

### 配置 Kerberosrealm

Kerberos 用于保护服务，并使用基于票证的身份验证协议对用户进行身份验证。您可以将 Elasticsearch 配置为使用 Kerberos V5 身份验证协议(这是一种行业标准协议)对用户进行身份验证。在此方案中，客户端必须提供 Kerberos 票证进行身份验证。

在 Kerberos 中，用户使用身份验证服务进行身份验证，然后使用票证授予服务进行身份验证以生成 TGT(票证授予票证)。然后，此票证将提供给服务进行身份验证。有关获取 TGT 的详细信息，请参阅您的 Kerberos 安装文档。Elasticsearch 客户端必须首先获取 TGT，然后启动使用 Elasticsearch 进行身份验证的过程。

#### 开始之前

1. 部署科贝罗斯。

您必须在您的环境中设置 Kerberos 基础结构。

Kerberos 需要大量外部服务才能正常运行，例如所有计算机之间的时间同步以及域中的正向和反向 DNS 映射。有关更多详细信息，请参阅 Kerberos 文档。

这些说明不包括设置和配置 Kerberosdeployment。在提供示例的地方，它们与 MIT Kerberos V5 部署有关。有关详细信息，请参阅 MIT Kerberos文档

2. 配置爪哇 GSS。

Elasticsearch使用Java GSS框架支持进行Kerberos身份验证。为了支持 Kerberos 身份验证，Elasticsearch 需要以下文件：

    * `krb5.conf`, a Kerberos configuration file 
    * A `keytab` file that contains credentials for the Elasticsearch service principal 

配置要求取决于您的 Kerberos 设置。请参阅 Kerberos 文档以配置 'krb5.conf' 文件。

有关 Java GSS 的更多信息，请参阅 Java GSS Kerberosrequirements。

3. 为 HTTP 启用 TLS。

如果您的 Elasticsearch 集群在生产模式下运行，则必须将 HTTP 接口配置为使用 SSL/TLS，然后才能启用 Kerberosauthentication。有关更多信息，请参阅 加密 HTTP 客户端通信以进行 Elasticsearch。

此步骤对于通过 Kibana 支持 Kerberos 身份验证是必需的。直接针对 ElasticsearchRest API 的 Kerberos 身份验证不需要它。

4. 启用令牌服务

Elasticsearch Kerberos 实现利用了 Elasticsearch tokenservice。如果在 HTTP 接口上配置 TLS，则会自动启用此服务。可以通过在"elasticsearch.yml"文件中添加以下设置来显式配置它：

    
        xpack.security.authc.token.enabled: true

此步骤对于通过 Kibana 支持 Kerberos 身份验证是必需的。直接针对 ElasticsearchRest API 的 Kerberos 身份验证不需要它。

#### 创建一个 Kerberosrealm

要在 Elasticsearch 中配置 Kerberos 领域，请执行以下操作：

1. 配置 JVM 以查找 Kerberos 配置文件。

Elasticsearch使用Java GSS和JAAS Krb5LoginModule使用简单且受保护的GSSAPI协商机制(SPNEGO)机制来支持Kerberosauthentication。Kerberos 配置文件 ('krb5.conf') 提供默认领域、密钥分发中心 (KDC) 以及 Kerberos 身份验证所需的其他配置详细信息等信息。当 JVM 需要某些配置属性时，它会尝试通过查找和加载此文件来查找这些值。用于配置文件路径的 JVM 系统属性是 'java.security.krb5.conf'。要配置 JVM 系统属性，请参阅设置 JVM选项。如果未指定此系统属性，Java 将尝试根据约定查找文件。

建议为 Elasticsearch 配置此系统属性。设置此属性的方法取决于您的 Kerberos 基础结构。有关更多详细信息，请参阅 Kerberos 文档。

欲了解更多信息，seekrb5.conf

2. 为 Elasticsearch 节点创建一个密钥表。

密钥表是存储主体和加密密钥对的文件。Elasticsearch使用密钥表中的密钥来解密用户提供的票证。您必须使用 Kerberos 实现提供的工具为 Elasticsearch 创建密钥表。例如，一些创建keytabs的工具在Windows上是"ktpass.exe"，对于MIT Kerberos是"kadmin"。

3. 将密钥表文件放入 Elasticsearch 配置目录中。

确保此密钥表文件具有读取权限。此文件包含凭据，因此您必须采取适当的措施来保护它。

Elasticsearch 在 HTTP 网络层使用 Kerberos，因此每个 Elasticsearch 节点上都必须有一个用于 HTTP 服务主体的密钥表文件。服务主体名称的格式必须为 HTTP/es.domain.local@ES。域。本地'。密钥表文件对于每个节点都是唯一的，因为它们包含主机名。Elasticsearch 节点可以充当客户端请求的任何主体，只要该主体及其凭据在配置的密钥表中找到即可。

4. 创建一个科贝罗斯领域。

要在 Elasticsearch 中启用 Kerberos 身份验证，您必须在领域链中添加 Kerberosrealm。

您只能在 Elasticsearch 节点上配置一个 Kerberos 领域。

要配置 Kerberos 领域，您需要在 'elasticsearch.yml' 配置文件中配置一些必需的领域设置和其他可选设置。在'xpack.security.authc.realms.kerberos'命名空间下添加一个领域配置。

Kerberos 领域最常见的配置如下：

    
        xpack.security.authc.realms.kerberos.kerb1:
      order: 3
      keytab.path: es.keytab
      remove_realm_name: false

"用户名"是从用户提供的票证中提取的，通常具有"username@REALM"格式。此"用户名"用于将角色映射到用户。如果领域设置"remove_realm_name"设置为"true"，则删除领域部分("@REALM")。生成的"用户名"用于角色映射。

有关可用领域设置的详细信息，请参阅 Kerberos 领域设置。

5. 重新启动弹性搜索 6.将 Kerberos 用户映射到角色。

"kerberos"领域使您能够将 Kerberos 用户映射到角色。您可以使用创建或更新角色映射 API 来配置这些角色映射。您可以通过用户的"用户名"字段来标识用户。

以下示例使用角色映射 API 将"user@REALM"映射到角色"监视"和"用户"：

    
        POST /_security/role_mapping/kerbrolemapping
    {
      "roles" : [ "monitoring_user" ],
      "enabled": true,
      "rules" : {
        "field" : { "username" : "user@REALM" }
      }
    }

如果要支持 Kerberos 跨领域身份验证，则可能需要基于 Kerberos 领域名称映射角色。对于此类方案，以下是可用于角色映射的其他用户元数据：\-'kerberos_realm' 将设置为 Kerberos 领域名称。\-'kerberos_user_principal_name' 将设置为 Kerberos 票证中的用户主体名称。

有关更多信息，请参阅将用户和组映射到角色。

Kerberos 领域支持授权领域作为角色映射的替代方法。

#### 为 Kerberos 配置 Kibana

如果要使用 Kerberos 通过浏览器和 Kibana 进行身份验证，则需要在 Kibana 配置中启用相关的身份验证提供程序。请参阅 Kerberos 单一登录

[« SAML authentication](saml-realm.md) [JWT authentication »](jwt-auth-
realm.md)
