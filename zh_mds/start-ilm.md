

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Fix other role nodes out of disk](fix-other-node-out-of-disk.md) [Start
Snapshot Lifecycle Management »](start-slm.md)

## 启动索引生命周期管理

自动索引生命周期和数据保留管理当前处于禁用状态。

要启动自动索引生命周期管理服务，请执行以下步骤：

弹性搜索服务 自我管理

为了启动索引生命周期管理，我们需要转到 Kibana 并执行 start 命令。

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

4. 启动索引生命周期管理：响应 = client.ilm.start 将响应放在 POST _ilm/启动

响应将如下所示：

    
        {
      "acknowledged": true
    }

5. 验证索引生命周期管理现在是否正在运行：响应 = client.ilm.get_status放置响应 获取_ilm/状态

响应将如下所示：

    
        {
      "operation_mode": "RUNNING"
    }

启动索引生命周期管理：

    
    
    response = client.ilm.start
    puts response
    
    
    POST _ilm/start

响应将如下所示：

    
    
    {
      "acknowledged": true
    }

验证索引生命周期管理现在是否正在运行：

    
    
    response = client.ilm.get_status
    puts response
    
    
    GET _ilm/status

响应将如下所示：

    
    
    {
      "operation_mode": "RUNNING"
    }

[« Fix other role nodes out of disk](fix-other-node-out-of-disk.md) [Start
Snapshot Lifecycle Management »](start-slm.md)
