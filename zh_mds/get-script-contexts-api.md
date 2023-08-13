

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Script APIs](script-apis.md)

[« Delete stored script API](delete-stored-script-api.md) [Get script
languages API »](get-script-languages-api.md)

## 获取脚本上下文API

检索支持的脚本上下文及其方法的列表。

    
    
    response = client.get_script_context
    puts response
    
    
    GET _script_context

###Request

"_script_context"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

[« Delete stored script API](delete-stored-script-api.md) [Get script
languages API »](get-script-languages-api.md)
