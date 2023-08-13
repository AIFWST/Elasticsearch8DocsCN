

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Configuring SAML single-sign-on on the Elastic Stack](saml-guide-
stack.md) [User authorization »](authorization.md)

## 使用 OpenIDConnect 配置单点登录弹性堆栈

Elastic Stack 支持使用 OpenID Connect 的单点登录 (SSO)，使用 Elasticsearch 作为拥有大部分功能的后端服务。Kibana 和 Elasticsearch 共同代表一个 OpenID ConnectRelying 方 (RP)，它支持授权代码流和隐式流，因为它们在 OpenID Connect 规范中定义。

本指南假定您有一个 OpenID Connect 提供程序，其中将注册 ElasticStack 信赖方。

Kibana 中的 OpenID Connect 领域支持旨在成为该 Kibana实例用户的主要身份验证方法。配置 Kibana 部分介绍了这意味着什么，以及如何在必要时进行设置以支持其他领域。

### OpenID ConnectProvider

OpenID Connect 提供程序 (OP) 是 OpenID Connect 中的实体，负责对用户进行身份验证并授予必要的令牌以及依赖方要使用的身份验证和用户信息。

为了使 Elastic Stack 能够使用 OpenID Connect 提供程序进行身份验证，需要在 OP 和 RP 之间建立信任关系。在 OpenID Connect 提供程序中，这意味着将 RP 注册为客户端。OpenID Connect 定义了动态客户端注册协议，但这通常面向实时客户端注册，而不是跨安全域单点登录的信任建立过程。所有 OP 还允许通过用户界面或(较少)使用元数据文档将 RP 手动注册为客户端。

注册 Elastic Stack RP 的过程与 OP 到 OP 的过程不同，遵循提供商的相关文档是谨慎的。注册时通常需要提供的 RP 信息如下：

* "信赖方名称"：信赖方的任意标识符。规范和 Elastic Stack 实现都不会对此值施加任何约束。  * "重定向 URI"：这是 OP 在身份验证后重定向用户浏览器的 URI。此值的适当值将取决于您的设置以及 Kibana 是否位于代理或负载均衡器后面。它通常是"${kibana-url}/api/security/oidc/callback"(对于授权代码流)或"${kibana-url}/api/security/oidc/implicit"(对于隐式流)，其中 _${kibana-url}_ 是 Kibana 实例的基本 URL。您可能还会看到这称为"回调 URI"。

在注册过程结束时，OP 将分配一个客户端标识符和一个客户端密钥供 RP(弹性堆栈)使用。请注意这两个值，因为它们将在 Elasticsearch 配置中使用。

### 为 OpenID Connect 身份验证配置 Elasticsearch

以下是在 Elasticsearch 中使用 OpenID Connect 启用身份验证所需的配置步骤摘要：

1. 为 HTTP 2 启用 SSL/TLS。启用令牌服务 3.创建一个或多个 OpenID 连接领域 4.配置角色映射

#### 为 HTTP 启用 TLS

如果您的 Elasticsearch 集群在生产模式下运行，那么您必须将 HTTP 接口配置为使用 SSL/TLS，然后才能启用 OpenIDConnect 身份验证。

有关更多信息，请参阅为 Elasticsearch 加密 HTTP 客户端通信。

#### 启用令牌服务

Elasticsearch OpenID Connect实现利用了ElasticsearchToken服务。如果您在 HTTP 接口上配置 TLS，则会自动启用此服务，并且可以通过在"elasticsearch.yml"文件中包含以下内容来显式配置：

    
    
    xpack.security.authc.token.enabled: true

#### 创建 OpenID 连接领域

基于 OpenID Connect 的身份验证是通过在 Elasticsearch 的身份验证链中配置适当的领域来实现的。

此领域有一些必需的设置和许多可选设置。可用设置在 OpenID Connect 领域设置中有详细说明。本指南将探讨最常见的设置。

在您的"elasticsearch.yml"文件中创建一个 OpenID Connect(领域类型为 'oidc')领域，如下所示：

