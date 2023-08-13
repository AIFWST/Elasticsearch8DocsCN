

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md) ›[Fix data nodes out of disk](fix-
data-node-out-of-disk.md)

[« Fix data nodes out of disk](fix-data-node-out-of-disk.md) [Decrease the
disk usage of data nodes »](decrease-disk-usage-data-node.md)

## 增加数据节点的磁盘容量

弹性搜索服务 自我管理

要增加集群中数据节点的磁盘容量：

1. 登录弹性云控制台。  2. 在"**弹性搜索服务**"面板上，单击"管理部署"列下与您的部署名称对应的齿轮。  3. 如果自动缩放可用但未启用，请启用它。您可以通过单击横幅上的"启用自动缩放"按钮来执行此操作，如下所示：

!自动缩放横幅

或者，您可以转到"编辑部署>操作"，选中复选框"自动缩放"，然后单击页面底部的"保存"。

!启用自动缩放

4. 如果自动缩放成功，群集应返回到"正常"状态。如果群集仍未耗尽磁盘，请检查自动缩放是否已达到其限制。您将通过以下横幅收到有关此情况的通知：

![Autoscaling
banner](images/troubleshooting/disk/autoscaling_limits_banner.png)

或者，您可以转到"编辑部署>操作"并查找标签"已达到限制"，如下所示：

!已达到自动缩放限制

如果看到横幅，请单击"更新自动缩放设置"以转到"编辑"页面。否则，你已在"编辑"页面中，单击"编辑设置"以增加自动缩放限制。执行更改后，单击页面底部的"保存"。

为了增加集群中的数据节点容量，您需要计算所需的额外磁盘空间量。

1. 首先，检索相关的磁盘阈值，该阈值将指示应有多少可用空间。相关阈值是除冻结层之外的所有层的高水位线和冻结层的冻结洪水阶段水位线。以下示例演示了热层中的磁盘短缺，因此我们仅检索高水位线：响应 = client.cluster.get_settings( include_defaults：true，filter_path："*.cluster.routing.allocation.disk.watermark.high*" ) 将响应 GET _cluster/settings？include_defaults&filter_path=*.cluster.routing.allocation.disk.watermark.high*

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
    }

以上意味着，为了解决磁盘短缺问题，我们需要将磁盘使用率降至 90% 以下或有超过 150GB 的可用空间，请在此处阅读有关此阈值如何工作的更多信息。

2.下一步是找出当前的磁盘使用情况，这将指示需要多少额外空间。为简单起见，我们的示例有一个节点，但您可以对超过相关阈值的每个节点应用相同的节点。           响应 = client.cat.allocation( v： true， s： 'disk.avail'， h： 'node，disk.percent，disk.avail，disk.total，disk.used，disk.index，shards' ) put response GET _cat/allocation？v&s=disk.avail&h=node，disk.percent，disk.avail，disk.total，disk.used，disk.index，shards

响应将如下所示：

    
        node                disk.percent disk.avail disk.total disk.used disk.indices shards
    instance-0000000000           91     4.6gb       35gb    31.1gb       29.9gb    111

3. 高水位线配置表示磁盘使用率需要降至 90% 以下。要实现这一目标，可以做两件事：

    * to add an extra data node to the cluster (this requires that you have more than one shard in your cluster), or 
    * to extend the disk space of the current node by approximately 20% to allow this node to drop to 70%. This will give enough space to this node to not run out of space soon. 

4. 在添加另一个数据节点的情况下，集群不会立即恢复。将某些分片重新定位到新节点可能需要一些时间。你可以在这里检查进度：响应 = client.cat.shards( v： true， h： 'state，node'， s： 'state' ) 把响应 GET /_cat/shards？v&h=state，node&s=state

如果在响应中分片的状态为"重新定位"，则表示分片仍在移动。等到所有分片都变为"已启动"或运行状况磁盘指示器变为"绿色"。

[« Fix data nodes out of disk](fix-data-node-out-of-disk.md) [Decrease the
disk usage of data nodes »](decrease-disk-usage-data-node.md)
