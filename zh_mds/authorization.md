

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md)

[« Configuring single sign-on to the Elastic Stack using OpenID Connect](oidc-
guide.md) [Built-in roles »](built-in-roles.md)

## 用户授权

弹性堆栈安全功能添加了 _authorization_ ，这是确定是否允许传入请求背后的用户执行请求的过程。

此过程在成功识别用户并对其进行身份验证后进行。

### 基于角色的访问控制

安全功能提供基于角色的访问控制 (RBAC) 机制，使您能够通过向角色分配权限以及向用户或组分配角色来授权用户。

!此图说明了基于角色的访问控制

授权过程围绕以下构造展开：

_Secured Resource_

     A resource to which access is restricted. Indices, aliases, documents, fields, users, and the Elasticsearch cluster itself are all examples of secured objects. 
_Privilege_

     A named group of one or more actions that a user may execute against a secured resource. Each secured resource has its own sets of available privileges. For example, `read` is an index privilege that represents all actions that enable reading the indexed/stored data. For a complete list of available privileges see [Security privileges](security-privileges.html "Security privileges"). 
_Permissions_

    

针对受保护资源的一组一个或多个特权。权限可以很容易地用语言来描述，这里有几个例子：

* 对"产品"数据流或索引的"读取"权限 * 群集上的"管理"权限 * 对"john"用户具有"run_as"权限 * 对与查询 X 匹配的文档具有"读取"权限 * 对"credit_card"字段具有"读取"权限

_Role_

     A named set of permissions 
_User_

     The authenticated user. 
_Group_

     One or more groups to which a user belongs. Groups are not supported in some realms, such as native, file, or PKI realms. 

角色具有唯一名称，并标识一组转换为资源特权的权限。您可以将用户或组与任意数量的角色相关联。将角色映射到组时，该组中用户的角色是分配给该组的角色和分配给该用户的角色的组合。同样，用户拥有的总权限集由其所有角色中的权限联合定义。

向用户分配角色的方法因用于对用户进行身份验证的领域而异。有关更多信息，请参阅将用户和组映射到角色。

### 基于属性的访问控制

安全功能还提供基于属性的访问控制 (ABAC) 机制，该机制使您能够使用属性来限制对搜索查询和聚合中的文档的访问。例如，可以将属性分配给用户和文档，然后在角色定义中实施访问策略。具有该角色的用户只有在具有所有必需属性时才能阅读特定文档。

有关详细信息，请参阅使用 X-Pack 6.1 进行文档级基于属性的访问控制。

[« Configuring single sign-on to the Elastic Stack using OpenID Connect](oidc-
guide.md) [Built-in roles »](built-in-roles.md)
