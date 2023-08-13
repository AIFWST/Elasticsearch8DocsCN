

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« URL decode processor](urldecode-processor.md) [User agent processor
»](user-agent-processor.md)

## URI 部件处理器

分析统一资源标识符 (URI) 字符串并将其组件提取为对象。此 URI 对象包括 URI 的域、路径、片段、端口、查询、方案、用户信息、用户名和密码的属性。

**表 47.URI 部件选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

包含 URI 字符串的字段。   "target_field"

|

no

|

`url`

|

URI 对象的输出字段。   "keep_original"

|

no

|

true

|

如果为"true"，处理器会将未解析的 URI 复制到"<target_field>.original"。   "remove_if_successful"

|

no

|

false

|

如果为"true"，则处理器在解析 URI 字符串后删除"字段"。如果解析失败，处理器不会删除"字段"。   "ignore_missing"

|

no

|

`false`

|

如果"true"和"field"不存在，处理器将静默退出，而不修改文档"描述"

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

处理器的标识符。对于调试和指标很有用。   下面是 URI 部件处理器的示例定义：

    
    
    {
      "description" : "...",
      "processors" : [
        {
          "uri_parts": {
            "field": "input_field",
            "target_field": "url",
            "keep_original": true,
            "remove_if_successful": false
          }
        }
      ]
    }

当上述处理器在以下文档上执行时：

    
    
    {
      "_source": {
        "input_field": "http://myusername:mypassword@www.example.com:80/foo.gif?key1=val1&key2=val2#fragment"
      }
    }

它产生以下结果：

    
    
    "_source" : {
      "input_field" : "http://myusername:mypassword@www.example.com:80/foo.gif?key1=val1&key2=val2#fragment",
      "url" : {
        "path" : "/foo.gif",
        "fragment" : "fragment",
        "extension" : "gif",
        "password" : "mypassword",
        "original" : "http://myusername:mypassword@www.example.com:80/foo.gif?key1=val1&key2=val2#fragment",
        "scheme" : "http",
        "port" : 80,
        "user_info" : "myusername:mypassword",
        "domain" : "www.example.com",
        "query" : "key1=val1&key2=val2",
        "username" : "myusername"
      }
    }

[« URL decode processor](urldecode-processor.md) [User agent processor
»](user-agent-processor.md)
