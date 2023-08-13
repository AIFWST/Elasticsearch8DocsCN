[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Allow Elasticsearch to allocate the data in the system](allow-all-cluster-
allocation.md) [Indices mix index allocation filters with data tiers node
roles to move through data tiers »](troubleshoot-migrate-to-tiers.md)

## 允许 Elasticsearch 分配索引

可以使用启用分配配置来控制数据的分配。在某些情况下，用户可能希望暂时禁用或限制数据的分配。

忘记重新允许所有数据分配可能会导致未分配的分片。

为了(重新)允许分配所有数据，请执行以下步骤：

弹性搜索服务 自我管理

为了分配分片，我们需要更改将分片的分配限制为"all"的配置的值。

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

4. 检查具有未分配分片的索引的"index.routing.allocation.enable"索引设置：

        response = client.indices.get_settings( 
                index: 'my-index-000001', 
                name:"index.routeting.allocation.enable",
                flat_settings：true 
        )
put 响应 

    GET /my-index-000001/_settings/index.routing.allocation.enable?flat_settings

响应将如下所示：
    
    {
      "my-index-000001": {
        "settings": {
          "index.routing.allocation.enable": "none" __}
      }
    }


表示当前配置的值，该值控制是否允许部分或全部分配索引。
5.更改配置值以允许完全分配索引：

    response = client.indices.put_settings(
        index:'my-index-000001', 
        body: {
            index： { "routeting.allocation.enable"： 'all' } 
        } 
    ) 

put response

    PUT /my-index-000001/_settings 
    { 
        "index" ： { "routeting.allocation.enable" ： "all"} 
    }


"my-index-000001"索引的"allocation.enable"配置的新值已更改，以允许分配所有分片。   ---|---   

为了分配分片，我们需要更改将分片的分配限制为"all"的配置的值。

检查具有未分配分片的索引的"index.routing.allocation.enable"索引设置：
    
        response = client.indices.get_settings(
            index: 'my-index-000001',
            name:"index.routeting.allocation.enable",
            flat_settings：true )
放置响应 

    GET /my-index-000001/_settings/index.routeting.allocation.enable?flat_settings

响应将如下所示：

    
        {
      "my-index-000001": {
        "settings": {
          "index.routing.allocation.enable": "none" __}
      }
    }


表示当前配置的值，该值控制是否允许部分或全部分配索引。

2.更改配置值以允许完全分配索引：

    response = client.indices.put_settings( 
    index: 'my-index-000001', 
    body: { 
        index: { "routeting.allocation.enable":'all' 
            }
        } ) 

put response 

    PUT /my-index-000001/_settings 
    { 
        "index" :
        { 
            "routeting.allocation.enable" :"all"
        }
    }



"my-index-000001"索引的"allocation.enable"配置的新值已更改，以允许分配所有分片。   


[« Allow Elasticsearch to allocate the data in the system](allow-all-cluster-
allocation.md) [Indices mix index allocation filters with data tiers node
roles to move through data tiers »](troubleshoot-migrate-to-tiers.md)
