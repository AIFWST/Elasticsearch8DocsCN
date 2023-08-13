

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« Kerberos authentication](kerberos-realm.md) [Integrating with other
authentication systems »](custom-realms.md)

## 智威通身份验证

Elasticsearch 可以配置为信任从外部服务颁发的 JSON Web 令牌 (JWT) 作为用于身份验证的持有者令牌。

当使用 JWT 领域对 Elasticsearch 进行身份验证时，需要区分连接到 Elasticsearch 的 _client_ 和请求应代表其运行的_user_on。JWT 对用户进行身份验证，单独的凭据对客户端进行身份验证。

JWT 领域支持两种令牌类型："id_token"(默认值)和"access_token"。它们分别适用于以下两种方案：

1. "id_token"-应用程序使用身份验证流程(例如OpenID Connect(OIDC))对用户进行身份验证和识别，然后使用符合OIDC ID令牌规范的JSON Web令牌(JWT)代表经过身份验证的用户访问Elasticsearch。  2. 'access_token' \- 应用程序使用自己的身份(编码为 JWT)访问 Elasticsearch，例如，应用程序使用 OAuth2 客户端凭证流向中央身份平台验证自身，然后使用生成的基于 JWT 的访问令牌连接到 Elasticsearch。

单个 JWT 领域只能使用单个令牌类型。要处理这两种令牌类型，您必须至少配置两个 JWT 领域。您应该根据用例仔细选择令牌类型，因为它会影响执行验证的方式。

JWT 领域根据其配置的令牌类型验证传入的 JWT。两种类型的 JSON Web 令牌 (JWT) 必须包含以下 5 条信息。虽然基于 OIDC 规范的 ID 令牌对哪些声明应提供这些信息有严格的规则，但访问令牌允许配置某些声明。

|

**索赔** ---|--- **信息**

|

ID 令牌

|

访问令牌颁发者

|

`iss`

|

"ISS"主题

|

`sub`

|

默认为"sub"，但如果"sub"不存在，则可以回退到另一个版权主张 受众群体

|

`aud`

|

默认为"aud"，但如果"aud"不存在，则可以回退到另一个声明 发行时间

|

`iat`

|

"iat"到期时间

|

`exp`

|

"exp" 此外，Elasticsearch 还会验证 IDTokens 的"nbf"和"auth_time"声明(如果存在这些声明)。但是，对于访问令牌，这些声明将被忽略。

总体而言，访问令牌类型具有更宽松的验证规则，适用于更通用的 JWT，包括自签名 JWT。

来自 OIDC 工作流的 ### ID 令牌

Elasticsearch 中的 JWT 身份验证源自 OIDC 用户工作流，其中 OIDC 提供商 (OP) 可以颁发不同的令牌，包括 ID Tokens.ID 来自 OIDC 提供商的令牌是定义完善的 JSON Web 令牌 (JWT)，应始终与"id_token"令牌类型的 JWT 领域兼容。ID 令牌的主题声明表示最终用户。这意味着 IDtoken 通常具有许多允许的主题。因此，"id_token"令牌类型的 JWT 领域不强制要求进行"allowed_subjects"验证。

由于 JWT 是在 Elasticsearch 外部获取的，因此您可以定义自定义工作流，而不是使用 OIDC 工作流。但是，JWT 格式仍必须是 JSON Web 签名 (JWS)。JWS 标头和 JWS 签名使用 OIDC ID 令牌验证规则进行验证。

Elasticsearch 支持单独的 OpenID Connect 领域。对于Elasticsearch可以充当OIDC RP的任何用例，它都是首选。OIDC 领域是在 Kibana 中启用 OIDC 身份验证的唯一受支持的方法。

使用 JWT 领域进行身份验证的用户可以选择使用"run_as"功能模拟其他用户。另请参阅将"run_as"权限应用于 JWT 领域用户。

### 访问令牌

获取访问令牌的常用方法是使用 OAuth2 客户端凭据流。此流的典型用法是让应用程序获取自身的凭据。这是"access_token"令牌类型设计的用例。此应用程序还可能为其最终用户获取 ID 令牌。为了防止最终用户 ID 令牌用于向为应用程序配置的 JWT 领域进行身份验证，当 JWT 领域具有令牌类型"access_token"时，我们强制要求"allowed_subjects"验证。

