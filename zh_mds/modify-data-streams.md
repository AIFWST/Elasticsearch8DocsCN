

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
streams](data-streams.md)

[« Use a data stream](use-a-data-stream.md) [Time series data stream (TSDS)
»](tsds.md)

## 修改数据流

### 更改数据流的映射和设置

每个数据流都有一个匹配的索引模板。此模板中的映射和索引设置将应用于为流创建的新支持索引。这包括流的第一个后备索引，该索引是在创建流时自动生成的。

在创建数据流之前，我们建议您仔细考虑要包含在此模板中的映射和设置。

如果以后需要更改数据流的映射或设置，您有以下几种选择：

* 向数据流添加新的字段映射 * 更改数据流中的现有字段映射 * 更改数据流的动态索引设置 * 更改数据流的静态索引设置

如果您的更改包括对现有字段映射或静态索引设置的修改，则通常需要 areindex 才能将更改应用于数据流的支持索引。如果已在执行重新索引，则可以使用相同的过程添加新的字段映射并更改动态索引设置。请参阅使用重新编制索引来更改映射或设置。

#### 向数据流添加新字段映射

若要将新字段的映射添加到数据流，请执行以下步骤：

1. 更新数据流使用的索引模板。这可确保将新的字段映射添加到为流创建的未来支持索引中。

例如，"my-data-stream-template"是"my-data-stream"使用的现有索引模板。

以下创建或更新索引模板请求将新字段"message"的映射添加到模板。

    
        PUT /_index_template/my-data-stream-template
    {
      "index_patterns": [ "my-data-stream*" ],
      "data_stream": { },
      "priority": 500,
      "template": {
        "mappings": {
          "properties": {
            "message": {                              __"type": "text"
            }
          }
        }
      }
    }

__

|

为新的"消息"字段添加映射。   ---|--- 2.使用更新映射 API 将新的字段映射添加到数据流。默认情况下，这会将映射添加到流的现有支持索引，包括写入索引。

以下更新映射 API 请求将新的"消息"字段映射到"我的数据流"。

    
        PUT /my-data-stream/_mapping
    {
      "properties": {
        "message": {
          "type": "text"
        }
      }
    }

若要仅将映射添加到流的写入索引，请将更新映射 API 的"write_index_only"查询参数设置为"true"。

以下更新映射请求仅将新的"消息"字段映射添加到"my-data-stream"的写入索引。新的字段映射不会添加到流的其他支持索引中。

    
        PUT /my-data-stream/_mapping?write_index_only=true
    {
      "properties": {
        "message": {
          "type": "text"
        }
      }
    }

#### 更改数据流中的现有字段映射

每个映射参数的文档指示是否可以使用更新映射 API 为现有字段更新它。若要更新现有字段的这些参数，请执行以下步骤：

1. 更新数据流使用的索引模板。这可确保将更新的字段映射添加到为流创建的未来支持索引中。

例如，"my-data-stream-template"是"my-data-stream"使用的现有索引模板。

以下创建或更新索引模板请求将"host.ip"字段的"ignore_malformed"映射参数的参数更改为"true"。

    
        PUT /_index_template/my-data-stream-template
    {
      "index_patterns": [ "my-data-stream*" ],
      "data_stream": { },
      "priority": 500,
      "template": {
        "mappings": {
          "properties": {
            "host": {
              "properties": {
                "ip": {
                  "type": "ip",
                  "ignore_malformed": true            __}
              }
            }
          }
        }
      }
    }

__

|

将"host.ip"字段的"ignore_malformed"值更改为"true"。   ---|--- 2.使用更新映射 API 将映射更改应用于数据流。默认情况下，这会将更改应用于流的现有支持索引，包括写入索引。

以下更新映射 API 请求以"我的数据流"为目标。该请求将"host.ip"字段的"ignore_malformed"映射参数的参数更改为"true"。

    
        response = client.indices.put_mapping(
      index: 'my-data-stream',
      body: {
        properties: {
          host: {
            properties: {
              ip: {
                type: 'ip',
                ignore_malformed: true
              }
            }
          }
        }
      }
    )
    puts response
    
        PUT /my-data-stream/_mapping
    {
      "properties": {
        "host": {
          "properties": {
            "ip": {
              "type": "ip",
              "ignore_malformed": true
            }
          }
        }
      }
    }

若要仅将映射更改应用于流的写入索引，请将 putmapping API 的"write_index_only"查询参数设置为"true"。

