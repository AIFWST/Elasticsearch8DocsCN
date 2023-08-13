

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Controlling the user cache](controlling-user-cache.md) [Configuring
single sign-on to the Elastic Stack using OpenID Connect »](oidc-guide.md)

## 在 ElasticStack 上配置 SAML 单点登录

Elastic Stack 支持 SAML 单点登录 (SSO) 到 Kibana，使用 Elasticsearch 作为后端服务。在 SAML 术语中，弹性堆栈作为_Service Provider_运行。

启用 SAML 单点登录所需的另一个组件是 the_Identity Provider_ ，这是一项处理您的凭据并执行用户实际身份验证的服务。

如果您有兴趣在 Kibana 中配置 SSO，则需要向 Elasticsearch 提供有关您的_Identity Provider_的信息，并且您需要将 Elastic Stack 注册为该身份提供程序的已知_Service Provider_within。在 Kibana 中还需要进行一些配置更改才能激活 SAML 身份验证提供程序。

Kibana 中的 SAML 支持旨在成为该 Kibana 实例用户的主要(或唯一)身份验证方法。在 Kibana 中启用 SAML 身份验证后，它将影响所有尝试登录的用户。配置 Kibana 部分提供了有关其工作原理的更多详细信息。

### 标识提供者

Elastic Stack 支持 SAML 2.0 _Web浏览器SSO_和 SAML 2.0_Single Logout_配置文件，并且可以与至少支持 SAML 2.0 _Web浏览器 SSO Profile_的任何身份提供程序 (IdP) 集成。它已经通过许多流行的IdP实现进行了测试，例如Microsoft ActiveDirectory联合服务(ADFS)，Azure Active Directory(AAD)和Okta。

本指南假定您已有 IdP，并希望将 Kibana 添加为服务提供商。

弹性堆栈使用标准 SAML _metadata_ 文档，采用 XML 格式，用于定义 IdP 的功能和特性。您应该能够在 IdP 管理界面中下载或生成此类文档。

下载 IdP 元数据文档并将其存储在每个 Elasticsearch 节点上的"config"目录中。就本指南而言，我们假设您将其存储为"config/saml/idp-metadata.xml"。

将为 IdP 分配一个标识符(SAML 术语中的 _EntityID_)，该标识符通常以资源Identifier_(URI) 形式表示_Uniform该标识符。您的管理界面可能会告诉您这是什么，或者您可能需要阅读元数据文档才能找到它 - 在"实体描述符"元素上查找"entityID"属性。

大多数 IdP 将提供包含 Elastic Stack 所需的所有功能的适当元数据文件，并且只应需要下面所述的配置步骤。为了完整起见，Elastic Stack 对 IdP 元数据的最低要求是：

* 带有<EntityDescriptor>与 Elasticsearch 配置匹配的"entityID" 的"" * <IDPSSODescriptor>支持 SAML 2.0 协议("urn：oasis：names：tc：SAML：2.0：protocol")的""。  * 至少一个为 _signing_ 配置的""(即，它有"use="signing""或未指定"use") * 绑定 HTTP-Redirect 的 '' ('urn：oasis：names：tc：SAML：2.0：bindings：HTTP-Redirect') <KeyDescriptor><SingleSignOnService>* 如果您希望支持单点注销，则使用<SingleLogoutService>绑定 HTTP-Redirect 的"" ('urn：oasis：names：tc：SAML：2.0：bindings：HTTP-Redirect')

弹性堆栈要求对来自 IdP 的所有消息进行签名。对于身份验证"<Response>"消息，签名可以应用于响应本身，也可以应用于单个断言。对于消息，<LogoutRequest>必须对消息本身进行签名，并且应按照 HTTP 重定向绑定的要求，将签名作为 URL 参数提供。

### 为 SAMLauthentication 配置弹性搜索

在 Elasticsearch 中启用 SAML 身份验证有五个配置步骤：

1. 为 HTTP 2 启用 SSL/TLS。启用令牌服务 3.创建一个或多个 SAML 领域 4.配置角色映射 5.生成供身份提供程序使用的 SAML 元数据文件 _(可选)_

#### 为 HTTP 启用 TLS

如果您的 Elasticsearch 集群在生产模式下运行，则必须先将 HTTP 接口配置为使用 SSL/TLS，然后才能启用 SAML身份验证。

有关更多信息，请参阅为 Elasticsearch 加密 HTTP 客户端通信。

#### 启用令牌服务

Elasticsearch SAML实现利用了Elasticsearch TokenService。如果您在 HTTP 接口上配置 TLS，则会自动启用此服务，并且可以通过在"elasticsearch.yml"文件中包含以下内容来显式配置：

    
    
    xpack.security.authc.token.enabled: true

#### 创建 SAML领域

SAML 身份验证是通过在 Elasticsearch 的身份验证链中配置 SAML 领域来启用的。

此领域有一些必需的设置和许多可选设置。安全设置中详细介绍了可用设置。例如，SAML 领域设置、SAML 领域签名设置、SAML 领域加密设置、SAML 领域 SSL 设置。本指南将引导您完成最常见的设置。

通过将以下内容添加到您的"elasticsearch.yml"配置文件来创建领域。下面介绍了每个配置值。

    
    
    xpack.security.authc.realms.saml.saml1:
      order: 2
      idp.metadata.path: saml/idp-metadata.xml
      idp.entity_id: "https://sso.example.com/"
      sp.entity_id:  "https://kibana.example.com/"
      sp.acs: "https://kibana.example.com/api/security/saml/callback"
      sp.logout: "https://kibana.example.com/logout"
      attributes.principal: "urn:oid:0.9.2342.19200300.100.1.1"
      attributes.groups: "urn:oid:1.3.6.1.4.1.5923.1.5.1."

