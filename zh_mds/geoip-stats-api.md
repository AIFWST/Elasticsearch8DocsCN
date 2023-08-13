

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Ingest APIs](ingest-apis.md)

[« Delete pipeline API](delete-pipeline-api.md) [Get pipeline API »](get-
pipeline-api.md)

## GeoIP statsAPI

获取与"geoip"处理器一起使用的 GeoIP2 数据库的下载统计信息。

    
    
    response = client.ingest.geo_ip_stats
    puts response
    
    
    GET _ingest/geoip/stats

###Request

"获取_ingest/地理IP/统计数据"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。  * 如果禁用了"ingest.geoip.downloader.enabled"，则此 API 返回零值和一个空的"节点"对象。

### 响应正文

`stats`

    

(对象)下载所有GeoIP2数据库的统计信息。

"统计"的属性

`successful_downloads`

     (integer) Total number of successful database downloads. 
`failed_downloads`

     (integer) Total number of failed database downloads. 
`total_download_time`

     (integer) Total milliseconds spent downloading databases. 
`database_count`

     (integer) Current number of databases available for use. 
`skipped_updates`

     (integer) Total number of database updates skipped. 

`nodes`

    

(对象)为每个节点下载了GeoIP2数据库。

"节点"的属性

`<node_id>`

    

(对象)已下载节点的数据库。字段键是节点 ID。

""的属性<node_id>

`databases`

    

(对象数组)已下载节点的数据库。

"数据库"对象的属性

`name`

     (string) Name of the database. 

`files_in_temp`

     (array of strings) Downloaded database files, including related license files. Elasticsearch stores these files in the node's [temporary directory](important-settings.html#es-tmpdir "Temporary directory settings"): `$ES_TMPDIR/geoip-databases/<node_id>`. 

[« Delete pipeline API](delete-pipeline-api.md) [Get pipeline API »](get-
pipeline-api.md)