并非每个访问令牌都格式化为 JSON Web 令牌 (JWT)。要使其与 JWT 领域兼容，它必须至少使用 JWT 格式并满足上表中的相关要求。

### 配置 Elasticsearch 以使用 JWTrealm

要使用 JWT 身份验证，请在 'elasticsearch.yml' 文件中创建领域，以在 Elasticsearch 身份验证链中对其进行配置。

JWT 领域有一些必需的设置，以及 JWT 领域设置中描述的可选设置。

默认情况下，为 JWT 领域启用客户端身份验证。禁用客户端身份验证是可能的，但强烈建议不要这样做。

1. 将您的 JWT 领域添加到 'elasticsearch.yml' 文件中。以下示例包括最常见的设置，这些设置并非适用于所有用例： xpack.security.authc.realms.jwt.jwt1： 顺序： 3 token_type： id_token client_authentication.type： shared_secret allowed_issuer： "https://issuer.example.com/jwt/" allowed_audiences： [ "8fb85eba-979c-496c-8ae2-a57fde3f12d0" ] allowed_signature_algorithms： [RS256，HS256] pkc_jwkset_path： jwt/jwkset.json claims.principal： sub

`order`

     Specifies a realm `order` of `3`, which indicates the order in which the configured realm is checked when authenticating a user. Realms are consulted in ascending order, where the realm with the lowest order value is consulted first. 
`token_type`

     Instructs the realm to treat and validate incoming JWTs as ID Tokens (`id_token`). 
`client_authentication.type`

     Specifies the client authentication type as `shared_secret`, which means that the client is authenticated using an HTTP request header that must match a pre-configured secret value. The client must provide this shared secret with every request in the `ES-Client-Authentication` header. The header value must be a case-sensitive match to the realm's `client_authentication.shared_secret`. 
`allowed_issuer`

     Sets a verifiable identifier for your JWT issuer. This value is typically a URL, UUID, or some other case-sensitive string value. 
`allowed_audiences`

     Specifies a list of JWT audiences that the realm will allow. These values are typically URLs, UUIDs, or other case-sensitive string values. 
`allowed_signature_algorithms`

     Indicates that Elasticsearch should use the `RS256` or `HS256` signature algorithms to verify the signature of the JWT from the JWT issuer. 
`pkc_jwkset_path`

     The file path to a JSON Web Key Set (JWKS) containing the public key material that the JWT realm uses to verify JWT signatures. If a path is provided, then it is resolved relative to the Elasticsearch configuration directory. In Elastic Cloud, use an absolute path starting with `/app/config/`. 
`claims.principal`

     The name of the JWT claim that contains the user's principal (username). 

以下是配置用于处理访问令牌的 JWT 域的示例代码段：

    
        xpack.security.authc.realms.jwt.jwt2:
      order: 4
      token_type: access_token
      client_authentication.type: shared_secret
      allowed_issuer: "https://issuer.example.com/jwt/"
      allowed_subjects: [ "123456-compute@developer.example.com" ]
      allowed_audiences: [ "elasticsearch" ]
      required_claims:
        token_use: access
        version: ["1.0", "2.0"]
      allowed_signature_algorithms: [RS256,HS256]
      pkc_jwkset_path: "https://idp-42.example.com/.well-known/configuration"
      fallback_claims.sub: client_id
      fallback_claims.aud: scope
      claims.principal: sub

`token_type`

     Instructs the realm to treat and validate incoming JWTs as access tokens (`access_token`). 
`allowed_subjects`

     Specifies a list of JWT subjects that the realm will allow. These values are typically URLs, UUIDs, or other case-sensitive string values. 

当"token_type"为"access_token"时，此设置是必需的。

`required_claims`

     Specifies a list of key/value pairs for additional verifications to be performed against a JWT. The values are either a string or an array of strings. 