下面使用的值仅供参考，并非适用于所有用例。配置代码段下方的详细信息提供了见解和建议，可帮助您根据 rOP 配置选择适当的值。

    
    
    xpack.security.authc.realms.oidc.oidc1:
      order: 2
      rp.client_id: "the_client_id"
      rp.response_type: code
      rp.redirect_uri: "https://kibana.example.org:5601/api/security/oidc/callback"
      op.issuer: "https://op.example.org"
      op.authorization_endpoint: "https://op.example.org/oauth2/v1/authorize"
      op.token_endpoint: "https://op.example.org/oauth2/v1/token"
      op.jwkset_path: oidc/jwkset.json
      op.userinfo_endpoint: "https://op.example.org/oauth2/v1/userinfo"
      op.endsession_endpoint: "https://op.example.org/oauth2/v1/logout"
      rp.post_logout_redirect_uri: "https://kibana.example.org:5601/security/logged_out"
      claims.principal: sub
      claims.groups: "http://example.info/claims/groups"

上面示例中使用的配置值为：

xpack.security.authc.realms.oidc.oidc1

     This defines a new `oidc` authentication realm named "oidc1". See [Realms](realms.html "Realms") for more explanation of realms. 
order

     You should define a unique order on each realm in your authentication chain. It is recommended that the OpenID Connect realm be at the bottom of your authentication chain (that is, that it has the _highest_ order). 
rp.client_id

     This, usually opaque, arbitrary string, is the Client Identifier that was assigned to the Elastic Stack RP by the OP upon registration. 
rp.response_type

    

这是一个标识符，用于控制此 RP 支持的 OpenID Connect 身份验证流以及此 RP 请求 OP 应遵循的流。支持的值为

* "代码"，表示 RP 想要使用授权代码流。如果您的 OP 支持授权代码流，则应选择此选项而不是隐式流。  * "id_token令牌"，这意味着 RP 想要使用隐式流，我们还从 OP 请求一个 oAuth2 访问令牌，我们可以将其用于后续请求(用户信息)。如果 OP 在其配置中提供 UserInfo 终结点，或者如果你知道需要用于角色映射的声明在 ID 令牌中不可用，则应选择此选项。  * "id_token"表示 RP 想要使用隐式流，但对获取 oAuth2 令牌也不感兴趣。如果确定所有必要的声明都将包含在 ID 令牌中，或者 OP 不提供用户信息终结点，请选择此选项。

