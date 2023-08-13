

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md) ›[Collecting monitoring data
using legacy collectors](collecting-monitoring-data.md)

[« HTTP exporters](http-exporter.md) [Roll up or transform your data
»](data-rollup-transform.md)

## 暂停数据收集

要停止在 Elasticsearch 中生成 X-Pack 监控数据，请禁用数据收集：

    
    
    xpack.monitoring.collection.enabled: false

当此设置为"false"时，不会收集 Elasticsearch 监控数据，并且忽略来自其他来源(如 Kibana、Beats 和 Logstashis)的所有监控数据。

可以使用群集更新设置 API 更新此设置。

如果您想从 Kibana、Beats 和 Logstash 等源收集数据，但不收集有关 Elasticsearch 集群的数据，则可以仅对 Elasticsearch 禁用数据收集：

    
    
    xpack.monitoring.collection.enabled: true
    xpack.monitoring.elasticsearch.collection.enabled: false

如果要单独禁用特定导出器，可以为每个导出器指定"已启用"设置(默认为"true")。例如：

    
    
    xpack.monitoring.exporters.my_http_exporter:
      type: http
      host: ["10.1.2.3:9200", "10.1.2.4:9200"]
      enabled: false __

__

|

禁用指定的导出器。如果未使用与现有导出器相同的名称，则将创建一个完全忽略的全新导出器。可以使用群集设置动态设置此值。   ---|--- 定义禁用的导出器会阻止创建默认导出器。

要重新启动数据收集，请重新启用这些设置。

[« HTTP exporters](http-exporter.md) [Roll up or transform your data
»](data-rollup-transform.md)
