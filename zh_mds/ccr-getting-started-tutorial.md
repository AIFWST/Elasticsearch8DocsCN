

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up a
cluster for high availability](high-availability.md) ›[Cross-cluster
replication](xpack-ccr.md)

[« Cross-cluster replication](xpack-ccr.md) [Manage cross-cluster
replication »](ccr-managing.md)

## 教程：设置跨集群复制

使用本指南在两个数据中心的群集之间设置跨群集复制 (CCR)。跨数据中心复制数据具有以下几个好处：

* 使数据更接近您的用户或应用程序服务器，以减少延迟和响应时间 * 为您的任务关键型应用程序提供承受数据中心或区域中断的容错能力

在本指南中，你将了解如何：

* 使用领导者索引配置远程集群 * 在本地集群上创建追随者索引 * 创建自动关注模式以自动关注在远程集群中定期创建的时间序列索引

您可以手动创建追随者索引以复制远程集群上的特定索引，或配置自动关注模式以复制滚动时间序列索引。

如果要在云中的集群之间复制数据，可以在 Elasticsearch Service 上配置远程集群。然后，您可以跨集群搜索并设置跨集群复制。

###Prerequisites

要完成本教程，您需要：

* 本地群集上的"管理"群集权限。  * 两个集群上的许可证，包括跨集群复制。激活 30 天免费试用版。  * 远程集群上的索引，其中包含要复制的数据。本教程使用示例电子商务订单数据集。加载示例数据。  * 在本地群集中，具有"主"节点角色的所有节点也必须具有"remote_cluster_client"角色。本地群集还必须至少有一个同时具有数据角色和"remote_cluster_client"角色的节点。用于根据本地群集中具有"remote_cluster_client"角色的数据节点数协调复制规模的单个任务。

### 连接到远程群集

要将远程群集(群集 A)上的索引复制到本地群集(群集 B)，请将群集 A 配置为群集 B 上的远程群集。

!集群 A 包含领导者索引，集群 B 包含追随者索引

要从 Kibana 中的堆栈管理配置远程集群，请执行以下操作：

1. 从侧面导航栏中选择**远程群集**。  2. 指定 Elasticsearch 终端节点 URL，或远程集群的 IP 地址或主机名("ClusterA")，后跟传输端口(默认为"9300")。例如，"cluster.es.eastus2.staging.azure.foundit.no:9400"或"192.168.1.1：9300"。

接口示例