以下更新映射请求仅更改"我的数据流"写入索引的"host.ip"字段的映射。此更改不会应用于流的其他支持索引。

    
        response = client.indices.put_mapping(
      index: 'my-data-stream',
      write_index_only: true,
      body: {
        properties: {
          host: {
            properties: {
              ip: {
                type: 'ip',
                ignore_malformed: true
              }
            }
          }
        }
      }
    )
    puts response
    
        PUT /my-data-stream/_mapping?write_index_only=true
    {
      "properties": {
        "host": {
          "properties": {
            "ip": {
              "type": "ip",
              "ignore_malformed": true
            }
          }
        }
      }
    }

除了支持的映射参数外，我们不建议您更改现有字段的映射或字段数据类型，即使在数据流的匹配索引模板或其后备索引中也是如此。更改现有字段的映射可能会使已编制索引的任何数据无效。

如果需要更改现有字段的映射，请创建新的数据流并将数据重新索引到其中。请参阅使用重新索引更改映射或设置。

#### 更改数据流的动态索引设置

若要更改数据流的动态索引设置，请执行以下步骤：

1. 更新数据流使用的索引模板。这可确保将设置应用于为流创建的未来支持索引。

例如，"my-data-stream-template"是"my-data-stream"使用的现有索引模板。

以下创建或更新索引模板请求将模板的"index.refresh_interval"索引设置更改为"30s"(30 秒)。

    
        PUT /_index_template/my-data-stream-template
    {
      "index_patterns": [ "my-data-stream*" ],
      "data_stream": { },
      "priority": 500,
      "template": {
        "settings": {
          "index.refresh_interval": "30s"             __}
      }
    }

__

|

将"index.refresh_interval"设置更改为"30 秒"(30 秒)。   ---|--- 2.使用更新索引设置 API 更新数据流的索引设置。默认情况下，这会将设置应用于流的现有支持索引，包括写入索引。

以下更新索引设置 API 请求更新"我的数据流"的"index.refresh_interval"设置。

    
        response = client.indices.put_settings(
      index: 'my-data-stream',
      body: {
        index: {
          refresh_interval: '30s'
        }
      }
    )
    puts response
    
        PUT /my-data-stream/_settings
    {
      "index": {
        "refresh_interval": "30s"
      }
    }

要更改"index.lifecycle.name"设置，请首先使用删除策略 API 删除现有的 ILM 策略。请参阅切换生命周期策略。

#### 更改数据流的静态索引设置

静态索引设置只能在创建后备索引时设置。无法使用更新索引设置 API 更新静态索引设置。

要将新的静态设置应用于将来的支持索引，请更新数据流使用的索引模板。该设置将自动应用于更新后创建的任何后备索引。

例如，"my-data-stream-template"是"my-data-stream"使用的现有索引模板。

以下创建或更新索引模板 API 请求将新的"sort.field"和"sort.order index"设置添加到模板。

    
    
    PUT /_index_template/my-data-stream-template
    {
      "index_patterns": [ "my-data-stream*" ],
      "data_stream": { },
      "priority": 500,
      "template": {
        "settings": {
          "sort.field": [ "@timestamp"],             __"sort.order": [ "desc"] __}
      }
    }

__

|

添加"排序字段"索引设置。   ---|---    __

|

添加"排序.顺序"索引设置。   如果需要，您可以滚动访问数据流以立即将设置应用于数据流的写入索引。这会影响滚动更新后添加到流的任何新数据。但是，它不会影响数据流的现有后备索引或现有数据。

要将静态设置更改应用于现有后备索引，必须创建新的数据流并将数据重新索引到其中。请参阅使用重新索引更改映射或设置。

#### 使用重新索引更改映射或设置

您可以使用重新索引来更改数据流的映射或设置。更改现有字段的数据类型或更新后备索引的静态索引设置通常需要执行此操作。

要为数据流重新编制索引，请首先创建或更新索引模板，使其包含所需的映射或设置更改。然后，您可以将现有数据流重新索引为与模板匹配的新流。这会将模板中的映射和设置更改应用于每个文档，并支持索引添加到新数据流。这些更改还会影响新流创建的任何未来支持索引。

请按照以下步骤操作：

1. 为新数据流选择名称或索引模式。此新数据流将包含现有流中的数据。

您可以使用解析索引 API 检查名称或模式是否与任何现有索引、别名或数据流匹配。如果是这样，您应该考虑使用其他名称或模式。

以下解析索引 API 请求检查以"新数据流"开头的任何现有索引、别名或数据流。如果没有，则可以使用"新数据流*"索引模式来创建新的数据流。

    
        response = client.indices.resolve_index(
      name: 'new-data-stream*'
    )
    puts response
    
        GET /_resolve/index/new-data-stream*

API 返回以下响应，指示没有与此模式匹配的现有目标。

    
        {
      "indices": [ ],
      "aliases": [ ],
      "data_streams": [ ]
    }

