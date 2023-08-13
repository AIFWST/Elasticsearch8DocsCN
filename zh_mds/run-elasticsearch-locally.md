

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md)

[« Install Elasticsearch with Docker](docker.md) [Configuring Elasticsearch
»](settings.md)

## 在本地运行弹性搜索

要在您自己的机器上试用 Elasticsearch，我们建议使用 Docker 并同时运行 Elasticsearch 和 Kibana。Docker 镜像可从 Elastic Docker 注册表获得。

从 Elasticsearch 8.0 开始，默认情况下启用安全性。首次启动 Elasticsearch 时，系统会自动配置 TLS 加密，为"弹性"用户生成密码，并创建 Kibana 注册令牌，以便您可以将 Kibana 连接到安全集群。

有关其他安装选项，请参阅 Elasticsearch 安装文档。

### 启动弹性搜索

1. 安装并启动 Docker 桌面。转到"首选项">"资源">"高级"**，并将"内存"设置为至少 4GB。  2. 启动一个 Elasticsearch 容器：docker 网络创建弹性 docker 拉取 docker.elastic.co/elasticsearch/elasticsearch:8.9.0 docker run --name elasticsearch --net elastic -p 9200：9200 -p 9300：9300 -e "discovery.type=single-node" -t docker.elastic.co/elasticsearch/elasticsearch:8.9.0

首次启动 Elasticsearch 时，生成的"弹性"用户密码和 Kibana 注册令牌将输出到终端。

您可能需要在终端中向后滚动一点才能查看密码和注册令牌。

3. 复制生成的密码和注册令牌，并将其保存在安全位置。这些值仅在您第一次启动 Elasticsearch 时显示。您将使用这些功能将 Kibana 注册到 Elasticsearch 集群并登录。

### 启动木花

Kibana 使您能够轻松地向 Elasticsearch 发送请求，并以交互方式分析、可视化和管理数据。

1. 在新的终端会话中，启动 Kibana 并将其连接到您的 Elasticsearch 容器： docker pull docker.elastic.co/kibana/kibana:8.9.0 docker run --name kibana --net elastic -p 5601：5601 docker.elastic.co/kibana/kibana:8.9.0

启动 Kibana 时，会将唯一的 URL 输出到您的终端。

2. 要访问 Kibana，请在浏览器中打开生成的 URL。

    1. Paste the enrollment token that you copied when starting Elasticsearch and click the button to connect your Kibana instance with Elasticsearch. 
    2. Log in to Kibana as the `elastic` user with the password that was generated when you started Elasticsearch. 

### 向 Elasticsearch 发送请求

您可以通过 REST API 向 Elasticsearch 发送数据和其他请求。您可以使用任何发送HTTP请求的客户端与Elasticsearch交互，例如Elasticsearch languageclient和curl。Kibana 的开发人员控制台提供了一种简单的方法来试验和测试请求。若要访问控制台，请转到"**管理>开发工具**"。

### 添加数据

您可以通过 REST API 发送 JSON 对象(文档)将数据索引到 Elasticsearch 中。无论您拥有结构化或非结构化文本、数字数据还是地理空间数据，Elasticsearch 都能高效地存储和索引这些数据，从而支持快速搜索。

对于带时间戳的数据(如日志和指标)，您通常会将文档添加到由多个自动生成的支持索引组成的数据流中。

要将单个文档添加到索引，请提交以索引为目标的 HTTP 发布请求。

    
    
    response = client.index(
      index: 'customer',
      id: 1,
      body: {
        firstname: 'Jennifer',
        lastname: 'Walters'
      }
    )
    puts response
    
    
    POST /customer/_doc/1
    {
      "firstname": "Jennifer",
      "lastname": "Walters"
    }

此请求会自动创建"客户"索引(如果不存在)，添加 ID 为 1 的新文档，并存储和索引"名字"和"姓氏"字段。

新文档可立即从群集中的任何节点访问。您可以使用指定其文档 ID 的 GET 请求来检索它：

    
    
    $params = [
        'index' => 'customer',
        'id' => '1',
    ];
    $response = $client->get($params);
    
    
    resp = client.get(index="customer", id="1")
    print(resp)
    
    
    response = client.get(
      index: 'customer',
      id: 1
    )
    puts response
    
    
    res, err := es.Get("customer", "1", es.Get.WithPretty())
    fmt.Println(res, err)
    
    
    const response = await client.get({
      index: 'customer',
      id: '1'
    })
    console.log(response)
    
    
    GET /customer/_doc/1

要在一次请求中添加多个文档，请使用"_bulk"API。批量数据必须是换行符分隔的 JSON (NDJSON)。每行必须以换行符 ('\n) 结尾，包括最后一行。

    
    
    response = client.bulk(
      index: 'customer',
      body: [
        {
          create: {}
        },
        {
          firstname: 'Monica',
          lastname: 'Rambeau'
        },
        {
          create: {}
        },
        {
          firstname: 'Carol',
          lastname: 'Danvers'
        },
        {
          create: {}
        },
        {
          firstname: 'Wanda',
          lastname: 'Maximoff'
        },
        {
          create: {}
        },
        {
          firstname: 'Jennifer',
          lastname: 'Takeda'
        }
      ]
    )
    puts response
    
    
    PUT customer/_bulk
    { "create": { } }
    { "firstname": "Monica","lastname":"Rambeau"}
    { "create": { } }
    { "firstname": "Carol","lastname":"Danvers"}
    { "create": { } }
    { "firstname": "Wanda","lastname":"Maximoff"}
    { "create": { } }
    { "firstname": "Jennifer","lastname":"Takeda"}

###Search

索引文档可用于近乎实时的搜索。以下搜索匹配"客户"索引中名字为 _Jennifer_ 的所有客户。

    
    
    response = client.search(
      index: 'customer',
      body: {
        query: {
          match: {
            firstname: 'Jennifer'
          }
        }
      }
    )
    puts response
    
    
    GET customer/_search
    {
      "query" : {
        "match" : { "firstname": "Jennifer" }
      }
    }

###Explore

您可以使用 Kibana 中的"发现"以交互方式搜索和筛选数据。从那里，您可以开始创建可视化以及构建和共享仪表板。

首先，创建一个连接到一个或多个 Elasticsearch 索引、数据流或索引别名的_data view_。

1. 转到 Kibana >数据视图>管理>堆栈管理**。  2. 选择**创建数据视图**。  3. 输入数据视图的名称以及与一个或多个索引匹配的模式，例如 _customer_。  4. 选择"将数据视图保存到 Kibana**"。

若要开始探索，请转到"**分析>发现**"。

[« Install Elasticsearch with Docker](docker.md) [Configuring Elasticsearch
»](settings.md)
