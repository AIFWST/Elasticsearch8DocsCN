

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Compact and aligned text (CAT) APIs](cat.md)

[« cat pending tasks API](cat-pending-tasks.md) [cat recovery API »](cat-
recovery.md)

## 猫插件API

cat API 仅供使用命令行或 Kibana 控制台的人类使用。它们_不是_供应用程序使用。对于应用程序使用，请使用节点信息 API。

返回在群集的每个节点上运行的插件的列表。

###Request

'获取/_cat/插件'

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

### 查询参数

`format`

     (Optional, string) Short version of the [HTTP accept header](https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html). Valid values include JSON, YAML, etc. 
`h`

     (Optional, string) Comma-separated list of column names to display. 
`help`

     (Optional, Boolean) If `true`, the response includes help information. Defaults to `false`. 
`local`

     (Optional, Boolean) If `true`, the request retrieves information from the local node only. Defaults to `false`, which means information is retrieved from the master node. 
`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`s`

     (Optional, string) Comma-separated list of column names or column aliases used to sort the response. 
`v`

     (Optional, Boolean) If `true`, the response includes column headings. Defaults to `false`. 

###Examples

    
    
    response = client.cat.plugins(
      v: true,
      s: 'component',
      h: 'name,component,version,description'
    )
    puts response
    
    
    GET /_cat/plugins?v=true&s=component&h=name,component,version,description

API 返回以下响应：

    
    
    name    component               version   description
    U7321H6 analysis-icu            8.9.0 The ICU Analysis plugin integrates the Lucene ICU module into Elasticsearch, adding ICU-related analysis components.
    U7321H6 analysis-kuromoji       8.9.0 The Japanese (kuromoji) Analysis plugin integrates Lucene kuromoji analysis module into elasticsearch.
    U7321H6 analysis-nori           8.9.0 The Korean (nori) Analysis plugin integrates Lucene nori analysis module into elasticsearch.
    U7321H6 analysis-phonetic       8.9.0 The Phonetic Analysis plugin integrates phonetic token filter analysis with elasticsearch.
    U7321H6 analysis-smartcn        8.9.0 Smart Chinese Analysis plugin integrates Lucene Smart Chinese analysis module into elasticsearch.
    U7321H6 analysis-stempel        8.9.0 The Stempel (Polish) Analysis plugin integrates Lucene stempel (polish) analysis module into elasticsearch.
    U7321H6 analysis-ukrainian      8.9.0 The Ukrainian Analysis plugin integrates the Lucene UkrainianMorfologikAnalyzer into elasticsearch.
    U7321H6 discovery-azure-classic 8.9.0 The Azure Classic Discovery plugin allows to use Azure Classic API for the unicast discovery mechanism
    U7321H6 discovery-ec2           8.9.0 The EC2 discovery plugin allows to use AWS API for the unicast discovery mechanism.
    U7321H6 discovery-gce           8.9.0 The Google Compute Engine (GCE) Discovery plugin allows to use GCE API for the unicast discovery mechanism.
    U7321H6 mapper-annotated-text   8.9.0 The Mapper Annotated_text plugin adds support for text fields with markup used to inject annotation tokens into the index.
    U7321H6 mapper-murmur3          8.9.0 The Mapper Murmur3 plugin allows to compute hashes of a field's values at index-time and to store them in the index.
    U7321H6 mapper-size             8.9.0 The Mapper Size plugin allows document to record their uncompressed size at index time.
    U7321H6 store-smb               8.9.0 The Store SMB plugin adds support for SMB stores.

[« cat pending tasks API](cat-pending-tasks.md) [cat recovery API »](cat-
recovery.md)
