

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Fix master nodes out of disk](fix-master-node-out-of-disk.md) [Start
index lifecycle management »](start-ilm.md)

## 修复磁盘外的其他角色节点

Elasticsearch可以使用专用节点来执行除存储数据或协调集群之外的其他功能，例如机器学习。如果其中一个或多个节点空间不足，则需要确保它们有足够的磁盘空间来运行。如果运行状况 API 报告不是主节点且不包含数据的节点空间不足，则需要增加此节点的磁盘容量。

弹性搜索服务 自我管理

1. 登录弹性云控制台。  2. 在"**弹性搜索服务**"面板上，单击"管理部署"列下与您的部署名称对应的齿轮。  3. 转到"编辑部署>的操作"，然后转到"协调实例"或"机器学习实例"部分，具体取决于诊断中列出的角色：

!增加其他节点的磁盘容量

4. 从下拉菜单中选择大于预选容量配置的容量配置，然后单击"保存"。等待应用计划，问题应该得到解决。

为了增加任何其他节点的磁盘容量，您需要将空间不足的实例替换为磁盘容量更高的实例。

1. 首先，检索指示需要多少磁盘空间的磁盘阈值。相关的阈值是高水位线，可以通过以下命令检索：响应 = client.cluster.get_settings( include_defaults： true， filter_path： '*.cluster.routing.allocation.disk.watermark.high*' ) put 响应 GET _cluster/settings？include_defaults&filter_path=*.cluster.routing.allocation.disk.watermark.high*

响应将如下所示：

    
        {
      "defaults": {
        "cluster": {
          "routing": {
            "allocation": {
              "disk": {
                "watermark": {
                  "high": "90%",
                  "high.max_headroom": "150GB"
                }
              }
            }
          }
        }
      }

以上意味着，为了解决磁盘短缺问题，我们需要将磁盘使用率降至 90% 以下或有超过 150GB 的可用空间，请在此处阅读更多此阈值的工作原理。

2.下一步是找出当前的磁盘使用情况，这将允许计算需要多少额外空间。在下面的示例中，出于可读性的目的，我们只显示一个机器学习节点：响应 = client.cat.nodes( v： true， h： 'name，node.role，disk.used_percent，disk.used，disk.avail，disk.total' ) 把响应 GET /_cat/nodes？v&h=name，node.role，disk.used_percent，disk.used，disk.avail，disk.total

响应将如下所示：

    
        name                node.role disk.used_percent disk.used disk.avail disk.total
    instance-0000000000     l                 85.31    3.4gb     500mb       4gb

3. 所需的情况是将磁盘使用率降至相关阈值以下，在我们的示例中为 90%。考虑添加一些填充，这样它就不会很快超过阈值。假设新节点已准备就绪，请将此节点添加到群集。  4. 验证新节点是否已加入集群：响应 = client.cat.nodes( v： true， h： 'name，node.role，disk.used_percent，disk.used，disk.avail，disk.total' ) 放置响应 GET /_cat/nodes？v&h=name，node.role，disk.used_percent，disk.used，disk.avail，disk.total

响应将如下所示：

    
        name                node.role disk.used_percent disk.used disk.avail disk.total
    instance-0000000000     l                 85.31    3.4gb     500mb       4gb
    instance-0000000001     l                 41.31    3.4gb     4.5gb       8gb

5.现在，您可以删除磁盘空间不足的实例。

[« Fix master nodes out of disk](fix-master-node-out-of-disk.md) [Start
index lifecycle management »](start-ilm.md)
