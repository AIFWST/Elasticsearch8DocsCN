

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md)

[« Ingest pipelines](ingest.md) [Enrich your data »](ingest-enriching-
data.md)

## 示例：解析通用日志格式的日志

在此示例教程中，你将使用引入管道在编制索引之前以通用 LogFormat 解析服务器日志。在开始之前，请检查引入管道的先决条件。

要分析的日志如下所示：

    
    
    212.87.37.154 - - [05/May/2099:16:21:15 +0000] "GET /favicon.ico HTTP/1.1" 200 3638 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"

这些日志包含时间戳、IP 地址和用户代理。您希望在 Elasticsearch 中为这三个项目提供自己的字段，以便更快地进行搜索和可视化。您还想知道请求来自何处。

1. 在 Kibana 中，打开主菜单并单击 **堆栈管理** > **摄取管道**。

!Kibana 的采集管道列表视图

2. 单击"新建管道>创建管道**"。  3. 将"名称"设置为"我的管道"，并选择性地为管道添加描述。  4. 添加 grok 处理器以解析日志消息：

    1. Click **Add a processor** and select the **Grok** processor type. 
    2. Set **Field** to `message` and **Patterns** to the following [grok pattern](grok.html "Grokking grok"):
        
                %{IPORHOST:source.ip} %{USER:user.id} %{USER:user.name} \[%{HTTPDATE:@timestamp}\] "%{WORD:http.request.method} %{DATA:url.original} HTTP/%{NUMBER:http.version}" %{NUMBER:http.response.status_code:int} (?:-|%{NUMBER:http.response.body.bytes:int}) %{QS:http.request.referrer} %{QS:user_agent}

    3. Click **Add** to save the processor. 
    4. Set the processor description to `Extract fields from 'message'`. 

5. 为时间戳、IP 地址和用户代理字段添加处理器。按如下方式配置处理器：

处理器类型 |字段 |其他选项 |描述 ---|---|---|--- **日期**

|

`@timestamp`

|

**格式** ： '日/MMM/yyyy：HH：mm：ss Z'

|

'将'@timestamp'格式设置为'dd/MMM/yyyy：HH：mm：ss Z'' **GeoIP**

|

`source.ip`

|

**目标字段** ： 'source.geo'

|

"为"source.ip"添加'source.geo'GeoIP数据" **用户代理**

|

`user_agent`

|

|

"从'user_agent'中提取字段 您的表单应如下所示：

!用于摄取管道的处理器

四个处理器将按顺序运行： 格罗克 > 日期 > GeoIP > 用户代理 您可以使用箭头图标对处理器重新排序。

或者，您可以单击**导入处理器**链接并将处理器定义为 JSON：

    
        {
      "processors": [
        {
          "grok": {
            "description": "Extract fields from 'message'",
            "field": "message",
            "patterns": ["%{IPORHOST:source.ip} %{USER:user.id} %{USER:user.name} \\[%{HTTPDATE:@timestamp}\\] \"%{WORD:http.request.method} %{DATA:url.original} HTTP/%{NUMBER:http.version}\" %{NUMBER:http.response.status_code:int} (?:-|%{NUMBER:http.response.body.bytes:int}) %{QS:http.request.referrer} %{QS:user_agent}"]
          }
        },
        {
          "date": {
            "description": "Format '@timestamp' as 'dd/MMM/yyyy:HH:mm:ss Z'",
            "field": "@timestamp",
            "formats": [ "dd/MMM/yyyy:HH:mm:ss Z" ]
          }
        },
        {
          "geoip": {
            "description": "Add 'source.geo' GeoIP data for 'source.ip'",
            "field": "source.ip",
            "target_field": "source.geo"
          }
        },
        {
          "user_agent": {
            "description": "Extract fields from 'user_agent'",
            "field": "user_agent"
          }
        }
      ]
    
    }

6. 要测试管道，请单击"**添加文档**"。  7. 在"**文档**"选项卡中，提供用于测试的示例文档：[ { "_source"： { "消息"： "212.87.37.154 - - [05/May/2099：16：21：15 +0000] \"GET /favicon.ico HTTP/1.1\" 200 3638 \"-\" "Mozilla/5.0 (Macintosh;Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML， like Gecko) Chrome/52.0.2743.116 Safari/537.36\"" } } ]

8. 单击"**运行管道**"并验证管道是否按预期工作。  9. 如果一切正常，请关闭面板，然后单击"创建管道**"。

现在，你已准备好将日志数据编制到数据流。

10. 创建启用了数据流的索引模板。           PUT _index_template/my-data-stream-template { "index_patterns"： [ "my-data-stream*" ]， "data_stream"： { }， "priority"： 500 }

11. 使用您创建的管道为文档编制索引。           POST my-data-stream/_doc？pipeline=my-pipeline { "message"： "89.160.20.128 - - [05/May/2099：16：21：15 +0000] \"GET /favicon.ico HTTP/1.1\" 200 3638 \"-\" "Mozilla/5.0 (Macintosh;Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML， like Gecko) Chrome/52.0.2743.116 Safari/537.36\"" }

12. 要进行验证，请搜索数据流以检索文档。以下搜索使用"filter_path"仅返回文档源。           响应 = client.search( index： 'my-data-stream'， filter_path： 'hits.hits._source' ) 把响应 GET my-data-stream/_search？filter_path=hits.hits._source

该 API 返回：

    
        {
      "hits": {
        "hits": [
          {
            "_source": {
              "@timestamp": "2099-05-05T16:21:15.000Z",
              "http": {
                "request": {
                  "referrer": "\"-\"",
                  "method": "GET"
                },
                "response": {
                  "status_code": 200,
                  "body": {
                    "bytes": 3638
                  }
                },
                "version": "1.1"
              },
              "source": {
                "ip": "89.160.20.128",
                "geo": {
                  "continent_name" : "Europe",
                  "country_name" : "Sweden",
                  "country_iso_code" : "SE",
                  "city_name" : "Linköping",
                  "region_iso_code" : "SE-E",
                  "region_name" : "Östergötland County",
                  "location" : {
                    "lon" : 15.6167,
                    "lat" : 58.4167
                  }
                }
              },
              "message": "89.160.20.128 - - [05/May/2099:16:21:15 +0000] \"GET /favicon.ico HTTP/1.1\" 200 3638 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36\"",
              "url": {
                "original": "/favicon.ico"
              },
              "user": {
                "name": "-",
                "id": "-"
              },
              "user_agent": {
                "original": "\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36\"",
                "os": {
                  "name": "Mac OS X",
                  "version": "10.11.6",
                  "full": "Mac OS X 10.11.6"
                },
                "name": "Chrome",
                "device": {
                  "name": "Mac"
                },
                "version": "52.0.2743.116"
              }
            }
          }
        ]
      }
    }

[« Ingest pipelines](ingest.md) [Enrich your data »](ingest-enriching-
data.md)
