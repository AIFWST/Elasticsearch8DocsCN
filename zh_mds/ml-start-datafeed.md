

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Machine learning anomaly detection APIs](ml-ad-
apis.md)

[« Revert model snapshots API](ml-revert-snapshot.md) [Stop datafeeds API
»](ml-stop-datafeed.md)

## 启动数据馈送接口

启动一个或多个数据馈送。

###Request

'POST _ml/datafeeds/<feed_id>/_start'

###Prerequisites

* 必须先打开异常情况检测作业，然后才能启动数据馈送。否则，将发生错误。  * 需要"manage_ml"群集权限。此权限包含在"machine_learning_admin"内置角色中。

###Description

必须启动数据馈送才能从 Elasticsearch 检索数据。Adatafeed 在其整个生命周期中可以多次启动和停止。

如果重新启动已停止的数据馈送，默认情况下，它会从停止后的下一毫秒开始继续处理输入数据。如果在停止和启动之间的精确毫秒内为新数据编制了索引，则将忽略该数据。

启用 Elasticsearch 安全功能后，您的数据馈送会记住上次创建或更新它的用户在创建/更新时的角色，并使用相同的角色运行查询。如果您在创建或更新数据馈送时提供了辅助授权标头，则会改用这些凭据。

### 路径参数

`<feed_id>`

     (Required, string) A numerical character string that uniquely identifies the datafeed. This identifier can contain lowercase alphanumeric characters (a-z and 0-9), hyphens, and underscores. It must start and end with alphanumeric characters. 

### 查询参数

`end`

    

(可选，字符串)数据馈送应结束的时间，可以使用下列格式之一指定：

* 带毫秒的 ISO 8601 格式，例如"2017-01-22T06：00：00.000Z" * 不含毫秒的 ISO 8601 格式，例如"2017-01-22T06：00：00+00：00" * 自纪元以来的毫秒，例如"1485061200000"

使用 ISO 8601 格式之一的日期时间参数必须具有时区指示符，其中"Z"被接受为 UTC 时间的缩写。

当需要 URL 时(例如，在浏览器中)，时区指示符中使用的"+"必须编码为"%2B"。

此值是独占的。如果未指定结束时间，数据馈送将连续运行。

`start`

    

(可选，字符串)数据馈送应开始的时间，可以使用与"end"参数相同的格式来指定。此值具有包容性。

如果未指定开始时间，并且数据馈送与新的异常情况检测作业相关联，则分析将从数据可用的最早时间开始。

如果重新启动已停止的数据馈送并指定早于最新处理记录的时间戳的"开始"值，则数据馈送将从最新处理记录的时间戳后的 1 毫秒继续。

`timeout`

     (Optional, time) Specifies the amount of time to wait until a datafeed starts. The default value is 20 seconds. 

### 请求正文

您还可以在请求正文中指定查询参数(例如"结束"和"开始")。

### 响应正文

`node`

     (string) The ID of the node that the datafeed was started on. If the datafeed is allowed to open lazily and has not yet been assigned to a node, this value is an empty string. 
`started`

     (Boolean) For a successful response, this value is always `true`. On failure, an exception is returned instead. 

###Examples

    
    
    POST _ml/datafeeds/datafeed-low_request_rate/_start
    {
      "start": "2019-04-07T18:22:16Z"
    }

当数据馈送启动时，您会收到以下结果：

    
    
    {
      "started" : true,
      "node" : "node-1"
    }

[« Revert model snapshots API](ml-revert-snapshot.md) [Stop datafeeds API
»](ml-stop-datafeed.md)
