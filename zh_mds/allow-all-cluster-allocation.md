

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Add a missing tier to the system](add-tier.md) [Allow Elasticsearch to
allocate the index »](allow-all-index-allocation.md)

## 允许 Elasticsearch 分配系统中的数据

Elasticsearch 部署中的数据分配可以使用启用集群分配配置进行控制。在某些情况下，用户可能希望暂时禁用或限制系统中数据的分配。

忘记重新允许所有数据分配可能会导致未分配的分片。

为了(重新)允许分配所有数据，请执行以下步骤：

弹性搜索服务 自我管理

为了分配分片，我们需要更改限制分片分配的配置值，以允许分配所有分片。

我们将通过检查系统范围的"cluster.routing.allocation.enable"群集设置并将配置的值更改为"all"来实现此目的。

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

4. 检查"cluster.routing.allocation.enable"集群设置：响应 = client.cluster.get_settings( flat_settings：true ) 放置响应 GET /_cluster/settings？flat_settings

响应将如下所示：

    
        {
      "persistent": {
        "cluster.routing.allocation.enable": "none" __},
      "transient": {}
    }

__

|

表示当前配置的值，该值控制是否允许在系统中部分分配数据或允许分配数据。   ---|--- 5.更改配置值以允许完全分配系统中的所有数据： 响应 = client.cluster.put_settings( body： { 持久： { "cluster.routing.allocation.enable"： 'all' } } ) put response PUT _cluster/settings { "persistent" ： { "cluster.routing.allocation.enable" ： "all" __} }

__

|

"allocation.enable"系统范围配置的新值已更改，以允许分配所有分片。   ---|---   

为了分配分片，我们需要更改限制分片分配的配置值，以允许分配所有分片。

我们将通过检查系统范围的"cluster.routing.allocation.enable"群集设置并将配置的值更改为"all"来实现此目的。

1. 检查"cluster.routing.allocation.enable"集群设置：响应 = client.cluster.get_settings( flat_settings： true ) 放置响应 GET /_cluster/settings？flat_settings

响应将如下所示：

    
        {
      "persistent": {
        "cluster.routing.allocation.enable": "none" __},
      "transient": {}
    }

__

|

表示当前配置的值，该值控制是否允许在系统中部分分配数据或允许分配数据。   ---|--- 2.更改配置值以允许完全分配系统中的所有数据： 响应 = client.cluster.put_settings( body： { 持久： { "cluster.routing.allocation.enable"： 'all' } } ) put response PUT _cluster/settings { "persistent" ： { "cluster.routing.allocation.enable" ： "all" __} }

__

|

"allocation.enable"系统范围配置的新值已更改，以允许分配所有分片。   ---|---   

[« Add a missing tier to the system](add-tier.md) [Allow Elasticsearch to
allocate the index »](allow-all-index-allocation.md)
