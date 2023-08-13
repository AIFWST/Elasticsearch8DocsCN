

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Geospatial analysis](geospatial-analysis.md) [EQL syntax reference
»](eql-syntax.md)

# EQL搜索

事件查询语言 (EQL) 是一种查询语言，用于基于事件的时间序列数据，例如日志、指标和跟踪。

### EQL 的优势

* **EQL 允许您表达事件之间的关系。 许多查询语言允许您匹配单个事件。EQL 允许您跨不同的事件类别和时间跨度匹配事件序列。

* **EQL 的学习曲线较低。 EQL 语法看起来像其他常见查询语言，例如 SQL。EQL 允许您直观地编写和读取查询，从而实现快速、迭代的搜索。

* **EQL 专为安全用例而设计。 虽然您可以将其用于任何基于事件的数据，但我们创建了用于威胁搜寻的 EQL。EQL 不仅支持入侵指标 (IOC) 搜索，还可以描述超出 IOC 的活动。

### 必填字段

除示例查询外，EQL 搜索要求搜索的数据流或索引包含 _timestamp_ 字段。默认情况下，EQL 使用弹性通用架构 (ECS) 中的"@timestamp"字段。

EQL 搜索还需要_event category_字段，除非您使用"any"关键字搜索没有事件类别字段的文档。默认情况下，EQL 使用 ECS 的"事件类别"字段。

要使用其他时间戳或事件类别字段，请参阅指定时间戳或事件类别字段。

虽然使用 EQL 不需要架构，但我们建议使用 ECS。默认情况下，EQL 搜索设计为使用核心 ECS 字段。

### 运行 EQLsearch

使用 EQL 搜索 API 运行基本 EQL 查询。

    
    
    response = client.eql.search(
      index: 'my-data-stream',
      body: {
        query: "\n    process where process.name == \"regsvr32.exe\"\n  "
      }
    )
    puts response
    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        process where process.name == "regsvr32.exe"
      """
    }

默认情况下，基本 EQL 查询返回 'hits.events' 属性中的 10 个最新匹配事件。这些命中按时间戳排序，自 Unix 纪元以来按升序转换为毫秒。

    
    
    {
      "is_partial": false,
      "is_running": false,
      "took": 60,
      "timed_out": false,
      "hits": {
        "total": {
          "value": 2,
          "relation": "eq"
        },
        "events": [
          {
            "_index": ".ds-my-data-stream-2099.12.07-000001",
            "_id": "OQmfCaduce8zoHT93o4H",
            "_source": {
              "@timestamp": "2099-12-07T11:07:09.000Z",
              "event": {
                "category": "process",
                "id": "aR3NWVOs",
                "sequence": 4
              },
              "process": {
                "pid": 2012,
                "name": "regsvr32.exe",
                "command_line": "regsvr32.exe  /s /u /i:https://...RegSvr32.sct scrobj.dll",
                "executable": "C:\\Windows\\System32\\regsvr32.exe"
              }
            }
          },
          {
            "_index": ".ds-my-data-stream-2099.12.07-000001",
            "_id": "xLkCaj4EujzdNSxfYLbO",
            "_source": {
              "@timestamp": "2099-12-07T11:07:10.000Z",
              "event": {
                "category": "process",
                "id": "GTSmSqgz0U",
                "sequence": 6,
                "type": "termination"
              },
              "process": {
                "pid": 2012,
                "name": "regsvr32.exe",
                "executable": "C:\\Windows\\System32\\regsvr32.exe"
              }
            }
          }
        ]
      }
    }

使用"size"参数获取更小或更大的匹配集：

    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        process where process.name == "regsvr32.exe"
      """,
      "size": 50
    }

### 搜索事件序列

使用 EQL 的序列语法搜索一系列有序事件。按时间升序列出事件项，最新事件列在最后：

    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        sequence
          [ process where process.name == "regsvr32.exe" ]
          [ file where stringContains(file.name, "scrobj.dll") ]
      """
    }

响应的"hits.sequences"属性包含 10 个最新的匹配序列。

    
    
    {
      ...
      "hits": {
        "total": ...,
        "sequences": [
          {
            "events": [
              {
                "_index": ".ds-my-data-stream-2099.12.07-000001",
                "_id": "OQmfCaduce8zoHT93o4H",
                "_source": {
                  "@timestamp": "2099-12-07T11:07:09.000Z",
                  "event": {
                    "category": "process",
                    "id": "aR3NWVOs",
                    "sequence": 4
                  },
                  "process": {
                    "pid": 2012,
                    "name": "regsvr32.exe",
                    "command_line": "regsvr32.exe  /s /u /i:https://...RegSvr32.sct scrobj.dll",
                    "executable": "C:\\Windows\\System32\\regsvr32.exe"
                  }
                }
              },
              {
                "_index": ".ds-my-data-stream-2099.12.07-000001",
                "_id": "yDwnGIJouOYGBzP0ZE9n",
                "_source": {
                  "@timestamp": "2099-12-07T11:07:10.000Z",
                  "event": {
                    "category": "file",
                    "id": "tZ1NWVOs",
                    "sequence": 5
                  },
                  "process": {
                    "pid": 2012,
                    "name": "regsvr32.exe",
                    "executable": "C:\\Windows\\System32\\regsvr32.exe"
                  },
                  "file": {
                    "path": "C:\\Windows\\System32\\scrobj.dll",
                    "name": "scrobj.dll"
                  }
                }
              }
            ]
          }
        ]
      }
    }

使用"with maxspan"将匹配序列限制为时间跨度：

    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        sequence with maxspan=1h
          [ process where process.name == "regsvr32.exe" ]
          [ file where stringContains(file.name, "scrobj.dll") ]
      """
    }

