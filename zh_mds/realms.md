

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« User profiles](user-profile.md) [Realm chains »](realm-chains.md)

##Realms

Elastic Stack 安全功能通过使用领域和一个或多个基于令牌的身份验证服务对用户进行身份验证。

_realm_ 用于根据身份验证令牌解析和验证用户。安全功能部件提供以下内置领域：

_native_

     An internal realm where users are stored in a dedicated Elasticsearch index. This realm supports an authentication token in the form of username and password, and is available by default when no realms are explicitly configured. The users are managed via the [user management APIs](security-api.html#security-user-apis "Users"). See [Native user authentication](native-realm.html "Native user authentication"). 
_ldap_

     A realm that uses an external LDAP server to authenticate the users. This realm supports an authentication token in the form of username and password, and requires explicit configuration in order to be used. See [LDAP user authentication](ldap-realm.html "LDAP user authentication"). 
_active_directory_

     A realm that uses an external Active Directory Server to authenticate the users. With this realm, users are authenticated by usernames and passwords. See [Active Directory user authentication](active-directory-realm.html "Active Directory user authentication"). 
_pki_

     A realm that authenticates users using Public Key Infrastructure (PKI). This realm works in conjunction with SSL/TLS and identifies the users through the Distinguished Name (DN) of the client's X.509 certificates. See [PKI user authentication](pki-realm.html "PKI user authentication"). 
_file_

     An internal realm where users are defined in files stored on each node in the Elasticsearch cluster. This realm supports an authentication token in the form of username and password and is always available. See [File-based user authentication](file-realm.html "File-based user authentication"). 
_saml_

     A realm that facilitates authentication using the SAML 2.0 Web SSO protocol. This realm is designed to support authentication through Kibana and is not intended for use in the REST API. See [SAML authentication](saml-realm.html "SAML authentication"). 
_kerberos_

     A realm that authenticates a user using Kerberos authentication. Users are authenticated on the basis of Kerberos tickets. See [Kerberos authentication](kerberos-realm.html "Kerberos authentication"). 
_oidc_

     A realm that facilitates authentication using OpenID Connect. It enables Elasticsearch to serve as an OpenID Connect Relying Party (RP) and provide single sign-on (SSO) support in Kibana. See [Configuring single sign-on to the Elastic Stack using OpenID Connect](oidc-guide.html "Configuring single sign-on to the Elastic Stack using OpenID Connect"). 
_jwt_

     A realm that facilitates using JWT identity tokens as authentication bearer tokens. Compatible tokens are OpenID Connect ID Tokens, or custom JWTs containing the same claims. See [JWT authentication](jwt-auth-realm.html "JWT authentication"). 

安全功能还支持自定义领域。如果您需要与其他身份验证系统集成，则可以构建自定义领域插件。有关详细信息，请参阅与其他身份验证系统集成。

### 内部和外部领域

领域类型大致可分为两类：

Internal

     Realms that are internal to Elasticsearch and don't require any communication with external parties. They are fully managed by the Elastic Stack security features. There can only be a maximum of one configured realm per internal realm type. The security features provide two internal realm types: `native` and `file`. 
External

     Realms that require interaction with parties/components external to Elasticsearch, typically, with enterprise grade identity management systems. Unlike internal realms, there can be as many external realms as one would like - each with its own unique name and configuration. The security features provide the following external realm types: `ldap`, `active_directory`, `saml`, `kerberos`, and `pki`. 

[« User profiles](user-profile.md) [Realm chains »](realm-chains.md)
