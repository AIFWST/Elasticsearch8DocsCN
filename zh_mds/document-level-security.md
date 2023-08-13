

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authorization](authorization.md)

[« Security privileges](security-privileges.md) [Field level security
»](field-level-security.md)

## 文档级安全性

文档级安全性限制用户具有读取访问权限的文档。特别是，它限制了可以从基于文档的读取 API 访问哪些文档。

若要启用文档级安全性，请使用查询来指定每个角色可以访问的文档。文档"query"与特定的数据流、索引或通配符 ('*') 模式相关联，并与为数据流和索引指定的特权一起运行。

指定的文档"查询"：

* 期望与搜索请求中定义的格式相同 * 支持模板化角色查询，可以访问当前经过身份验证的用户的详细信息 * 接受以字符串值或嵌套 JSON 形式编写的查询 * 支持大多数 Elasticsearch Query 域特定语言 (DSL)，但对字段和文档级安全性有一些限制

省略"query"参数将完全禁用相应索引权限条目的文档级安全性。

以下角色定义仅授予对所有"events-*"数据流和索引中属于"单击"类别的文档的读取访问权限：

    
    
    POST /_security/role/click_role
    {
      "indices": [
        {
          "names": [ "events-*" ],
          "privileges": [ "read" ],
          "query": "{\"match\": {\"category\": \"click\"}}"
        }
      ]
    }

您可以使用嵌套的 JSON 语法编写相同的查询：

    
    
    POST _security/role/click_role
    {
      "indices": [
        {
          "names": [ "events-*" ],
          "privileges": [ "read" ],
          "query": {
            "match": {
              "category": "click"
            }
          }
        }
      ]
    }

以下角色仅授予对"department_id"等于"12"的文档的读取访问权限：

    
    
    POST /_security/role/dept_role
    {
      "indices" : [
        {
          "names" : [ "*" ],
          "privileges" : [ "read" ],
          "query" : {
            "term" : { "department_id" : 12 }
          }
        }
      ]
    }

[« Security privileges](security-privileges.md) [Field level security
»](field-level-security.md)
