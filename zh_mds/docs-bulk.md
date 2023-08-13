

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Document APIs](docs.md)

[« Multi get (mget) API](docs-multi-get.md) [Reindex API »](docs-
reindex.md)

## 批量接口

在单个 API 调用中执行多个索引或删除操作。这减少了开销，并可以大大提高索引速度。

    
    
    $params = [
        'body' => [
            [
                'index' => [
                    '_index' => 'test',
                    '_id' => '1',
                ],
            ],
            [
                'field1' => 'value1',
            ],
            [
                'delete' => [
                    '_index' => 'test',
                    '_id' => '2',
                ],
            ],
            [
                'create' => [
                    '_index' => 'test',
                    '_id' => '3',
                ],
            ],
            [
                'field1' => 'value3',
            ],
            [
                'update' => [
                    '_id' => '1',
                    '_index' => 'test',
                ],
            ],
            [
                'doc' => [
                    'field2' => 'value2',
                ],
            ],
        ],
    ];
    $response = $client->bulk($params);
    
    
    resp = client.bulk(
        body=[
            {"index": {"_index": "test", "_id": "1"}},
            {"field1": "value1"},
            {"delete": {"_index": "test", "_id": "2"}},
            {"create": {"_index": "test", "_id": "3"}},
            {"field1": "value3"},
            {"update": {"_id": "1", "_index": "test"}},
            {"doc": {"field2": "value2"}},
        ],
    )
    print(resp)
    
    
    response = client.bulk(
      body: [
        {
          index: {
            _index: 'test',
            _id: '1'
          }
        },
        {
          "field1": 'value1'
        },
        {
          delete: {
            _index: 'test',
            _id: '2'
          }
        },
        {
          create: {
            _index: 'test',
            _id: '3'
          }
        },
        {
          "field1": 'value3'
        },
        {
          update: {
            _id: '1',
            _index: 'test'
          }
        },
        {
          doc: {
            "field2": 'value2'
          }
        }
      ]
    )
    puts response
    
    
    res, err := es.Bulk(
    	strings.NewReader(`
    { "index" : { "_index" : "test", "_id" : "1" } }
    { "field1" : "value1" }
    { "delete" : { "_index" : "test", "_id" : "2" } }
    { "create" : { "_index" : "test", "_id" : "3" } }
    { "field1" : "value3" }
    { "update" : {"_id" : "1", "_index" : "test"} }
    { "doc" : {"field2" : "value2"} }
    `),
    )
    fmt.Println(res, err)
    
    
    const response = await client.bulk({
      body: [
        {
          index: {
            _index: 'test',
            _id: '1'
          }
        },
        {
          field1: 'value1'
        },
        {
          delete: {
            _index: 'test',
            _id: '2'
          }
        },
        {
          create: {
            _index: 'test',
            _id: '3'
          }
        },
        {
          field1: 'value3'
        },
        {
          update: {
            _id: '1',
            _index: 'test'
          }
        },
        {
          doc: {
            field2: 'value2'
          }
        }
      ]
    })
    console.log(response)
    
    
    POST _bulk
    { "index" : { "_index" : "test", "_id" : "1" } }
    { "field1" : "value1" }
    { "delete" : { "_index" : "test", "_id" : "2" } }
    { "create" : { "_index" : "test", "_id" : "3" } }
    { "field1" : "value3" }
    { "update" : {"_id" : "1", "_index" : "test"} }
    { "doc" : {"field2" : "value2"} }

###Request

"发布/_bulk"

"发布/<target>/_bulk"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须对目标数据流、索引或索引别名具有以下索引权限：

    * To use the `create` action, you must have the `create_doc`, `create`, `index`, or `write` index privilege. Data streams support only the `create` action. 
    * To use the `index` action, you must have the `create`, `index`, or `write` index privilege. 
    * To use the `delete` action, you must have the `delete` or `write` index privilege. 
    * To use the `update` action, you must have the `index` or `write` index privilege. 
    * To automatically create a data stream or index with a bulk API request, you must have the `auto_configure`, `create_index`, or `manage` index privilege. 
    * To make the result of a bulk operation visible to search using the `refresh` parameter, you must have the `maintenance` or `manage` index privilege. 

* 自动数据流创建需要启用数据流的匹配索引模板。请参阅_Set数据stream_。

###Description

提供一种在单个请求中执行多个"索引"、"创建"、"删除"和"更新"操作的方法。

操作使用换行符分隔的 JSON(NDJSON) 结构在请求正文中指定：

    
    
    action_and_meta_data\n
    optional_source\n
    action_and_meta_data\n
    optional_source\n
    ....
    action_and_meta_data\n
    optional_source\n

"index"和"create"操作需要在下一行有一个源，并且与标准索引API中的"op_type"参数具有相同的语义："创建"失败，如果目标中已存在具有相同ID的文档，则"index"根据需要添加或替换文档。

