

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md) ›[Ingest processor reference](processors.md)

[« Geo-grid processor](ingest-geo-grid-processor.md) [Grok processor
»](grok-processor.md)

## 地理IP处理器

"geoip"处理器添加有关IPv4或IPv6地址地理位置的信息。

默认情况下，处理器使用MaxMind的GeoLite2 City，GeoLite2 Country和GeoLite2 ASN GeoIP2数据库，这些数据库在CCBY-SA 4.0许可证下共享。如果您的节点可以连接到"storage.googleapis.com"域并且以下任一情况，它会自动下载这些数据库：

* "ingest.geoip.downloader.eager.download"设置为 true * 您的集群至少有一个带有"geoip"处理器的管道

Elasticsearch 会自动从 Elastic GeoIP 端点下载这些数据库的更新：https：//geoip.elastic.co/v1/database。若要获取这些更新的下载统计信息，请使用 GeoIP 统计信息 API。

如果您的集群无法连接到弹性 GeoIP 终端节点，或者您想要管理自己的更新，请参阅管理您自己的 GeoIP2 数据库更新。

如果 Elasticsearch 在 30 天内无法连接到端点，则所有更新的数据库都将变为无效。Elasticsearch 将停止使用 geoip 数据丰富文档，而是添加"tags： ["_geoip_expired_database"]"字段。

### 在管道中使用"geoip"处理器

**表 22."geoip"选项**

姓名 |必填 |默认 |描述 ---|---|---|--- 'field'

|

yes

|

-

|

用于从中获取用于地理查找的 IP 地址的字段。   "target_field"

|

no

|

geoip

|

保存从MaxMind数据库中查找的地理信息的字段。   "database_file"

|

no

|

GeoLite2-City.mmdb

|

数据库文件名是指模块附带的数据库(GeoLite2-City.mmdb、GeoLite2-Country.mmdb 或 GeoLite2-ASN.mmdb)或"ingest-geoip"配置目录中的自定义数据库。   "属性"

|

no

|

["continent_name"、"country_iso_code"、"country_name"、"region_iso_code"、"region_name"、"city_name"、"位置"] *

|

根据地理查找控制将哪些属性添加到"target_field"。   "ignore_missing"

|

no

|

`false`

|

如果"true"和"field"不存在，处理器将悄悄退出，而不修改文档"first_only"

|

no

|

`true`

|

如果"true"，则仅返回首先找到的geoip数据，即使"field"包含数组"download_database_on_pipeline_creation"

|

no

|

`true`

|

如果"true"(并且"ingest.geoip.downloader.eager.download"为"false")，则在创建管道时下载缺少的数据库。否则，当管道用作索引中的"default_pipeline"或"final_pipeline"时，会触发下载。   *取决于"database_file"中可用的内容：

* 如果使用GeoLite2 City数据库，则可以在"target_field"下添加以下字段："ip"，"country_iso_code"，"country_name"，"continent_name"，"region_iso_code"，"region_name"，"city_name"，"时区"，"纬度"，"经度"和"位置"。实际添加的字段取决于已找到的内容以及在"属性"中配置的属性。  * 如果使用GeoLite2国家数据库，则可以在"target_field"下添加以下字段："ip"，"country_iso_code"，"country_name"和"continent_name"。实际添加的字段取决于已找到的内容以及在"属性"中配置的属性。  * 如果使用 GeoLite2 ASN 数据库，则可以在"target_field"下添加以下字段："ip"、"asn"、"organization_name"和"网络"。实际添加的字段取决于已找到的内容以及在"属性"中配置的属性。

