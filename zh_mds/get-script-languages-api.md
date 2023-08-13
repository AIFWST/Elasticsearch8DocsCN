

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Script APIs](script-apis.md)

[« Get script contexts API](get-script-contexts-api.md) [Get stored script
API »](get-stored-script-api.md)

## 获取脚本语言接口

检索支持的脚本语言及其上下文的列表。

    
    
    response = client.get_script_languages
    puts response
    
    
    GET _script_language

###Request

"拿_script_language"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"管理"集群权限才能使用此 API。

[« Get script contexts API](get-script-contexts-api.md) [Get stored script
API »](get-stored-script-api.md)