使用"by"关键字匹配共享相同字段值的事件：

    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        sequence with maxspan=1h
          [ process where process.name == "regsvr32.exe" ] by process.pid
          [ file where stringContains(file.name, "scrobj.dll") ] by process.pid
      """
    }

如果应在所有事件之间共享字段值，请使用"序列依据"关键字。以下查询等效于上一个查询。

    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        sequence by process.pid with maxspan=1h
          [ process where process.name == "regsvr32.exe" ]
          [ file where stringContains(file.name, "scrobj.dll") ]
      """
    }

"hits.sequences.join_keys"属性包含共享字段值。

    
    
    {
      ...
      "hits": ...,
        "sequences": [
          {
            "join_keys": [
              2012
            ],
            "events": ...
          }
        ]
      }
    }

使用"直到"关键字指定序列的过期事件。匹配序列必须在此事件之前结束。

    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        sequence by process.pid with maxspan=1h
          [ process where process.name == "regsvr32.exe" ]
          [ file where stringContains(file.name, "scrobj.dll") ]
        until [ process where event.type == "termination" ]
      """
    }

### 按时间顺序排列的无序事件示例

使用 EQL 的示例语法搜索与一个或多个联接键和一组筛选器匹配的事件。样本类似于序列，但不按时间顺序返回事件。事实上，示例查询可以在没有时间戳的数据上运行。示例查询可用于查找并不总是以相同顺序发生或跨较长时间发生的事件中的相关性。

单击以显示以下示例中使用的示例数据

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        mappings: {
          properties: {
            ip: {
              type: 'ip'
            },
            version: {
              type: 'version'
            },
            missing_keyword: {
              type: 'keyword'
            },
            "@timestamp": {
              type: 'date'
            },
            type_test: {
              type: 'keyword'
            },
            "@timestamp_pretty": {
              type: 'date',
              format: 'dd-MM-yyyy'
            },
            event_type: {
              type: 'keyword'
            },
            event: {
              properties: {
                category: {
                  type: 'alias',
                  path: 'event_type'
                }
              }
            },
            host: {
              type: 'keyword'
            },
            os: {
              type: 'keyword'
            },
            bool: {
              type: 'boolean'
            },
            uptime: {
              type: 'long'
            },
            port: {
              type: 'long'
            }
          }
        }
      }
    )
    puts response
    
    response = client.indices.create(
      index: 'my-index-000002',
      body: {
        mappings: {
          properties: {
            ip: {
              type: 'ip'
            },
            "@timestamp": {
              type: 'date'
            },
            "@timestamp_pretty": {
              type: 'date',
              format: 'yyyy-MM-dd'
            },
            type_test: {
              type: 'keyword'
            },
            event_type: {
              type: 'keyword'
            },
            event: {
              properties: {
                category: {
                  type: 'alias',
                  path: 'event_type'
                }
              }
            },
            host: {
              type: 'keyword'
            },
            op_sys: {
              type: 'keyword'
            },
            bool: {
              type: 'boolean'
            },
            uptime: {
              type: 'long'
            },
            port: {
              type: 'long'
            }
          }
        }
      }
    )
    puts response
    
    response = client.indices.create(
      index: 'my-index-000003',
      body: {
        mappings: {
          properties: {
            host_ip: {
              type: 'ip'
            },
            "@timestamp": {
              type: 'date'
            },
            date: {
              type: 'date'
            },
            event_type: {
              type: 'keyword'
            },
            event: {
              properties: {
                category: {
                  type: 'alias',
                  path: 'event_type'
                }
              }
            },
            missing_keyword: {
              type: 'keyword'
            },
            host: {
              type: 'keyword'
            },
            os: {
              type: 'keyword'
            },
            bool: {
              type: 'boolean'
            },
            uptime: {
              type: 'long'
            },
            port: {
              type: 'long'
            }
          }
        }
      }
    )
    puts response
    
    response = client.bulk(
      index: 'my-index-000001',
      refresh: true,
      body: [
        {
          index: {
            _id: 1
          }
        },
        {
          "@timestamp": '1234567891',
          "@timestamp_pretty": '12-12-2022',
          missing_keyword: 'test',
          type_test: 'abc',
          ip: '10.0.0.1',
          event_type: 'alert',
          host: 'doom',
          uptime: 0,
          port: 1234,
          os: 'win10',
          version: '1.0.0',
          id: 11
        },
        {
          index: {
            _id: 2
          }
        },
        {
          "@timestamp": '1234567892',
          "@timestamp_pretty": '13-12-2022',
          event_type: 'alert',
          type_test: 'abc',
          host: 'CS',
          uptime: 5,
          port: 1,
          os: 'win10',
          version: '1.2.0',
          id: 12
        },
        {
          index: {
            _id: 3
          }
        },
        {
          "@timestamp": '1234567893',
          "@timestamp_pretty": '12-12-2022',
          event_type: 'alert',
          type_test: 'abc',
          host: 'farcry',
          uptime: 1,
          port: 1234,
          bool: false,
          os: 'win10',
          version: '2.0.0',
          id: 13
        },
        {
          index: {
            _id: 4
          }
        },
        {
          "@timestamp": '1234567894',
          "@timestamp_pretty": '13-12-2022',
          event_type: 'alert',
          type_test: 'abc',
          host: 'GTA',
          uptime: 3,
          port: 12,
          os: 'slack',
          version: '10.0.0',
          id: 14
        },
        {
          index: {
            _id: 5
          }
        },
        {
          "@timestamp": '1234567895',
          "@timestamp_pretty": '17-12-2022',
          event_type: 'alert',
          host: 'sniper 3d',
          uptime: 6,
          port: 1234,
          os: 'fedora',
          version: '20.1.0',
          id: 15
        },
        {
          index: {
            _id: 6
          }
        },
        {
          "@timestamp": '1234568896',
          "@timestamp_pretty": '17-12-2022',
          event_type: 'alert',
          host: 'doom',
          port: 65_123,
          bool: true,
          os: 'redhat',
          version: '20.10.0',
          id: 16
        },
        {
          index: {
            _id: 7
          }
        },
        {
          "@timestamp": '1234567897',
          "@timestamp_pretty": '17-12-2022',
          missing_keyword: 'yyy',
          event_type: 'failure',
          host: 'doom',
          uptime: 15,
          port: 1234,
          bool: true,
          os: 'redhat',
          version: '20.2.0',
          id: 17
        },
        {
          index: {
            _id: 8
          }
        },
        {
          "@timestamp": '1234567898',
          "@timestamp_pretty": '12-12-2022',
          missing_keyword: 'test',
          event_type: 'success',
          host: 'doom',
          uptime: 16,
          port: 512,
          os: 'win10',
          version: '1.2.3',
          id: 18
        },
        {
          index: {
            _id: 9
          }
        },
        {
          "@timestamp": '1234567899',
          "@timestamp_pretty": '15-12-2022',
          missing_keyword: 'test',
          event_type: 'success',
          host: 'GTA',
          port: 12,
          bool: true,
          os: 'win10',
          version: '1.2.3',
          id: 19
        },
        {
          index: {
            _id: 10
          }
        },
        {
          "@timestamp": '1234567893',
          missing_keyword: nil,
          ip: '10.0.0.5',
          event_type: 'alert',
          host: 'farcry',
          uptime: 1,
          port: 1234,
          bool: true,
          os: 'win10',
          version: '1.2.3',
          id: 110
        }
      ]
    )
    puts response
    
    response = client.bulk(
      index: 'my-index-000002',
      refresh: true,
      body: [
        {
          index: {
            _id: 1
          }
        },
        {
          "@timestamp": '1234567991',
          type_test: 'abc',
          ip: '10.0.0.1',
          event_type: 'alert',
          host: 'doom',
          uptime: 0,
          port: 1234,
          op_sys: 'win10',
          id: 21
        },
        {
          index: {
            _id: 2
          }
        },
        {
          "@timestamp": '1234567992',
          type_test: 'abc',
          event_type: 'alert',
          host: 'CS',
          uptime: 5,
          port: 1,
          op_sys: 'win10',
          id: 22
        },
        {
          index: {
            _id: 3
          }
        },
        {
          "@timestamp": '1234567993',
          type_test: 'abc',
          "@timestamp_pretty": '2022-12-17',
          event_type: 'alert',
          host: 'farcry',
          uptime: 1,
          port: 1234,
          bool: false,
          op_sys: 'win10',
          id: 23
        },
        {
          index: {
            _id: 4
          }
        },
        {
          "@timestamp": '1234567994',
          event_type: 'alert',
          host: 'GTA',
          uptime: 3,
          port: 12,
          op_sys: 'slack',
          id: 24
        },
        {
          index: {
            _id: 5
          }
        },
        {
          "@timestamp": '1234567995',
          event_type: 'alert',
          host: 'sniper 3d',
          uptime: 6,
          port: 1234,
          op_sys: 'fedora',
          id: 25
        },
        {
          index: {
            _id: 6
          }
        },
        {
          "@timestamp": '1234568996',
          "@timestamp_pretty": '2022-12-17',
          ip: '10.0.0.5',
          event_type: 'alert',
          host: 'doom',
          port: 65_123,
          bool: true,
          op_sys: 'redhat',
          id: 26
        },
        {
          index: {
            _id: 7
          }
        },
        {
          "@timestamp": '1234567997',
          "@timestamp_pretty": '2022-12-17',
          event_type: 'failure',
          host: 'doom',
          uptime: 15,
          port: 1234,
          bool: true,
          op_sys: 'redhat',
          id: 27
        },
        {
          index: {
            _id: 8
          }
        },
        {
          "@timestamp": '1234567998',
          ip: '10.0.0.1',
          event_type: 'success',
          host: 'doom',
          uptime: 16,
          port: 512,
          op_sys: 'win10',
          id: 28
        },
        {
          index: {
            _id: 9
          }
        },
        {
          "@timestamp": '1234567999',
          ip: '10.0.0.1',
          event_type: 'success',
          host: 'GTA',
          port: 12,
          bool: false,
          op_sys: 'win10',
          id: 29
        }
      ]
    )
    puts response
    
    response = client.bulk(
      index: 'my-index-000003',
      refresh: true,
      body: [
        {
          index: {
            _id: 1
          }
        },
        {
          "@timestamp": '1334567891',
          host_ip: '10.0.0.1',
          event_type: 'alert',
          host: 'doom',
          uptime: 0,
          port: 12,
          os: 'win10',
          id: 31
        },
        {
          index: {
            _id: 2
          }
        },
        {
          "@timestamp": '1334567892',
          event_type: 'alert',
          host: 'CS',
          os: 'win10',
          id: 32
        },
        {
          index: {
            _id: 3
          }
        },
        {
          "@timestamp": '1334567893',
          event_type: 'alert',
          host: 'farcry',
          bool: true,
          os: 'win10',
          id: 33
        },
        {
          index: {
            _id: 4
          }
        },
        {
          "@timestamp": '1334567894',
          event_type: 'alert',
          host: 'GTA',
          os: 'slack',
          bool: true,
          id: 34
        },
        {
          index: {
            _id: 5
          }
        },
        {
          "@timestamp": '1234567895',
          event_type: 'alert',
          host: 'sniper 3d',
          os: 'fedora',
          id: 35
        },
        {
          index: {
            _id: 6
          }
        },
        {
          "@timestamp": '1234578896',
          host_ip: '10.0.0.1',
          event_type: 'alert',
          host: 'doom',
          bool: true,
          os: 'redhat',
          id: 36
        },
        {
          index: {
            _id: 7
          }
        },
        {
          "@timestamp": '1234567897',
          event_type: 'failure',
          missing_keyword: 'test',
          host: 'doom',
          bool: true,
          os: 'redhat',
          id: 37
        },
        {
          index: {
            _id: 8
          }
        },
        {
          "@timestamp": '1234577898',
          event_type: 'success',
          host: 'doom',
          os: 'win10',
          id: 38,
          date: '1671235200000'
        },
        {
          index: {
            _id: 9
          }
        },
        {
          "@timestamp": '1234577899',
          host_ip: '10.0.0.5',
          event_type: 'success',
          host: 'GTA',
          bool: true,
          os: 'win10',
          id: 39
        }
      ]
    )
    puts response
    
    
    PUT /my-index-000001
    {
        "mappings": {
            "properties": {
                "ip": {
                    "type":"ip"
                },
                "version": {
                    "type": "version"
                },
                "missing_keyword": {
                    "type": "keyword"
                },
                "@timestamp": {
                  "type": "date"
                },
                "type_test": {
                    "type": "keyword"
                },
                "@timestamp_pretty": {
                  "type": "date",
                  "format": "dd-MM-yyyy"
                },
                "event_type": {
                  "type": "keyword"
                },
                "event": {
                  "properties": {
                    "category": {
                      "type": "alias",
                      "path": "event_type"
                    }
                  }
                },
                "host": {
                  "type": "keyword"
                },
                "os": {
                  "type": "keyword"
                },
                "bool": {
                  "type": "boolean"
                },
                "uptime" : {
                  "type" : "long"
                },
                "port" : {
                  "type" : "long"
                }
            }
        }
    }
    
    PUT /my-index-000002
    {
        "mappings": {
            "properties": {
                "ip": {
                    "type":"ip"
                },
                "@timestamp": {
                  "type": "date"
                },
                "@timestamp_pretty": {
                  "type": "date",
                  "format": "yyyy-MM-dd"
                },
                "type_test": {
                    "type": "keyword"
                },
                "event_type": {
                  "type": "keyword"
                },
                "event": {
                  "properties": {
                    "category": {
                      "type": "alias",
                      "path": "event_type"
                    }
                  }
                },
                "host": {
                  "type": "keyword"
                },
                "op_sys": {
                  "type": "keyword"
                },
                "bool": {
                  "type": "boolean"
                },
                "uptime" : {
                  "type" : "long"
                },
                "port" : {
                  "type" : "long"
                }
            }
        }
    }
    
    PUT /my-index-000003
    {
        "mappings": {
            "properties": {
                "host_ip": {
                    "type":"ip"
                },
                "@timestamp": {
                  "type": "date"
                },
                "date": {
                  "type": "date"
                },
                "event_type": {
                  "type": "keyword"
                },
                "event": {
                  "properties": {
                    "category": {
                      "type": "alias",
                      "path": "event_type"
                    }
                  }
                },
                "missing_keyword": {
                    "type": "keyword"
                },
                "host": {
                  "type": "keyword"
                },
                "os": {
                  "type": "keyword"
                },
                "bool": {
                  "type": "boolean"
                },
                "uptime" : {
                  "type" : "long"
                },
                "port" : {
                  "type" : "long"
                }
            }
        }
    }
    
    POST /my-index-000001/_bulk?refresh
    {"index":{"_id":1}}
    {"@timestamp":"1234567891","@timestamp_pretty":"12-12-2022","missing_keyword":"test","type_test":"abc","ip":"10.0.0.1","event_type":"alert","host":"doom","uptime":0,"port":1234,"os":"win10","version":"1.0.0","id":11}
    {"index":{"_id":2}}
    {"@timestamp":"1234567892","@timestamp_pretty":"13-12-2022","event_type":"alert","type_test":"abc","host":"CS","uptime":5,"port":1,"os":"win10","version":"1.2.0","id":12}
    {"index":{"_id":3}}
    {"@timestamp":"1234567893","@timestamp_pretty":"12-12-2022","event_type":"alert","type_test":"abc","host":"farcry","uptime":1,"port":1234,"bool":false,"os":"win10","version":"2.0.0","id":13}
    {"index":{"_id":4}}
    {"@timestamp":"1234567894","@timestamp_pretty":"13-12-2022","event_type":"alert","type_test":"abc","host":"GTA","uptime":3,"port":12,"os":"slack","version":"10.0.0","id":14}
    {"index":{"_id":5}}
    {"@timestamp":"1234567895","@timestamp_pretty":"17-12-2022","event_type":"alert","host":"sniper 3d","uptime":6,"port":1234,"os":"fedora","version":"20.1.0","id":15}
    {"index":{"_id":6}}
    {"@timestamp":"1234568896","@timestamp_pretty":"17-12-2022","event_type":"alert","host":"doom","port":65123,"bool":true,"os":"redhat","version":"20.10.0","id":16}
    {"index":{"_id":7}}
    {"@timestamp":"1234567897","@timestamp_pretty":"17-12-2022","missing_keyword":"yyy","event_type":"failure","host":"doom","uptime":15,"port":1234,"bool":true,"os":"redhat","version":"20.2.0","id":17}
    {"index":{"_id":8}}
    {"@timestamp":"1234567898","@timestamp_pretty":"12-12-2022","missing_keyword":"test","event_type":"success","host":"doom","uptime":16,"port":512,"os":"win10","version":"1.2.3","id":18}
    {"index":{"_id":9}}
    {"@timestamp":"1234567899","@timestamp_pretty":"15-12-2022","missing_keyword":"test","event_type":"success","host":"GTA","port":12,"bool":true,"os":"win10","version":"1.2.3","id":19}
    {"index":{"_id":10}}
    {"@timestamp":"1234567893","missing_keyword":null,"ip":"10.0.0.5","event_type":"alert","host":"farcry","uptime":1,"port":1234,"bool":true,"os":"win10","version":"1.2.3","id":110}
    
    POST /my-index-000002/_bulk?refresh
    {"index":{"_id":1}}
    {"@timestamp":"1234567991","type_test":"abc","ip":"10.0.0.1","event_type":"alert","host":"doom","uptime":0,"port":1234,"op_sys":"win10","id":21}
    {"index":{"_id":2}}
    {"@timestamp":"1234567992","type_test":"abc","event_type":"alert","host":"CS","uptime":5,"port":1,"op_sys":"win10","id":22}
    {"index":{"_id":3}}
    {"@timestamp":"1234567993","type_test":"abc","@timestamp_pretty":"2022-12-17","event_type":"alert","host":"farcry","uptime":1,"port":1234,"bool":false,"op_sys":"win10","id":23}
    {"index":{"_id":4}}
    {"@timestamp":"1234567994","event_type":"alert","host":"GTA","uptime":3,"port":12,"op_sys":"slack","id":24}
    {"index":{"_id":5}}
    {"@timestamp":"1234567995","event_type":"alert","host":"sniper 3d","uptime":6,"port":1234,"op_sys":"fedora","id":25}
    {"index":{"_id":6}}
    {"@timestamp":"1234568996","@timestamp_pretty":"2022-12-17","ip":"10.0.0.5","event_type":"alert","host":"doom","port":65123,"bool":true,"op_sys":"redhat","id":26}
    {"index":{"_id":7}}
    {"@timestamp":"1234567997","@timestamp_pretty":"2022-12-17","event_type":"failure","host":"doom","uptime":15,"port":1234,"bool":true,"op_sys":"redhat","id":27}
    {"index":{"_id":8}}
    {"@timestamp":"1234567998","ip":"10.0.0.1","event_type":"success","host":"doom","uptime":16,"port":512,"op_sys":"win10","id":28}
    {"index":{"_id":9}}
    {"@timestamp":"1234567999","ip":"10.0.0.1","event_type":"success","host":"GTA","port":12,"bool":false,"op_sys":"win10","id":29}
    
    POST /my-index-000003/_bulk?refresh
    {"index":{"_id":1}}
    {"@timestamp":"1334567891","host_ip":"10.0.0.1","event_type":"alert","host":"doom","uptime":0,"port":12,"os":"win10","id":31}
    {"index":{"_id":2}}
    {"@timestamp":"1334567892","event_type":"alert","host":"CS","os":"win10","id":32}
    {"index":{"_id":3}}
    {"@timestamp":"1334567893","event_type":"alert","host":"farcry","bool":true,"os":"win10","id":33}
    {"index":{"_id":4}}
    {"@timestamp":"1334567894","event_type":"alert","host":"GTA","os":"slack","bool":true,"id":34}
    {"index":{"_id":5}}
    {"@timestamp":"1234567895","event_type":"alert","host":"sniper 3d","os":"fedora","id":35}
    {"index":{"_id":6}}
    {"@timestamp":"1234578896","host_ip":"10.0.0.1","event_type":"alert","host":"doom","bool":true,"os":"redhat","id":36}
    {"index":{"_id":7}}
    {"@timestamp":"1234567897","event_type":"failure","missing_keyword":"test","host":"doom","bool":true,"os":"redhat","id":37}
    {"index":{"_id":8}}
    {"@timestamp":"1234577898","event_type":"success","host":"doom","os":"win10","id":38,"date":"1671235200000"}
    {"index":{"_id":9}}
    {"@timestamp":"1234577899","host_ip":"10.0.0.5","event_type":"success","host":"GTA","bool":true,"os":"win10","id":39}

示例查询使用"by"关键字指定至少一个联接键，以及最多五个筛选器：

    
    
    GET /my-index*/_eql/search
    {
      "query": """
        sample by host
          [any where uptime > 0]
          [any where port > 100]
          [any where bool == true]
      """
    }

默认情况下，响应的"hits.sequences"属性最多包含 10 个样本。每个样本都有一组"join_keys"和一个数组，每个筛选器都有一个匹配事件。事件按它们匹配的筛选器的顺序返回：

    
    
    {
      ...
      "hits": {
        "total": {
          "value": 2,
          "relation": "eq"
        },
        "sequences": [
          {
            "join_keys": [
              "doom"                                      __],
            "events": [
              { __"_index": "my-index-000001",
                "_id": "7",
                "_source": {
                  "@timestamp": "1234567897",
                  "@timestamp_pretty": "17-12-2022",
                  "missing_keyword": "yyy",
                  "event_type": "failure",
                  "host": "doom",
                  "uptime": 15,
                  "port": 1234,
                  "bool": true,
                  "os": "redhat",
                  "version": "20.2.0",
                  "id": 17
                }
              },
              { __"_index": "my-index-000001",
                "_id": "1",
                "_source": {
                  "@timestamp": "1234567891",
                  "@timestamp_pretty": "12-12-2022",
                  "missing_keyword": "test",
                  "type_test": "abc",
                  "ip": "10.0.0.1",
                  "event_type": "alert",
                  "host": "doom",
                  "uptime": 0,
                  "port": 1234,
                  "os": "win10",
                  "version": "1.0.0",
                  "id": 11
                }
              },
              { __"_index": "my-index-000001",
                "_id": "6",
                "_source": {
                  "@timestamp": "1234568896",
                  "@timestamp_pretty": "17-12-2022",
                  "event_type": "alert",
                  "host": "doom",
                  "port": 65123,
                  "bool": true,
                  "os": "redhat",
                  "version": "20.10.0",
                  "id": 16
                }
              }
            ]
          },
          {
            "join_keys": [
              "farcry" __],
            "events": [
              {
                "_index": "my-index-000001",
                "_id": "3",
                "_source": {
                  "@timestamp": "1234567893",
                  "@timestamp_pretty": "12-12-2022",
                  "event_type": "alert",
                  "type_test": "abc",
                  "host": "farcry",
                  "uptime": 1,
                  "port": 1234,
                  "bool": false,
                  "os": "win10",
                  "version": "2.0.0",
                  "id": 13
                }
              },
              {
                "_index": "my-index-000001",
                "_id": "10",
                "_source": {
                  "@timestamp": "1234567893",
                  "missing_keyword": null,
                  "ip": "10.0.0.5",
                  "event_type": "alert",
                  "host": "farcry",
                  "uptime": 1,
                  "port": 1234,
                  "bool": true,
                  "os": "win10",
                  "version": "1.2.3",
                  "id": 110
                }
              },
              {
                "_index": "my-index-000003",
                "_id": "3",
                "_source": {
                  "@timestamp": "1334567893",
                  "event_type": "alert",
                  "host": "farcry",
                  "bool": true,
                  "os": "win10",
                  "id": 33
                }
              }
            ]
          }
        ]
      }
    }

__

|

第一个示例中的事件对于"主机"的值为"doom"。   ---|---    __

|

此事件与第一个筛选器匹配。   __

|

此事件与第二个筛选器匹配。   __

|

此事件与第三个筛选器匹配。   __

|

第二个样本中的事件具有"host"的值"farcry"。   您可以指定多个联接键：

    
    
    GET /my-index*/_eql/search
    {
      "query": """
        sample by host
          [any where uptime > 0]   by os
          [any where port > 100]   by op_sys
          [any where bool == true] by os
      """
    }

此查询将返回示例，其中每个事件共享相同的值对于"os"或"op_sys"以及"host"。例如：

    
    
    {
      ...
      "hits": {
        "total": {
          "value": 2,
          "relation": "eq"
        },
        "sequences": [
          {
            "join_keys": [
              "doom",                                      __"redhat"
            ],
            "events": [
              {
                "_index": "my-index-000001",
                "_id": "7",
                "_source": {
                  "@timestamp": "1234567897",
                  "@timestamp_pretty": "17-12-2022",
                  "missing_keyword": "yyy",
                  "event_type": "failure",
                  "host": "doom",
                  "uptime": 15,
                  "port": 1234,
                  "bool": true,
                  "os": "redhat",
                  "version": "20.2.0",
                  "id": 17
                }
              },
              {
                "_index": "my-index-000002",
                "_id": "6",
                "_source": {
                  "@timestamp": "1234568996",
                  "@timestamp_pretty": "2022-12-17",
                  "ip": "10.0.0.5",
                  "event_type": "alert",
                  "host": "doom",
                  "port": 65123,
                  "bool": true,
                  "op_sys": "redhat",
                  "id": 26
                }
              },
              {
                "_index": "my-index-000001",
                "_id": "6",
                "_source": {
                  "@timestamp": "1234568896",
                  "@timestamp_pretty": "17-12-2022",
                  "event_type": "alert",
                  "host": "doom",
                  "port": 65123,
                  "bool": true,
                  "os": "redhat",
                  "version": "20.10.0",
                  "id": 16
                }
              }
            ]
          },
          {
            "join_keys": [
              "farcry",
              "win10"
            ],
            "events": [
              {
                "_index": "my-index-000001",
                "_id": "3",
                "_source": {
                  "@timestamp": "1234567893",
                  "@timestamp_pretty": "12-12-2022",
                  "event_type": "alert",
                  "type_test": "abc",
                  "host": "farcry",
                  "uptime": 1,
                  "port": 1234,
                  "bool": false,
                  "os": "win10",
                  "version": "2.0.0",
                  "id": 13
                }
              },
              {
                "_index": "my-index-000002",
                "_id": "3",
                "_source": {
                  "@timestamp": "1234567993",
                  "type_test": "abc",
                  "@timestamp_pretty": "2022-12-17",
                  "event_type": "alert",
                  "host": "farcry",
                  "uptime": 1,
                  "port": 1234,
                  "bool": false,
                  "op_sys": "win10",
                  "id": 23
                }
              },
              {
                "_index": "my-index-000001",
                "_id": "10",
                "_source": {
                  "@timestamp": "1234567893",
                  "missing_keyword": null,
                  "ip": "10.0.0.5",
                  "event_type": "alert",
                  "host": "farcry",
                  "uptime": 1,
                  "port": 1234,
                  "bool": true,
                  "os": "win10",
                  "version": "1.2.3",
                  "id": 110
                }
              }
            ]
          }
        ]
      }
    }

__

|

此示例中的事件对于"主机"的值为"doom"，对于"os"或"op_sys"的值为"redhat"。   ---|--- 默认情况下，示例查询的响应最多包含 10 个样本，每个唯一的联接键集包含一个样本。使用"size"参数获取更小或更大的样本集。若要检索每组联接键的多个示例，请使用"max_samples_per_key"参数。示例查询不支持管道。

    
    
    GET /my-index*/_eql/search
    {
      "max_samples_per_key": 2,     __"size": 20, __"query": """
        sample
          [any where uptime > 0]   by host,os
          [any where port > 100]   by host,op_sys
          [any where bool == true] by host,os
      """
    }

__

|

每组联接键最多检索 2 个样本。   ---|---    __

|

总共最多可检索 20 个样本。   ### 检索所选字段编辑

默认情况下，搜索响应中的每个命中都包含文档"_source"，这是为文档编制索引时提供的整个 JSON 对象。

您可以使用"filter_path"查询参数来筛选 API 响应。例如，以下搜索仅返回每个匹配事件的"_source"中的时间戳和 PID。

    
    
    GET /my-data-stream/_eql/search?filter_path=hits.events._source.@timestamp,hits.events._source.process.pid
    {
      "query": """
        process where process.name == "regsvr32.exe"
      """
    }

API 返回以下响应。

    
    
    {
      "hits": {
        "events": [
          {
            "_source": {
              "@timestamp": "2099-12-07T11:07:09.000Z",
              "process": {
                "pid": 2012
              }
            }
          },
          {
            "_source": {
              "@timestamp": "2099-12-07T11:07:10.000Z",
              "process": {
                "pid": 2012
              }
            }
          }
        ]
      }
    }

您还可以使用"fields"参数来检索响应中的特定字段并设置其格式。此字段与搜索 API 的"字段"参数相同。

由于它查询索引映射，因此与直接引用"_source"相比，"fields"参数提供了几个优点。具体来说，"字段"参数：

* 以与其映射类型匹配的标准化方式返回每个值 * 接受多字段和字段别名 * 设置日期和空间数据类型的格式 * 检索运行时字段值 * 返回脚本在索引时计算的字段 * 使用查找运行时字段从相关索引返回字段

以下搜索请求使用"fields"参数检索"event.type"字段的值，所有以"process."开头的字段和"@timestamp"字段。该请求还使用"filter_path"查询参数来排除每个匹配的"_source"。

    
    
    GET /my-data-stream/_eql/search?filter_path=-hits.events._source
    {
      "query": """
        process where process.name == "regsvr32.exe"
      """,
      "fields": [
        "event.type",
        "process.*",                __{
          "field": "@timestamp",
          "format": "epoch_millis" __}
      ]
    }

__

|

接受完整字段名称和通配符模式。   ---|---    __

|

使用"format"参数为字段的值应用自定义格式。   响应在每次命中的"字段"部分中以平面列表的形式包含值。

    
    
    {
      ...
      "hits": {
        "total": ...,
        "events": [
          {
            "_index": ".ds-my-data-stream-2099.12.07-000001",
            "_id": "OQmfCaduce8zoHT93o4H",
            "fields": {
              "process.name": [
                "regsvr32.exe"
              ],
              "process.name.keyword": [
                "regsvr32.exe"
              ],
              "@timestamp": [
                "4100324829000"
              ],
              "process.command_line": [
                "regsvr32.exe  /s /u /i:https://...RegSvr32.sct scrobj.dll"
              ],
              "process.command_line.keyword": [
                "regsvr32.exe  /s /u /i:https://...RegSvr32.sct scrobj.dll"
              ],
              "process.executable.keyword": [
                "C:\\Windows\\System32\\regsvr32.exe"
              ],
              "process.pid": [
                2012
              ],
              "process.executable": [
                "C:\\Windows\\System32\\regsvr32.exe"
              ]
            }
          },
          ....
        ]
      }
    }

### 使用运行时字段

使用"runtime_mappings"参数在搜索期间提取和创建运行时字段。使用"fields"参数在响应中包含运行时字段。

以下搜索从"@timestamp"创建一个"day_of_week"运行时字段，并在响应中返回该字段。

    
    
    GET /my-data-stream/_eql/search?filter_path=-hits.events._source
    {
      "runtime_mappings": {
        "day_of_week": {
          "type": "keyword",
          "script": "emit(doc['@timestamp'].value.dayOfWeekEnum.toString())"
        }
      },
      "query": """
        process where process.name == "regsvr32.exe"
      """,
      "fields": [
        "@timestamp",
        "day_of_week"
      ]
    }

该 API 返回：

    
    
    {
      ...
      "hits": {
        "total": ...,
        "events": [
          {
            "_index": ".ds-my-data-stream-2099.12.07-000001",
            "_id": "OQmfCaduce8zoHT93o4H",
            "fields": {
              "@timestamp": [
                "2099-12-07T11:07:09.000Z"
              ],
              "day_of_week": [
                "MONDAY"
              ]
            }
          },
          ....
        ]
      }
    }

### 指定时间戳或事件类别字段

EQL 搜索 API 默认使用弹性云服务器中的"@timestamp"和"事件类别"字段。要指定不同的字段，请使用"timestamp_field"和"event_category_field"参数：

    
    
    GET /my-data-stream/_eql/search
    {
      "timestamp_field": "file.accessed",
      "event_category_field": "file.type",
      "query": """
        file where (file.size > 1 and file.type == "file")
      """
    }

事件类别字段必须映射为"关键字"系列字段类型。时间戳字段应映射为"日期"字段类型。不支持"date_nanos"时间戳字段。不能使用"嵌套"字段或"嵌套"字段的子字段作为时间戳或事件类别字段。

### 指定排序仲裁系统

默认情况下，EQL 搜索 API 按时间戳返回匹配的命中。如果两个或更多事件共享相同的时间戳，Elasticsearch 将使用仲裁字段值按升序对事件进行排序。Elasticsearch 将没有仲裁值的事件排序在具有值的事件之后。

如果您没有指定仲裁字段，或者事件也共享相同的仲裁值，Elasticsearch 会考虑并发事件，并且可能不会以一致的排序顺序返回它们。

要指定仲裁字段，请使用"tiebreaker_field"参数。如果您使用弹性云服务器，我们建议使用"事件.序列"作为仲裁字段。

    
    
    GET /my-data-stream/_eql/search
    {
      "tiebreaker_field": "event.sequence",
      "query": """
        process where process.name == "cmd.exe" and stringContains(process.executable, "System32")
      """
    }

### 使用 QueryDSL 进行筛选

"filter"参数使用查询 DSL 来限制运行 EQL 查询的文档。

    
    
    GET /my-data-stream/_eql/search
    {
      "filter": {
        "range": {
          "@timestamp": {
            "gte": "now-1d/d",
            "lt": "now/d"
          }
        }
      },
      "query": """
        file where (file.type == "file" and file.name == "cmd.exe")
      """
    }

### 运行异步 EQLsearch

默认情况下，EQL 搜索请求是同步的，并在返回响应之前等待完整的结果。但是，在大型数据集或冻结数据中进行搜索时，可能需要更长的时间才能获得完整的结果。

为避免长时间等待，请运行异步 EQL 搜索。将"wait_for_completion_timeout"设置为要等待同步结果的持续时间。

    
    
    GET /my-data-stream/_eql/search
    {
      "wait_for_completion_timeout": "2s",
      "query": """
        process where process.name == "cmd.exe"
      """
    }

如果请求未在超时期限内完成，则搜索将变为 sasync 并返回包含以下内容的响应：

* 搜索 ID * "is_partial"值为"true"，表示搜索结果不完整 * "is_running"值为"true"，表示搜索正在进行中

异步搜索继续在后台运行，而不会阻止其他请求。

    
    
    {
      "id": "FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=",
      "is_partial": true,
      "is_running": true,
      "took": 2000,
      "timed_out": false,
      "hits": ...
    }

要检查异步搜索的进度，请使用带有搜索 ID 的获取异步 EQL 搜索API。在"wait_for_completion_timeout"参数中指定您希望多长时间才能获得完整结果。

    
    
    response = client.eql.get(
      id: 'FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=',
      wait_for_completion_timeout: '2s'
    )
    puts response
    
    
    GET /_eql/search/FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=?wait_for_completion_timeout=2s

如果响应的"is_running"值为"false"，则异步搜索已完成。如果"is_partial"值为"false"，则返回的搜索结果已完成。

    
    
    {
      "id": "FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=",
      "is_partial": false,
      "is_running": false,
      "took": 2000,
      "timed_out": false,
      "hits": ...
    }

检查异步搜索进度的另一种更轻量级的方法是将获取异步 EQL 状态 API 与搜索 ID 一起使用。

    
    
    response = client.eql.get_status(
      id: 'FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE='
    )
    puts response
    
    
    GET /_eql/search/status/FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=
    
    
    {
      "id": "FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=",
      "is_running": false,
      "is_partial": false,
      "expiration_time_in_millis": 1611690295000,
      "completion_status": 200
    }

### 更改搜索保留期

默认情况下，EQL 搜索 API 将异步搜索存储五天。在此期限之后，将删除所有搜索及其结果。使用"keep_alive"参数更改此保留期：

    
    
    GET /my-data-stream/_eql/search
    {
      "keep_alive": "2d",
      "wait_for_completion_timeout": "2s",
      "query": """
        process where process.name == "cmd.exe"
      """
    }

可以使用获取异步 EQL 搜索 API 的"keep_alive"参数稍后更改保留期。新的保留期从 get 请求运行后开始。

    
    
    response = client.eql.get(
      id: 'FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=',
      keep_alive: '5d'
    )
    puts response
    
    
    GET /_eql/search/FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=?keep_alive=5d

使用删除异步 EQL 搜索 API 在"keep_alive"周期结束之前手动删除异步 EQL 搜索。如果搜索仍在进行中，Elasticsearch 会取消搜索请求。

    
    
    response = client.eql.delete(
      id: 'FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE='
    )
    puts response
    
    
    DELETE /_eql/search/FmNJRUZ1YWZCU3dHY1BIOUhaenVSRkEaaXFlZ3h4c1RTWFNocDdnY2FSaERnUTozNDE=

### 存储同步 EQL 搜索

默认情况下，EQL 搜索 API 仅存储异步搜索。要保存异步搜索，请将"keep_on_completion"设置为"true"：

    
    
    GET /my-data-stream/_eql/search
    {
      "keep_on_completion": true,
      "wait_for_completion_timeout": "2s",
      "query": """
        process where process.name == "cmd.exe"
      """
    }

响应包括搜索 ID."is_partial"和"is_running"为"false"，表示 EQL 搜索是同步的并返回完整的结果。

    
    
    {
      "id": "FjlmbndxNmJjU0RPdExBTGg0elNOOEEaQk9xSjJBQzBRMldZa1VVQ2pPa01YUToxMDY=",
      "is_partial": false,
      "is_running": false,
      "took": 52,
      "timed_out": false,
      "hits": ...
    }

稍后使用获取异步 EQL 搜索 API 获取相同的结果：

    
    
    response = client.eql.get(
      id: 'FjlmbndxNmJjU0RPdExBTGg0elNOOEEaQk9xSjJBQzBRMldZa1VVQ2pPa01YUToxMDY='
    )
    puts response
    
    
    GET /_eql/search/FjlmbndxNmJjU0RPdExBTGg0elNOOEEaQk9xSjJBQzBRMldZa1VVQ2pPa01YUToxMDY=

保存的同步搜索仍受"keep_alive"参数的保留期的约束。此时间段结束时，将删除搜索及其结果。

您还可以使用获取异步 EQL 状态 API 仅检查保存的同步搜索的状态，而不检查结果。

您还可以使用删除异步 EQL 搜索 API 手动删除保存的同步搜索。

### 跨集群运行 EQL 搜索

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

EQL 搜索 API 支持跨集群搜索。但是，如果本地集群和远程集群的版本低于 7.17.7(包含)或低于 8.5.1(包含)，则必须使用相同的 Elasticsearch 版本。

以下群集更新设置请求添加两个远程群集："cluster_one"和"cluster_two"。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          cluster: {
            remote: {
              cluster_one: {
                seeds: [
                  '127.0.0.1:9300'
                ]
              },
              cluster_two: {
                seeds: [
                  '127.0.0.1:9301'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "persistent": {
        "cluster": {
          "remote": {
            "cluster_one": {
              "seeds": [
                "127.0.0.1:9300"
              ]
            },
            "cluster_two": {
              "seeds": [
                "127.0.0.1:9301"
              ]
            }
          }
        }
      }
    }

若要将远程群集上的数据流或索引作为目标，请使用"<cluster>："<target>语法。

    
    
    GET /cluster_one:my-data-stream,cluster_two:my-data-stream/_eql/search
    {
      "query": """
        process where process.name == "regsvr32.exe"
      """
    }

### EQL 断路器设置

相关的断路器设置可以在断路器页面中找到。

[« Geospatial analysis](geospatial-analysis.md) [EQL syntax reference
»](eql-syntax.md)
