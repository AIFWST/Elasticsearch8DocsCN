

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Features APIs](features-apis.md)

[« Features APIs](features-apis.md) [Reset features API »](reset-features-
api.md)

## 获取功能接口

获取可在创建快照时使用"feature_states"字段包含在快照中的功能列表。

    
    
    response = client.features.get_features
    puts response
    
    
    GET /_features

###Request

"获取/_features"

###Description

您可以使用获取特征 API 来确定拍摄快照时要包括的功能状态。默认情况下，如果快照包含全局状态，则快照中包含所有功能状态;如果不包含全局状态，则不包含任何功能状态。

功能状态包括给定功能正常运行所需的一个或多个系统索引。为了确保数据完整性，构成功能状态的所有系统索引都一起快照和还原。

此 API 列出的功能是内置功能和插件定义的功能的组合。为了使功能的状态在此 API 中列出，并由创建快照 API 识别为有效的功能状态，必须在主节点上安装定义该功能的插件。

###Examples

    
    
    {
        "features": [
            {
                "name": "tasks",
                "description": "Manages task results"
            },
            {
                "name": "kibana",
                "description": "Manages Kibana configuration and reports"
            }
        ]
    }

[« Features APIs](features-apis.md) [Reset features API »](reset-features-
api.md)
