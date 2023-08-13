

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« URI parts processor](uri-parts-processor.md) [Aliases »](aliases.md)

## 用户代理处理器

"user_agent"处理器从浏览器随其 Web 请求一起发送的用户代理字符串中提取详细信息。此处理器默认在"user_agent"字段下添加此信息。

默认情况下，ingest-user-agent 模块附带由 uap-java 提供的 regexes.yaml 和 Apache 2.0 许可证。有关更多详细信息，请参阅<https://github.com/ua-parser/uap-core>。

### 在管道中使用user_agent处理器

**表 48.用户代理选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

包含用户代理字符串的字段。   "target_field"

|

no

|

user_agent

|

将使用用户代理详细信息填充的字段。   "regex_file"

|

no

|

-

|

"config/ingest-user-agent"目录中的文件的名称，其中包含用于解析用户代理字符串的正则表达式。目录和文件都必须在启动 Elasticsearch 之前创建。如果未指定，ingest-user-agent 将使用它附带的 uap-core 中的 regexes.yaml(见下文)。   "属性"

|

no

|

["名称"、"主要"、"次要"、"补丁"、"内部版本"、"操作系统"、"os_name"、"os_major"、"os_minor"、"设备"]

|

控制将哪些属性添加到"target_field"。   "extract_device_type"

|

no

|

`false`

|

[测试版] 此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。 尽最大努力从用户代理字符串中提取设备类型。   "ignore_missing"

|

no

|

`false`

|

如果"true"和"field"不存在，处理器将悄悄退出而不修改文档 下面是一个基于"代理"字段将用户代理详细信息添加到"user_agent"字段的示例：

    
    
    response = client.ingest.put_pipeline(
      id: 'user_agent',
      body: {
        description: 'Add user agent information',
        processors: [
          {
            user_agent: {
              field: 'agent'
            }
          }
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'my_id',
      pipeline: 'user_agent',
      body: {
        agent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
      }
    )
    puts response
    
    response = client.get(
      index: 'my-index-000001',
      id: 'my_id'
    )
    puts response
    
    
    PUT _ingest/pipeline/user_agent
    {
      "description" : "Add user agent information",
      "processors" : [
        {
          "user_agent" : {
            "field" : "agent"
          }
        }
      ]
    }
    PUT my-index-000001/_doc/my_id?pipeline=user_agent
    {
      "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    }
    GET my-index-000001/_doc/my_id

哪个返回

    
    
    {
      "found": true,
      "_index": "my-index-000001",
      "_id": "my_id",
      "_version": 1,
      "_seq_no": 22,
      "_primary_term": 1,
      "_source": {
        "agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        "user_agent": {
          "name": "Chrome",
          "original": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
          "version": "51.0.2704.103",
          "os": {
            "name": "Mac OS X",
            "version": "10.10.5",
            "full": "Mac OS X 10.10.5"
          },
          "device" : {
            "name" : "Mac"
          }
        }
      }
    }

#### 使用自定义正则表达式文件

要使用自定义正则表达式文件来解析用户代理，该文件必须放入"config/ingest-user-agent"目录中，并且必须具有".yml"文件扩展名。该文件必须在节点启动时存在，对它的任何更改或在节点运行时添加的任何新文件都不会产生任何影响。

在实践中，任何自定义正则表达式文件都是默认文件的变体，无论是较新版本还是自定义版本，都是最有意义的。

"ingest-user-agent"中包含的默认文件是"regexes.yaml"fromuap-core：<https://github.com/ua-parser/uap-core/blob/master/regexes.yaml>

#### 节点设置

"user_agent"处理器支持以下设置：

`ingest.user_agent.cache_size`

     The maximum number of results that should be cached. Defaults to `1000`. 

请注意，这些设置是节点设置，适用于所有"user_agent"处理器，即所有定义的"user_agent"处理器都有一个缓存。

[« URI parts processor](uri-parts-processor.md) [Aliases »](aliases.md)