2. 创建或更新索引模板。此模板应包含要应用于新数据流的支持索引的映射和设置。

此索引模板必须满足数据流模板的要求。它还应该在"index_patterns"属性中包含您之前选择的名称或索引模式。

如果您只添加或更改一些内容，我们建议您通过复制现有模板并根据需要对其进行修改来创建新模板。

例如，"my-data-stream-template"是"my-data-stream"使用的现有索引模板。

以下创建或更新索引模板 API 请求创建新的索引模板"新数据流模板"。"new-data-stream-template"使用"my-data-stream-template"作为其基础，但有以下更改：

    * The index pattern in `index_patterns` matches any index or data stream starting with `new-data-stream`. 
    * The `@timestamp` field mapping uses the `date_nanos` field data type rather than the `date` data type. 
    * The template includes `sort.field` and `sort.order` index settings, which were not in the original `my-data-stream-template` template. 
    
        response = client.indices.put_index_template(
      name: 'new-data-stream-template',
      body: {
        index_patterns: [
          'new-data-stream*'
        ],
        data_stream: {},
        priority: 500,
        template: {
          mappings: {
            properties: {
              "@timestamp": {
                type: 'date_nanos'
              }
            }
          },
          settings: {
            "sort.field": [
              '@timestamp'
            ],
            "sort.order": [
              'desc'
            ]
          }
        }
      }
    )
    puts response
    
        PUT /_index_template/new-data-stream-template
    {
      "index_patterns": [ "new-data-stream*" ],
      "data_stream": { },
      "priority": 500,
      "template": {
        "mappings": {
          "properties": {
            "@timestamp": {
              "type": "date_nanos"                 __}
          }
        },
        "settings": {
          "sort.field": [ "@timestamp"], __"sort.order": [ "desc"] __}
      }
    }

__

|

将"@timestamp"字段映射更改为"date_nanos"字段数据类型。   ---|---    __

|

添加"排序字段"索引设置。   __

|

添加"排序.顺序"索引设置。     3. 使用创建数据流 API 手动创建新数据流。数据流的名称必须与新模板的"index_patterns"属性中定义的索引模式匹配。

我们不建议为创建新数据流编制索引。稍后，您需要将现有数据流中的旧数据重新索引到此新流中。这可能会导致一个或多个包含新旧数据混合的后备索引。

**在数据流中混合新旧数据**

虽然混合新旧数据是安全的，但它可能会干扰数据保留。如果删除较旧的索引，则可能会意外删除同时包含新数据和旧数据的后备索引。为了防止过早丢失数据，您需要保留这样的后备索引，直到您准备好删除其最新数据。

以下创建数据流 API 请求以"新数据流"为目标，该请求与"新数据流模板"的索引模式匹配。由于没有现有索引或数据流使用此名称，因此此请求将创建"新数据流"数据流。

    
        response = client.indices.create_data_stream(
      name: 'new-data-stream'
    )
    puts response
    
        PUT /_data_stream/new-data-stream

4. 如果您不想在新数据流中混合使用新旧数据，请暂停新文档的索引。虽然混合新旧数据是安全的，但它可能会干扰数据保留。请参阅在数据流中混合新旧数据。  5. 如果使用 ILM 自动滚动更新，请缩短 ILM 轮询间隔。这可确保当前写入索引在等待滚动更新检查时不会变得太大。默认情况下，ILM 每 10 分钟检查一次滚动更新条件。

以下群集更新设置 API 请求将"indices.lifecycle.poll_interval"设置降低到"1m"(一分钟)。

    
        response = client.cluster.put_settings(
      body: {
        persistent: {
          "indices.lifecycle.poll_interval": '1m'
        }
      }
    )
    puts response
    
        PUT /_cluster/settings
    {
      "persistent": {
        "indices.lifecycle.poll_interval": "1m"
      }
    }

6. 使用"创建"的"op_type"将数据重新索引到新的数据流。

如果要按照最初编制索引的顺序对数据进行分区，可以运行单独的重新索引请求。这些重新索引请求可以使用单个后备索引作为源。您可以使用获取数据流 API 来检索支持索引的列表。

例如，您计划将数据从"我的数据流"重新索引为"新数据流"。但是，您希望为"my-data-stream"中的每个支持索引提交单独的重新索引请求，从最早的支持索引开始。这将保留最初为数据编制索引的顺序。

以下获取数据流 API 请求检索有关"my-data-stream"的信息，包括其后备索引的列表。

    
        response = client.indices.get_data_stream(
      name: 'my-data-stream'
    )
    puts response
    
        GET /_data_stream/my-data-stream

