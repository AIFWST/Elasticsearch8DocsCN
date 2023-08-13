

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md) ›[Fix data nodes out of disk](fix-
data-node-out-of-disk.md)

[« Increase the disk capacity of data nodes](increase-capacity-data-node.md)
[Fix master nodes out of disk »](fix-master-node-out-of-disk.md)

## 降低数据节点的磁盘使用率

为了在不丢失任何数据的情况下降低集群中的磁盘使用率，您可以尝试减少索引的副本。

减少索引的副本可能会降低搜索吞吐量和数据冗余。但是，它可以迅速为集群提供喘息空间，直到更永久的解决方案到位。

弹性搜索服务 自我管理

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到**堆栈管理>索引管理**。  4. 在所有索引的列表中，单击"副本"列两次，根据索引的副本数量对索引进行排序，从具有最多副本的副本开始。浏览索引，逐个选择重要性最低且副本数较多的索引。

减少索引的副本可能会降低搜索吞吐量和数据冗余。

5. 对于您选择的每个索引，单击其名称，然后在出现的面板上单击"编辑设置"，将"index.number_of_replicas"的值减小到所需的值，然后单击"保存"。

!减少副本

6. 继续此过程，直到群集再次正常运行。

为了估计需要删除的副本数，首先需要估计需要释放的磁盘空间量。

1. 首先，检索相关的磁盘阈值，该阈值将指示应释放多少空间。相关阈值是除冻结层之外的所有层的高水位线和冻结层的冻结洪水阶段水位线。以下示例演示了热层中的磁盘短缺，因此我们仅检索高水位线：响应 = client.cluster.get_settings( include_defaults：true，filter_path："*.cluster.routing.allocation.disk.watermark.high*" ) 将响应 GET _cluster/settings？include_defaults&filter_path=*.cluster.routing.allocation.disk.watermark.high*

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

2.下一步是找出当前的磁盘使用情况;这将指示应释放多少空间。为简单起见，我们的示例有一个节点，但您可以对超过相关阈值的每个节点应用相同的节点。           响应 = client.cat.allocation( v： true， s： 'disk.avail'， h： 'node，disk.percent，disk.avail，disk.total，disk.used，disk.index，shards' ) put response GET _cat/allocation？v&s=disk.avail&h=node，disk.percent，disk.avail，disk.total，disk.used，disk.index，shards

响应将如下所示：

    
        node                disk.percent disk.avail disk.total disk.used disk.indices shards
    instance-0000000000           91     4.6gb       35gb    31.1gb       29.9gb    111

3. 高水位线配置表示磁盘使用率需要降至 90% 以下。考虑允许一些填充，以便节点在不久的将来不会超过阈值。在此示例中，让我们释放大约 7GB。  4. 下一步是列出所有索引并选择要减少的副本。

以下命令按副本数和主存储大小降序对索引进行排序。我们这样做是为了帮助您选择要减少的副本，假设您拥有的副本越多，删除副本时风险就越小，并且副本越大，释放的空间就越多。这没有考虑任何功能要求，因此请将其视为仅建议。

    
        response = client.cat.indices(
      v: true,
      s: 'rep:desc,pri.store.size:desc',
      h: 'health,index,pri,rep,store.size,pri.store.size'
    )
    puts response
    
        GET _cat/indices?v&s=rep:desc,pri.store.size:desc&h=health,index,pri,rep,store.size,pri.store.size

响应将如下所示：

    
        health index                                                      pri rep store.size pri.store.size
    green  my_index                                                     2   3      9.9gb          3.3gb
    green  my_other_index                                               2   3      1.8gb        470.3mb
    green  search-products                                              2   3    278.5kb         69.6kb
    green  logs-000001                                                  1   0      7.7gb          7.7gb

5. 在上面的列表中，我们看到，如果我们将副本减少到索引 'my_index' 和 'my_other_index' 中的 1，我们将释放所需的磁盘空间。没有必要减少"搜索产品"的副本，并且"logs-000001"无论如何都没有任何副本。使用索引更新设置 API 减少一个或多个索引的副本：

减少索引的副本可能会降低搜索吞吐量和数据冗余。

    
        response = client.indices.put_settings(
      index: 'my_index,my_other_index',
      body: {
        "index.number_of_replicas": 1
      }
    )
    puts response
    
        PUT my_index,my_other_index/_settings
    {
      "index.number_of_replicas": 1
    }

[« Increase the disk capacity of data nodes](increase-capacity-data-node.md)
[Fix master nodes out of disk »](fix-master-node-out-of-disk.md)
