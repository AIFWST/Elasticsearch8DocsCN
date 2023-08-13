

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Important Elasticsearch configuration](important-settings.md) [Auditing
security settings »](auditing-settings.md)

## 安全设置

某些设置是敏感的，依靠文件系统权限来保护其值是不够的。对于此用例，Elasticsearch 提供了密钥库和"elasticsearch-keystore"工具来管理密钥库中的设置。

只有某些设置设计为从密钥库中读取。但是，密钥库没有验证来阻止不受支持的设置。将不支持的设置添加到密钥库会导致 Elasticsearch 无法启动。要查看密钥库中是否支持设置，请在设置参考中查找"安全"限定符。

对密钥库的所有修改只有在重新启动 Elasticsearch 后才会生效。

这些设置，就像"elasticsearch.yml"配置文件中的常规设置一样，需要在集群中的每个节点上指定。目前，所有安全设置都是特定于节点的设置，每个节点上必须具有相同的值。

### 可重新加载的安全设置

就像 'elasticsearch.yml' 中的设置值一样，对密钥库内容的更改不会自动应用于正在运行的 Elasticsearch 节点。重新读取设置需要重新启动节点。但是，某些安全设置标记为"可重新加载**"。此类设置可以重新读取并应用于正在运行的节点。

所有安全设置的值(无论是否可重新加载)在所有群集节点中必须相同。在进行所需的安全设置更改后，使用"bin/elasticsearch-keystore add"命令调用：

    
    
    response = client.nodes.reload_secure_settings(
      body: {
        secure_settings_password: 'keystore-password'
      }
    )
    puts response
    
    
    POST _nodes/reload_secure_settings
    {
      "secure_settings_password": "keystore-password" __}

__

|

用于加密 Elasticsearch 密钥库的密码。   ---|--- 此 API 解密并重新读取每个集群节点上的整个密钥库，但仅应用**可重新装入** 安全设置。对其他设置的更改在下次重新启动之前不会生效。调用返回后，加载已完成，这意味着依赖于这些设置的所有内部数据结构都已更改。一切看起来都好像设置从一开始就具有新值。

更改多个 **可重新加载** 安全设置时，请在每个群集节点上修改所有设置，然后在每次修改后发出"reload_secure_settings"调用，而不是重新加载。

有可重新加载的安全设置：

* Azure 存储库插件 * EC2 发现插件 * GCS 存储库插件 * S3 存储库插件 * 监视设置 * 观察程序设置

[« Important Elasticsearch configuration](important-settings.md) [Auditing
security settings »](auditing-settings.md)
