

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Set processor](set-processor.md) [Sort processor »](sort-processor.md)

## 设置安全用户处理器

通过预处理收录，将当前经过身份验证的用户相关的详细信息(例如"用户名"、"角色"、"电子邮件"、"full_name"、"元数据"、"api_key"、"领域"和"authentication_type")从当前经过身份验证的用户设置到当前文档。仅当用户使用 API 密钥进行身份验证时，"api_key"属性才存在。它是一个对象，包含 API 密钥的"id"、"名称"和"元数据"(如果存在且为非空)字段。"realm"属性也是一个具有两个字段的对象，"name"和"type"。使用 API 密钥身份验证时，"领域"属性是指从中创建 API 密钥的领域。'authentication_type' 属性是一个字符串，可以从 'REALM'、'API_KEY'、'TOKEN' 和 'ANONYMOUS' 中获取值。

索引请求需要经过身份验证的用户。

**表 41.设置安全用户选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

要将用户信息存储到的字段。   "属性"

|

no

|

["用户名"、"角色"、"电子邮件"、"full_name"、"元数据"、"api_key"、"领域"、"authentication_type"]

|

控制将哪些用户相关属性添加到"字段"。   "说明"

|

no

|

-

|

处理器的说明。用于描述处理器的目的或其配置。   "如果"

|

no

|

-

|

有条件地执行处理器。请参阅有条件运行处理器。   "ignore_failure"

|

no

|

`false`

|

忽略处理器的故障。请参阅处理管道故障。   "on_failure"

|

no

|

-

|

处理处理器的故障。请参阅处理管道故障。   "标签"

|

no

|

-

|

处理器的标识符。对于调试和指标很有用。   以下示例将当前经过身份验证的用户的所有用户详细信息添加到此管道处理的所有文档的"user"字段中：

    
    
    {
      "processors" : [
        {
          "set_security_user": {
            "field": "user"
          }
        }
      ]
    }

[« Set processor](set-processor.md) [Sort processor »](sort-processor.md)
