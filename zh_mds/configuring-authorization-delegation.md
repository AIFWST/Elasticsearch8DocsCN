

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authorization](authorization.md)

[« Submitting requests on behalf of other users](run-as-privilege.md)
[Customizing roles and authorization »](custom-roles-authorization.md)

## 配置授权委托

在某些情况下，在用户通过某个领域进行身份验证后，我们可能希望将用户查找和角色分配委派给另一个领域。任何支持用户查找(不需要用户凭据)的领域都可以用作授权领域。

例如，可以在 LDAP 领域中查找由 Kerberos 领域进行身份验证的用户。LDAP 领域负责在 LDAP 中搜索用户并确定角色。在这种情况下，LDAP 领域充当an_authorization realm_。

### LDAP 领域作为授权领域

以下是可用作_authorization realm_的 LDAP 域的示例配置。此 LDAP 领域是在用户搜索模式下使用指定的过滤器配置的。

有关配置 LDAP 领域的更多信息，请参阅 LDAP 用户身份验证。

    
    
    xpack:
      security:
        authc:
          realms:
            ldap:
              ldap1:
                order: 0
                authentication.enabled: true __user_search:
                  base_dn: "dc=example,dc=org"
                  filter: "(cn={0})"
                group_search:
                  base_dn: "dc=example,dc=org"
                files:
                  role_mapping: "ES_PATH_CONF/role_mapping.yml"
                unmapped_groups_as_roles: false

__

|

在这里，我们明确允许使用 LDAP 领域进行身份验证(即，用户可以使用其 LDAP 用户名和密码进行身份验证)。如果我们希望此 LDAP 领域仅用于授权，那么我们会将其设置为 'false'。   ---|--- ### Kerberos 领域配置为委派授权编辑

下面是一个示例配置，其中 Kerberos 域对用户进行身份验证，然后将授权委托给 LDAP 域。Kerberos 对用户进行身份验证并提取用户主体名称(通常为格式为"user@REALM")。在此示例中，我们启用"remove_realm_name"设置以从用户主体名称中删除"@REALM"部分以获取用户名。此用户名用于通过配置的授权域(在本例中为 LDAP 域)执行用户查找。

有关 Kerberos 领域的详细信息，请参阅 Kerberos 身份验证。

    
    
    xpack:
      security:
        authc:
          realms:
            kerberos:
              kerb1:
                order: 1
                keytab.path: "ES_PATH_CONF/es.keytab"
                remove_realm_name: true
                authorization_realms: ldap1

### 配置为委派授权的 PKI 领域

我们类似地配置 PKI 领域以将授权委托给 LDAP 领域。用户由 PKI 领域进行身份验证，授权委托给 LDAP 领域。在此示例中，用户名是从客户端证书的 DN 中提取的公用名 (CN)。LDAP 领域使用此用户名来查找用户并分配角色。

有关 PKI 领域的详细信息，请参阅 PKI 用户身份验证。

    
    
    xpack:
      security:
        authc:
          realms:
            pki:
              pki1:
                order: 2
                authorization_realms: ldap1

与上述示例类似，我们可以配置领域以将授权委托给授权领域(授权领域能够通过用户名查找用户并分配角色)。

[« Submitting requests on behalf of other users](run-as-privilege.md)
[Customizing roles and authorization »](custom-roles-authorization.md)
