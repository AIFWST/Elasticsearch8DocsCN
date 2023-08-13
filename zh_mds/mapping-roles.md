

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authorization](authorization.md)

[« Granting privileges for data streams and aliases](securing-aliases.md)
[Setting up field and document level security »](field-and-document-access-
control.md)

## 将用户和组映射到角色

除"本机"和"文件"之外的所有领域都支持角色映射。

本机域和文件域将角色直接分配给用户。本机领域使用用户管理 API。文件领域使用基于文件的角色管理。

可以通过角色映射 API(推荐)或角色映射文件映射角色。

PKI、LDAP、AD、Kerberos、OpenID Connect、JWT 和 SAML 领域支持角色映射 API。只有 PKI、LDAP 和 AD 领域支持角色映射文件。

PKI、LDAP、AD、Kerberos、OpenID Connect、JWT 和 SAML 领域也支持委托授权。您可以映射领域的角色，也可以使用委派授权;您不能同时使用两者。

若要使用角色映射，请创建角色和角色映射规则。角色映射规则可以基于领域名称、领域类型、用户名、组、其他用户元数据或这些值的组合。

启用匿名访问后，匿名用户的角色也会分配给所有其他用户。

如果存在通过 API 创建的角色映射规则以及角色映射文件，则会合并这些规则。单个用户可以拥有通过 API 映射的一些角色，以及根据角色映射文件分配的其他角色。您可以通过 API 定义角色映射，也可以通过文件管理它们。这两个角色映射源在 Elasticsearch 安全功能中组合在一起，因此单个用户可以拥有通过 API 映射的一些角色，以及通过文件映射的其他角色。

未分配角色的用户将未经授权执行任何操作。换句话说，他们可能能够进行身份验证，但他们没有角色。没有角色意味着没有权限，没有权限意味着没有发出请求的授权。

使用角色映射向用户分配角色时，角色必须存在。角色有两个来源。应使用角色管理 API 添加可用角色，或者使用角色文件中定义的角色管理 API。任一角色映射方法都可以使用任一角色管理方法。例如，使用角色映射 API 时，可以将用户映射到 API 托管角色和文件托管角色(同样，对于基于文件的角色映射也是如此)。

### 使用角色映射API

可以通过添加角色映射 API 定义角色映射。

### 使用角色映射文件

若要使用基于文件的角色映射，必须在 YAMLfile 中配置映射，并将其复制到群集中的每个节点。像Puppet或Chef这样的工具可以帮助解决这个问题。

默认情况下，角色映射存储在"ES_PATH_CONF/role_mapping.yml"中，其中"ES_PATH_CONF"是"ES_HOME/config"(zip/tar安装)或"/etc/elasticsearch"(软件包安装)。要指定其他位置，请在"elasticsearch.yml"中的 ActiveDirectory、LDAP 和 PKI 领域设置中配置"files.role_mapping"设置。

在角色映射文件中，安全角色是键和组，用户是值。映射可以具有多对多关系。将角色映射到组时，该组中用户的角色是分配给该组的角色和分配给该用户的角色的组合。

默认情况下，Elasticsearch 每 5 秒检查一次角色映射文件是否有更改。您可以通过更改"elasticsearch.yml"文件中的"resource.reload.interval.high"设置来更改此默认行为。由于这是 Elasticsearch 中的常见设置，因此更改其值可能会影响系统中的其他计划。

虽然_role映射APIs_是管理角色映射的首选方法，但使用"role_mapping.yml"文件在几个用例中非常有用：

1. 如果要定义固定的角色映射，没有人(除了对 Elasticsearch 节点具有物理访问权限的管理员)能够更改。  2. 如果集群管理依赖于来自外部领域的用户，并且即使集群为 RED 时，这些用户也需要将其角色映射到他们。例如，通过 LDAP 或 PKI 进行身份验证并分配管理员角色的管理员，以便他们可以执行纠正措施。

但请注意，"role_mapping.yml"文件是作为最小管理功能提供的，并不旨在涵盖和用于定义所有用例的角色。

您无法使用角色映射 API 查看、编辑或删除角色映射文件中定义的任何角色。

### 领域特定详细信息

##### Active Directory 和 LDAPrealms

若要在角色映射中指定用户和组，请使用其 _可分辨名称_ (DN)。DN 是唯一标识用户或组的字符串，例如"cn=John Doe，cn=contractors，dc=example，dc=com""。

Elasticsearch 安全功能仅支持 Active Directory 安全组。不能将通讯组映射到角色。

例如，以下代码片段使用基于文件的方法将"管理员"组映射到"监视"角色，并将"John Doe"用户、"用户"组和"管理员"组映射到"用户"角色。

    
    
    monitoring: __- "cn=admins,dc=example,dc=com" __user:
      - "cn=John Doe,cn=contractors,dc=example,dc=com" __- "cn=users,dc=example,dc=com"
      - "cn=admins,dc=example,dc=com"

__

|

角色的名称。   ---|---    __

|

LDAP 组或活动目录安全组的可分辨名称。   __

|

LDAP 或活动目录用户的可分辨名称。   可以使用角色映射 API 定义等效映射，如下所示：

    
    
    PUT /_security/role_mapping/admins
    {
      "roles" : [ "monitoring", "user" ],
      "rules" : { "field" : { "groups" : "cn=admins,dc=example,dc=com" } },
      "enabled": true
    }
    
    
    PUT /_security/role_mapping/basic_users
    {
      "roles" : [ "user" ],
      "rules" : { "any" : [
          { "field" : { "dn" : "cn=John Doe,cn=contractors,dc=example,dc=com" } },
          { "field" : { "groups" : "cn=users,dc=example,dc=com" } }
      ] },
      "enabled": true
    }

##### PKI领域

PKI 领域支持将用户映射到角色，但不能映射组，因为 PKI 领域没有组的概念。

以下是使用基于文件的映射的示例：

    
    
    monitoring:
      - "cn=Admin,ou=example,o=com"
    user:
      - "cn=John Doe,ou=example,o=com"

以下示例使用 API 创建等效映射：

    
    
    PUT /_security/role_mapping/admin_user
    {
      "roles" : [ "monitoring" ],
      "rules" : { "field" : { "dn" : "cn=Admin,ou=example,o=com" } },
      "enabled": true
    }
    
    
    PUT /_security/role_mapping/basic_user
    {
      "roles" : [ "user" ],
      "rules" : { "field" : { "dn" : "cn=John Doe,ou=example,o=com" } },
      "enabled": true
    }

[« Granting privileges for data streams and aliases](securing-aliases.md)
[Setting up field and document level security »](field-and-document-access-
control.md)