响应的"索引"属性包含流的当前支持索引的数组。数组中的第一项包含有关流最旧的支持索引的信息。

    
        {
      "data_streams": [
        {
          "name": "my-data-stream",
          "timestamp_field": {
            "name": "@timestamp"
          },
          "indices": [
            {
              "index_name": ".ds-my-data-stream-2099.03.07-000001", __"index_uuid": "Gpdiyq8sRuK9WuthvAdFbw"
            },
            {
              "index_name": ".ds-my-data-stream-2099.03.08-000002",
              "index_uuid": "_eEfRrFHS9OyhqWntkgHAQ"
            }
          ],
          "generation": 2,
          "status": "GREEN",
          "template": "my-data-stream-template",
          "hidden": false,
          "system": false,
          "allow_custom_routing": false,
          "replicated": false
        }
      ]
    }

__

|

"我的数据流"的"索引"数组中的第一项。此项包含有关流最早的支持索引".ds-my-data-stream-2099.03.07-000001"的信息。   ---|--- 以下重新索引 API 请求将文档从".ds-my-data-stream-2099.03.07-000001"复制到"new-data-stream"。请求的"op_type"是"创建"。

    
        response = client.reindex(
      body: {
        source: {
          index: '.ds-my-data-stream-2099.03.07-000001'
        },
        dest: {
          index: 'new-data-stream',
          op_type: 'create'
        }
      }
    )
    puts response
    
        POST /_reindex
    {
      "source": {
        "index": ".ds-my-data-stream-2099.03.07-000001"
      },
      "dest": {
        "index": "new-data-stream",
        "op_type": "create"
      }
    }

您还可以使用查询仅对每个请求的文档子集重新编制索引。

以下重新索引 API 请求将文档从"我的数据流"复制到"新数据流"。该请求使用"范围"查询仅对具有上周内时间戳的文档重新编制索引。请注意，请求的"op_type"是"创建"。

    
        response = client.reindex(
      body: {
        source: {
          index: 'my-data-stream',
          query: {
            range: {
              "@timestamp": {
                gte: 'now-7d/d',
                lte: 'now/d'
              }
            }
          }
        },
        dest: {
          index: 'new-data-stream',
          op_type: 'create'
        }
      }
    )
    puts response
    
        POST /_reindex
    {
      "source": {
        "index": "my-data-stream",
        "query": {
          "range": {
            "@timestamp": {
              "gte": "now-7d/d",
              "lte": "now/d"
            }
          }
        }
      },
      "dest": {
        "index": "new-data-stream",
        "op_type": "create"
      }
    }

7. 如果您之前更改了 ILM 轮询间隔，请在重新编制索引完成后将其更改回其原始值。这可以防止主节点上不必要的负载。

以下群集更新设置 API 请求将"indices.lifecycle.poll_interval"设置重置为其默认值。

    
        response = client.cluster.put_settings(
      body: {
        persistent: {
          "indices.lifecycle.poll_interval": nil
        }
      }
    )
    puts response
    
        PUT /_cluster/settings
    {
      "persistent": {
        "indices.lifecycle.poll_interval": null
      }
    }

8. 使用新数据流恢复索引。现在，对此流的搜索将查询新数据和重新编制索引的数据。  9. 确认所有重新编制索引的数据在新数据流中可用后，您可以安全地删除旧数据流。

以下删除数据流 API 请求删除"我的数据流"。此请求还会删除流的后备索引及其包含的任何数据。

    
        response = client.indices.delete_data_stream(
      name: 'my-data-stream'
    )
    puts response
    
        DELETE /_data_stream/my-data-stream

### 更新或向数据流添加别名

使用别名 API 更新现有数据流的别名。更改现有数据流在其索引模式中的别名不起作用。

例如，"logs"别名指向单个数据流。以下请求将流交换为别名。在此交换期间，"logs"别名没有停机时间，并且永远不会同时指向两个流。

    
    
    response = client.indices.update_aliases(
      body: {
        actions: [
          {
            remove: {
              index: 'logs-nginx.access-prod',
              alias: 'logs'
            }
          },
          {
            add: {
              index: 'logs-my_app-default',
              alias: 'logs'
            }
          }
        ]
      }
    )
    puts response
    
    
    POST _aliases
    {
      "actions": [
        {
          "remove": {
            "index": "logs-nginx.access-prod",
            "alias": "logs"
          }
        },
        {
          "add": {
            "index": "logs-my_app-default",
            "alias": "logs"
          }
        }
      ]
    }

[« Use a data stream](use-a-data-stream.md) [Time series data stream (TSDS)
»](tsds.md)
