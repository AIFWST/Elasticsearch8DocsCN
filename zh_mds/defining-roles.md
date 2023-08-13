

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authorization](authorization.md)

[« Built-in roles](built-in-roles.md) [Role restriction »](role-
restriction.md)

## 定义角色

角色由以下 JSON 结构定义：

    
    
    {
      "run_as": [ ... ], __"cluster": [ ... ], __"global": { ... }, __"indices": [ ... ], __"applications": [ ... ] __}

__

|

此角色的所有者可以模拟的用户名列表。   ---|---    __

|

群集权限列表。这些权限定义具有此角色的用户能够执行的集群级别操作。此字段是可选的(缺少"群集"权限实际上意味着没有群集级别权限)。   __

|

定义全局权限的对象。全局特权是请求敏感的群集特权的一种形式。标准群集特权仅根据正在执行的操作做出授权决策。全局特权还会考虑请求中包含的参数。对全局权限的支持目前仅限于应用程序权限的管理。此字段是可选的。   __

|

索引权限条目的列表。此字段是可选的(缺少"索引"权限实际上意味着没有索引级别权限)。   __

|

应用程序特权条目的列表。此字段是可选的。   角色名称必须至少为 1 个字符且不超过 507 个字符。它们可以包含字母数字字符("a-z"、"A-Z"、"0-9")、空格、标点符号和基本拉丁语 (ASCII) 块中的可打印符号)。不允许使用前导或尾随空格。

### 索引特权

下面描述了索引权限条目的结构：

    
    
    {
      "names": [ ... ], __"privileges": [ ... ], __"field_security" : { ... }, __"query": "..." __"allow_restricted_indices": false __}

__

|

应用此条目中的权限的数据流、索引和别名的列表。支持通配符 ("*")。   ---|---    __

|

角色所有者对"names"参数中指定的关联数据流和索引的索引级别特权。   __

|

角色所有者具有读取访问权限的文档字段的规范。有关详细信息，请参阅设置字段和文档级别安全性。   __

|

定义角色所有者具有读取访问权限的文档的搜索查询。关联数据流和索引中的文档必须与此查询匹配，角色所有者才能访问该文档。   __

|

受限索引是内部用于存储配置数据的特殊索引类别，不应直接访问。通常只有内部系统角色才能授予对受限索引的权限。**强烈建议不要切换此标志，因为它可以有效地授予对关键数据的不受限制的操作，从而使整个系统不稳定或泄露敏感信息。** 但是，如果出于管理目的，您需要创建一个具有涵盖受限索引的权限的角色，则必须将此字段设置为"true"(默认值为"false")， 然后"名称"字段也将涵盖受限制的索引。   "names"参数接受通配符和正则表达式，这些表达式可能引用多个数据流、索引和别名。

* 通配符(默认)- 简单的通配符匹配，其中"*"是零个或多个字符的占位符，"？"是单个字符的占位符，"\"可以用作转义字符。  * 正则表达式 - 一种更强大的语法，用于匹配更复杂的模式。此正则表达式基于 Lucene 的正则表达式自动机语法。若要启用此语法，必须将其括在一对正斜杠 ('/') 中。任何以"/"开头但不以"/"结尾的模式都被视为格式不正确。

**正则表达式示例。

    
    
    "foo-bar":               # match the literal `foo-bar`
    "foo-*":                 # match anything beginning with "foo-"
    "logstash-201?-*":       # ? matches any one character
    "/.*-201[0-9]-.*/":      # use a regex to match anything containing 2010-2019
    "/foo":                  # syntax error - missing final /

### 全球特权

下面描述了全局权限条目的结构：

    
    
    {
      "application": {
        "manage": {    __"applications": [ ... ] __}
      },
      "profile": {
        "write": { __"applications": [ ... ] __}
      }
    }

__

|

管理应用程序权限的权限 ---|--- __

|