`fallback_claims.sub`

     The name of the JWT claim to extract the subject information if the `sub` claim does not exist. This setting is only available when `token_type` is `access_token`. The fallback is applied everywhere the `sub` claim is used. In the above snippet, it means the `claims.principal` will also fallback to `client_id` if `sub` does not exist. 
`fallback_claims.aud`

     The name of the JWT claim to extract the audiences information if the `aud` claim does not exist. This setting is only available when `token_type` is `access_token`. The fallback is applied everywhere the `aud` claim is used. 

2. 定义设置后，使用"弹性搜索密钥库"工具将安全设置的值存储在 Elasticsearch 密钥库中。

    1. Store the `shared_secret` value for `client_authentication.type`:
        
                bin/elasticsearch-keystore add xpack.security.authc.realms.jwt.jwt1.client_authentication.shared_secret

    2. Store the HMAC keys for `allowed_signature_algorithms`, which use the HMAC SHA-256 algorithm `HS256` in the example:
        
                bin/elasticsearch-keystore add-file xpack.security.authc.realms.jwt.jwt1.hmac_jwkset <path> __

__

|

JWKS 的路径，它是一组 JSON 编码的密钥的资源。将内容加载到 Elasticsearchkey 存储中后，可以删除该文件。   ---|--- 最好使用 JWKS。但是，您可以使用以下命令以字符串格式添加 HMAC 密钥。此格式与 HMAC UTF-8 密钥兼容，但仅支持没有属性的单个密钥。您只能同时使用一种 HMAC 格式("hmac_jwkset"或"hmac_key")。

        
                bin/elasticsearch-keystore add xpack.security.authc.realms.jwt.jwt1.hmac_key

### JWT 编码和验证

JWT 可以解析为三个部分：

Header

     Provides information about how to validate the token. 
Claims

     Contains data about the calling user or application. 
Signature

     The data that's used to validate the token. 
    
    
    Header: {"typ":"JWT","alg":"HS256"}
    Claims: {"aud":"aud8","sub":"security_test_user","iss":"iss8","exp":4070908800,"iat":946684800}
    Signature: UnnFmsoFKfNmKMsVoDQmKI_3-j95PCaKdgqqau3jPMY

此示例说明了 JWT 的部分解码。有效期为 2000 年至 2099 年(含)，由签发时间 ("iat") 和到期时间 ("exp") 定义。JWT的有效期通常短于100年，例如1-2小时或1-7天，而不是整个人类生命。

此示例中的签名是确定性的，因为标头、声明和 HMAC 密钥是固定的。JWT 通常具有"随机数"声明，以使签名不确定。支持的 JWT 编码是 JSON Web 签名 (JWS)，JWS "标头"和"签名"使用 OpenID Connect ID 令牌验证规则进行验证。某些验证可以通过 JWT 领域设置进行自定义。

#### 标头声明

标头声明指示令牌类型和用于对令牌进行签名的算法。

`alg`

     (Required, String) Indicates the algorithm that was used to sign the token, such as `HS256`. The algorithm must be in the realm's allow list. 
`typ`

     (Optional, String) Indicates the token type, which must be `JWT`. 

#### 有效负载声明

令牌包含多个声明，这些声明提供有关颁发令牌的用户和令牌本身的信息。根据令牌类型，可以选择通过不同的声明来标识这些信息。

##### JWT 有效负载声明

以下声明由 OIDC ID 令牌规则的子集进行验证。

Elasticsearch 不会验证"nonce"声明，但自定义 JWT 颁发者可以添加随机的"nonce"声明以将熵引入签名。

您可以通过设置"allowed_clock_skew"来放宽对任何基于时间的声明的验证。此值设置在验证 JWT 之前允许的最大时钟偏差，包括其身份验证时间 ("auth_time")、创建 ("iat")、不之前 ("nbf") 和过期时间 ("exp")。

`iss`

     (Required, String) Denotes the issuer that created the ID token. The value must be an exact, case-sensitive match to the value in the `allowed_issuer` setting. 
`sub`

     (Required*, String) Indicates the subject that the ID token is created for. If the JWT realm is of the `id_token` type, this claim is mandatory. A JWT realm of the `id_token` type by defaults accepts all subjects. A JWT realm of the access_token type must specify the `allowed_subjects` setting and the subject value must be an exact, case-sensitive match to any of the CSV values in the allowed_subjects setting. A JWT realm of the access_token type can specify a fallback claim that will be used in place where the `sub` claim does not exist. 