下面是一个使用默认城市数据库并根据"ip"字段将地理信息添加到"geoip"字段的示例：

    
    
    response = client.ingest.put_pipeline(
      id: 'geoip',
      body: {
        description: 'Add geoip info',
        processors: [
          {
            geoip: {
              field: 'ip'
            }
          }
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'my_id',
      pipeline: 'geoip',
      body: {
        ip: '89.160.20.128'
      }
    )
    puts response
    
    response = client.get(
      index: 'my-index-000001',
      id: 'my_id'
    )
    puts response
    
    
    PUT _ingest/pipeline/geoip
    {
      "description" : "Add geoip info",
      "processors" : [
        {
          "geoip" : {
            "field" : "ip"
          }
        }
      ]
    }
    PUT my-index-000001/_doc/my_id?pipeline=geoip
    {
      "ip": "89.160.20.128"
    }
    GET my-index-000001/_doc/my_id

其中返回：

    
    
    {
      "found": true,
      "_index": "my-index-000001",
      "_id": "my_id",
      "_version": 1,
      "_seq_no": 55,
      "_primary_term": 1,
      "_source": {
        "ip": "89.160.20.128",
        "geoip": {
          "continent_name": "Europe",
          "country_name": "Sweden",
          "country_iso_code": "SE",
          "city_name" : "Linköping",
          "region_iso_code" : "SE-E",
          "region_name" : "Östergötland County",
          "location": { "lat": 58.4167, "lon": 15.6167 }
        }
      }
    }

下面是一个使用默认国家/地区数据库并根据"ip"字段将地理信息添加到"geo"字段的示例。请注意，此数据库包含在模块中。所以这个：

    
    
    response = client.ingest.put_pipeline(
      id: 'geoip',
      body: {
        description: 'Add geoip info',
        processors: [
          {
            geoip: {
              field: 'ip',
              target_field: 'geo',
              database_file: 'GeoLite2-Country.mmdb'
            }
          }
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'my_id',
      pipeline: 'geoip',
      body: {
        ip: '89.160.20.128'
      }
    )
    puts response
    
    response = client.get(
      index: 'my-index-000001',
      id: 'my_id'
    )
    puts response
    
    
    PUT _ingest/pipeline/geoip
    {
      "description" : "Add geoip info",
      "processors" : [
        {
          "geoip" : {
            "field" : "ip",
            "target_field" : "geo",
            "database_file" : "GeoLite2-Country.mmdb"
          }
        }
      ]
    }
    PUT my-index-000001/_doc/my_id?pipeline=geoip
    {
      "ip": "89.160.20.128"
    }
    GET my-index-000001/_doc/my_id

返回以下内容：

    
    
    {
      "found": true,
      "_index": "my-index-000001",
      "_id": "my_id",
      "_version": 1,
      "_seq_no": 65,
      "_primary_term": 1,
      "_source": {
        "ip": "89.160.20.128",
        "geo": {
          "continent_name": "Europe",
          "country_name": "Sweden",
          "country_iso_code": "SE"
        }
      }
    }

并非所有 IP 地址都从数据库中查找地理信息，发生这种情况时，不会在文档中插入"target_field"。

下面是在找不到"80.231.5.0"的信息时将索引的文档的示例：

    
    
    response = client.ingest.put_pipeline(
      id: 'geoip',
      body: {
        description: 'Add geoip info',
        processors: [
          {
            geoip: {
              field: 'ip'
            }
          }
        ]
      }
    )
    puts response
    
    response = client.index(
      index: 'my-index-000001',
      id: 'my_id',
      pipeline: 'geoip',
      body: {
        ip: '80.231.5.0'
      }
    )
    puts response
    
    response = client.get(
      index: 'my-index-000001',
      id: 'my_id'
    )
    puts response
    
    
    PUT _ingest/pipeline/geoip
    {
      "description" : "Add geoip info",
      "processors" : [
        {
          "geoip" : {
            "field" : "ip"
          }
        }
      ]
    }
    
    PUT my-index-000001/_doc/my_id?pipeline=geoip
    {
      "ip": "80.231.5.0"
    }
    
    GET my-index-000001/_doc/my_id

其中返回：

    
    
    {
      "_index" : "my-index-000001",
      "_id" : "my_id",
      "_version" : 1,
      "_seq_no" : 71,
      "_primary_term": 1,
      "found" : true,
      "_source" : {
        "ip" : "80.231.5.0"
      }
    }

#### 将位置识别为地理点

尽管此处理器使用包含 IP 地址的估计纬度和经度的"位置"字段来丰富您的文档，但如果没有在映射中明确定义该字段，则不会在 Elasticsearch 中将此字段索引为"geo_point"类型。

您可以对上面的示例索引使用以下映射：

    
    
    response = client.indices.create(
      index: 'my_ip_locations',
      body: {
        mappings: {
          properties: {
            geoip: {
              properties: {
                location: {
                  type: 'geo_point'
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT my_ip_locations
    {
      "mappings": {
        "properties": {
          "geoip": {
            "properties": {
              "location": { "type": "geo_point" }
            }
          }
        }
      }
    }

### 管理您自己的 GeoIP2 数据库更新

如果您无法从弹性终端节点自动更新 GeoIP2 数据库，则还有其他一些选择：

* 使用代理端点 * 使用自定义端点 * 手动更新您的 GeoIP2 数据库

**使用代理终结点**

如果无法直接连接到弹性 GeoIP 终端节点，请考虑设置安全代理。然后，您可以在每个节点的"elasticsearch.yml"文件的"ingest.geoip.downloader.endpoint"设置中指定代理端点URL。

在严格设置中，可能需要将以下域添加到允许域列表中：

* "geoip.elastic.co" * "storage.googleapis.com"

**使用自定义终结点**

您可以创建模拟弹性 GeoIP 终端节点的服务。然后，您可以从此服务获取自动更新。

1. 从 MaxMind 站点下载您的".mmdb"数据库文件。  2. 将数据库文件复制到单个目录。  3. 从你的 Elasticsearch 目录中，运行：./bin/elasticsearch-geoip -s my/source/dir [-t target/directory]

4. 提供目录中的静态数据库文件。例如，您可以使用Docker从nginx服务器提供文件：docker run -v my/source/dir：/usr/share/nginx/html：ro nginx

5. 在每个节点的"elasticsearch.yml"文件的"ingest.geoip.downloader.endpoint"设置中指定服务的终端节点 URL。

默认情况下，Elasticsearch 每三天检查一次端点是否有更新。要使用另一个轮询间隔，请使用群集更新设置 API 设置"ingest.geoip.downloader.poll.interval"。

**手动更新您的GeoIP2数据库**

1. 使用群集更新设置 API 将"ingest.geoip.downloader.enabled"设置为"false"。这将禁用可能覆盖数据库更改的自动更新。这也会删除所有下载的数据库。  2. 从 MaxMind 站点下载您的".mmdb"数据库文件。

您还可以使用自定义城市、国家/地区和 ASN".mmdb"文件。这些文件必须解压缩，并使用相应的"-City.mmdb"、"-Country.mmdb"或"-ASN.mmdb"扩展名。

3. 在 Elasticsearch Service 部署中，使用自定义捆绑包上传数据库。  4. 在自我管理部署中，将数据库文件复制到"$ES_CONFIG/ingest-geoip"。  5. 在"geoip"处理器中，配置"database_file"参数以使用自定义数据库文件。

#### 节点设置

"geoip"处理器支持以下设置：

`ingest.geoip.cache_size`

     The maximum number of results that should be cached. Defaults to `1000`. 

请注意，这些设置是节点设置，适用于所有"geoip"处理器，即所有定义的"geoip"处理器都有一个缓存。

#### 群集设置

`ingest.geoip.downloader.enabled`

     ([Dynamic](settings.html#dynamic-cluster-setting), Boolean) If `true`, Elasticsearch automatically downloads and manages updates for GeoIP2 databases from the `ingest.geoip.downloader.endpoint`. If `false`, Elasticsearch does not download updates and deletes all downloaded databases. Defaults to `true`. 

`ingest.geoip.downloader.eager.download`

     ([Dynamic](settings.html#dynamic-cluster-setting), Boolean) If `true`, Elasticsearch downloads GeoIP2 databases immediately, regardless of whether a pipeline exists with a geoip processor. If `false`, Elasticsearch only begins downloading the databases if a pipeline with a geoip processor exists or is added. Defaults to `false`. 

`ingest.geoip.downloader.endpoint`

     ([Static](settings.html#static-cluster-setting), string) Endpoint URL used to download updates for GeoIP2 databases. For example, `https://myDomain.com/overview.json`. Defaults to `https://geoip.elastic.co/v1/database`. Elasticsearch stores downloaded database files in each node's [temporary directory](important-settings.html#es-tmpdir "Temporary directory settings") at `$ES_TMPDIR/geoip-databases/<node_id>`. Note that Elasticsearch will make a GET request to `${ingest.geoip.downloader.endpoint}?elastic_geoip_service_tos=agree`, expecting the list of metadata about databases typically found in `overview.json`. 

`ingest.geoip.downloader.poll.interval`

     ([Dynamic](settings.html#dynamic-cluster-setting), [time value](api-conventions.html#time-units "Time units")) How often Elasticsearch checks for GeoIP2 database updates at the `ingest.geoip.downloader.endpoint`. Must be greater than `1d` (one day). Defaults to `3d` (three days). 

[« Geo-grid processor](ingest-geo-grid-processor.md) [Grok processor
»](grok-processor.md)
