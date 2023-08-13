

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Enrich APIs](enrich-apis.md)

[« Create enrich policy API](put-enrich-policy-api.md) [Get enrich policy
API »](get-enrich-policy-api.md)

## 删除扩充策略接口

删除现有扩充策略及其扩充索引。

    
    
    response = client.enrich.delete_policy(
      name: 'my-policy'
    )
    puts response
    
    
    DELETE /_enrich/policy/my-policy

###Request

"删除/_enrich/策略/<enrich-policy>"

###Prerequisites

如果您使用 Elasticsearch 安全功能，则必须具备：

* 使用的任何索引的"读取"索引权限 * "enrich_user"内置角色

###Description

使用删除扩充策略 API 删除现有扩充策略及其扩充索引。

在删除之前，必须从任何正在使用的引入管道中删除扩充策略。无法删除正在使用的扩充策略。

### 路径参数

`<enrich-policy>`

     (Required, string) Enrich policy to delete. 

[« Create enrich policy API](put-enrich-policy-api.md) [Get enrich policy
API »](get-enrich-policy-api.md)