`aud`

     (Required*, String) Indicates the audiences that the ID token is for, expressed as a comma-separated value (CSV). One of the values must be an exact, case-sensitive match to any of the CSV values in the `allowed_audiences` setting. If the JWT realm is of the `id_token` type, this claim is mandatory. A JWT realm of the `access_token` type can specify a fallback claim that will be used in place where the `aud` claim does not exist. 
`exp`

     (Required, integer) Expiration time for the ID token, expressed in UTC seconds since epoch. 
`iat`

     (Required, integer) Time that the ID token was issued, expressed in UTC seconds since epoch. 
`nbf`

     (Optional, integer) Indicates the time before which the JWT must not be accepted, expressed as UTC seconds since epoch. This claim is optional. If it exists, a JWT realm of `id_token` type will verify it, while a JWT realm of `access_token` will just ignore it. 
`auth_time`

     (Optional, integer) Time when the user authenticated to the JWT issuer, expressed as UTC seconds since epoch. This claim is optional. If it exists, a JWT realm of `id_token` type will verify it, while a JWT realm of `access_token` will just ignore it. 

##### 用于使用 JWTclaim 的弹性搜索设置

Elasticsearch 对以下设置使用 JWT 声明。

`principal`

     (Required, String) Contains the user's principal (username). The value is configurable using the realm setting `claims.principal`. You can configure an optional regular expression using the `claim_patterns.principal` to extract a substring. 
`groups`

     (Optional, JSON array) Contains the user's group membership. The value is configurable using the realm setting `claims.groups`. You can configure an optional regular expression using the realm setting `claim_patterns.groups` to extract a substring value. 
`name`

     (Optional, String) Contains a human-readable identifier that identifies the subject of the token. The value is configurable using the realm setting `claims.name`. You can configure an optional regular expression using the realm setting `claim_patterns.name` to extract a substring value. 
`mail`

     (Optional, String) Contains the e-mail address to associate with the user. The value is configurable using the realm setting `claims.mail`. You can configure an optional regular expression using the realm setting `claim_patterns.mail` to extract a substring value. 
`dn`

     (Optional, String) Contains the user's Distinguished Name (DN), which uniquely identifies a user or group. The value is configurable using the realm setting `claims.dn`. You can configure an optional regular expression using the realm setting `claim_patterns.dn` to extract a substring value. 

### 智威汤逊领域授权

JWT 领域支持使用创建或更新角色映射 API 进行授权，或者将授权委派给另一个领域。不能同时使用这些方法，因此请选择最适合您的环境的方法。

不能使用"role_mapping.yml"文件映射 JWT 领域中的角色。

#### 使用角色映射API 进行授权

可以使用创建或更新角色映射 API 来定义角色映射，这些映射确定应根据用户名、组或其他元数据为每个用户分配哪些角色。

    
    
    PUT /_security/role_mapping/jwt1_users?refresh=true
    {
      "roles" : [ "user" ],
      "rules" : { "all" : [
          { "field": { "realm.name": "jwt1" } },
          { "field": { "username": "principalname1" } },
          { "field": { "dn": "CN=Principal Name 1,DC=example.com" } },
          { "field": { "groups": "group1" } },
          { "field": { "metadata.jwt_claim_other": "other1" } }
      ] },
      "enabled": true
    }

如果在 JWT 领域中使用此 API，则以下声明可用于角色映射：

`principal`

     (Required, String) Principal claim that is used as the Elasticsearch user's username. 
`dn`

     (Optional, String) Distinguished Name (DN) that is used as the Elasticsearch user's DN. 
`groups`

     (Optional, String) Comma-separated value (CSV) list that is used as the Elasticsearch user's list of groups. 
`metadata`

     (Optional, object) Additional metadata about the user, such as strings, integers, boolean values, and collections that are used as the Elasticsearch user's metadata. These values are key value pairs formatted as `metadata.jwt_claim_<key>` = `<value>`. 

