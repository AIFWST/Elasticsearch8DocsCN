

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Licensing APIs](licensing-apis.md)

[« Licensing APIs](licensing-apis.md) [Get license API »](get-license.md)

## 删除许可证接口

使用此 API，可以删除许可信息。

####Request

"删除/_license"

####Description

当您的许可证到期时，X-Pack 将以降级模式运行。有关详细信息，请参阅许可证过期。

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。  * 如果启用了操作员权限功能，则只有操作员用户才能使用此 API。

####Examples

以下示例查询信息 API：

    
    
    response = client.license.delete
    puts response
    
    
    DELETE /_license

成功删除许可证后，API 将返回以下响应：

    
    
    {
      "acknowledged": true
    }

[« Licensing APIs](licensing-apis.md) [Get license API »](get-license.md)
