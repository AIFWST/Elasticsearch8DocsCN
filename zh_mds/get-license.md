

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Licensing APIs](licensing-apis.md)

[« Delete license API](delete-license.md) [Get trial status API »](get-
trial-status.md)

## 获取许可证API

此 API 使您能够检索许可信息。

####Request

"获取/_license"

####Description

例如，此 API 返回有关许可证类型、颁发时间和到期时间的信息。

有关不同类型的许可证的详细信息，请参阅 seehttps://www.elastic.co/subscriptions。

如果主节点正在生成新的集群状态，则获取许可证 API 可能会返回"404 未找到"响应。如果在群集启动后收到意外的"404"响应，请稍等片刻，然后重试请求。

#### 查询参数

`local`

     (Boolean) Specifies whether to retrieve local information. The default value is `false`, which means the information is retrieved from the master node. 
`accept_enterprise`

     (Boolean) If `true`, this parameter returns `enterprise` for Enterprise license types. If `false`, this parameter returns `platinum` for both `platinum` and `enterprise` license types. This behavior is maintained for backwards compatibility. 

### 在 7.6.0 中已弃用。

此参数已弃用，在 8.x 中将始终设置为"true"。

####Authorization

您必须具有"监视"群集权限才能使用此 API。有关详细信息，请参阅安全权限。

####Examples

以下示例提供有关试用许可证的信息：

    
    
    response = client.license.get
    puts response
    
    
    GET /_license
    
    
    {
      "license" : {
        "status" : "active",
        "uid" : "cbff45e7-c553-41f7-ae4f-9205eabd80xx",
        "type" : "trial",
        "issue_date" : "2018-10-20T22:05:12.332Z",
        "issue_date_in_millis" : 1540073112332,
        "expiry_date" : "2018-11-19T22:05:12.332Z",
        "expiry_date_in_millis" : 1542665112332,
        "max_nodes" : 1000,
        "max_resource_units" : null,
        "issued_to" : "test",
        "issuer" : "elasticsearch",
        "start_date_in_millis" : -1
      }
    }

[« Delete license API](delete-license.md) [Get trial status API »](get-
trial-status.md)