#### 将 JWT 授权委托给另一个领域

如果将授权委托给 JWTrealm 中的其他领域，则只有"主体"声明可用于角色查找。将角色的分配和查找从 JWTrealm 委托给另一个领域时，"dn"、"组"、"邮件"、"元数据"和"名称"的声明不会用于 Elasticsearch 用户的值。只有 JWT"主体"声明传递到委派的授权领域。委托授权的领域 - 而不是 JWT 领域 - 负责填充所有 Elasticsearch 用户的值。

以下示例显示了如何在 'elasticsearch.yml' 文件中定义委派授权到来自 JWT 领域的多个其他领域。名为"jwt2"的 JWTrealm 正在将授权委托给多个领域：

    
    
    xpack.security.authc.realms.jwt.jwt2.authorization_realms: file1,native1,ldap1,ad1

然后，您可以使用创建或更新角色映射 API 将角色映射到授权领域。以下示例映射"principalname1"JWT 主体的"native1"领域中的角色。

    
    
    PUT /_security/role_mapping/native1_users?refresh=true
    {
      "roles" : [ "user" ],
      "rules" : { "all" : [
          { "field": { "realm.name": "native1" } },
          { "field": { "username": "principalname1" } }
      ] },
      "enabled": true
    }

如果领域 'jwt2' 成功地使用委托人 'principalname1' 的 JWT 对客户端进行身份验证，并将授权委托给列出的领域之一(例如 'native1')，那么该领域可以查找 Elasticsearch 用户的值。通过此定义的角色映射，领域还可以查找链接到领域"native1"的角色映射规则。

#### 将"run_as"权限应用于 JWT 领域用户

Elasticsearch 可以通过角色映射或委托授权来检索 JWT 用户的角色。无论选择哪个选项，您都可以将"run_as"权限应用于角色，以便用户可以提交经过身份验证的请求以"以其他用户身份运行"。要以其他用户身份提交请求，请在请求中包含"es-security-runas-user"标头。请求就像是从该用户发出一样运行，Elasticsearch 使用它们的角色。

例如，假设有一个用户名为"user123_runas"的用户。以下请求创建一个名为"jwt_role1"的用户角色，该角色指定具有"user123_runas"用户名的"run_as"用户。任何具有"jwt_role1"角色的用户都可以作为指定的"run_as"用户发出请求。

    
    
    POST /_security/role/jwt_role1?refresh=true
    {
      "cluster": ["manage"],
      "indices": [ { "names": [ "*" ], "privileges": ["read"] } ],
      "run_as": [ "user123_runas" ],
      "metadata" : { "version" : 1 }
    }

然后，您可以将该角色映射到特定领域中的用户。以下请求将"jwt_role1"角色映射到"jwt2"JWT 领域中用户名为"user2"的用户。这意味着 Elasticsearch 将使用 'jwt2' 领域来验证名为 'user2' 的用户。由于"user2"具有包含"run_as"权限的角色("jwt_role1"角色)，因此Elasticsearch检索"user123_runas"用户的角色映射，并使用该用户的角色提交请求。

    
    
    POST /_security/role_mapping/jwt_user1?refresh=true
    {
      "roles": [ "jwt_role1"],
      "rules" : { "all" : [
          { "field": { "realm.name": "jwt2" } },
          { "field": { "username": "user2" } }
      ] },
      "enabled": true,
      "metadata" : { "version" : 1 }
    }

映射角色后，您可以使用 JWT 对 Elasticsearch 进行经过身份验证的调用，并包含"ES-Client-Authentication"标头：

    
    
    curl -s -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOlsiZXMwMSIsImVzMDIiLCJlczAzIl0sInN1YiI6InVzZXIyIiwiaXNzIjoibXktaXNzdWVyIiwiZXhwIjo0MDcwOTA4ODAwLCJpYXQiOjk0NjY4NDgwMCwiZW1haWwiOiJ1c2VyMkBzb21ldGhpbmcuZXhhbXBsZS5jb20ifQ.UgO_9w--EoRyUKcWM5xh9SimTfMzl1aVu6ZBsRWhxQA" -H "ES-Client-Authentication: sharedsecret test-secret" https://localhost:9200/_security/_authenticate

