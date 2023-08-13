

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Upgrade
Elasticsearch](setup-upgrade.md)

[« Upgrade Elasticsearch](setup-upgrade.md) [Reading indices from older
Elasticsearch versions »](archive-indices.md)

## 存档设置

如果您将具有已弃用的持久集群设置的集群升级到不再支持该设置的厌恶，Elasticsearch 会自动存档该设置。同样，如果您升级的集群包含具有不受支持的索引设置的索引，Elasticsearch 将存档索引设置。

我们建议您在升级后删除所有已存档的设置。存档设置被视为无效，可能会干扰您配置其他设置的能力。

已归档设置以"已归档"前缀开头。

### 存档群集设置

使用以下群集更新设置请求检查存档的群集设置。如果请求返回空对象 ('{ }')，则没有存档的集群设置。

    
    
    response = client.cluster.get_settings(
      flat_settings: true,
      filter_path: 'persistent.archived*'
    )
    puts response
    
    
    GET _cluster/settings?flat_settings=true&filter_path=persistent.archived*

若要删除任何存档的群集设置，请使用以下群集更新设置请求。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "archived.*": nil
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent": {
        "archived.*": null
      }
    }

Elasticsearch 不会存档瞬态集群设置或 'elasticsearch.yml' 中的设置。如果节点在"elasticsearch.yml"中包含不受支持的设置，它将在启动时返回错误。

### 存档索引设置

在升级之前，请从索引和组件模板中删除任何不受支持的索引设置。Elasticsearch 不会在升级期间将不受支持的索引设置存档到模板中。尝试使用包含不受支持的索引设置的模板将失败并返回错误。这包括自动化操作，如 ILM 滚动更新操作。

存档的索引设置不会影响索引的配置或大多数索引操作，例如索引或搜索。但是，您需要先删除它们，然后才能为索引配置其他设置，例如"index.hidden"。

使用以下获取索引设置请求获取具有存档设置的列表索引。如果请求返回空对象 ('{ }')，则没有存档的索引设置。

    
    
    response = client.indices.get_settings(
      index: '*',
      flat_settings: true,
      filter_path: '**.settings.archived*'
    )
    puts response
    
    
    GET */_settings?flat_settings=true&filter_path=**.settings.archived*

若要删除任何存档的索引设置，请使用以下索引更新设置请求。

    
    
    response = client.indices.put_settings(
      index: 'my-index',
      body: {
        "archived.*": nil
      }
    )
    puts response
    
    
    PUT /my-index/_settings
    {
      "archived.*": null
    }

[« Upgrade Elasticsearch](setup-upgrade.md) [Reading indices from older
Elasticsearch versions »](archive-indices.md)
