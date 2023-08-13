

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Security APIs](security-api.md)

[« Create or update application privileges API](security-api-put-
privileges.md) [Create or update roles API »](security-api-put-role.md)

## 创建或更新角色映射API

创建和更新角色映射。

###Request

"发布/_security/role_mapping/<name>"

"放 /_security/role_mapping<name>/"

###Prerequisites

* 要使用此 API，您必须至少具有"manage_security"群集权限。

###Description

角色映射定义分配给每个用户的角色。每个映射has_rules_标识用户以及授予这些用户的_角色_列表。

角色映射 API 通常是管理角色映射的首选方法，而不是使用角色映射文件。创建或更新角色映射 API 无法更新角色映射文件中定义的角色映射。

此 API 不会创建角色。相反，它将用户映射到现有角色。可以使用创建或更新角色 API 或角色文件创建角色。

有关更多信息，请参阅将用户和组映射到角色。

#### 角色模板

角色映射的最常见用途是创建从用户上的已知值到固定角色名称的映射。例如，在 Elasticsearch 中，'cn=admin，dc=example，dc=com' LDAP 组中的所有用户都应该被赋予"超级用户"角色。"角色"字段用于此目的。

对于更复杂的需求，可以使用 Mustache 模板动态确定应授予用户的角色的名称。"role_templates"字段用于此目的。

若要成功使用角色模板，必须启用相关的脚本功能。否则，使用角色模板创建角色映射的所有尝试都将失败。请参阅允许的脚本类型设置。

角色映射"规则"中可用的所有用户字段在角色模板中也可用。因此，可以将用户分配给反映其"用户名"、其"组"或其身份验证的"领域"名称的角色。

默认情况下，将评估模板以生成单个字符串，该字符串是应分配给用户的角色的名称。如果模板的"格式"设置为"json"，则模板应为角色名称生成 JSON 字符串或 JSON 字符串数组。

### 路径参数

`name`

     (string) The distinct name that identifies the role mapping. The name is used solely as an identifier to facilitate interaction via the API; it does not affect the behavior of the mapping in any way. 

### 请求正文

可以在 PUT 或 POST 请求的正文中指定以下参数，这些参数与添加角色映射有关：

`enabled`

     (Required, Boolean) Mappings that have `enabled` set to `false` are ignored when role mapping is performed. 
`metadata`

     (object) Additional metadata that helps define which roles are assigned to each user. Within the `metadata` object, keys beginning with `_` are reserved for system usage. 
`roles`

     (list of strings) A list of role names that are granted to the users that match the role mapping rules. _Exactly one of`roles` or `role_templates` must be specified_. 
`role_templates`

     (list of objects) A list of mustache templates that will be evaluated to determine the roles names that should granted to the users that match the role mapping rules. The format of these objects is defined below. _Exactly one of`roles` or `role_templates` must be specified_. 
`rules`

     (Required, object) The rules that determine which users should be matched by the mapping. A rule is a logical condition that is expressed by using a JSON DSL. See [Role mapping resources](role-mapping-resources.html "Role mapping resources"). 

###Examples

以下示例将"用户"角色分配给所有用户：

    
    
    POST /_security/role_mapping/mapping1
    {
      "roles": [ "user"],
      "enabled": true, __"rules": {
        "field" : { "username" : "*" }
      },
      "metadata" : { __"version" : 1
      }
    }

__

|

执行角色映射时，将忽略"已启用"设置为"false"的映射。   ---|---    __

|

元数据是可选的。   成功的调用会返回一个 JSON 结构，该结构显示映射是否已创建或更新。

    
    
    {
      "role_mapping" : {
        "created" : true __}
    }

__

|

更新现有映射时，"created"设置为 false。   ---|--- 以下示例将"用户"和"管理员"角色分配给特定用户：

    
    
    POST /_security/role_mapping/mapping2
    {
      "roles": [ "user", "admin" ],
      "enabled": true,
      "rules": {
         "field" : { "username" : [ "esadmin01", "esadmin02" ] }
      }
    }

以下示例匹配针对特定领域进行身份验证的用户：

    
    
    POST /_security/role_mapping/mapping3
    {
      "roles": [ "ldap-user" ],
      "enabled": true,
      "rules": {
        "field" : { "realm.name" : "ldap1" }
      }
    }

以下示例匹配用户名为"esadmin"或用户位于"cn=admin，dc=example，dc=com"组中的任何用户：

    
    
    POST /_security/role_mapping/mapping4
    {
      "roles": [ "superuser" ],
      "enabled": true,
      "rules": {
        "any": [
          {
            "field": {
              "username": "esadmin"
            }
          },
          {
            "field": {
              "groups": "cn=admins,dc=example,dc=com"
            }
          }
        ]
      }
    }

