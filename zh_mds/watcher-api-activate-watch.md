

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Watcher APIs](watcher-api.md)

[« Ack watch API](watcher-api-ack-watch.md) [Deactivate watch API
»](watcher-api-deactivate-watch.md)

## 激活监视接口

手表可以处于活动状态，也可以处于非活动状态。此 API 使您能够激活当前处于非活动状态的监视。

###Request

"放_watcher/观察/<watch_id>/_activate"

###Prerequisites

* 您必须具有"manage_watcher"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

### 路径参数

`<watch_id>`

     (Required, string) Identifier for the watch. 

###Examples

调用获取监视 API 时，将随监视定义一起返回非活动监视的状态：

    
    
    GET _watcher/watch/my_watch
    
    
    {
      "found": true,
      "_id": "my_watch",
      "_seq_no": 0,
      "_primary_term": 1,
      "_version": 1,
      "status": {
        "state" : {
          "active" : false,
          "timestamp" : "2015-08-20T12:21:32.734Z"
        },
        "actions": ...,
        "version": 1
      },
      "watch": ...
    }

您可以通过执行以下 API 调用来激活手表：

    
    
    PUT _watcher/watch/my_watch/_activate

手表的新状态将作为其整体状态的一部分返回：

    
    
    {
      "status": {
        "state" : {
          "active" : true,
          "timestamp" : "2015-09-04T08:39:46.816Z"
        },
        "actions": ...,
        "version": 1
      }
    }

[« Ack watch API](watcher-api-ack-watch.md) [Deactivate watch API
»](watcher-api-deactivate-watch.md)