rp.redirect_uri

     The redirect URI where the OP will redirect the browser after authentication. This needs to be _exactly_ the same as the one [configured with the OP upon registration](oidc-guide.html#oidc-guide-op "The OpenID Connect Provider") and will typically be `${kibana-url}/api/security/oidc/callback` where _${kibana-url}_ is the base URL for your Kibana instance 
op.issuer

     A verifiable Identifier for your OpenID Connect Provider. An Issuer Identifier is usually a case sensitive URL. The value for this setting should be provided by your OpenID Connect Provider. 
op.authorization_endpoint

     The URL for the Authorization Endpoint in the OP. This is where the user's browser will be redirected to start the authentication process. The value for this setting should be provided by your OpenID Connect Provider. 
op.token_endpoint

     The URL for the Token Endpoint in the OpenID Connect Provider. This is the endpoint where Elasticsearch will send a request to exchange the code for an ID Token. This setting is optional when you use the implicit flow. The value for this setting should be provided by your OpenID Connect Provider. 
op.jwkset_path

     The path to a file or a URL containing a JSON Web Key Set with the key material that the OpenID Connect Provider uses for signing tokens and claims responses. If a path is set, it is resolved relative to the Elasticsearch config directory. Elasticsearch will automatically monitor this file for changes and will reload the configuration whenever it is updated. Your OpenID Connect Provider should provide you with this file or a URL where it is available. 
op.userinfo_endpoint

     (Optional) The URL for the UserInfo Endpoint in the OpenID Connect Provider. This is the endpoint of the OP that can be queried to get further user information, if required. The value for this setting should be provided by your OpenID Connect Provider. 
op.endsession_endpoint

     (Optional) The URL to the End Session Endpoint in the OpenID Connect Provider. This is the endpoint where the user's browser will be redirected after local logout, if the realm is configured for RP initiated Single Logout and the OP supports it. The value for this setting should be provided by your OpenID Connect Provider. 
rp.post_logout_redirect_uri

     (Optional) The Redirect URL where the OpenID Connect Provider should redirect the user after a successful Single Logout (assuming `op.endsession_endpoint` above is also set). This should be set to a value that will not trigger a new OpenID Connect Authentication, such as `${kibana-url}/security/logged_out` or `${kibana-url}/login?msg=LOGGED_OUT` where _${kibana-url}_ is the base URL for your Kibana instance. 
claims.principal

     See [Claims mapping](oidc-guide.html#oidc-claims-mappings "Claims mapping"). 
claims.groups

     See [Claims mapping](oidc-guide.html#oidc-claims-mappings "Claims mapping"). 

OpenID Connect 领域的最后一项配置是设置在 OP 中注册期间分配给 RP 的"客户端密钥"。这是一个安全的设置，因此不会在 'elasticsearch.yml' 的领域配置中定义，而是添加到 elasticsearch 密钥库中。例如

    
    
    bin/elasticsearch-keystore add xpack.security.authc.realms.oidc.oidc1.rp.client_secret

根据OpenID Connect规范，OP还应该在众所周知的URL上提供他们的配置，这是他们的"Issuer"值与".well-known/openid-configuration"字符串的连接。例如："https://op.org.com/.well-known/openid-configuration" 该文档应包含在 Elasticsearch 中配置 OpenID Connectrealm 的所有必要信息。

#### 声明映射

##### 声明和作用域

使用 OpenID Connect 向 Kibana 进行身份验证时，OP 将以 OpenID Connect 声明的形式提供有关用户的信息，这些信息可以包含在 ID 令牌中，也可以从 OP 的 UserInfo 端点检索。声明定义为 OP 为经过身份验证的用户断言的一条信息。简单地说，声明是包含有关用户的信息的名称/值对。与声明相关，我们也有OpenID Connect Scopes的概念。范围是用于请求访问特定声明列表的标识符。该标准定义了一组可以请求的范围标识符。唯一强制性的是"openid"，而常用的是"个人资料"和"电子邮件"。"个人资料"范围请求访问"姓名"、"family_name"、"given_name"、"middle_name"、"昵称"、"preferred_username"、"个人资料"、"图片"、"网站"、"性别"、"出生日期"、"zoneinfo"、"区域设置"和"updated_at"声明。"电子邮件"范围请求访问"电子邮件"和"email_verified"声明。该过程是 RP 在身份验证请求期间请求特定范围。如果 OP 隐私政策允许并且身份验证用户同意它，则相关声明将返回到 RP(在 ID 令牌中或作为 UserInfo 响应)。

支持的声明列表将根据您使用的 OP 而有所不同，但您可以预期标准声明将在很大程度上得到支持。

##### 将声明映射到用户属性

声明映射的目标是配置 Elasticsearch，以便能够将指定返回声明的值映射到 Elasticsearch 支持的用户属性之一。然后，这些用户属性用于在 Kibana UI 或审核日志中标识用户，还可用于创建角色映射规则。

配置 OpenID 声明映射的建议步骤如下：

1. 请查阅您的 OP 配置，了解它可能支持哪些声明。请注意，OP 的元数据或 OP 的配置页中提供的列表是可能受支持的声明的列表。但是，出于隐私原因，它可能不是完整的声明，或者并非所有受支持的声明都可用于所有经过身份验证的用户。  2. 通读 Elasticsearch 支持的用户属性列表，并确定其中哪些对您有用，并且可以由您的 OP 以声明的形式提供。在 _minimum_ 中，"主体"用户属性是必需的。  3. 配置您的 OP 以将这些声明"释放"给您的 Elastic Stack 信赖方。此过程因提供商而异。可以使用静态配置，而其他配置将支持 RP 请求与声明对应的范围在身份验证时"释放"。有关如何配置要请求的范围的详细信息，请参阅"rp.requested_scopes"。为了确保互操作性并最大限度地减少错误，您应该只请求 OP 支持的范围，以及您打算映射到 Elasticsearch 用户属性的范围。           注意：您只能使用字符串、数字、布尔值或上述数组的值映射声明。

4. 在 Elasticsearch 中配置 OpenID Connect 领域，以将 Elasticsearch 用户属性(请参阅下面的列表)与您的 OP 将发布的声明的名称相关联。在上面的示例中，我们配置了"主体"和"组"用户属性，如下所示：

    1. `claims.principal: sub` : This instructs Elasticsearch to look for the OpenID Connect claim named `sub` in the ID Token that the OP issued for the user ( or in the UserInfo response ) and assign the value of this claim to the `principal` user property. `sub` is a commonly used claim for the principal property as it is an identifier of the user in the OP and it is also a required claim of the ID Token, thus offering guarantees that it will be available. It is, however, only used as an example here, the OP may provide another claim that is a better fit for your needs. 
    2. `claims.groups: "http://example.info/claims/groups"` : Similarly, this instructs Elasticsearch to look for the claim with the name `http://example.info/claims/groups` (note that this is a URI - an identifier, treated as a string and not a URL pointing to a location that will be retrieved) either in the ID Token or in the UserInfo response, and map the value(s) of it to the user property `groups` in Elasticsearch. There is no standard claim in the specification that is used for expressing roles or group memberships of the authenticated user in the OP, so the name of the claim that should be mapped here, will vary greatly between providers. Consult your OP documentation for more details. 

##### 弹性搜索用户属性

Elasticsearch OpenID Connect 领域可以配置为将 OpenID Connect声明映射到经过身份验证的用户的以下属性：

principal

     _(Required)_ This is the _username_ that will be applied to a user that authenticates against this realm. The `principal` appears in places such as the Elasticsearch audit logs. 

如果无法从声明映射主体属性，则身份验证将失败。

groups

     _(Recommended)_ If you wish to use your OP's concept of groups or roles as the basis for a user's Elasticsearch privileges, you should map them with this property. The `groups` are passed directly to your [role mapping rules](oidc-guide.html#oidc-role-mappings "Configuring role mappings"). 
name

     _(Optional)_ The user's full name. 
mail

     _(Optional)_ The user's email address. 
dn

     _(Optional)_ The user's X.500 _Distinguished Name_. 

##### 从 OpenID 连接声明中提取部分值

在某些情况下，声明的价值可能包含比您希望在 Elasticsearch 中使用的更多的信息。一个常见的例子是 OP 专门处理电子邮件地址，但您希望用户的"主体"使用电子邮件地址的 _local name_部分。例如，如果他们的电子邮件地址是"james.wong@staff.example.com"，那么您希望他们的校长只是"james.wong"。

这可以使用 Elasticsearchrealm 中的"claim_patterns"设置来实现，如下面的领域配置所示：

    
    
    xpack.security.authc.realms.oidc.oidc1:
      order: 2
      rp.client_id: "the_client_id"
      rp.response_type: code
      rp.redirect_uri: "https://kibana.example.org:5601/api/security/oidc/callback"
      op.authorization_endpoint: "https://op.example.org/oauth2/v1/authorize"
      op.token_endpoint: "https://op.example.org/oauth2/v1/token"
      op.userinfo_endpoint: "https://op.example.org/oauth2/v1/userinfo"
      op.endsession_endpoint: "https://op.example.org/oauth2/v1/logout"
      op.issuer: "https://op.example.org"
      op.jwkset_path: oidc/jwkset.json
      claims.principal: email_verified
      claim_patterns.principal: "^([^@]+)@staff\\.example\\.com$"

在这种情况下，用户的"主体"是从"email_verified"声明映射的，但在将值分配给用户之前，会先对值应用正则表达式。如果正则表达式匹配，则第一组的结果用作有效值。如果正则表达式不匹配，则声明映射失败。

在此示例中，电子邮件地址必须属于"staff.example.com"域，然后本地部分("@"之前的任何内容)用作主体。任何尝试使用其他电子邮件域登录的用户都将失败，因为正则表达式将与其电子邮件地址不匹配，因此不会填充其主体用户属性(这是必需的)。

这些正则表达式中的小错误可能会产生严重的安全后果。例如，如果我们不小心遗漏了上面示例中的尾随"$"，那么我们将匹配域以"staff.example.com"开头的任何电子邮件地址，这将接受诸如"admin@staff.example.com.attacker.net"之类的电子邮件地址。请务必确保正则表达式尽可能精确，以免无意中为用户模拟攻击打开途径。

#### 第三方发起的单点登录

Elasticsearch 中的 Open ID Connect 领域支持第三方发起的登录，如相关规范中所述。

这允许 OP 本身或 RP 以外的其他第三方在请求将 OP 用于身份验证时启动身份验证过程。请注意，应已为此 OP 配置了弹性堆栈 RP，以便此过程成功。

#### OpenID ConnectLogout

Elasticsearch 中的 OpenID Connect 领域支持 RP 发起的注销功能，如规范的相关部分所述

在此过程中，OpenID Connect RP(在本例中为 Elastic Stack)会在成功完成本地注销后将用户的浏览器重定向到 OP 的预定义 URL。然后，OP 也可以注销用户，具体取决于配置，并最终将用户重定向回 RP。领域配置中的"op.endsession_endpoint"决定了浏览器将被重定向到的 OP 中的 URL。"rp.post_logout_redirect_uri"设置确定在 OP 注销用户后将用户重定向回的 URL。

配置"rp.post_logout_redirect_uri"时，应注意将其指向将触发用户重新身份验证的 URL。例如，当使用 OpenID Connect 支持单点登录 Kibana 时，可以将其设置为"${kibana-url}/security/logged_out"，这将向用户显示用户友好的消息，或者"${kibana-url}/login？msg=LOGGED_OUT"，这将把用户带到 Kibana 中的登录选择器。

#### OpenID Connect Realm SSLConfiguration

OpenID Connect 依靠 TLS 来提供安全属性，例如传输中加密和端点身份验证。RP 需要与 OP 建立反向通道通信，以便在授权代码授予流期间交换 ID 令牌的代码，并从 UserInfo 端点获取其他用户信息。此外，如果您将"op.jwks_path"配置为URL，Elasticsearch将需要从托管在那里的文件中获取OP的签名密钥。因此，重要的是Elasticsearch可以验证和信任OP用于TLS的服务器证书。由于系统信任库用于传出 https 连接的客户端上下文，因此如果您的 OP 使用的是来自受信任的 CA 的证书，则无需进行其他配置。

但是，如果您的 OP 证书的颁发者不受运行 Elasticsearch 的 JVM 的信任(例如，它使用组织 CA)，那么您必须将 Elasticsearch 配置为信任该 CA。 假设您有 CA 证书，该证书已签署 OP 用于 TLS 的证书存储在存储在 Elasticsearch 配置目录中的 /oidc/company-ca.pem 文件中， 您需要在领域配置中设置以下属性：

    
    
    xpack.security.authc.realms.oidc.oidc1:
      order: 1
      ...
      ssl.certificate_authorities: ["/oidc/company-ca.pem"]

### 配置角色映射

当用户使用 OpenID Connect 进行身份验证时，他们会被识别到 Elastic Stack，但这不会自动授予他们执行任何操作或访问任何数据的访问权限。

您的 OpenID Connect 用户在被分配角色之前无法执行任何操作。这可以通过添加角色映射 API 或授权域来完成。

不能使用角色映射文件向通过 OpenIDConnect 进行身份验证的用户授予角色。

这是一个简单角色映射的示例，该映射将"example_role"角色授予针对"oidc1"OpenID Connect 领域进行身份验证的任何用户：

    
    
    PUT /_security/role_mapping/oidc-example
    {
      "roles": [ "example_role" ], __"enabled": true,
      "rules": {
        "field": { "realm.name": "oidc1" }
      }
    }

__

|

"example_role"角色不是内置的 Elasticsearch 角色。此示例假定您已创建自己的自定义角色，并具有对数据流、索引和 Kibana 功能的适当访问权限。   ---|--- 通过领域配置映射的用户属性用于处理角色映射规则，这些规则确定授予用户哪些角色。

提供给角色映射的用户字段派生自 OpenID Connect 声明，如下所示：

* "用户名"："主体"用户属性 * "dn"："dn"用户属性 * "组"："组"用户属性 * "元数据"：请参阅用户元数据

有关详细信息，请参阅将用户和组映射到角色和角色映射。

如果您的 OP 能够通过使用 OpenID 声明向 RP 提供组或角色，那么您应该将此声明映射到 Elasticsearch 领域中的"claims.groups"设置(请参阅将声明映射到用户属性)，然后按照以下示例在角色映射中使用它。

此映射将 Elasticsearch 的"finance_data"角色授予通过"oidc1"领域进行身份验证且具有"财务团队"组成员身份的任何用户。

    
    
    PUT /_security/role_mapping/oidc-finance
    {
      "roles": [ "finance_data" ],
      "enabled": true,
      "rules": { "all": [
            { "field": { "realm.name": "oidc1" } },
            { "field": { "groups": "finance-team" } }
      ] }
    }

如果您的用户也存在于 Elasticsearch 可以直接访问的存储库中(例如 LDAP 目录)，那么您可以使用授权域而不是角色映射。

在这种情况下，请执行以下步骤：

1. 在 OpenID Connect 领域中，通过配置"claims.principal"设置，分配一个声明以充当查找用户 ID。  2. 创建一个可以从本地存储库中查找用户的新领域(例如"ldap"领域) 3.在 OpenID Connect 领域中，将"authorization_realms"设置为在步骤 2 中创建的领域的名称。

### 用户元数据

默认情况下，通过 OpenID Connect 进行身份验证的用户将具有一些额外的元数据字段。这些字段将包括身份验证响应中提供的每个 OpenID 声明(无论它是否映射到 Elasticsearch 用户属性)。例如，在元数据字段'oidc(claim_name)'中，"claim_name"是声明的名称，因为它包含在 ID 令牌或用户信息响应中。请注意，这些将包括与身份验证事件相关的所有 ID 令牌声明，而不是用户本身。

可以通过在 oidc 领域中添加"populate_user_metadata：false"作为设置来禁用此行为。

### 配置木bana

Kibana 中的 OpenID Connect 身份验证除了标准 Kibana 安全配置外，还需要少量其他设置。TheKibana 安全文档提供了有关您可以应用的可用配置选项的详细信息。

特别是，由于您的 Elasticsearch 节点已配置为在 HTTP 接口上使用 TLSa，因此您必须将 Kibana 配置为使用 'https' URL 连接到 Elasticsearch，并且您可能需要配置"elasticsearch.ssl.certificateAuthority" 以信任 Elasticsearch 已配置为使用的证书。

Kibana 中的 OpenID Connect 身份验证受制于"kibana.yml"中的以下超时设置：

* 'xpack.security.session.idleTimeout' * 'xpack.security.session.lifespan'

您可能需要根据安全要求调整这些超时。

OpenID Connect 支持所需的三个附加设置如下所示：

    
    
    xpack.security.authc.providers:
      oidc.oidc1:
        order: 0
        realm: "oidc1"

上面示例中使用的配置值为：

`xpack.security.authc.providers`

     Add `oidc` provider to instruct Kibana to use OpenID Connect single sign-on as the authentication method. This instructs Kibana to attempt to initiate an SSO flow everytime a user attempts to access a URL in Kibana, if the user is not already authenticated. If you also want to allow users to login with a username and password, you must enable the `basic` authentication provider too. For example: 
    
    
    xpack.security.authc.providers:
      oidc.oidc1:
        order: 0
        realm: "oidc1"
      basic.basic1:
        order: 1

这将允许尚未使用 OpenID Connect 进行身份验证的用户使用 Kibana 登录表单登录。

`xpack.security.authc.providers.oidc.<provider-name>.realm`

     The name of the OpenID Connect realm in Elasticsearch that should handle authentication for this Kibana instance. 

### OpenID 连接没有 Kibana

OpenID Connect 领域旨在允许用户向 Kibana 进行身份验证，因此，上述指南的大部分部分都假设使用了 Kibana。本节介绍自定义 Web 应用程序如何使用相关的 OpenID Connect REST API，以便通过 OpenID Connect 对用户进行 Elasticsearch 身份验证。

OpenID Connect 和 SAML 等单点登录领域使用 Elasticsearch 中的 TokenService，原则上将 SAML 或 OpenID ConnectAuthentication 响应交换为 Elasticsearch 访问令牌和刷新令牌。访问令牌用作后续调用 Elasticsearch 的凭据。刷新令牌使用户能够在当前访问令牌过期后获取新的 Elasticsearch 访问令牌。

Elasticsearch 令牌服务可以看作是一个最小的 oAuth2 授权服务器，上面提到的访问令牌和刷新令牌是与此授权服务器相关的令牌。它们由Elasticsearch生成和consumed_only_，与OpenID Connect提供程序颁发的令牌(访问令牌和ID令牌)无关。

#### 向 OpenID 连接提供程序注册 RP

信赖方(Elasticsearch 和自定义 Web 应用程序)需要注册为 OpenID Connect 提供程序的客户端。请注意，注册"重定向 URI"时，它必须是自定义 Web 应用中的 URL。

#### OpenID ConnectRealm

OpenID Connect 领域需要在 Elasticsearch 中创建和配置。请参阅为 OpenID 连接身份验证配置 Elasticsearch

#### 用于访问 API 的服务帐户用户

在设计该领域时，假设需要一个特权实体充当身份验证代理。在这种情况下，自定义 Web 应用程序是处理最终用户身份验证的身份验证代理(更准确地说，将身份验证"委托"给 OpenID 连接提供程序)。OpenID Connect API 需要身份验证和经过身份验证的用户的必要授权级别。因此，需要创建服务帐户用户并为其分配一个角色，以授予他们"manage_oidc"群集权限。身份验证发生后，必须使用"manage_token"群集权限，以便用户可以保持访问权限或随后注销。

    
    
    POST /_security/role/facilitator-role
    {
      "cluster" : ["manage_oidc", "manage_token"]
    }
    
    
    POST /_security/user/facilitator
    {
      "password" : "<somePasswordHere>",
      "roles"    : [ "facilitator-role"]
    }

#### 处理身份验证流

在高级别上，自定义 Web 应用程序需要执行以下步骤才能使用 OpenID Connect 对用户进行身份验证：

1. 向"_security/oidc/prepare"发出HTTP POST请求，以"促进者"用户的身份进行身份验证，使用请求正文中Elasticsearch配置中的OpenID Connect领域名称。有关更多详细信息，请参阅 OpenID 连接准备身份验证。           POST /_security/oidc/prepare { "realm" ： "oidc1" }

2. 处理对"/_security/oidc/prepare"的响应。来自 Elasticsearch 的响应将包含 3 个参数："重定向"、"状态"、"随机数"。自定义 Web 应用程序需要在用户的会话中存储"state"和"nonce"的值(如果会话信息以这种方式持久保存，则在 cookie 或服务器端中存储)，并将用户的浏览器重定向到将包含在"重定向"值中的 URL。  3. 处理来自 OP 的后续响应。用户使用 OpenID Connect 提供程序成功进行身份验证后，他们将被重定向回调/重定向 URI。收到此 HTTP GET 请求后，自定义 Web 应用程序将需要向"_security/oidc/authenticate"发出 HTTP POST 请求，再次 - 以"促进者"用户的身份进行身份验证 - 将用户浏览器重定向到的 URL 作为参数传递，以及之前保存在用户会话中的"nonce"和"state"的值。如果配置了多个 OpenID Connect 领域，则自定义 Web 应用程序可以指定用于处理此问题的领域名称，但此参数是可选的。有关更多详细信息，请参阅 OpenID 连接身份验证。           POST /_security/oidc/authenticate { "redirect_uri" ： "https://oidc-kibana.elastic.co:5603/api/security/oidc/callback?code=jtI3Ntt8v3_XvcLzCFGq&state=4dbrihtIAt3wBTwo6DxK-vdk-sSyDBV8Yf0AjdkdT5I"， "state" ： "4dbrihtIAt3wBTwo6DxK-vdk-sSyDBV8Yf0AjdkdT5I"， "nonce" ： "WaBPH0KqPVdG5HHdSxPRjfoZbXMCicm5v1OiAj0DUFM"， "realm" ： "oidc1" }

Elasticsearch 将对此进行验证，如果一切正确，将使用访问令牌进行响应，该令牌可用作后续请求的"持有者"令牌，以及稍后可用于刷新给定访问令牌的刷新令牌，如获取令牌中所述。

4. 在某些时候，如有必要，自定义 Web 应用程序可以使用 OIDC 注销 API 将用户注销，并将访问令牌和刷新令牌作为参数传递。例如： POST /_security/oidc/logout { "token" ： "dGhpcyBpcyBub3QgYSByZWFsIHRva2VuIGJ1dCBpdCBpcyBvbmx5IHRlc3QgZGF0YS4gZG8gbm90IHRyeSB0byByZWFkIHRva2VuIQ=="， "refresh_token"： "vLBPvmAB6KvwvJZr27cS" }

如果相应地配置了领域，则可能会导致带有"重定向"参数的响应，指示用户需要在 OP 中重定向到何处才能完成注销过程。

[« Configuring SAML single-sign-on on the Elastic Stack](saml-guide-
stack.md) [User authorization »](authorization.md)
