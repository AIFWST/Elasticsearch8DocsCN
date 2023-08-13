

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authorization](authorization.md)

[« Setting up field and document level security](field-and-document-access-
control.md) [Configuring authorization delegation »](configuring-
authorization-delegation.md)

## 代表其他用户提交请求

Elasticsearch 角色支持"run_as"权限，使经过身份验证的用户能够代表其他用户提交请求。例如，如果您的外部应用程序被信任对用户进行身份验证，则 Elasticsearch 可以对外部应用程序进行身份验证，并使用_run as_机制以其他用户的身份发出授权请求，而无需重新验证每个用户。

若要"运行身份"(模拟)其他用户，第一个用户(身份验证用户)必须由支持运行方式委派的机制进行身份验证。第二个用户("run_as"用户)必须由支持按用户名委派运行方式查找的机制授权。

"run_as"权限本质上类似于委托授权的辅助形式。委派授权适用于身份验证用户，"run_as"权限适用于被模拟的用户。

对用户进行身份验证

对于身份验证用户，以下领域(加上 API 密钥)都支持"run_as"委派："本机"、"文件"、"Active Directory"、"JWT"、"Kerberos"、"LDAP和 PKI"。

服务令牌、Elasticsearch Token Service、SAML 2.0 和 OIDC 1.0 不支持"run_as"委派。

"run_as"用户

Elasticsearch 支持任何支持用户查找的领域使用"run_as"。并非所有领域都支持用户查找。请参阅支持的领域列表，并确保您希望使用的域配置为支持用户查找。

"run_as"用户必须从领域检索 - 不能作为服务帐户、API 密钥或访问令牌运行。

要代表其他用户提交请求，您需要在您的角色中具有"run_as"权限。例如，以下请求创建一个"my_director"角色，该角色授予代表"jacknich"或"redeniro"提交请求的权限：

    
    
    POST /_security/role/my_director?refresh=true
    {
      "cluster": ["manage"],
      "indices": [
        {
          "names": [ "index1", "index2" ],
          "privileges": [ "manage" ]
        }
      ],
      "run_as": [ "jacknich", "rdeniro" ],
      "metadata" : {
        "version" : 1
      }
    }

要以其他用户身份提交请求，请在"es-security-runas-user"请求标头中指定该用户。例如：

    
    
    curl -H "es-security-runas-user: jacknich" -u es-admin -X GET http://localhost:9200/

通过 'es-security-runas-user' 标头传入的 'run_as' 用户必须来自支持按用户名委派授权查找的领域。不支持用户查找的领域不能由其他领域的"run_as"委派使用。

例如，JWT 领域可以对 JWT 中指定的外部用户进行身份验证，并以"本机"领域中的"run_as"用户身份执行请求。Elasticsearch将检索指示的"runas"用户，并使用他们的角色以该用户的身份执行请求。

### 将"run_as"权限应用于角色

您可以在使用创建或更新角色 API 创建角色时应用"run_as"权限。分配了包含"run_as"权限的角色的用户将从其角色继承所有权限，还可以代表指定的用户提交请求。

经过身份验证的用户和"run_as"用户的角色不会合并。如果用户在未指定"run_as"参数的情况下进行身份验证，则仅使用经过身份验证的用户的角色。如果用户进行身份验证，并且其角色包含"run_as"参数，则仅使用"run_as"用户的角色。

用户成功向 Elasticsearch 进行身份验证后，授权过程将确定是否允许传入请求背后的用户运行该请求。如果经过身份验证的用户在其权限列表中具有"run_as"权限并指定运行方式标头，则Elasticsearch_discards_经过身份验证的用户和关联的角色。然后，它会查找领域链中的每个已配置领域，直到找到与"run_as"用户关联的用户名，并使用这些角色来执行任何请求。

考虑管理员角色和分析师角色。管理员角色具有更高的权限，但可能还希望以其他用户身份提交请求以测试和验证其权限。

首先，我们将创建一个名为"my_admin_role"的管理员角色。此角色对整个集群和索引子集具有"管理"权限。此角色还包含"run_as"权限，该权限使具有此角色的任何用户都可以代表指定的"analyst_user"提交请求。

    
    
    POST /_security/role/my_admin_role?refresh=true
    {
      "cluster": ["manage"],
      "indices": [
        {
          "names": [ "index1", "index2" ],
          "privileges": [ "manage" ]
        }
      ],
      "applications": [
        {
          "application": "myapp",
          "privileges": [ "admin", "read" ],
          "resources": [ "*" ]
        }
      ],
      "run_as": [ "analyst_user" ],
      "metadata" : {
        "version" : 1
      }
    }

接下来，我们将创建一个名为"my_analyst_role"的分析师角色，该角色对索引子集具有更多受限制的"监视"群集权限和"管理"权限。

    
    
    POST /_security/role/my_analyst_role?refresh=true
    {
      "cluster": [ "monitor"],
      "indices": [
        {
          "names": [ "index1", "index2" ],
          "privileges": ["manage"]
        }
      ],
      "applications": [
        {
          "application": "myapp",
          "privileges": [ "read" ],
          "resources": [ "*" ]
        }
      ],
      "metadata" : {
        "version" : 1
      }
    }

我们将创建一个管理员用户，并为其分配名为"my_admin_role"的角色，该角色允许该用户以"analyst_user"的身份提交请求。

    
    
    POST /_security/user/admin_user?refresh=true
    {
      "password": "l0ng-r4nd0m-p@ssw0rd",
      "roles": [ "my_admin_role" ],
      "full_name": "Eirian Zola",
      "metadata": { "intelligence" : 7}
    }

我们还可以创建一个分析师用户，并为其分配名为"my_analyst_role"的角色。

    
    
    POST /_security/user/analyst_user?refresh=true
    {
      "password": "l0nger-r4nd0mer-p@ssw0rd",
      "roles": [ "my_analyst_role" ],
      "full_name": "Monday Jaffe",
      "metadata": { "innovation" : 8}
    }

然后，您可以以"admin_user"或"analyst_user"的身份向 Elasticsearch 进行身份验证。但是，"admin_user"可以选择代表"analyst_user"提交请求。以下请求使用"基本"授权令牌向 Elasticsearch 进行身份验证，并将请求作为"analyst_user"提交：

    
    
    curl -s -X GET -H "Authorization: Basic YWRtaW5fdXNlcjpsMG5nLXI0bmQwbS1wQHNzdzByZA==" -H "es-security-runas-user: analyst_user" https://localhost:9200/_security/_authenticate

响应指示"analyst_user"使用分配给该用户的"my_analyst_role"提交了此请求。当"admin_user"提交请求时，Elasticsearch 对该用户进行身份验证，丢弃其角色，然后使用"run_as"用户的角色。

    
    
    {"username":"analyst_user","roles":["my_analyst_role"],"full_name":"Monday Jaffe","email":null,
    "metadata":{"innovation":8},"enabled":true,"authentication_realm":{"name":"native",
    "type":"native"},"lookup_realm":{"name":"native","type":"native"},"authentication_type":"realm"}
    %

响应中的"authentication_realm"和"lookup_realm"都指定了"本机"领域，因为"admin_user"和"analyst_user"都来自该领域。如果两个用户位于不同的领域，则"authentication_realm"和"lookup_realm"的值会不同(例如"pki"和"native")。

[« Setting up field and document level security](field-and-document-access-
control.md) [Configuring authorization delegation »](configuring-
authorization-delegation.md)