当身份管理系统中的组名(如 Active Directory 或 SAML 身份提供程序)与 Elasticsearch 中的角色名称没有一对一对应关系时，上述示例非常有用。角色映射是将_group name_与_role name_链接的方式。

如果有多个组，则可以对组字段使用数组语法。这将匹配任何组(而不是所有组)：

    
    
    POST /_security/role_mapping/mapping4
    {
      "roles": [ "superuser" ],
      "enabled": true,
      "rules": {
        "any": [
          {
            "field": {
              "username": "esadmin"
            }
          },
          {
            "field": {
              "groups": [
                   "cn=admins,dc=example,dc=com",
                   "cn=other,dc=example,dc=com"
                ]
            }
          }
        ]
      }
    }

但是，在极少数情况下，组的名称可能与 Elasticsearch 角色的名称完全匹配。当您的 SAMLIdentity 提供程序包含自己的"组映射"功能并且可以配置为在用户的 SAML 属性中释放 Elasticsearch 角色名称时，可能会出现这种情况。

在这些情况下，可以使用将组名称视为角色名称的模板。

**注意**：仅当您打算为所有提供的组定义角色时，才应执行此操作。将用户映射到大量不必要的或未定义的角色效率低下，并且可能会对系统性能产生负面影响。如果只需要映射组的子集，则应使用显式映射来执行此操作。

    
    
    POST /_security/role_mapping/mapping5
    {
      "role_templates": [
        {
          "template": { "source": "{{#tojson}}groups{{/tojson}}" }, __"format" : "json" __}
      ],
      "rules": {
        "field" : { "realm.name" : "saml1" }
      },
      "enabled": true
    }

__

|

"tojson"胡须函数用于将组名列表转换为有效的 JSON 数组。   ---|---    __

|

由于模板生成 JSON 数组，因此格式必须设置为"json"。   以下示例匹配特定 LDAP 子树中的用户：

    
    
    POST /_security/role_mapping/mapping6
    {
      "roles": [ "example-user" ],
      "enabled": true,
      "rules": {
        "field" : { "dn" : "*,ou=subtree,dc=example,dc=com" }
      }
    }

以下示例匹配特定领域中特定 LDAP 子树中的用户：

    
    
    POST /_security/role_mapping/mapping7
    {
      "roles": [ "ldap-example-user" ],
      "enabled": true,
      "rules": {
        "all": [
          { "field" : { "dn" : "*,ou=subtree,dc=example,dc=com" } },
          { "field" : { "realm.name" : "ldap1" } }
        ]
      }
    }

规则可能更复杂，包括通配符匹配。例如，以下映射匹配满足这些条件的所有用户：

* _Distinguished Name_与模式"*，ou=admin，dc=example，dc=com"匹配，或用户名为"es-admin"，或用户名为"es-system" * "cn=people，dc=example，dc=com"组中的用户 * 用户没有"terminated_date"

    
    
    POST /_security/role_mapping/mapping8
    {
      "roles": [ "superuser" ],
      "enabled": true,
      "rules": {
        "all": [
          {
            "any": [
              {
                "field": {
                  "dn": "*,ou=admin,dc=example,dc=com"
                }
              },
              {
                "field": {
                  "username": [ "es-admin", "es-system" ]
                }
              }
            ]
          },
          {
            "field": {
              "groups": "cn=people,dc=example,dc=com"
            }
          },
          {
            "except": {
              "field": {
                "metadata.terminated_date": null
              }
            }
          }
        ]
      }
    }

模板化角色可用于自动将每个用户映射到其自己的自定义角色。角色本身可以通过角色 API 或使用自定义角色提供程序来定义。

在此示例中，使用"cloud-saml"领域进行身份验证的每个用户将自动映射到两个角色 - "saml_user"角色和用户名前缀为"_user_"的角色。例如，将为用户"nwong"分配"saml_user"和"_user_nwong"角色。

    
    
    POST /_security/role_mapping/mapping9
    {
      "rules": { "field": { "realm.name": "cloud-saml" } },
      "role_templates": [
        { "template": { "source" : "saml_user" } }, __{ "template": { "source" : "_user_{{username}}" } }
      ],
      "enabled": true
    }

__

|

由于不可能在同一角色映射中同时指定"角色"和"role_templates"，因此我们可以使用没有替换的模板来应用"固定名称"角色。   ---|--- « 创建或更新应用程序权限 API 创建或更新角色 API »