数据流仅支持"创建"操作。要更新或删除数据流中的文档，必须以包含该文档的后备索引为目标。请参阅更新或删除后备索引中的文档。

"update"期望在下一行指定部分文档、更新程序和脚本及其选项。

"delete"不需要下一行的源，并且具有与标准删除API相同的语义。

数据的最后一行必须以换行符"\n"结尾。每个换行符前面可以带有回车符"\r"。将 NDJSON 数据发送到"_bulk"端点时，请使用"application/json"或"application/x-ndjson"的"内容类型"标头。

由于此格式使用文本"\n"作为分隔符，因此请确保 JSON 操作和源未打印出来。

如果在<target>请求路径中提供""，则它用于未显式指定"_index"参数的任何操作。

关于格式的说明：这里的想法是尽可能快地处理它。由于某些操作被重定向到其他节点上的其他分片，因此在接收节点端仅解析"action_meta_data"。

使用此协议的客户端库应尝试并努力在客户端执行类似操作，并尽可能减少缓冲。

在单个批量请求中没有要执行的"正确"操作数。尝试不同的设置，为特定工作负载找到最佳大小。请注意，默认情况下，Elasticsearch 将 HTTPrequest 的最大大小限制为"100mb"，因此客户端必须确保没有请求超过此大小。无法为超过大小限制的单个文档编制索引，因此在将任何此类文档发送到 Elasticsearch 之前，您必须将任何此类文档预处理成更小的部分。例如，在索引文档之前将文档拆分为页面或章节，或者将原始二进制数据存储在 Elasticsearch 外部的系统中，并在发送到 Elasticsearch 的文档中将原始数据替换为指向外部系统的链接。

##### 客户端对批量请求的支持

一些官方支持的客户端提供了帮助程序来帮助批量请求和重新索引：