还可以使用群集更新设置 API 添加远程群集：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          cluster: {
            remote: {
              leader: {
                seeds: [
                  '127.0.0.1:9300'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "persistent" : {
        "cluster" : {
          "remote" : {
            "leader" : {
              "seeds" : [
                "127.0.0.1:9300" __]
            }
          }
        }
      }
    }

__

|

指定远程群集中种子节点的主机名和传输端口。   ---|--- 您可以验证本地群集是否已成功连接到远程群集。

    
    
    response = client.cluster.remote_info
    puts response
    
    
    GET /_remote/info

API 响应指示本地集群已连接到集群别名为"leader"的远程集群。

    
    
    {
      "leader" : {
        "seeds" : [
          "127.0.0.1:9300"
        ],
        "connected" : true,
        "num_nodes_connected" : 1, __"max_connections_per_cluster" : 3,
        "initial_connect_timeout" : "30s",
        "skip_unavailable" : false,
        "mode" : "sniff"
      }
    }

__

|

本地群集连接到的远程群集中的节点数。   ---|--- ### 配置跨集群复制的权限编辑

跨集群复制用户需要远程集群和本地集群上的不同集群和索引权限。使用以下请求在本地和远程群集上创建单独的角色，然后创建具有所需角色的用户。

##### 远程群集

在包含领导索引的远程集群上，跨集群复制角色需要领导者索引的"read_ccr"集群权限以及"监控"和"读取"权限。

如果使用 API 密钥对请求进行身份验证，则 API 密钥需要对 **local** 群集(而不是远程群集)具有上述权限。

如果代表其他用户发出请求，则身份验证用户必须在远程群集上具有"run_as"权限。

以下请求在远程群集上创建"远程复制"角色：

    
    
    POST /_security/role/remote-replication
    {
      "cluster": [
        "read_ccr"
      ],
      "indices": [
        {
          "names": [
            "leader-index-name"
          ],
          "privileges": [
            "monitor",
            "read"
          ]
        }
      ]
    }

##### 本地群集

在包含从属索引的本地集群上，"远程复制"角色需要"manage_ccr"集群特权，以及关注方索引的"监视"、"读取"、"写入"和"manage_follow_index"特权。

以下请求在本地群集上创建"远程复制"角色：

    
    
    POST /_security/role/remote-replication
    {
      "cluster": [
        "manage_ccr"
      ],
      "indices": [
        {
          "names": [
            "follower-index-name"
          ],
          "privileges": [
            "monitor",
            "read",
            "write",
            "manage_follow_index"
          ]
        }
      ]
    }

在每个群集上创建"远程复制"角色后，使用创建器更新用户 API 在本地群集群集上创建用户并分配"远程复制"角色。例如，以下请求将"远程复制"角色分配给名为"跨群集用户"的用户：

    
    
    POST /_security/user/cross-cluster-user
    {
      "password" : "l0ng-r4nd0m-p@ssw0rd",
      "roles" : [ "remote-replication" ]
    }

您只需在 **local** 群集上创建此用户。

### 创建关注者索引以复制特定索引

创建关注者索引时，您将引用远程集群中的远程集群和领导者索引。

要从 Kibana 中的堆栈管理创建追随者索引，请执行以下操作：

1. 在侧边导航中选择**跨集群复制**，然后选择**关注者索引**选项卡。  2. 选择包含要复制的领导者索引的集群 (集群 A)。  3. 输入领导者索引的名称，如果您正在按照教程进行操作，则为"kibana_sample_data_ecommerce"。  4. 输入关注者索引的名称，例如"关注者-kibana-sample-data"。

Elasticsearch 使用远程恢复过程初始化追随者，该过程将现有的 Lucene 段文件从 leaderindex 传输到追随者索引。索引状态更改为"**已暂停**"。远程恢复过程完成后，将开始执行索引，状态将更改为"**活动**"。

当您将文档索引到领导者索引中时，Elasticsearch 会复制追随者索引中的文档。

!Kibana 中的跨集群复制页面

接口示例

您还可以使用创建追随者 API 来创建追随者索引。创建从属索引时，必须引用远程集群和在远程集群中创建的领导索引。

启动关注者请求时，响应会在远程恢复过程完成之前返回。要等待该过程完成，请将"wait_for_active_shards"参数添加到您的请求中。

    
    
    PUT /server-metrics-follower/_ccr/follow?wait_for_active_shards=1
    {
      "remote_cluster" : "leader",
      "leader_index" : "server-metrics"
    }

使用获取关注者统计信息 API 检查复制状态。

### 创建自动跟随模式以复制时间序列索引

您可以使用自动关注模式为滚动时间序列索引自动创建新的关注者。只要远程集群上新索引的名称与自动关注模式匹配，就会向本地集群添加相应的关注者索引。请注意，只有在创建自动关注模式后在远程集群上创建的索引才会被自动关注：远程集群上的现有索引将被忽略，即使它们与模式匹配。

自动跟随模式指定要从中复制的远程集群，以及一个或多个指定要复制的滚动时间序列索引的索引模式。

要从 Kibana 中的堆栈管理创建自动关注模式，请执行以下操作：

1. 在侧面导航中选择**跨集群复制**，然后选择**自动关注模式**选项卡。  2. 输入自动跟随模式的名称，例如"节拍"。  3. 选择包含要复制的索引的远程集群，在示例场景中为集群 A。  4. 输入一个或多个索引模式，用于标识要从远程集群复制的索引。例如，输入"metricbeat-* packetbeat-*"以自动为 Metricbeat 和 Packetbeat 索引创建关注者。  5. 输入 **follower-** 作为前缀以应用于从属索引的名称，以便您可以更轻松地识别复制的索引。

当在远程设备上创建与这些模式匹配的新索引时，Elasticsearch 会自动将它们复制到本地关注者索引。

!Kibana 中的自动跟踪模式页面

接口示例

使用创建自动关注模式 API 配置自动关注模式。

    
    
    PUT /_ccr/auto_follow/beats
    {
      "remote_cluster" : "leader",
      "leader_index_patterns" :
      [
        "metricbeat-*", __"packetbeat-*" __],
      "follow_index_pattern" : "{{leader_index}}-copy" __}

__

|

自动跟踪新的指标节拍指数。   ---|---    __

|

自动跟随新的数据包节拍索引。   __

|

追随者索引的名称是通过将后缀"-copy"添加到领导者索引的名称来派生的领导者索引的名称。   « 跨集群复制 管理跨集群复制 »