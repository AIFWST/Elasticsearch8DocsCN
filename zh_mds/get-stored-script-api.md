

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Script APIs](script-apis.md)

[« Get script languages API](get-script-languages-api.md) [Search APIs
»](search.md)

## 获取存储的脚本接口

检索存储的脚本或搜索模板。

    
    
    response = client.get_script(
      id: 'my-stored-script'
    )
    puts response
    
    
    GET _scripts/my-stored-script

###Request

"得到_scripts/<script-id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

### 路径参数

`<script-id>`

     (Required, string) Identifier for the stored script or search template. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

[« Get script languages API](get-script-languages-api.md) [Search APIs
»](search.md)