Go

     See [esutil.BulkIndexer](https://github.com/elastic/go-elasticsearch/tree/master/_examples/bulk#indexergo)
Perl

     See [Search::Elasticsearch::Client::5_0::Bulk](https://metacpan.org/pod/Search::Elasticsearch::Client::5_0::Bulk) and [Search::Elasticsearch::Client::5_0::Scroll](https://metacpan.org/pod/Search::Elasticsearch::Client::5_0::Scroll)
Python

     See [elasticsearch.helpers.*](https://elasticsearch-py.readthedocs.org/en/master/helpers.html)
JavaScript

     See [client.helpers.*](/guide/en/elasticsearch/client/javascript-api/current/client-helpers.html)
.NET

     See [`BulkAllObservable`](/guide/en/elasticsearch/client/net-api/current/indexing-documents.html)
PHP

     See [Bulk indexing](/guide/en/elasticsearch/client/php-api/current/indexing_documents.html#_bulk_indexing)

##### 使用 cURL 提交批量请求

如果要向"curl"提供文本文件输入，则必须使用"--data-binary"标志而不是纯"-d"。后者不保留换行符。例：

    
    
    $ cat requests
    { "index" : { "_index" : "test", "_id" : "1" } }
    { "field1" : "value1" }
    $ curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/_bulk --data-binary "@requests"; echo
    {"took":7, "errors": false, "items":[{"index":{"_index":"test","_id":"1","_version":1,"result":"created","forced_refresh":false}}]}

##### 乐观并发控制

批量 API 调用中的每个"索引"和"删除"操作都可以在其各自的操作和元数据行中包含"if_seq_no"和"if_primary_term"参数。"if_seq_no"和"if_primary_term"参数根据对现有文档的最后修改控制如何执行操作。有关更多详细信息，请参阅乐观并发控制。

#####Versioning

每个批量项目都可以使用"版本"字段包含版本值。它根据"_version"映射自动遵循索引/删除操作的行为。它还支持"version_type"(参见版本控制)。

#####Routing

每个散装物料都可以使用"工艺路线"字段包含路由值。它根据"_routing"映射自动遵循索引/删除操作的行为。

数据流不支持自定义路由，除非它们是在模板中启用"allow_custom_routing"设置的情况下创建的。

##### 等待活动分片

进行批量调用时，您可以将"wait_for_active_shards"参数设置为要求在开始处理批量请求之前，最小数量的分片副本处于活动状态。有关更多详细信息和使用示例，请参阅此处。

#####Refresh

控制此请求所做的更改何时可供搜索。见提神。

只有接收批量请求的分片才会受到"刷新"的影响。想象一下，一个包含三个文档的"_bulk？refresh=wait_for"请求恰好被路由到具有五个分片的索引中的不同分片。请求只会等待这三个分片刷新。构成索引的另外两个分片根本不参与"_bulk"请求。

#####Security

请参阅基于 URL 的访问控制。

### 路径参数

`<target>`

     (Optional, string) Name of the data stream, index, or index alias to perform bulk actions on. 

### 查询参数

`pipeline`

     (Optional, string) ID of the pipeline to use to preprocess incoming documents. If the index has a default ingest pipeline specified, then setting the value to `_none` disables the default ingest pipeline for this request. If a final pipeline is configured it will always run, regardless of the value of this parameter. 
`refresh`

     (Optional, enum) If `true`, Elasticsearch refreshes the affected shards to make this operation visible to search, if `wait_for` then wait for a refresh to make this operation visible to search, if `false` do nothing with refreshes. Valid values: `true`, `false`, `wait_for`. Default: `false`. 
`require_alias`

     (Optional, Boolean) If `true`, the request's actions must target an index alias. Defaults to `false`. 
`routing`

     (Optional, string) Custom value used to route operations to a specific shard. 
`_source`

     (Optional, string) True or false to return the `_source` field or not, or a list of fields to return. 
`_source_excludes`

    

(可选，字符串)要从响应中排除的源字段的逗号分隔列表。

您还可以使用此参数从"_source_includes"查询参数中指定的子集中排除字段。

如果"_source"参数为"false"，则忽略此参数。

`_source_includes`

    

(可选，字符串)要包含在响应中的源字段的逗号分隔列表。

如果指定此参数，则仅返回这些源字段。您可以使用"_source_excludes"查询参数从此子集中排除字段。

如果"_source"参数为"false"，则忽略此参数。

`timeout`

    

(可选，时间单位)周期每个操作等待以下操作：

* 自动创建索引 * 动态映射更新 * 等待活动分片

默认为"1m"(一分钟)。这保证了 Elasticsearch 在失败之前至少等待超时。实际等待时间可能会更长，尤其是在发生多次等待时。

`wait_for_active_shards`

    

(可选，字符串)在继续操作之前必须处于活动状态的分片副本数。设置为"all"或任何正整数，最多为索引中的分片总数("number_of_replicas+1")。默认值：1，主分片。

请参阅活动分片。

### 请求正文

请求正文包含"创建"、"删除"、"索引"和"更新"操作及其关联的源数据的换行符分隔列表。

`create`

    

(可选，字符串)为指定的文档(如果尚不存在)编制索引。以下行必须包含要编制索引的源数据。

`_index`

     (Optional, string) Name of the data stream, index, or index alias to perform the action on. This parameter is required if a `<target>` is not specified in the request path. 
`_id`

     (Optional, string) The document ID. If no ID is specified, a document ID is automatically generated. 
`require_alias`

     (Optional, Boolean) If `true`, the action must target an [index alias](aliases.html "Aliases"). Defaults to `false`. 
`dynamic_templates`

     (Optional, map) A map from the full name of fields to the name of [dynamic templates](dynamic-templates.html "Dynamic templates"). Defaults to an empty map. If a name matches a dynamic template, then that template will be applied regardless of other match predicates defined in the template. And if a field is already defined in the mapping, then this parameter won't be used. 

`delete`

    

(可选，字符串)从索引中删除指定的文档。

`_index`

     (Optional, string) Name of the index or index alias to perform the action on. This parameter is required if a `<target>` is not specified in the request path. 
`_id`

     (Required, string) The document ID. 
`require_alias`

     (Optional, Boolean) If `true`, the action must target an [index alias](aliases.html "Aliases"). Defaults to `false`. 

`index`

    

(可选，字符串)为指定的文档编制索引。如果文档存在，则替换文档并递增版本。以下行必须包含要编制索引的源数据。

`_index`

     (Optional, string) Name of the index or index alias to perform the action on. This parameter is required if a `<target>` is not specified in the request path. 
`_id`

     (Optional, string) The document ID. If no ID is specified, a document ID is automatically generated. 
`require_alias`

     (Optional, Boolean) If `true`, the action must target an [index alias](aliases.html "Aliases"). Defaults to `false`. 
`dynamic_templates`

     (Optional, map) A map from the full name of fields to the name of [dynamic templates](dynamic-templates.html "Dynamic templates"). Defaults to an empty map. If a name matches a dynamic template, then that template will be applied regardless of other match predicates defined in the template. And if a field is already defined in the mapping, then this parameter won't be used. 

`update`

    

(可选，字符串)执行部分文档更新。以下行必须包含部分文档和更新选项。

`_index`

     (Optional, string) Name of the index or index alias to perform the action on. This parameter is required if a `<target>` is not specified in the request path. 
`_id`

     (Required, string) The document ID. 
`require_alias`

     (Optional, Boolean) If `true`, the action must target an [index alias](aliases.html "Aliases"). Defaults to `false`. 

`doc`

     (Optional, object) The partial document to index. Required for `update` operations. 
`<fields>`

     (Optional, object) The document source to index. Required for `create` and `index` operations. 

### 响应正文

批量 API 的响应包含请求中每个操作的单独结果，按提交的顺序返回。单个操作的成功或失败不会影响请求中的其他操作。

`took`

     (integer) How long, in milliseconds, it took to process the bulk request. 
`errors`

     (Boolean) If `true`, one or more of the operations in the bulk request did not complete successfully. 
`items`

    

(对象数组)包含批量请求中每个操作的结果，按其提交顺序排列。

"项"对象的属性

<action>

    

(对象)参数名称是与操作关联的操作。可能的值为"创建"、"删除"、"索引"和"更新"。

参数值是一个对象，其中包含关联操作的信息。

""的属性<action>

`_index`

     (string) Name of the index associated with the operation. If the operation targeted a data stream, this is the backing index into which the document was written. 
`_id`

     (integer) The document ID associated with the operation. 
`_version`

    

(整数)与操作关联的文档版本。每次更新文档时，文档版本都会递增。

仅当操作成功时，才会返回此参数。

`result`

    

(字符串)操作的结果。成功的值是"创建"、"删除"和"更新"。

仅当操作成功时，才会返回此参数。

`_shards`

    

(对象)包含操作的分片信息。

仅当操作成功时，才会返回此参数。

"_shards"的属性

`total`

     (integer) Number of shards the operation attempted to execute on. 
`successful`

     (integer) Number of shards the operation succeeded on. 
`failed`

     (integer) Number of shards the operation attempted to execute on but failed. 

`_seq_no`

    

(整数)分配给操作的文档的序列号。序列号用于确保文档的较旧版本不会覆盖较新版本。请参阅乐观并发控制。

仅当操作成功时，才会返回此参数。

`_primary_term`

    

(整数)分配给操作文档的主要术语。请参阅乐观并发控制。

仅当操作成功时，才会返回此参数。

`status`

     (integer) HTTP status code returned for the operation. 
`error`

    

(对象)包含有关失败操作的其他信息。

仅对失败的操作返回该参数。

"错误"的属性

`type`

     (string) Error type for the operation. 
`reason`

     (string) Reason for the failed operation. 
`index_uuid`

     (string) The universally unique identifier (UUID) of the index associated with the failed operation. 
`shard`

     (string) ID of the shard associated with the failed operation. 
`index`

     (string) Name of the index associated with the failed operation. If the operation targeted a data stream, this is the backing index into which the document was attempted to be written. 

###Examples

    
    
    $params = [
        'body' => [
            [
                'index' => [
                    '_index' => 'test',
                    '_id' => '1',
                ],
            ],
            [
                'field1' => 'value1',
            ],
            [
                'delete' => [
                    '_index' => 'test',
                    '_id' => '2',
                ],
            ],
            [
                'create' => [
                    '_index' => 'test',
                    '_id' => '3',
                ],
            ],
            [
                'field1' => 'value3',
            ],
            [
                'update' => [
                    '_id' => '1',
                    '_index' => 'test',
                ],
            ],
            [
                'doc' => [
                    'field2' => 'value2',
                ],
            ],
        ],
    ];
    $response = $client->bulk($params);
    
    
    resp = client.bulk(
        body=[
            {"index": {"_index": "test", "_id": "1"}},
            {"field1": "value1"},
            {"delete": {"_index": "test", "_id": "2"}},
            {"create": {"_index": "test", "_id": "3"}},
            {"field1": "value3"},
            {"update": {"_id": "1", "_index": "test"}},
            {"doc": {"field2": "value2"}},
        ],
    )
    print(resp)
    
    
    response = client.bulk(
      body: [
        {
          index: {
            _index: 'test',
            _id: '1'
          }
        },
        {
          "field1": 'value1'
        },
        {
          delete: {
            _index: 'test',
            _id: '2'
          }
        },
        {
          create: {
            _index: 'test',
            _id: '3'
          }
        },
        {
          "field1": 'value3'
        },
        {
          update: {
            _id: '1',
            _index: 'test'
          }
        },
        {
          doc: {
            "field2": 'value2'
          }
        }
      ]
    )
    puts response
    
    
    res, err := es.Bulk(
    	strings.NewReader(`
    { "index" : { "_index" : "test", "_id" : "1" } }
    { "field1" : "value1" }
    { "delete" : { "_index" : "test", "_id" : "2" } }
    { "create" : { "_index" : "test", "_id" : "3" } }
    { "field1" : "value3" }
    { "update" : {"_id" : "1", "_index" : "test"} }
    { "doc" : {"field2" : "value2"} }
    `),
    )
    fmt.Println(res, err)
    
    
    const response = await client.bulk({
      body: [
        {
          index: {
            _index: 'test',
            _id: '1'
          }
        },
        {
          field1: 'value1'
        },
        {
          delete: {
            _index: 'test',
            _id: '2'
          }
        },
        {
          create: {
            _index: 'test',
            _id: '3'
          }
        },
        {
          field1: 'value3'
        },
        {
          update: {
            _id: '1',
            _index: 'test'
          }
        },
        {
          doc: {
            field2: 'value2'
          }
        }
      ]
    })
    console.log(response)
    
    
    POST _bulk
    { "index" : { "_index" : "test", "_id" : "1" } }
    { "field1" : "value1" }
    { "delete" : { "_index" : "test", "_id" : "2" } }
    { "create" : { "_index" : "test", "_id" : "3" } }
    { "field1" : "value3" }
    { "update" : {"_id" : "1", "_index" : "test"} }
    { "doc" : {"field2" : "value2"} }

API 返回以下结果：

    
    
    {
       "took": 30,
       "errors": false,
       "items": [
          {
             "index": {
                "_index": "test",
                "_id": "1",
                "_version": 1,
                "result": "created",
                "_shards": {
                   "total": 2,
                   "successful": 1,
                   "failed": 0
                },
                "status": 201,
                "_seq_no" : 0,
                "_primary_term": 1
             }
          },
          {
             "delete": {
                "_index": "test",
                "_id": "2",
                "_version": 1,
                "result": "not_found",
                "_shards": {
                   "total": 2,
                   "successful": 1,
                   "failed": 0
                },
                "status": 404,
                "_seq_no" : 1,
                "_primary_term" : 2
             }
          },
          {
             "create": {
                "_index": "test",
                "_id": "3",
                "_version": 1,
                "result": "created",
                "_shards": {
                   "total": 2,
                   "successful": 1,
                   "failed": 0
                },
                "status": 201,
                "_seq_no" : 2,
                "_primary_term" : 3
             }
          },
          {
             "update": {
                "_index": "test",
                "_id": "1",
                "_version": 2,
                "result": "updated",
                "_shards": {
                    "total": 2,
                    "successful": 1,
                    "failed": 0
                },
                "status": 200,
                "_seq_no" : 3,
                "_primary_term" : 4
             }
          }
       ]
    }

##### 批量更新示例

使用"update"操作时，"retry_on_conflict"可以用作操作本身(而不是在额外有效负载行中)的字段，以指定在版本冲突的情况下应重试更新的次数。

"update"操作有效负载支持以下选项："doc"(部分文档)、"upsert"、"doc_as_upsert"、"script"、"params"(脚本)、"lang"(脚本)和"_source"。有关选项的详细信息，请参阅更新文档。更新操作示例：

    
    
    $params = [
        'body' => [
            [
                'update' => [
                    '_id' => '1',
                    '_index' => 'index1',
                    'retry_on_conflict' => 3,
                ],
            ],
            [
                'doc' => [
                    'field' => 'value',
                ],
            ],
            [
                'update' => [
                    '_id' => '0',
                    '_index' => 'index1',
                    'retry_on_conflict' => 3,
                ],
            ],
            [
                'script' => [
                    'source' => 'ctx._source.counter += params.param1',
                    'lang' => 'painless',
                    'params' => [
                        'param1' => 1,
                    ],
                ],
                'upsert' => [
                    'counter' => 1,
                ],
            ],
            [
                'update' => [
                    '_id' => '2',
                    '_index' => 'index1',
                    'retry_on_conflict' => 3,
                ],
            ],
            [
                'doc' => [
                    'field' => 'value',
                ],
                'doc_as_upsert' => true,
            ],
            [
                'update' => [
                    '_id' => '3',
                    '_index' => 'index1',
                    '_source' => true,
                ],
            ],
            [
                'doc' => [
                    'field' => 'value',
                ],
            ],
            [
                'update' => [
                    '_id' => '4',
                    '_index' => 'index1',
                ],
            ],
            [
                'doc' => [
                    'field' => 'value',
                ],
                '_source' => true,
            ],
        ],
    ];
    $response = $client->bulk($params);
    
    
    resp = client.bulk(
        body=[
            {
                "update": {
                    "_id": "1",
                    "_index": "index1",
                    "retry_on_conflict": 3,
                }
            },
            {"doc": {"field": "value"}},
            {
                "update": {
                    "_id": "0",
                    "_index": "index1",
                    "retry_on_conflict": 3,
                }
            },
            {
                "script": {
                    "source": "ctx._source.counter += params.param1",
                    "lang": "painless",
                    "params": {"param1": 1},
                },
                "upsert": {"counter": 1},
            },
            {
                "update": {
                    "_id": "2",
                    "_index": "index1",
                    "retry_on_conflict": 3,
                }
            },
            {"doc": {"field": "value"}, "doc_as_upsert": True},
            {"update": {"_id": "3", "_index": "index1", "_source": True}},
            {"doc": {"field": "value"}},
            {"update": {"_id": "4", "_index": "index1"}},
            {"doc": {"field": "value"}, "_source": True},
        ],
    )
    print(resp)
    
    
    response = client.bulk(
      body: [
        {
          update: {
            _id: '1',
            _index: 'index1',
            retry_on_conflict: 3
          }
        },
        {
          doc: {
            field: 'value'
          }
        },
        {
          update: {
            _id: '0',
            _index: 'index1',
            retry_on_conflict: 3
          }
        },
        {
          script: {
            source: 'ctx._source.counter += params.param1',
            lang: 'painless',
            params: {
              "param1": 1
            }
          },
          upsert: {
            counter: 1
          }
        },
        {
          update: {
            _id: '2',
            _index: 'index1',
            retry_on_conflict: 3
          }
        },
        {
          doc: {
            field: 'value'
          },
          doc_as_upsert: true
        },
        {
          update: {
            _id: '3',
            _index: 'index1',
            _source: true
          }
        },
        {
          doc: {
            field: 'value'
          }
        },
        {
          update: {
            _id: '4',
            _index: 'index1'
          }
        },
        {
          doc: {
            field: 'value'
          },
          _source: true
        }
      ]
    )
    puts response
    
    
    res, err := es.Bulk(
    	strings.NewReader(`
    { "update" : {"_id" : "1", "_index" : "index1", "retry_on_conflict" : 3} }
    { "doc" : {"field" : "value"} }
    { "update" : { "_id" : "0", "_index" : "index1", "retry_on_conflict" : 3} }
    { "script" : { "source": "ctx._source.counter += params.param1", "lang" : "painless", "params" : {"param1" : 1}}, "upsert" : {"counter" : 1}}
    { "update" : {"_id" : "2", "_index" : "index1", "retry_on_conflict" : 3} }
    { "doc" : {"field" : "value"}, "doc_as_upsert" : true }
    { "update" : {"_id" : "3", "_index" : "index1", "_source" : true} }
    { "doc" : {"field" : "value"} }
    { "update" : {"_id" : "4", "_index" : "index1"} }
    { "doc" : {"field" : "value"}, "_source": true}
    `),
    )
    fmt.Println(res, err)
    
    
    const response = await client.bulk({
      body: [
        {
          update: {
            _id: '1',
            _index: 'index1',
            retry_on_conflict: 3
          }
        },
        {
          doc: {
            field: 'value'
          }
        },
        {
          update: {
            _id: '0',
            _index: 'index1',
            retry_on_conflict: 3
          }
        },
        {
          script: {
            source: 'ctx._source.counter += params.param1',
            lang: 'painless',
            params: {
              param1: 1
            }
          },
          upsert: {
            counter: 1
          }
        },
        {
          update: {
            _id: '2',
            _index: 'index1',
            retry_on_conflict: 3
          }
        },
        {
          doc: {
            field: 'value'
          },
          doc_as_upsert: true
        },
        {
          update: {
            _id: '3',
            _index: 'index1',
            _source: true
          }
        },
        {
          doc: {
            field: 'value'
          }
        },
        {
          update: {
            _id: '4',
            _index: 'index1'
          }
        },
        {
          doc: {
            field: 'value'
          },
          _source: true
        }
      ]
    })
    console.log(response)
    
    
    POST _bulk
    { "update" : {"_id" : "1", "_index" : "index1", "retry_on_conflict" : 3} }
    { "doc" : {"field" : "value"} }
    { "update" : { "_id" : "0", "_index" : "index1", "retry_on_conflict" : 3} }
    { "script" : { "source": "ctx._source.counter += params.param1", "lang" : "painless", "params" : {"param1" : 1}}, "upsert" : {"counter" : 1}}
    { "update" : {"_id" : "2", "_index" : "index1", "retry_on_conflict" : 3} }
    { "doc" : {"field" : "value"}, "doc_as_upsert" : true }
    { "update" : {"_id" : "3", "_index" : "index1", "_source" : true} }
    { "doc" : {"field" : "value"} }
    { "update" : {"_id" : "4", "_index" : "index1"} }
    { "doc" : {"field" : "value"}, "_source": true}

##### 失败操作示例

以下批量 API 请求包括更新不存在的文档的操作。

    
    
    $params = [
        'body' => [
            [
                'update' => [
                    '_id' => '5',
                    '_index' => 'index1',
                ],
            ],
            [
                'doc' => [
                    'my_field' => 'foo',
                ],
            ],
            [
                'update' => [
                    '_id' => '6',
                    '_index' => 'index1',
                ],
            ],
            [
                'doc' => [
                    'my_field' => 'foo',
                ],
            ],
            [
                'create' => [
                    '_id' => '7',
                    '_index' => 'index1',
                ],
            ],
            [
                'my_field' => 'foo',
            ],
        ],
    ];
    $response = $client->bulk($params);
    
    
    resp = client.bulk(
        body=[
            {"update": {"_id": "5", "_index": "index1"}},
            {"doc": {"my_field": "foo"}},
            {"update": {"_id": "6", "_index": "index1"}},
            {"doc": {"my_field": "foo"}},
            {"create": {"_id": "7", "_index": "index1"}},
            {"my_field": "foo"},
        ],
    )
    print(resp)
    
    
    response = client.bulk(
      body: [
        {
          update: {
            _id: '5',
            _index: 'index1'
          }
        },
        {
          doc: {
            my_field: 'foo'
          }
        },
        {
          update: {
            _id: '6',
            _index: 'index1'
          }
        },
        {
          doc: {
            my_field: 'foo'
          }
        },
        {
          create: {
            _id: '7',
            _index: 'index1'
          }
        },
        {
          my_field: 'foo'
        }
      ]
    )
    puts response
    
    
    res, err := es.Bulk(
    	strings.NewReader(`
    { "update": {"_id": "5", "_index": "index1"} }
    { "doc": {"my_field": "foo"} }
    { "update": {"_id": "6", "_index": "index1"} }
    { "doc": {"my_field": "foo"} }
    { "create": {"_id": "7", "_index": "index1"} }
    { "my_field": "foo" }
    `),
    )
    fmt.Println(res, err)
    
    
    const response = await client.bulk({
      body: [
        {
          update: {
            _id: '5',
            _index: 'index1'
          }
        },
        {
          doc: {
            my_field: 'foo'
          }
        },
        {
          update: {
            _id: '6',
            _index: 'index1'
          }
        },
        {
          doc: {
            my_field: 'foo'
          }
        },
        {
          create: {
            _id: '7',
            _index: 'index1'
          }
        },
        {
          my_field: 'foo'
        }
      ]
    })
    console.log(response)
    
    
    POST /_bulk
    { "update": {"_id": "5", "_index": "index1"} }
    { "doc": {"my_field": "foo"} }
    { "update": {"_id": "6", "_index": "index1"} }
    { "doc": {"my_field": "foo"} }
    { "create": {"_id": "7", "_index": "index1"} }
    { "my_field": "foo" }

由于这些操作无法成功完成，因此 API 会返回带有"错误"标志"true"的响应。

响应还包括任何失败操作的"错误"对象。"error"对象包含有关失败的其他信息，例如错误类型和原因。

    
    
    {
      "took": 486,
      "errors": true,
      "items": [
        {
          "update": {
            "_index": "index1",
            "_id": "5",
            "status": 404,
            "error": {
              "type": "document_missing_exception",
              "reason": "[5]: document missing",
              "index_uuid": "aAsFqTI0Tc2W0LCWgPNrOA",
              "shard": "0",
              "index": "index1"
            }
          }
        },
        {
          "update": {
            "_index": "index1",
            "_id": "6",
            "status": 404,
            "error": {
              "type": "document_missing_exception",
              "reason": "[6]: document missing",
              "index_uuid": "aAsFqTI0Tc2W0LCWgPNrOA",
              "shard": "0",
              "index": "index1"
            }
          }
        },
        {
          "create": {
            "_index": "index1",
            "_id": "7",
            "_version": 1,
            "result": "created",
            "_shards": {
              "total": 2,
              "successful": 1,
              "failed": 0
            },
            "_seq_no": 0,
            "_primary_term": 1,
            "status": 201
          }
        }
      ]
    }

若要仅返回有关失败操作的信息，请使用带有"items.*.error"参数的"filter_path"查询参数。

    
    
    $params = [
        'body' => [
            [
                'update' => [
                    '_id' => '5',
                    '_index' => 'index1',
                ],
            ],
            [
                'doc' => [
                    'my_field' => 'baz',
                ],
            ],
            [
                'update' => [
                    '_id' => '6',
                    '_index' => 'index1',
                ],
            ],
            [
                'doc' => [
                    'my_field' => 'baz',
                ],
            ],
            [
                'update' => [
                    '_id' => '7',
                    '_index' => 'index1',
                ],
            ],
            [
                'doc' => [
                    'my_field' => 'baz',
                ],
            ],
        ],
    ];
    $response = $client->bulk($params);
    
    
    resp = client.bulk(
        filter_path="items.*.error",
        body=[
            {"update": {"_id": "5", "_index": "index1"}},
            {"doc": {"my_field": "baz"}},
            {"update": {"_id": "6", "_index": "index1"}},
            {"doc": {"my_field": "baz"}},
            {"update": {"_id": "7", "_index": "index1"}},
            {"doc": {"my_field": "baz"}},
        ],
    )
    print(resp)
    
    
    response = client.bulk(
      filter_path: 'items.*.error',
      body: [
        {
          update: {
            _id: '5',
            _index: 'index1'
          }
        },
        {
          doc: {
            my_field: 'baz'
          }
        },
        {
          update: {
            _id: '6',
            _index: 'index1'
          }
        },
        {
          doc: {
            my_field: 'baz'
          }
        },
        {
          update: {
            _id: '7',
            _index: 'index1'
          }
        },
        {
          doc: {
            my_field: 'baz'
          }
        }
      ]
    )
    puts response
    
    
    res, err := es.Bulk(
    	strings.NewReader(`
    { "update": {"_id": "5", "_index": "index1"} }
    { "doc": {"my_field": "baz"} }
    { "update": {"_id": "6", "_index": "index1"} }
    { "doc": {"my_field": "baz"} }
    { "update": {"_id": "7", "_index": "index1"} }
    { "doc": {"my_field": "baz"} }
    `),
    	es.Bulk.WithFilterPath("items.*.error"),
    )
    fmt.Println(res, err)
    
    
    const response = await client.bulk({
      filter_path: 'items.*.error',
      body: [
        {
          update: {
            _id: '5',
            _index: 'index1'
          }
        },
        {
          doc: {
            my_field: 'baz'
          }
        },
        {
          update: {
            _id: '6',
            _index: 'index1'
          }
        },
        {
          doc: {
            my_field: 'baz'
          }
        },
        {
          update: {
            _id: '7',
            _index: 'index1'
          }
        },
        {
          doc: {
            my_field: 'baz'
          }
        }
      ]
    })
    console.log(response)
    
    
    POST /_bulk?filter_path=items.*.error
    { "update": {"_id": "5", "_index": "index1"} }
    { "doc": {"my_field": "baz"} }
    { "update": {"_id": "6", "_index": "index1"} }
    { "doc": {"my_field": "baz"} }
    { "update": {"_id": "7", "_index": "index1"} }
    { "doc": {"my_field": "baz"} }

API 返回以下结果。

    
    
    {
      "items": [
        {
          "update": {
            "error": {
              "type": "document_missing_exception",
              "reason": "[5]: document missing",
              "index_uuid": "aAsFqTI0Tc2W0LCWgPNrOA",
              "shard": "0",
              "index": "index1"
            }
          }
        },
        {
          "update": {
            "error": {
              "type": "document_missing_exception",
              "reason": "[6]: document missing",
              "index_uuid": "aAsFqTI0Tc2W0LCWgPNrOA",
              "shard": "0",
              "index": "index1"
            }
          }
        }
      ]
    }

##### 动态模板示例参数

下面的示例创建一个动态模板，然后执行由具有"dynamic_templates"参数的索引/创建请求组成的批量请求。

    
    
    response = client.indices.create(
      index: 'my-index',
      body: {
        mappings: {
          dynamic_templates: [
            {
              geo_point: {
                mapping: {
                  type: 'geo_point'
                }
              }
            }
          ]
        }
      }
    )
    puts response
    
    response = client.bulk(
      body: [
        {
          index: {
            _index: 'my_index',
            _id: '1',
            dynamic_templates: {
              work_location: 'geo_point'
            }
          }
        },
        {
          field: 'value1',
          work_location: '41.12,-71.34',
          raw_location: '41.12,-71.34'
        },
        {
          create: {
            _index: 'my_index',
            _id: '2',
            dynamic_templates: {
              home_location: 'geo_point'
            }
          }
        },
        {
          field: 'value2',
          home_location: '41.12,-71.34'
        }
      ]
    )
    puts response
    
    
    PUT my-index/
    {
      "mappings": {
        "dynamic_templates": [
          {
            "geo_point": {
                 "mapping": {
                    "type" : "geo_point"
                 }
            }
          }
        ]
      }
    }
    
    POST /_bulk
    { "index" : { "_index" : "my_index", "_id" : "1", "dynamic_templates": {"work_location": "geo_point"}} }
    { "field" : "value1", "work_location": "41.12,-71.34", "raw_location": "41.12,-71.34"}
    { "create" : { "_index" : "my_index", "_id" : "2", "dynamic_templates": {"home_location": "geo_point"}} }
    { "field" : "value2", "home_location": "41.12,-71.34"}

批量请求根据"dynamic_templates"参数创建两个类型为"geo_point"的新字段"work_location"和"home_location";但是，"raw_location"字段是使用默认的动态映射规则创建的，在这种情况下作为"文本"字段，因为它在 JSON 文档中作为字符串提供。

[« Multi get (mget) API](docs-multi-get.md) [Reindex API »](docs-
reindex.md)
