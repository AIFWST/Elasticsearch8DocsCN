

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Start index lifecycle management](start-ilm.md) [Restore from snapshot
»](restore-from-snapshot.md)

## 启动快照生命周期管理

自动快照生命周期管理当前已禁用。不会自动创建新的备份快照。

要启动快照生命周期管理服务，请执行以下步骤：

弹性搜索服务 自我管理

为了启动快照生命周期管理，我们需要转到 Kibana 并执行启动命令。

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

4. 启动快照生命周期管理：开机自检_slm/启动

响应将如下所示：

    
        {
      "acknowledged": true
    }

5. 验证快照生命周期管理现在是否正在运行：响应 = client.slm.get_status放置响应 获取_slm/状态

响应将如下所示：

    
        {
      "operation_mode": "RUNNING"
    }

启动快照生命周期管理：

    
    
    POST _slm/start

响应将如下所示：

    
    
    {
      "acknowledged": true
    }

验证快照生命周期管理现在是否正在运行：

    
    
    response = client.slm.get_status
    puts response
    
    
    GET _slm/status

响应将如下所示：

    
    
    {
      "operation_mode": "RUNNING"
    }

[« Start index lifecycle management](start-ilm.md) [Restore from snapshot
»](restore-from-snapshot.md)
