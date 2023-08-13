

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Redact processor](redact-processor.md) [Remove processor »](remove-
processor.md)

## 已注册的域处理器

从完全限定域名 (FQDN) 中提取已注册域(也称为有效顶级域或 eTLD)、子域和顶级域。使用 Mozilla Public 后缀列表中定义的已注册域。

**表 35.注册域名选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

|

包含源 FQDN 的字段。   "target_field"

|

no

|

"<空字符串>"

|

包含提取的域组件的对象字段。如果是"<空字符串>"，处理器会将组件添加到文档的根目录。   "ignore_missing"

|

no

|

`true`

|

如果缺少"true"并且缺少任何必填字段，处理器将静默退出而不修改文档。   "说明"

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

处理器的标识符。对于调试和指标很有用。   #####Examplesedit

以下示例说明了已注册的域处理器的用法：

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          processors: [
            {
              registered_domain: {
                field: 'fqdn',
                target_field: 'url'
              }
            }
          ]
        },
        docs: [
          {
            _source: {
              fqdn: 'www.example.ac.uk'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _ingest/pipeline/_simulate
    {
      "pipeline": {
        "processors": [
          {
            "registered_domain": {
              "field": "fqdn",
              "target_field": "url"
            }
          }
        ]
      },
      "docs": [
        {
          "_source": {
            "fqdn": "www.example.ac.uk"
          }
        }
      ]
    }

这将产生以下结果：

    
    
    {
      "docs": [
        {
          "doc": {
            ...
            "_source": {
              "fqdn": "www.example.ac.uk",
              "url": {
                "subdomain": "www",
                "registered_domain": "example.ac.uk",
                "top_level_domain": "ac.uk",
                "domain": "www.example.ac.uk"
              }
            }
          }
        }
      ]
    }

[« Redact processor](redact-processor.md) [Remove processor »](remove-
processor.md)
