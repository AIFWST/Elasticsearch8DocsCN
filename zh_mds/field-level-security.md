

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authorization](authorization.md)

[« Document level security](document-level-security.md) [Granting privileges
for data streams and aliases »](securing-aliases.md)

## 字段级安全性

字段级别安全性限制用户具有读取访问权限的字段。特别是，它限制了可以从基于文档的 readAPI 访问哪些字段。

若要启用字段级别安全性，请指定每个角色可以访问的字段作为角色定义中的索引权限的一部分。因此，字段级安全性绑定到一组明确定义的数据流或索引(以及一组文档)。

以下角色定义仅授予对所有"events-*"数据流和索引中的"类别"、"@timestamp"和"消息"字段的读取访问权限。

    
    
    POST /_security/role/test_role1
    {
      "indices": [
        {
          "names": [ "events-*" ],
          "privileges": [ "read" ],
          "field_security" : {
            "grant" : [ "category", "@timestamp", "message" ]
          }
        }
      ]
    }

始终允许访问以下元数据字段："_id"、"_type"、"_parent"、"_routing"、"_timestamp"、"_ttl"、"_size"和"_index"。如果指定空字段列表，则只能访问这些元数据字段。

省略字段条目将完全禁用字段级别安全性。

您还可以指定字段表达式。例如，以下示例授予对以"event_"前缀开头的所有字段的读取访问权限：

    
    
    POST /_security/role/test_role2
    {
      "indices" : [
        {
          "names" : [ "*" ],
          "privileges" : [ "read" ],
          "field_security" : {
            "grant" : [ "event_*" ]
          }
        }
      ]
    }

使用点表示法来引用更复杂的文档中的嵌套字段。例如，假设以下文档：

    
    
    {
      "customer": {
        "handle": "Jim",
        "email": "jim@mycompany.com",
        "phone": "555-555-5555"
      }
    }

以下角色定义仅允许对客户"句柄"字段进行读取访问：

    
    
    POST /_security/role/test_role3
    {
      "indices" : [
        {
          "names" : [ "*" ],
          "privileges" : [ "read" ],
          "field_security" : {
            "grant" : [ "customer.handle" ]
          }
        }
      ]
    }

这就是通配符支持的亮点。例如，使用"customer.*"启用对"客户"数据的只读访问权限：

    
    
    POST /_security/role/test_role4
    {
      "indices" : [
        {
          "names" : [ "*" ],
          "privileges" : [ "read" ],
          "field_security" : {
            "grant" : [ "customer.*" ]
          }
        }
      ]
    }

您可以使用以下语法拒绝访问字段的权限：

    
    
    POST /_security/role/test_role5
    {
      "indices" : [
        {
          "names" : [ "*" ],
          "privileges" : [ "read" ],
          "field_security" : {
            "grant" : [ "*"],
            "except": [ "customer.handle" ]
          }
        }
      ]
    }

以下规则适用：

* 角色中缺少"field_security"等同于 * 访问权限。  * 如果已明确授予某些字段的权限，则可以指定拒绝字段。拒绝的字段必须是被授予权限的字段的子集。  * 定义拒绝和授权字段意味着访问所有已授予字段，但与拒绝字段中的模式匹配的字段除外。

例如：

    
    
    POST /_security/role/test_role6
    {
      "indices" : [
        {
          "names" : [ "*" ],
          "privileges" : [ "read" ],
          "field_security" : {
            "except": [ "customer.handle" ],
            "grant" : [ "customer.*" ]
          }
        }
      ]
    }

在上面的示例中，用户可以读取前缀为"客户"的所有字段。除了"客户.句柄"。

"grant"的空数组(例如，"grant"：[]")表示尚未授予对任何字段的访问权限。

当用户具有多个指定字段级别权限的角色时，每个数据流或索引生成的字段级别权限是各个角色权限的并集。例如，如果合并了这两个角色：

    
    
    POST /_security/role/test_role7
    {
      "indices" : [
        {
          "names" : [ "*" ],
          "privileges" : [ "read" ],
          "field_security" : {
            "grant": [ "a.*" ],
            "except" : [ "a.b*" ]
          }
        }
      ]
    }
    
    POST /_security/role/test_role8
    {
      "indices" : [
        {
          "names" : [ "*" ],
          "privileges" : [ "read" ],
          "field_security" : {
            "grant": [ "a.b*" ],
            "except" : [ "a.b.c*" ]
          }
        }
      ]
    }

生成的权限等于：

    
    
    {
      // role 1 + role 2
      ...
      "indices" : [
        {
          "names" : [ "*" ],
          "privileges" : [ "read" ],
          "field_security" : {
            "grant": [ "a.*" ],
            "except" : [ "a.b.c*" ]
          }
        }
      ]
    }

不应在"别名"字段上设置字段级安全性。要保护具体字段，必须直接使用其字段名称。

有关详细信息，请参阅设置字段和文档级别安全性。

[« Document level security](document-level-security.md) [Granting privileges
for data streams and aliases »](securing-aliases.md)