响应包括提交请求的用户 ('user2')，包括您在 JWT 领域中映射到此用户的"jwt_role1"角色：

    
    
    {"username":"user2","roles":["jwt_role1"],"full_name":null,"email":"user2@something.example.com",
    "metadata":{"jwt_claim_email":"user2@something.example.com","jwt_claim_aud":["es01","es02","es03"],
    "jwt_claim_sub":"user2","jwt_claim_iss":"my-issuer"},"enabled":true,"authentication_realm":
    {"name":"jwt2","type":"jwt"},"lookup_realm":{"name":"jwt2","type":"jwt"},"authentication_type":"realm"}
    %

如果要将请求指定为"run_as"用户，请在要作为其提交请求的用户的名称中包含"es-security-runas-user"标头。以下请求使用"user123_runas"用户：

    
    
    curl -s -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOlsiZXMwMSIsImVzMDIiLCJlczAzIl0sInN1YiI6InVzZXIyIiwiaXNzIjoibXktaXNzdWVyIiwiZXhwIjo0MDcwOTA4ODAwLCJpYXQiOjk0NjY4NDgwMCwiZW1haWwiOiJ1c2VyMkBzb21ldGhpbmcuZXhhbXBsZS5jb20ifQ.UgO_9w--EoRyUKcWM5xh9SimTfMzl1aVu6ZBsRWhxQA" -H "ES-Client-Authentication: sharedsecret test-secret" -H "es-security-runas-user: user123_runas" https://localhost:9200/_security/_authenticate

在响应中，您将看到"user123_runas"用户提交了请求，而 Elasticsearch 使用了"jwt_role1"角色：

    
    
    {"username":"user123_runas","roles":["jwt_role1"],"full_name":null,"email":null,"metadata":{},
    "enabled":true,"authentication_realm":{"name":"jwt2","type":"jwt"},"lookup_realm":{"name":"native",
    "type":"native"},"authentication_type":"realm"}%

#### PKC JWKS重新加载

JWT 身份验证支持使用 PKC(公钥加密)或 HMAC 算法进行签名验证。

PKC JSON Web 令牌密钥集 (JWKS) 可以包含公共 RSA 和 EC 密钥。HMACJWKS 或 HMAC UTF-8 JWK 包含密钥。JWT 颁发者通常更频繁地轮换PKC JWKS(例如每天)，因为 RSA 和 EC 公钥的设计比 HMAC 等密钥更易于分发。

JWT 领域在启动时加载 PKC JWKS 和 HMAC JWKS 或 HMAC UTF-8 JWK。JWTrealms 还可以在运行时重新加载 PKC JWKS 内容;重新加载由签名验证失败触发。

目前不支持 HMAC JWKS 或 HMAC UTF-8 JWK 重新加载。

加载失败、解析错误和配置错误会阻止节点启动(和重新启动)。但是，运行时 PKC 重新加载错误和恢复是正常处理的。

在签名失败触发 PKC JWKS 重新加载之前，会检查所有其他 JWT 领域验证。如果单个 Elasticsearch 节点同时发生多个 JWT 认证签名失败，则会合并重新加载以减少外部发送的重新加载。

如果触发 JWT 签名失败，则无法合并单独的重新加载请求：

* PKC JWKS 在不同的 Elasticsearch 节点中重新加载 * PKC JWKS 在不同时间在同一 Elasticsearch 节点中重新加载

强烈建议启用客户端身份验证("client_authentication.type")。只有受信任的客户端应用程序和特定于领域的 JWT 用户才能触发 PKC 重新加载尝试。此外，建议配置以下 JWT安全设置：

* "allowed_audiences" * "allowed_clock_skew" * "allowed_issuer" * "allowed_signature_algorithms"

### 使用 HMAC UTF-8 密钥授权到 JWT 领域

以下设置适用于 JWT 颁发者 Elasticsearch 和 Elasticsearch 的客户端。示例 HMAC 密钥采用与 HMAC 兼容的 OIDC 格式。密钥字节是 UNICODE 字符的 UTF-8 编码。

