

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md)

[« Example: Enrich your data by matching a value to a range](range-enrich-
policy-type.md) [Append processor »](append-processor.md)

## 引入处理器参考

Elasticsearch包括几个可配置的处理器。若要获取可用处理器的列表，请使用节点信息 API。

    
    
    response = client.nodes.info(
      node_id: 'ingest',
      filter_path: 'nodes.*.ingest.processors'
    )
    puts response
    
    
    GET _nodes/ingest?filter_path=nodes.*.ingest.processors

本节中的页面包含每个处理器的参考文档。

### 处理器插件

您可以安装其他处理器作为插件。

您必须在群集中的所有节点上安装任何插件处理器。否则，Elasticsearch 将无法创建包含处理器的管道。

通过在"elasticsearch.yml"中设置"plugin.mandatory"将插件标记为必需插件。如果未安装强制插件，节点将无法启动。

    
    
    plugin.mandatory: my-ingest-plugin

[« Example: Enrich your data by matching a value to a range](range-enrich-
policy-type.md) [Append processor »](append-processor.md)