SAML 在通过 Kibana 进行身份验证时使用，但它不是直接向 Elasticsearch REST API 进行身份验证的有效方法。因此，我们建议您在身份验证链中至少包含一个额外的领域，例如本机领域，以供 API 客户端使用。

上面示例中使用的配置值为：

xpack.security.authc.realms.saml.saml1

     This defines a new `saml` authentication realm named "saml1". See [Realms](realms.html "Realms") for more explanation of realms. 
order

     The order of the realm within the realm chain. Realms with a lower order have highest priority and are consulted first. We recommend giving password-based realms such as file, native, LDAP, and Active Directory the lowest order (highest priority), followed by SSO realms such as SAML and OpenID Connect. If you have multiple realms of the same type, give the most frequently accessed realm the lowest order to have it consulted first. 
idp.metadata.path

     This is the path to the metadata file that you saved for your Identity Provider. The path that you enter here is relative to your `config/` directory. Elasticsearch will automatically monitor this file for changes and will reload the configuration whenever it is updated. 
idp.entity_id

     This is the identifier (SAML EntityID) that your IdP uses. It should match the `entityID` attribute within the metadata file. 
sp.entity_id

     This is a unique identifier for your Kibana instance, expressed as a URI. You will use this value when you add Kibana as a service provider within your IdP. We recommend that you use the base URL for your Kibana instance as the entity ID. 
sp.acs

     The _Assertion Consumer Service_ (ACS) endpoint is the URL within Kibana that accepts authentication messages from the IdP. This ACS endpoint supports the SAML HTTP-POST binding only. It must be a URL that is accessible from the web browser of the user who is attempting to login to Kibana, it does not need to be directly accessible by Elasticsearch or the IdP. The correct value may vary depending on how you have installed Kibana and whether there are any proxies involved, but it will typically be `${kibana-url}/api/security/saml/callback` where _${kibana-url}_ is the base URL for your Kibana instance. 
sp.logout

     This is the URL within Kibana that accepts logout messages from the IdP. Like the `sp.acs` URL, it must be accessible from the web browser, but does not need to be directly accessible by Elasticsearch or the IdP. The correct value may vary depending on how you have installed Kibana and whether there are any proxies involved, but it will typically be `${kibana-url}/logout` where _${kibana-url}_ is the base URL for your Kibana instance. 
