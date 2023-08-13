

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md)

[« Failures due to relocation of the configuration files](trb-security-
path.md) [Watcher »](xpack-alerting.md)

## 安全限制

###Plugins

Elasticsearch的插件基础设施在可以扩展的内容方面非常灵活。虽然它为Elasticsearch打开了各种(通常是自定义的)附加功能，但在安全性方面，这种高可扩展性级别是有代价的。我们无法控制第三方插件的代码(无论是否开源)，因此我们无法保证它们符合 Elastic Stack 安全功能。因此，启用了安全功能的集群上不正式支持第三方插件。

### 通配符行为的更改

启用了安全功能的 Elasticsearch 集群会将"_all"和其他通配符应用于当前用户拥有权限的数据流、索引和别名，而不是集群上的所有数据流、索引和别名。

### 多文档接口

多获取和多术语向量 API 在尝试访问用户无权访问的非现有索引时抛出 IndexNotFoundException。通过这样做，它们会泄漏有关数据流或索引不存在的事实的信息，而用户无权了解有关这些数据流或索引的任何信息。

### 筛选的索引别名

包含筛选器的别名不是限制对单个文档的访问的安全方法，因为索引中描述的限制，并且在使用别名时可能会泄漏字段名称。Elastic Stack 安全功能提供了一种通过文档级安全功能限制对文档访问的安全方法。

### 字段和文档级安全性限制

当用户的角色为数据流或索引启用文档或字段级安全性时：

* 用户无法执行写入操作：

    * The update API isn't supported. 
    * Update requests included in bulk requests aren't supported. 

* 用户无法执行有效使内容以其他名称访问的操作，包括来自以下 API 的操作：

    * [Clone index API](indices-clone-index.html "Clone index API")
    * [Shrink index API](indices-shrink-index.html "Shrink index API")
    * [Split index API](indices-split-index.html "Split index API")
    * [Aliases API](indices-aliases.html "Aliases API")

* 如果满足以下任一条件，则会为搜索请求禁用请求缓存：

    * The role query that defines document level security is [templated](field-and-document-access-control.html#templating-role-query "Templating a role query") using a [stored script](modules-scripting-using.html#script-stored-scripts "Store and retrieve scripts"). 
    * The target indices are a mix of local and remote indices. 

当用户的角色为数据流或索引启用文档级安全性时：

* 文档级安全性不会影响相关性评分使用的全局索引统计信息。这意味着在不考虑角色查询的情况下计算分数。与角色查询不匹配的文档永远不会返回。  * 不支持将"has_child"和"has_parent"查询作为角色定义中的查询参数。可以在启用了文档级安全性的搜索 API 中使用"has_child"和"has_parent"查询。  * 日期数学表达式不能在带有日期字段的范围查询中包含"now" * 不支持任何进行远程调用以获取查询数据的查询，包括以下查询：

    * `terms` query with terms lookup 
    * `geo_shape` query with indexed shapes 
    * `percolate` query 

* 如果指定了建议器并启用了文档级安全性，则会忽略指定的建议器。  * 如果启用了文档级安全性，则无法分析搜索请求。  * 如果启用了文档级安全性，则术语枚举 API 不会返回术语。

虽然文档级安全性阻止用户查看受限制的文档，但仍可以编写返回有关整个索引的聚合信息的搜索请求。其访问权限仅限于索引中的特定文档的用户仍然可以了解仅存在于无法访问的文档中的字段名称和术语，并计算包含给定术语的无法访问文档的数量。

### 使用别名时可能会泄露索引和字段名称

在别名上调用某些 Elasticsearch API 可能会泄露有关用户无权访问的索引的信息。例如，当您使用"_mapping"API 获取别名的映射时，响应将包括别名应用到的每个索引的索引名称和映射。

在解决此限制之前，请避免包含机密或敏感信息的索引和字段名称。

### LDAP领域

LDAP 领域当前不支持发现嵌套的 LDAP 组。例如，如果用户是"group_1"的成员，而"group_1"是"group_2"的成员，则只会发现"group_1"。但是，Active Directory Realm 确实支持可传递的组成员身份。

### 用户和 API 密钥的资源共享检查

异步搜索和滚动请求的结果稍后可由提交初始请求的同一用户或 API 密钥检索。验证过程涉及比较用户名、身份验证领域类型和(文件或本机以外的领域)领域名称。如果您使用 API 密钥提交请求，则只有该密钥可以检索结果。此逻辑也有一些限制：

* 两个不同的领域在不同的节点上可以具有相同的名称。这不是配置域的推荐方法，因此资源共享检查不会尝试检测这种不一致。  * 领域可以重命名。这可能会导致资源共享检查不一致，当您提交异步搜索或滚动，然后重命名领域并尝试检索结果时。因此，应谨慎处理更改领域名称，因为它可能会导致不仅仅是资源共享检查的复杂性。  * 用户名是针对某些外部身份验证提供程序支持的领域动态计算的。例如，用户名可以从 LDAP 领域中的部分 DN 派生。从理论上讲，外部系统中的两个不同用户可能会映射到相同的用户名。我们的建议是首先避免这种情况。因此，资源共享检查不考虑这种潜在的差异。

[« Failures due to relocation of the configuration files](trb-security-
path.md) [Watcher »](xpack-alerting.md)