可以管理的应用程序名称的列表。此列表支持通配符(例如"myapp-*"")和正则表达式(例如""/app[0-9]*/"') __

|

能够写入任何用户配置文件的"访问"和"数据"的特权 __

|

写入权限限制为 ### 应用程序权限编辑的名称、通配符和正则表达式的列表

下面介绍了应用程序特权条目的结构：

    
    
    {
      "application": "my_app", __"privileges": [ ... ], __"resources": [ ... ] __}

__

|

应用程序的名称。   ---|---    __

|

要授予此角色的应用程序权限的名称列表。   __

|

应用这些权限的资源。这些处理方式与"索引"权限中的索引名称模式相同。这些资源对 Elasticsearch 安全功能没有任何特殊意义。   有关这些字段的验证规则的详细信息，请参阅添加应用程序权限 API。

角色可以引用不存在的应用程序权限 - 即，它们尚未通过添加应用程序权限 API 定义(或者已定义，但此后已删除)。在这种情况下，权限无效，并且不会授予具有权限 API 中的任何操作。

###Example

以下代码片段显示了"clicks_admin"角色的示例定义：

    
    
    POST /_security/role/clicks_admin
    {
      "run_as": [ "clicks_watcher_1" ],
      "cluster": [ "monitor" ],
      "indices": [
        {
          "names": [ "events-*" ],
          "privileges": [ "read" ],
          "field_security" : {
            "grant" : [ "category", "@timestamp", "message" ]
          },
          "query": "{\"match\": {\"category\": \"click\"}}"
        }
      ]
    }

根据上述定义，拥有"clicks_admin"角色的用户可以：

* 模拟"clicks_watcher_1"用户并代表其执行请求。  * 监控 Elasticsearch 集群 * 从所有以"events-"为前缀的索引中读取数据 * 在这些索引中，仅读取"点击"类别的事件 * 在这些文档中，仅读取"类别"、"@timestamp"和"消息"字段。

有关可用集群和索引权限的完整列表

有两种可用的机制来定义角色：使用 _Role ManagementAPIs_ 或在 Elasticsearch 节点上的本地文件中。还可以实现自定义角色提供程序。如果需要与其他系统集成以检索用户角色，则可以构建自定义角色提供程序插件。有关更多信息，请参阅自定义角色和授权。

### 角色管理界面

您可以在 Kibana 中轻松管理用户和角色。要管理角色，请登录 toKibana 并转到 **管理 / 安全 / 角色**。

### 角色管理接口

_Role管理APIs_使您能够动态添加、更新、删除和检索角色。当您使用 API 管理"本机"领域中的角色时，角色存储在内部 Elasticsearch 索引中。有关详细信息和示例，请参阅角色。

### 基于文件的角色管理

除了_Role管理APIs_，角色也可以在位于"ES_PATH_CONF"的local'roles.yml'文件中定义。这是一个 YAML 文件，其中每个角色定义都按其名称进行键控。

如果在"roles.yml"文件中使用相同的角色名称，并且通过_RoleManagement APIs_，则将使用在文件中找到的角色。

虽然_Role管理APIs_是定义角色的首选机制，但如果要定义固定角色，使用"roles.yml"文件会很有用，没有人(除了对Elasticsearch节点具有物理访问权限的管理员)能够更改。但请注意，"roles.yml"文件是作为最小的管理功能提供的，并不打算涵盖和用于定义所有用例的角色。

您无法使用角色管理 UI 或角色管理 API 查看、编辑或删除在"roles.yml"中定义的任何角色。

"roles.yml"文件由节点在本地管理，而不是由群集全局管理。这意味着，对于典型的多节点群集，需要在群集中的每个节点上应用完全相同的更改。

更安全的方法是在其中一个节点上应用更改，并将"roles.yml"分发/复制到群集中的所有其他节点(手动或使用配置管理系统，如Puppet或Chef)。

以下代码片段显示了"roles.yml"文件配置的示例：

    
    
    click_admins:
      run_as: [ 'clicks_watcher_1' ]
      cluster: [ 'monitor' ]
      indices:
        - names: [ 'events-*' ]
          privileges: [ 'read' ]
          field_security:
            grant: ['category', '@timestamp', 'message' ]
          query: '{"match": {"category": "click"}}'

Elasticsearch 持续监控 'roles.yml' 文件，并自动选取并应用任何更改。

[« Built-in roles](built-in-roles.md) [Role restriction »](role-
restriction.md)
