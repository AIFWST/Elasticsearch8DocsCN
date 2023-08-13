

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Monitor a
cluster](monitor-elasticsearch-cluster.md) ›[Configuring data
streams/indices for monitoring](config-monitoring-indices.md)

[« Configuring data streams created by Metricbeat 8](config-monitoring-data-
streams-metricbeat-8.md) [Collecting monitoring data using legacy collectors
»](collecting-monitoring-data.md)

## 配置由 Metricbeat 7 或内部集合创建的索引

使用 Metricbeat 7 或内部集合进行监视时，数据存储在一组称为以下任一的索引中：

* '.monitoring-{product}-7-mb-{date}'，当使用 Metricbeat 7 时。  * ".monitoring-{product}-7-{date}"，当使用内部集合时。

这些索引的设置和映射由名为".monitoring-{product}"的旧索引模板确定。您可以在 Kibana 中检索这些模板，方法是导航到 **堆栈管理**> **索引管理**> **索引模板**，或使用 Elasticsearch '_template' API：

    
    
    response = client.indices.get_template(
      name: '.monitoring-*'
    )
    puts response
    
    
    GET /_template/.monitoring-*

要更改索引的设置，请添加自定义索引模板。您可以在 Kibana 中或使用 Elasticsearch API 执行此操作：

* 设置"index_patterns"以匹配".monitoring-{product}-7-*"索引。  * 将模板"订单"设置为"1"。这可确保在默认模板(顺序为 0)之后应用模板。  * 在"设置"部分中指定"number_of_shards"和/或"number_of_replicas"。

    
    
    response = client.indices.put_template(
      name: 'custom_monitoring',
      body: {
        index_patterns: [
          '.monitoring-beats-7-*',
          '.monitoring-es-7-*',
          '.monitoring-kibana-7-*',
          '.monitoring-logstash-7-*'
        ],
        order: 1,
        settings: {
          number_of_shards: 5,
          number_of_replicas: 2
        }
      }
    )
    puts response
    
    
    PUT /_template/custom_monitoring
    {
      "index_patterns": [".monitoring-beats-7-*", ".monitoring-es-7-*", ".monitoring-kibana-7-*", ".monitoring-logstash-7-*"],
      "order": 1,
      "settings": {
        "number_of_shards": 5,
        "number_of_replicas": 2
      }
    }

更改索引模板后，更新的设置仅应用于新索引。

[« Configuring data streams created by Metricbeat 8](config-monitoring-data-
streams-metricbeat-8.md) [Collecting monitoring data using legacy collectors
»](collecting-monitoring-data.md)