attributes.principal

     See [Attribute mapping](saml-guide-stack.html#saml-attributes-mapping "Attribute mapping"). 
attributes.groups

     See [Attribute mapping](saml-guide-stack.html#saml-attributes-mapping "Attribute mapping"). 

#### 属性映射

当用户通过您的身份提供程序连接到 Kibana 时，身份提供程序将提供有关该用户的 SAML 断言。断言将包含一个_Authentication Statement_，指示用户已成功向 IdP 进行身份验证，并且一个或多个_Attribute Statements_that将包含用户的 _Attributes_。

这些属性可能包括以下内容：

* 用户的用户名 * 用户的电子邮件地址 * 用户的组或角色

SAML 中的属性使用 URI 命名，例如 'urn：oid：0.9.2342.19200300.100.1.1' 或 'http：//schemas.xmlsoap.org/ws/2005/05/identity/claims/upn'，并具有一个或多个与之关联的值。

这些属性标识符因 IdP 而异，大多数 IdP 都提供自定义 URI 及其关联值的方法。

Elasticsearch 使用这些属性来推断有关已登录用户的信息，它们可用于角色映射(如下)。

为了使这些属性有用，Elasticsearch 和 IdP 需要为属性名称提供一个通用值。这是手动完成的，方法是将 IdP 和 SAML 领域配置为对每个逻辑用户属性使用相同的 URI 名称。

配置这些 SAML 属性的建议步骤如下：

1. 请咨询您的 IdP，了解它可以提供哪些用户属性。这在提供商之间差异很大，但您应该能够从文档或本地管理员获取列表。  2. 通读 Elasticsearch 支持的用户属性列表，并确定哪些对您有用，并且可以由您的 IdP 提供。在 _minimum_ 中，"principal" 属性是必需的。  3. 配置您的 IdP 以将这些属性"释放"给您的 Kibana SAML 服务提供商。此过程因提供程序而异 - 有些提供程序将为此提供用户界面，而其他提供程序可能需要您编辑配置文件。通常，IdP(或您的本地管理员)会就每个属性使用的 URI 提供建议。您可以简单地接受这些建议，因为 Elasticsearch 服务是完全可配置的，不需要使用任何特定的 URI。  4. 在 Elasticsearch 中配置 SAML 领域，以将 Elasticsearch 用户属性(请参阅下面的列表)与您在 IdP 中配置的 URI 相关联。在上面的示例中，我们配置了"主体"和"组"属性。

##### 特殊属性名称

通常，Elasticsearch 期望属性的配置值是一个 URI，例如 'urn：oid：0.9.2342.19200300.100.1.1'，但是可以使用一些其他名称：

`nameid`

     This uses the SAML `NameID` value (all leading and trailing whitespace removed) instead of a SAML attribute. SAML `NameID` elements are an optional, but frequently provided, field within a SAML Assertion that the IdP may use to identify the Subject of that Assertion. In some cases the `NameID` will relate to the user's login identifier (username) within the IdP, but in many cases they will be internally generated identifiers that have no obvious meaning outside of the IdP. 
`nameid:persistent`

     This uses the SAML `NameID` value (all leading and trailing whitespace removed), but only if the NameID format is `urn:oasis:names:tc:SAML:2.0:nameid-format:persistent`. A SAML `NameID` element has an optional `Format` attribute that indicates the semantics of the provided name. It is common for IdPs to be configured with "transient" NameIDs that present a new identifier for each session. Since it is rarely useful to use a transient NameID as part of an attribute mapping, the "nameid:persistent" attribute name can be used as a safety mechanism that will cause an error if you attempt to map from a `NameID` that does not have a persistent value. 

可以将身份提供程序静态配置为释放具有特定格式的"NameID"，也可以将其配置为尝试符合 SP 的要求。SP 使用称为"NameIDPolicy"的元素将其要求声明为身份验证请求的一部分。如果需要，您可以设置名为"nameid_format"的相关设置，以请求 IdP 发布具有特定格式的"NameID"。

_friendlyName_

     A SAML attribute may have a _friendlyName_ in addition to its URI based name. For example the attribute with a name of `urn:oid:0.9.2342.19200300.100.1.1` might also have a friendlyName of `uid`. You may use these friendly names within an attribute mapping, but it is recommended that you use the URI based names, as friendlyNames are neither standardized or mandatory. 

下面的示例将领域配置为对主体使用持久 nameid，并为用户的组使用具有友好名称"roles"的属性。

    
    
    xpack.security.authc.realms.saml.saml1:
      order: 2
      idp.metadata.path: saml/idp-metadata.xml
      idp.entity_id: "https://sso.example.com/"
      sp.entity_id:  "https://kibana.example.com/"
      sp.acs: "https://kibana.example.com/api/security/saml/callback"
      attributes.principal: "nameid:persistent"
      attributes.groups: "roles"
      nameid_format: "urn:oasis:names:tc:SAML:2.0:nameid-format:persistent"

##### 弹性搜索用户属性

Elasticsearch SAML 领域可以配置为将 SAML "属性"映射到经过身份验证的用户的以下属性：

principal

     _(Required)_ This is the _username_ that will be applied to a user that authenticates against this realm. The `principal` appears in places such as the Elasticsearch audit logs. 
groups

    

_(推荐)_ 如果您希望使用 IdP 的组或角色概念作为用户 Elasticsearch 权限的基础，则应使用此属性映射它们。"组"将直接传递到角色映射规则。

一些 IdP 配置为将"组"列表作为逗号分隔的字符串发送，但 Elasticsearch 无法将此字符串解析为组数组。要将此 SAML 属性映射到 Elasticsearch 领域中的"attributes.groups"设置，集群安全管理员可以在配置角色映射时使用通配符。虽然灵活，但通配符不太准确，并且可以匹配不需要的模式。相反，群集安全管理员可以使用正则表达式创建仅与单个组匹配的角色映射规则。例如，以下正则表达式仅在"elasticsearch-admins"组中匹配：

    
    
    /^(.*,)?elasticsearch-admins(,.*)?$/

这些正则表达式基于 Lucene 的正则表达式语法，可以匹配更复杂的模式。所有正则表达式必须以正斜杠开头和结尾。

name

     _(Optional)_ The user's full name. 
mail

     _(Optional)_ The user's email address. 
dn

     _(Optional)_ The user's X.500 _Distinguished Name_. 

##### 从 SAML 属性中提取部分值

在某些情况下，IdP 的属性可能包含比您希望在 Elasticsearch 中使用的更多信息。一个常见的例子是 IdP 专门使用电子邮件地址，但您希望用户的"委托人"使用电子邮件地址的 _local name_部分。例如，如果他们的电子邮件地址 was'james.wong@staff.example.com"，那么你希望他们的校长简单地是"james.wong"。

这可以使用 Elasticsearch 领域中的"attribute_patterns"设置来实现，如下面的领域配置所示：

    
    
    xpack.security.authc.realms.saml.saml1:
      order: 2
      idp.metadata.path: saml/idp-metadata.xml
      idp.entity_id: "https://sso.example.com/"
      sp.entity_id:  "https://kibana.example.com/"
      sp.acs: "https://kibana.example.com/api/security/saml/callback"
      attributes.principal: "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress"
      attribute_patterns.principal: "^([^@]+)@staff\\.example\\.com$"

在这种情况下，用户的"主体"是从电子邮件属性映射的，但在将值分配给用户之前，会将正则表达式应用于该值。如果正则表达式匹配，则第一组的结果用作有效值。如果正则表达式不匹配，则属性映射失败。

在此示例中，电子邮件地址必须属于"staff.example.com"域，然后本地部分("@"之前的任何内容)用作主体。任何尝试使用其他电子邮件域登录的用户都将失败，因为正则表达式将与其电子邮件地址不匹配，因此不会填充其主体属性(这是必需的)。

这些正则表达式中的小错误可能会产生严重的安全后果。例如，如果我们不小心遗漏了上面示例中的尾随"$"，那么我们将匹配域以"staff.example.com"开头的任何电子邮件地址，这将接受诸如"admin@staff.example.com.attacker.net"之类的电子邮件地址。请务必确保正则表达式尽可能精确，以免无意中为用户模拟攻击打开途径。

#### 请求特定的身份验证方法

有时，SAML SP 必须能够对将在 IdP 上进行的身份验证施加特定限制，以便评估它可以在相应的身份验证响应中放置的置信度。这些限制可能与身份验证方法(密码、客户端证书等)、注册期间的用户标识方法以及其他详细信息有关。Elasticsearch实现了SAML 2.0身份验证上下文，可用于SAML 2.0核心规范中定义的此目的。

简而言之，SAML SP 定义了一组身份验证上下文类引用值，这些引用值描述了要对 IdP 施加的限制，并在身份验证请求中发送这些限制。IdP 尝试授予这些限制。如果无法授予它们，则身份验证尝试将失败。如果用户已成功通过身份验证，SAML 响应的身份验证语句将包含已满足限制的指示。

您可以使用 SAML 领域配置中的"req_authn_context_class_ref"选项定义身份验证上下文类引用值。请参阅SAML 领域设置。

Elasticsearch 仅支持身份验证上下文的"精确"比较方法。当 Elasticsearch 收到来自 IdP 的身份验证响应时，它会检查 Authentication Context ClassReference 的值，该值是 SAML 断言的身份验证语句的一部分。如果它与请求的值之一匹配，则认为身份验证成功。否则，身份验证尝试将失败。

#### SAML注销

SAML 协议支持单点注销 (SLO) 的概念。对 SLO 的支持级别因标识提供者而异。您应查阅 IdP 的文档，以确定它提供哪些注销服务。

默认情况下，如果满足以下条件，弹性堆栈将支持 SAML SLO：

* 您的 IdP 元数据指定 IdP 提供 SLO 服务 * 您的 IdP 在它为您的用户发出的 SAML 断言的主题中发布 NameID * 您配置"sp.logout" * 设置"idp.use_single_logout"不是"假"

##### IdP SLOservice

Elasticsearch 从 IdP 的 SAML 元数据中读取的值之一是"<SingleLogoutService>"。为了使单点登录与 Elasticstack 一起使用，Elasticsearch 要求存在并支持绑定 'urn：oasis：names：tc：SAML：2.0：bindings：HTTP-Redirect'。

弹性堆栈会<LogoutRequest><LogoutResponse>根据需要向该服务发送""和"消息。

##### sp.logoutset

Elasticsearch 领域设置"sp.logout"在 Kibana 中指定了一个 URL，IdP 可以向其发送 '' <LogoutRequest><LogoutResponse>和 '' 消息。此服务使用 SAML HTTP-重定向绑定。

Elasticsearch 将处理 '<LogoutRequest>' 消息，并执行全局注销，使与提供的 SAML 会话关联的任何现有 Elasticsearch 安全令牌失效。

如果您没有为 'sp.logout' 配置值，Elasticsearch 将拒绝所有<LogoutRequest>消息。

IdP 通常要求对"注销请求"消息进行签名，因此您可能需要配置签名凭据。

##### idp.use_single_logoutsetting

如果您的 IdP 提供了"<SingleLogoutService>"，但您不希望使用它，您可以在 SAML 领域中配置"idp.use_single_logout：false"，Elasticsearch 将忽略您的 IdP 提供的 SLO 服务。在这种情况下，当用户注销 Kibana 时，其 Elasticsearchsession(安全令牌)将失效，但不会在 IdP 上执行任何注销。

##### 使用 Kibana 无需单次注销

如果您的 IdP 不支持单点注销，或者您选择不使用它，则 Kibana 将仅执行"本地注销"。

这意味着 Kibana 将使用于与 Elasticsearch 通信的会话令牌失效，但无法对身份提供程序会话执行任何类型的失效。在大多数情况下，这意味着 Kibana 用户仍被视为已登录到 IdP。因此，如果用户导航到 Kibana 登录页面，他们将自动重新进行身份验证，并将开始新的 Kibana 会话，而无需输入任何凭据。

此问题的可能解决方案是：

* 请您的 IdP 管理员或供应商提供单点注销服务 * 如果您的 Idp 确实提供单点注销服务，请确保它包含在 IdP 元数据文件中，并且不要将"idp.use_single_logout"设置为"false"。  * 建议用户在退出 Kibana 后关闭浏览器 * 在 SAML 领域启用"force_authn"设置。此设置会导致弹性堆栈在用户每次尝试登录 Kibana 时向 IdP 请求新的身份验证。此设置默认为"false"，因为它可能是更麻烦的用户体验，但它也可以成为阻止用户捎带现有 IdP 会话的有效保护。

#### 加密和签名

弹性堆栈支持生成签名的 SAML 消息(用于身份验证和/或注销)、验证来自 IdP 的签名 SAML 消息(用于身份验证和注销)，并且可以处理加密的内容。

您可以配置 Elasticsearch 进行签名、加密或两者兼而有之，每个密钥都使用相同或单独的密钥。

弹性堆栈使用带有 RSA 私钥的 X.509 证书进行 SAML 加密。这些密钥可以使用任何标准的SSL工具生成，包括"elasticsearch-certutil"工具。

您的 IdP 可能要求弹性堆栈具有用于对 SAML 消息进行签名的加密密钥，并且您在服务提供商配置中(在弹性堆栈 SAML 元数据文件中或在 IdPadministration 界面中手动配置)提供相应的签名证书。虽然大多数 IdP 不希望对身份验证请求进行签名，但注销请求通常需要签名。您的 IdP 将根据已为弹性堆栈服务提供商配置的签名证书验证这些签名。

很少需要加密证书，但 Elastic Stack 在 IdP 或本地策略强制要求使用加密证书的情况下支持加密证书。

##### 生成证书和密钥

Elasticsearch 支持 PEM、PKCS#12 或 JKSs 格式的证书和密钥。某些身份提供程序在支持的格式方面更具限制性，并且会要求您以特定格式的文件形式提供证书。您应查阅 IdP 的文档以确定它们支持的格式。由于 PEM 格式是最常用的支持格式，因此以下示例将以该格式生成证书。

使用"elasticsearch-certutil"工具，您可以使用以下命令生成签名证书：

    
    
    bin/elasticsearch-certutil cert --self-signed --pem --days 1100 --name saml-sign --out saml-sign.zip

这将

* 生成证书和密钥对("证书"子命令) * 以 PEM 格式创建文件("-pem"选项) * 生成有效期为 3 年的证书("-days 1100") * 将证书命名为"SAML 签名"("-名称"选项) * 将证书和密钥保存在"SAML 签名.zip"文件中("-out"选项)

生成的 zip 存档将包含 3 个文件：

* 'saml-sign.crt'，用于签名的公共证书 * 'saml-sign.key'，证书的私钥 * 'ca.crt'，不需要的 CA 证书，可以忽略。

可以使用相同的过程生成加密证书。

##### 配置弹性搜索签名

默认情况下，如果配置了签名密钥，Elasticsearch 将对 _all_ 传出 SAML 消息进行签名。

如果您希望使用**PEM 格式的**密钥和证书进行签名，则应在 SAML 域上配置以下设置：

`signing.certificate`

     The path to the PEM formatted certificate file. e.g. `saml/saml-sign.crt`
`signing.key`

     The path to the PEM formatted key file. e.g. `saml/saml-sign.key`
`signing.secure_key_passphrase`

     The passphrase for the key, if the file is encrypted. This is a [secure setting](secure-settings.html "Secure settings") that must be set with the `elasticsearch-keystore` tool. 

如果要使用 PKCS#12 格式的 ** 文件或 Java 密钥库进行签名，则应在 SAML 域上配置以下设置：

`signing.keystore.path`

     The path to the PKCS#12 or JKS keystore. e.g. `saml/saml-sign.p12`
`signing.keystore.alias`

     The alias of the key within the keystore. e.g. `signing-key`
`signing.keystore.secure_password`

     The passphrase for the keystore, if the file is encrypted. This is a [secure setting](secure-settings.html "Secure settings") that must be set with the `elasticsearch-keystore` tool. 

如果要对一些(但不是全部)传出的 **SAML 消息进行签名，则应在 SAML 域上配置以下设置：

`signing.saml_messages`

     A list of message types to sign. A message type is identified by the _local name_ of the XML element used for the message. Supported values are: `AuthnRequest`, `LogoutRequest` and `LogoutResponse`. 

##### 为加密消息配置 Elasticsearch

Elasticsearch 安全功能支持单个密钥进行消息解密。如果配置了密钥，则 Elasticsearch 会尝试使用它来解密身份验证响应中的"EncryptedAssertion"和"EncryptedAttribute"元素，以及注销请求中的"EncryptedID"元素。

Elasticsearch 拒绝任何包含无法解密的"加密断言"的 SAML 消息。

如果"断言"同时包含加密属性和纯文本属性，则解密加密属性失败不会导致自动拒绝。相反，Elasticsearch处理可用的纯文本属性(以及任何可以解密的"加密属性")。

如果您希望使用 **PEM 格式的 ** 密钥和证书进行 SAML 加密，则应在 SAMLrealm 上配置以下设置：

`encryption.certificate`

     The path to the PEM formatted certificate file. e.g. `saml/saml-crypt.crt`
`encryption.key`

     The path to the PEM formatted key file. e.g. `saml/saml-crypt.key`
`encryption.secure_key_passphrase`

     The passphrase for the key, if the file is encrypted. This is a [secure setting](secure-settings.html "Secure settings") that must be set with the `elasticsearch-keystore` tool. 

如果您希望使用 PKCS#12 格式的 ** 文件或 Java 密钥库**进行 SAML 加密，则应在 SAMLrealm 上配置以下设置：

`encryption.keystore.path`

     The path to the PKCS#12 or JKS keystore. e.g. `saml/saml-crypt.p12`
`encryption.keystore.alias`

     The alias of the key within the keystore. e.g. `encryption-key`
`encryption.keystore.secure_password`

     The passphrase for the keystore, if the file is encrypted. This is a [secure setting](secure-settings.html "Secure settings") that must be set with the `elasticsearch-keystore` tool. 

### 生成 SP元数据

某些身份提供程序支持从服务提供商导入元数据文件。这将自动配置 IdP 和 SP 之间的许多集成选项。

Elastic Stack 支持使用 'bin/elasticsearch-saml-metadata' 命令或 SAML 服务提供商元数据 API 生成此类元数据文件。

您可以通过向 Elasticsearch 发出 API 请求来生成 SAML 元数据，并使用 'jq' 等工具将其存储为 XML 文件。例如，以下命令为 SAML 领域"realm1"生成元数据，并将其保存到"元数据.xml"文件中：

    
    
    curl -u user_name:password  -X GET http://localhost:9200/_security/saml/metadata/saml1 -H 'Content-Type: application/json' | jq -r '.[]' > metadata.xml

### 配置角色映射

当用户使用 SAML 进行身份验证时，他们会被识别到 ElasticStack，但这不会自动授予他们执行任何操作或访问任何数据的访问权限。

您的 SAML 用户在分配角色之前无法执行任何操作。这可以通过添加角色映射 API 或授权域来实现。

不能使用角色映射文件向通过 SAML 进行身份验证的用户授予角色。

下面是一个简单的角色映射示例，该映射将"example_role"角色授予针对"saml1"域进行身份验证的任何用户：

    
    
    PUT /_security/role_mapping/saml-example
    {
      "roles": [ "example_role" ], __"enabled": true,
      "rules": {
        "field": { "realm.name": "saml1" }
      }
    }

__

|

"example_role"角色不是内置的 Elasticsearch 角色。此示例假定您已创建自己的自定义角色，并具有对数据流、索引和 Kibana 功能的适当访问权限。   ---|--- 通过领域配置映射的属性用于处理角色映射规则，这些规则确定授予用户哪些角色。

提供给角色映射的用户字段派生自 SAML 属性，如下所示：

* "用户名"："主体"属性 * "dn"："dn"属性 * "组"："组"属性 * "元数据"：请参阅用户元数据

有关详细信息，请参阅将用户和组映射到角色和角色映射。

如果您的 IdP 能够向服务提供商提供组或角色，则应将此 SAML 属性映射到 Elasticsearch 领域中的"attributes.groups"设置，然后在角色映射中使用它，如下例所示。

此映射将 Elasticsearch "finance_data"角色授予通过"saml1"领域与"财务团队"组进行身份验证的任何用户。

    
    
    PUT /_security/role_mapping/saml-finance
    {
      "roles": [ "finance_data" ],
      "enabled": true,
      "rules": { "all": [
            { "field": { "realm.name": "saml1" } },
            { "field": { "groups": "finance-team" } } __] }
    }

__

|

"groups"属性支持使用通配符("*")。有关详细信息，请参阅创建或更新角色映射 API。   ---|--- 如果您的用户也存在于可以被 Elasticsearch 直接访问的存储库(例如 LDAP 目录)中，那么您可以使用授权领域而不是角色映射。

在这种情况下，您可以执行以下步骤：1\。在您的 SAML 领域中，通过配置"属性.principal"设置，分配了一个 SAML 属性来充当查找用户标识。2\.创建一个可以从本地存储库(例如"ldap"域)中查找用户的新领域 3\.在 SAML 领域中，将"authorization_realms"设置为您在步骤 2 中创建的领域的名称。

### 用户元数据

默认情况下，通过 SAML 进行身份验证的用户将具有一些额外的元数据字段。

* "saml_nameid"将设置为 SAML 身份验证响应中"NameID"元素的值 * "saml_nameid_format"将设置为 NameID 的"format"属性的完整 URI * 身份验证响应中提供的每个 SAML 属性(无论它是否映射到 Elasticsearch 用户属性)都将添加为元数据字段"saml(name)"，其中"name"是属性的完整 URI 名称。例如'saml(urn：oid：0.9.2342.19200300.100.1.3)'。  * 对于每个具有 _friendlyName_ 的 SAML 属性，也将添加为元数据字段"saml_friendlyName"，其中"name"是属性的完整 URI 名称。例如"saml_mail"。

可以通过在 saml 领域中的 asa 设置中添加"populate_user_metadata：false"来禁用此行为。

### 配置木bana

除了标准的 Kibana 安全配置外，Kibana 中的 SAML 身份验证还需要少量其他设置。Kibanasecurity 文档提供了有关您可以应用的可用配置选项的详细信息。

特别是，由于您的 Elasticsearch 节点已配置为在 HTTP 接口上使用 TLSa，因此您必须将 Kibana 配置为使用 'https' URL 连接到 Elasticsearch，并且您可能需要配置"elasticsearch.ssl.certificateAuthority" 以信任 Elasticsearch 已配置为使用的证书。

Kibana 中的 SAML 身份验证受"kibana.yml"中的以下超时设置的约束：

* 'xpack.security.session.idleTimeout' * 'xpack.security.session.lifespan'

您可能需要根据安全要求调整这些超时。

SAML 支持所需的三个附加设置如下所示：

    
    
    xpack.security.authc.providers:
      saml.saml1:
        order: 0
        realm: "saml1"

上面示例中使用的配置值为：

`xpack.security.authc.providers`

     Add `saml` provider to instruct Kibana to use SAML SSO as the authentication method. 
`xpack.security.authc.providers.saml.<provider-name>.realm`

     Set this to the name of the SAML realm that you have used in your [Elasticsearch realm configuration](saml-guide-stack.html#saml-create-realm "Create a SAML realm"), for instance: `saml1`

#### 在 Kibana 中支持 SAML 和基本身份验证

Kibana 中的 SAML 支持旨在成为该 Kibana 实例用户的主要(或唯一)身份验证方法。但是，可以通过设置"xpack.security.authc.providers"在单个 Kibana 实例中同时支持 SAML 和基本身份验证，如下例所示：

    
    
    xpack.security.authc.providers:
      saml.saml1:
        order: 0
        realm: "saml1"
      basic.basic1:
        order: 1

如果以这种方式配置 Kibana，则会在登录选择器 UI 中向用户显示一个选项。他们使用 SAML 登录，或者提供用户名和密码，并依赖于 Elasticsearch 中的其他安全域之一。只有拥有已配置的 Elasticsearchauthentication 域的用户名和密码的用户才能通过 Kibana 登录表单登录。

或者，启用"基本"身份验证提供程序后，您可以在 Kibana 前面放置一个反向代理，并将其配置为为每个请求发送基本身份验证标头("授权：基本 ....")。如果此标头存在且有效，Kibana 将不会启动 SAML 身份验证过程。

#### 操作多个 Kibana实例

如果您希望有多个 Kibana 实例针对同一个 Elasticsearch 集群进行身份验证，则为每个配置为 SAML 身份验证的 Kibana 实例都需要自己的 SAML 领域。

每个 SAML 领域都必须有自己唯一的实体 ID ("sp.entity_id")，并_Assertion使用者Service_ ("sp.acs") 中播出。每个 Kibana 实例都将通过查找匹配的"sp.acs"值映射到正确的领域。

这些领域可以使用相同的身份提供程序，但不是必需的。

以下示例显示 3 个不同的 Kibana 实例，其中 2 个使用相同的内部 IdP，另一个使用不同的 IdP。

    
    
    xpack.security.authc.realms.saml.saml_finance:
      order: 2
      idp.metadata.path: saml/idp-metadata.xml
      idp.entity_id: "https://sso.example.com/"
      sp.entity_id:  "https://kibana.finance.example.com/"
      sp.acs: "https://kibana.finance.example.com/api/security/saml/callback"
      sp.logout: "https://kibana.finance.example.com/logout"
      attributes.principal: "urn:oid:0.9.2342.19200300.100.1.1"
      attributes.groups: "urn:oid:1.3.6.1.4.1.5923.1.5.1."
    xpack.security.authc.realms.saml.saml_sales:
      order: 3
      idp.metadata.path: saml/idp-metadata.xml
      idp.entity_id: "https://sso.example.com/"
      sp.entity_id:  "https://kibana.sales.example.com/"
      sp.acs: "https://kibana.sales.example.com/api/security/saml/callback"
      sp.logout: "https://kibana.sales.example.com/logout"
      attributes.principal: "urn:oid:0.9.2342.19200300.100.1.1"
      attributes.groups: "urn:oid:1.3.6.1.4.1.5923.1.5.1."
    xpack.security.authc.realms.saml.saml_eng:
      order: 4
      idp.metadata.path: saml/idp-external.xml
      idp.entity_id: "https://engineering.sso.example.net/"
      sp.entity_id:  "https://kibana.engineering.example.com/"
      sp.acs: "https://kibana.engineering.example.com/api/security/saml/callback"
      sp.logout: "https://kibana.engineering.example.com/logout"
      attributes.principal: "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/upn"

可以有一个或多个使用 SAML 的 Kibana 实例，而其他实例则针对另一种领域类型(例如本机或 LDAP)使用基本身份验证。

### SAML 领域配置疑难解答

SAML 2.0 规范为标准的实施者提供了许多选项和灵活性，这反过来又增加了服务提供商(弹性堆栈)和身份提供商上可用的配置选项的复杂性和数量。此外，不同的安全域具有不同的安全要求，需要特定的配置才能满足。我们已经有意识地努力使用合理的默认值和上面的详细文档来掩盖这种复杂性，但如果您在配置 SAML 领域时遇到问题，您可以查看我们的 SAML 故障排除文档，其中包含针对常见问题的建议和解决方案。

### 没有 Kibana 的 SAML

Elasticsearch 中的 SAML 领域旨在允许用户对 ToKibana 进行身份验证，因此，上述指南的大部分部分都假设使用了 Kibana。本节介绍自定义 Web 应用程序如何使用相关的 SAML REST API 来验证用户使用 SAML 进行 Elasticsearch 身份验证。

本节假定读者熟悉 SAML 2.0 标准，更具体地说，熟悉 SAML 2.0 Web 浏览器单一登录配置文件。

OpenID Connect 和 SAML 等单点登录领域使用 Elasticsearch 中的 TokenService，原则上将 SAML 或 OpenID ConnectAuthentication 响应交换为 Elasticsearch 访问令牌和刷新令牌。访问令牌用作后续调用 Elasticsearch 的凭据。刷新令牌使用户能够在当前访问令牌过期后获取新的 Elasticsearch 访问令牌。

#### SAMLrealm

您必须在 Elasticsearch 中创建 SAML 领域并对其进行相应的配置。请参见为 SAML 身份验证配置 Elasticsearch

#### 用于访问 API 的服务帐户用户

在设计该领域时，假设需要一个特权实体充当身份验证代理。在这种情况下，自定义 Web 应用程序是处理最终用户身份验证的身份验证代理(更准确地说，将身份验证"委派"给 SAML 身份提供程序)。与 SAML 相关的 API 需要身份验证和经过身份验证的用户所需的授权级别。因此，您必须创建一个服务帐户用户，并为其分配一个角色，以授予其"manage_saml"群集权限。身份验证发生后，必须使用"manage_token"群集特权，以便服务帐户用户可以保持访问权限，以便代表经过身份验证的用户刷新访问令牌或随后将其注销。

    
    
    POST /_security/role/saml-service-role
    {
      "cluster" : ["manage_saml", "manage_token"]
    }
    
    
    POST /_security/user/saml-service-user
    {
      "password" : "<somePasswordHere>",
      "roles"    : ["saml-service-role"]
    }

#### 处理 SP 启动的身份验证流

在高级别上，自定义 Web 应用程序需要执行以下步骤，以便使用 SAML 针对 stElasticsearch 对用户进行身份验证：

1. 向"_security/saml/prepare"发出 HTTP POST 请求，以"saml-service-user"用户的身份进行身份验证。在 Elasticsearch 配置中使用 SAML 领域的名称，或在请求正文中使用断言使用者服务 URL 的值。有关更多详细信息，请参阅 SAML 准备身份验证 API。           POST /_security/saml/prepare { "realm" ： "saml1" }

2. 处理来自"/_security/saml/prepare"的响应。来自 Elasticsearch 的响应将包含 3 个参数："重定向"、"领域"和"id"。自定义 Web 应用程序需要在用户的会话中存储"id"的值(客户端在 Cookie 中，如果会话信息以这种方式持久化，则存储在服务器端)。它还必须将用户的浏览器重定向到"重定向"参数中返回的 URL。不应忽略"id"值，因为它在 SAML 中用作随机数，以减轻重放攻击。  3. 处理来自 SAML IdP 的后续响应。用户成功通过身份提供程序的身份验证后，他们将被重定向回断言使用者服务 URL。此"sp.acs"需要定义为自定义 Web 应用程序处理的 URL。当它收到这个HTTP POST请求时，自定义Web应用程序必须解析它，并向"_security/saml/authenticate"API发出HTTP POST请求。它必须以"SAML 服务用户"用户的身份进行身份验证，并传递作为请求正文发送的 Base64 编码的 SAML 响应。它还必须传递之前保存在用户会话中的"id"值。

有关更多详细信息，请参阅 SAML 身份验证 API。

    
        POST /_security/saml/authenticate
    {
      "content" : "PHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMD.....",
      "ids" : ["4fee3b046395c4e751011e97f8900b5273d56685"]
    }

Elasticsearch 将对此进行验证，如果一切正确，将使用访问令牌进行响应，该令牌可用作后续请求的"持有者"令牌。它还提供了一个刷新令牌，该令牌稍后可用于刷新给定访问令牌，如获取令牌 API 中所述。

4. 对调用"/_security/saml/authenticate"的响应将仅包含经过身份验证的用户的用户名。如果需要获取该用户的 SAML 响应中包含的 SAML 属性的值，可以使用访问令牌作为"持有者"令牌调用身份验证 API"/_security/_authenticate/"，SAML 属性值将作为用户元数据的一部分包含在响应中。

#### 处理 IdP 启动的身份验证流

Elasticsearch 还可以处理 SAML 2 Web 浏览器 SSO 配置文件的 IdP 发起的单点登录流程。在这种情况下，身份验证从来自 SAML 身份提供程序的未经请求的身份验证响应开始。与 SP 启动的 SSO 的不同之处在于，Web 应用程序需要处理对"sp.acs"的请求，这些请求不会作为对先前重定向的响应。因此，它不会已经为用户提供会话，并且不会有任何存储的"id"参数值。在这种情况下，对"_security/saml/authenticate"API 的请求将如下所示：

    
    
    POST /_security/saml/authenticate
    {
      "content" : "PHNhbWxwOlJlc3BvbnNlIHhtbG5zOnNhbWxwPSJ1cm46b2FzaXM6bmFtZXM6dGM6U0FNTDoyLjA6cHJvdG9jb2wiIHhtbG5zOnNhbWw9InVybjpvYXNpczpuYW1lczp0YzpTQU1MOjIuMD.....",
      "ids" : []
    }

#### 处理日志流出

1. 在某些时候，如有必要，自定义 Web 应用程序可以使用 SAML 注销 API 并将访问令牌和刷新令牌作为参数传递，从而注销用户。例如： POST /_security/saml/logout { "token" ： "46ToAxZVaXVVZTVKOVF5YU04ZFJVUDVSZlV3"， "refresh_token"： "mJdXLtmvTUSpoLwMvdBt_w" }

如果相应地配置了 SAML 领域，并且 IdP 支持它(请参阅 SAML注销)，则此请求将触发 SAML SP 启动的单点注销。在这种情况下，响应将包含一个"重定向"参数，指示用户需要重定向到 IdP 的位置才能完成注销。

2. 或者，IdP 可能会在某个时候启动单点注销流程。为了处理此问题，注销 URL("sp.logout")需要由自定义 Web 应用程序处理。用户将被重定向到的URL的查询部分将包含SAML注销请求，并且此查询部分需要使用SAML无效API POST /_security/saml/invalid{"query"中继到Elasticsearch： "SAMLRequest=nZFda4MwFIb%2FiuS%2BmviRpqFaClKQdbvo2g12M2KMraCJ9cRR9utnW4Wyi13sMie873MeznJ1aWrnS3VQGR0j4mLkKC1NUeljjA77zYyhVbIE0dR%2By7fmaHq7U%2BdegXWGpAZ%2B%2F4pR32luBFTAtWgUcCv56%2Fp5y30X87Yz1khTIycdgpUW9kY7WdsC9zxoXTvMvWuVV v98YyMnSGH2SYE5pwALBIr9QKiwDGpW0oGVUznGeMyJZKFkQ4jBf5HnhUymjIhzCAL3KNFihbYx8TBYzzGaY7EnIyZwHzCWMfiDnbRIftkSjJr%2BFu0e9v%2B0EgOquRiiZjKpiVFp6j50T4WXoyNJ%2FEWC9fdqc1t%2F1%2B2F3aUpjzhPiXpqMz1%2FHSn4A&SigAlg=http%3A%2F%2Fwww.w3.org%2F2001%2F04%2Fxmldsig-more%23rsa-sha256&Signature=MsAYz2NFdovMG2mXf6TSpu5vlQQyEJAg%2B4KCwBqJTmrb3yGXKUtIgvjqf88eCAK32v3eN8vupjPC8LglYmke1ZnjK0%2FKxzkvSjTVA7mMQe2AQdKbkyC038zzRq%2FYHcjFDE%2Bz0qISwSHZY2NyLePmwU7SexEXnIz37jKC6NMEhus%3D"， "realm" ： "saml1" }

然后，自定义 Web 应用程序还需要处理响应，其中包括一个"重定向"参数，该参数在 IdP 中包含一个包含 SAML 注销响应的 URL。应用程序应将用户重定向到那里以完成注销。

对于 SP 发起的单点注销，IdP 可能会发回一个注销响应，Elasticsearch 可以使用 SAML 完整注销 API 验证该响应。

[« Controlling the user cache](controlling-user-cache.md) [Configuring
single sign-on to the Elastic Stack using OpenID Connect »](oidc-guide.md)
