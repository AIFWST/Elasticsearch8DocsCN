

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Script APIs](script-apis.md)

[« Create or update stored script API](create-stored-script-api.md) [Get
script contexts API »](get-script-contexts-api.md)

## 删除存储的脚本接口

删除存储的脚本或搜索模板。

    
    
    response = client.delete_script(
      id: 'my-stored-script'
    )
    puts response
    
    
    DELETE _scripts/my-stored-script

###Request

"删除_scripts/<script-id>"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

### 路径参数

`<script-id>`

     (Required, string) Identifier for the stored script or search template. 

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 
`timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

[« Create or update stored script API](create-stored-script-api.md) [Get
script contexts API »](get-script-contexts-api.md)
