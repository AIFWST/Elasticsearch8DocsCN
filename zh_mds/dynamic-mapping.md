

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Mapping](mapping.md)

[« Mapping](mapping.md) [Dynamic field mapping »](dynamic-field-
mapping.md)

## 动态映射

Elasticsearch最重要的功能之一是它试图摆脱你的束缚，让你尽快开始探索你的数据。要为文档编制索引，您不必先创建索引、定义映射类型和定义字段 - 您只需为文档编制索引，索引、类型和字段将自动显示：

    
    
    response = client.index(
      index: 'data',
      id: 1,
      body: {
        count: 5
      }
    )
    puts response
    
    
    PUT data/_doc/1 __{ "count": 5 }

__

|

创建"data"索引、"_doc"映射类型和一个名为"count"的字段，数据类型为"long"。   ---|--- 自动检测和添加新字段称为 _dynamicmapping_。可以自定义动态映射规则以满足您的目的：

动态字段映射

     The rules governing dynamic field detection. 
[Dynamic templates](dynamic-templates.html "Dynamic templates")

     Custom rules to configure the mapping for dynamically added fields. 

索引模板允许您配置新索引的默认映射、设置和别名，无论是自动创建的还是显式创建的。

[« Mapping](mapping.md) [Dynamic field mapping »](dynamic-field-
mapping.md)
