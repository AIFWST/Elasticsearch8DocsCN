

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Decrease the disk usage of data nodes](decrease-disk-usage-data-node.md)
[Fix other role nodes out of disk »](fix-other-node-out-of-disk.md)

## 修复主节点磁盘外问题

Elasticsearch 使用主节点来协调集群。如果主节点或任何符合主节点条件的节点空间不足，则需要确保它们有足够的磁盘空间来运行。如果运行状况 API 报告您的主节点空间不足，则需要增加主节点的磁盘容量。

弹性搜索服务 自我管理

1. 登录弹性云控制台。  2. 在"**弹性搜索服务**"面板上，单击"管理部署"列下与您的部署名称对应的齿轮。  3. 转到"操作>编辑部署"，然后转到"主实例"部分：

!增加主节点的磁盘容量

4. 从下拉菜单中选择大于预选容量配置的容量配置，然后单击"保存"。等待应用计划，问题应该得到解决。

为了增加主节点的磁盘容量，您需要将**所有**主节点替换为磁盘容量更高的主节点。

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

2.下一步是找出当前的磁盘使用情况，这将允许计算需要多少额外空间。在下面的示例中，出于可读性的目的，我们仅显示主节点： 响应 = client.cat.nodes( v： true， h： 'name，master，node.role，disk.used_percent，disk.used，disk.avail，disk.total' ) 把响应 GET /_cat/nodes？v&h=name，master，node.role，disk.used_percent，disk.used，disk.avail，disk.total

响应将如下所示：

    
        name                master node.role disk.used_percent disk.used disk.avail disk.total
    instance-0000000000 *      m                    85.31    3.4gb     500mb       4gb
    instance-0000000001 *      m                    50.02    2.1gb     1.9gb       4gb
    instance-0000000002 *      m                    50.02    1.9gb     2.1gb       4gb

3. 所需的情况是将磁盘使用率降至相关阈值以下，在我们的示例中为 90%。考虑添加一些填充，这样它就不会很快超过阈值。如果您有多个主节点，则需要确保**所有**个主节点都具有此容量。假设您已准备好新节点，请对每个主节点执行以下三个步骤。  4. 关闭其中一个主节点。  5. 启动其中一个新的主节点并等待它加入集群。您可以通过以下方式检查： response = client.cat.nodes( v： true， h： 'name，master，node.role，disk.used_percent，disk.used，disk.avail，disk.total' ) put response GET /_cat/nodes？v&h=name，master，node.role，disk.used_percent，disk.used，disk.avail，disk.total

6. 只有在确认集群具有初始数量的主节点后，才向前移动到下一个主节点，直到替换了所有初始主节点。

[« Decrease the disk usage of data nodes](decrease-disk-usage-data-node.md)
[Fix other role nodes out of disk »](fix-other-node-out-of-disk.md)
