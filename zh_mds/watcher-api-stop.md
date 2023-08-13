

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Watcher APIs](watcher-api.md)

[« Start watch service API](watcher-api-start.md) [Definitions »](api-
definitions.md)

## 秒表服务接口

停止观察程序服务(如果它正在运行)。

###Request

"发布_watcher/_stop"

###Prerequisites

* 您必须具有"manage_watcher"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

### 查询参数

`master_timeout`

     (Optional, [time units](api-conventions.html#time-units "Time units")) Specifies the period of time to wait for a connection to the master node. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

###Examples

    
    
    response = client.watcher.stop
    puts response
    
    
    POST _watcher/_stop

如果请求成功，观察程序将返回以下响应：

    
    
    {
       "acknowledged": true
    }

[« Start watch service API](watcher-api-start.md) [Definitions »](api-
definitions.md)