HMAC UTF-8 密钥需要比 HMAC 随机字节密钥长才能实现相同的密钥强度。

#### JWTissuer

以下值适用于定制的 JWT 颁发者。

    
    
    Issuer:     iss8
    Audiences:  aud8
    Algorithms: HS256
    HMAC UTF-8: hmac-oidc-key-string-for-hs256-algorithm

#### JWT 领域设置

要定义 JWT 领域，请将以下领域设置添加到 'elasticsearch.yml'。

    
    
    xpack.security.authc.realms.jwt.jwt8.order: 8 __xpack.security.authc.realms.jwt.jwt8.allowed_issuer: iss8
    xpack.security.authc.realms.jwt.jwt8.allowed_audiences: [aud8]
    xpack.security.authc.realms.jwt.jwt8.allowed_signature_algorithms: [HS256]
    xpack.security.authc.realms.jwt.jwt8.claims.principal: sub
    xpack.security.authc.realms.jwt.jwt8.client_authentication.type: shared_secret

__

|

在 Elastic Cloud 中，领域顺序从"2"开始。"0"和"1"保留在 Elastic Cloud 上的领域链中。   ---|--- #### JWT 领域安全设置编辑

定义领域设置后，使用"弹性搜索密钥库"工具将以下安全设置添加到 Elasticsearch 密钥库。在 Elastic Cloud 中，您可以在部署中的"**安全性**"下定义 Elasticsearch 密钥库的设置。

    
    
    xpack.security.authc.realms.jwt.jwt8.hmac_key: hmac-oidc-key-string-for-hs256-algorithm
    xpack.security.authc.realms.jwt.jwt8.client_authentication.shared_secret: client-shared-secret-string

#### JWT 领域角色映射规则

以下请求在"jwt8"域中为用户"principalname1"创建Elasticsearch的角色映射：

    
    
    PUT /_security/role_mapping/jwt8_users?refresh=true
    {
      "roles" : [ "user" ],
      "rules" : { "all" : [
          { "field": { "realm.name": "jwt8" } },
          { "field": { "username": "principalname1" } }
      ] },
      "enabled": true
    }

#### 请求标头

以下标头设置适用于 Elasticsearch 客户端。

    
    
    Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJpc3M4IiwiYXVkIjoiYXVkOCIsInN1YiI6InNlY3VyaXR5X3Rlc3RfdXNlciIsImV4cCI6NDA3MDkwODgwMCwiaWF0Ijo5NDY2ODQ4MDB9.UnnFmsoFKfNmKMsVoDQmKI_3-j95PCaKdgqqau3jPMY
    ES-Client-Authentication: SharedSecret client-shared-secret-string

您可以在"curl"请求中使用此标头来对Elasticsearch进行经过身份验证的调用。必须使用"-H"选项将持有者令牌和客户端授权令牌指定为单独的标头：

    
    
    curl -s -X GET -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJpc3M4IiwiYXVkIjoiYXVkOCIsInN1YiI6InNlY3VyaXR5X3Rlc3RfdXNlciIsImV4cCI6NDA3MDkwODgwMCwiaWF0Ijo5NDY2ODQ4MDB9.UnnFmsoFKfNmKMsVoDQmKI_3-j95PCaKdgqqau3jPMY" -H "ES-Client-Authentication: SharedSecret client-shared-secret-string" https://localhost:9200/_security/_authenticate

如果在 JWT 领域中使用角色映射，则响应包括用户的"用户名"、其"角色"、有关用户的元数据以及有关 JWT 领域本身的详细信息。

    
    
    {"username":"user2","roles":["jwt_role1"],"full_name":null,"email":"user2@something.example.com",
    "metadata":{"jwt_claim_email":"user2@something.example.com","jwt_claim_aud":["es01","es02","es03"],
    "jwt_claim_sub":"user2","jwt_claim_iss":"my-issuer"},"enabled":true,"authentication_realm":
    {"name":"jwt2","type":"jwt"},"lookup_realm":{"name":"jwt2","type":"jwt"},"authentication_type":"realm"}

[« Kerberos authentication](kerberos-realm.md) [Integrating with other
authentication systems »](custom-realms.md)
