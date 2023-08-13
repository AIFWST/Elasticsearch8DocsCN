

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Reroute processor](reroute-processor.md) [Set processor »](set-
processor.md)

## 脚本处理器

对传入的文档运行内联脚本或存储脚本。脚本在"引入"上下文中运行。

脚本处理器使用脚本缓存来避免为每个传入文档重新编译脚本。若要提高性能，请确保在生产中使用脚本处理器之前正确调整脚本缓存的大小。

**表 39.脚本选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'lang'

|

no

|

"painless"

|

脚本语言。   'id'

|

no

|

-

|

存储脚本的 ID。如果未指定"源"，则此参数是必需的。   "源"

|

no

|

-

|

内联脚本。如果未指定"id"，则此参数是必需的。   "参数"

|

no

|

-

|

包含脚本参数的对象。   "说明"

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

处理器的标识符。对于调试和指标很有用。   #### 访问源字段编辑

脚本处理器将每个传入文档的 JSON 源字段解析为一组映射、列表和基元。要使用 Painlessscript 访问这些字段，请使用映射访问运算符："ctx['my-field']"。您也可以使用速记'ctx。<my-field>'语法。

脚本处理器不支持"ctx['_source']['my-field']'"或'ctx._source。<my-field>'语法。

以下处理器使用无痛脚本从"env"源字段中提取"标签"字段。

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          processors: [
            {
              script: {
                description: "Extract 'tags' from 'env' field",
                lang: 'painless',
                source: "\n            String[] envSplit = ctx['env'].splitOnToken(params['delimiter']);\n            ArrayList tags = new ArrayList();\n            tags.add(envSplit[params['position']].trim());\n            ctx['tags'] = tags;\n          ",
                params: {
                  delimiter: '-',
                  position: 1
                }
              }
            }
          ]
        },
        docs: [
          {
            _source: {
              env: 'es01-prod'
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
            "script": {
              "description": "Extract 'tags' from 'env' field",
              "lang": "painless",
              "source": """
                String[] envSplit = ctx['env'].splitOnToken(params['delimiter']);
                ArrayList tags = new ArrayList();
                tags.add(envSplit[params['position']].trim());
                ctx['tags'] = tags;
              """,
              "params": {
                "delimiter": "-",
                "position": 1
              }
            }
          }
        ]
      },
      "docs": [
        {
          "_source": {
            "env": "es01-prod"
          }
        }
      ]
    }

处理器产生：

    
    
    {
      "docs": [
        {
          "doc": {
            ...
            "_source": {
              "env": "es01-prod",
              "tags": [
                "prod"
              ]
            }
          }
        }
      ]
    }

#### 访问元数据字段

您还可以使用脚本处理器访问元数据字段。以下处理器使用无痛脚本来设置传入文档的"_index"。

    
    
    response = client.ingest.simulate(
      body: {
        pipeline: {
          processors: [
            {
              script: {
                description: 'Set index based on `lang` field and `dataset` param',
                lang: 'painless',
                source: "\n            ctx['_index'] = ctx['lang'] + '-' + params['dataset'];\n          ",
                params: {
                  dataset: 'catalog'
                }
              }
            }
          ]
        },
        docs: [
          {
            _index: 'generic-index',
            _source: {
              lang: 'fr'
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
            "script": {
              "description": "Set index based on `lang` field and `dataset` param",
              "lang": "painless",
              "source": """
                ctx['_index'] = ctx['lang'] + '-' + params['dataset'];
              """,
              "params": {
                "dataset": "catalog"
              }
            }
          }
        ]
      },
      "docs": [
        {
          "_index": "generic-index",
          "_source": {
            "lang": "fr"
          }
        }
      ]
    }

处理器将文档的"_index"从"泛型索引"更改为"fr-catalog"。

    
    
    {
      "docs": [
        {
          "doc": {
            ...
            "_index": "fr-catalog",
            "_source": {
              "lang": "fr"
            }
          }
        }
      ]
    }

[« Reroute processor](reroute-processor.md) [Set processor »](set-
processor.md)
