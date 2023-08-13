

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Snapshot
and restore](snapshot-restore.md)

[« Create a snapshot](snapshots-take-snapshot.md) [Searchable snapshots
»](searchable-snapshots.md)

## 恢复快照

本指南介绍如何还原快照。快照是将数据副本存储在集群外部的便捷方法。您可以还原快照以在删除或硬件故障后恢复索引和数据流。您还可以使用快照在集群之间传输数据。

在本指南中，你将了解如何：

* 获取可用快照列表 * 从快照还原索引或数据流 * 恢复功能状态 * 还原整个集群 * 监视还原操作 * 取消正在进行的还原

本指南还提供了有关还原到另一个群集和排查常见还原错误的提示。

###Prerequisites

* 要使用 Kibana 的"快照和还原"功能，您必须具有以下权限：

    * [Cluster privileges](security-privileges.html#privileges-list-cluster "Cluster privileges"): `monitor`, `manage_slm`, `cluster:admin/snapshot`, and `cluster:admin/repository`
    * [Index privilege](security-privileges.html#privileges-list-indices "Indices privileges"): `all` on the `monitor` index 

* 您只能将快照还原到具有选定主节点的正在运行的集群。快照的存储库必须已注册并可供群集使用。  * 快照和集群版本必须兼容。请参阅快照兼容性。  * 要还原快照，集群的全局元数据必须是可写的。确保没有任何阻止写入的群集块。还原操作将忽略索引块。  * 在恢复数据流之前，请确保集群包含启用了数据流的匹配索引模板。要进行检查，请使用 Kibana 的 **索引管理** 功能或获取索引模板 API： 响应 = client.indices.get_index_template( 名称： '*'， filter_path： 'index_templates.name，index_templates.index_template.index_patterns，index_templates.index_template.data_stream' ) 将响应 GET _index_template/*？filter_path=index_templates.name，index_templates.index_template.index_patterns，index_templates.index_template.data_stream

如果不存在此类模板，则可以创建一个模板或还原包含该模板的群集状态。如果没有匹配的索引模板，则 adata 流无法滚动更新或创建后备索引。

* 如果您的快照包含来自 App Search 或 Workplace 搜索的数据，请确保在还原快照之前已还原企业级搜索加密密钥。

###Considerations

从快照还原数据时，请记住以下几点：

* 如果还原数据流，则还会还原其后备索引。  * 仅当现有索引已关闭且快照中的索引具有相同数量的主分片时，才能还原现有索引。  * 无法还原现有的打开索引。这包括数据流的支持索引。  * 还原操作会自动打开还原的索引，包括后备索引。  * 您只能从数据流中恢复特定的后备索引。但是，还原操作不会将还原的支持索引添加到任何现有数据流。

### 获取可用快照列表

要查看 Kibana 中的可用快照列表，请转到主菜单并单击**堆栈管理>快照和还原**。

您还可以使用获取存储库 API 和获取快照 API 来查找可用于还原的快照。首先，使用获取存储库 API 获取已注册快照存储库的列表。

    
    
    response = client.snapshot.get_repository
    puts response
    
    
    GET _snapshot

然后使用获取快照 API 获取特定存储库中的快照列表。这还会返回每个快照的内容。

    
    
    response = client.snapshot.get(
      repository: 'my_repository',
      snapshot: '*',
      verbose: false
    )
    puts response
    
    
    GET _snapshot/my_repository/*?verbose=false

### 还原索引或数据流

您可以使用 Kibana 的"快照和还原"功能或还原快照 API 来还原快照。

默认情况下，还原请求会尝试还原快照中的所有常规索引和常规数据流。在大多数情况下，您只需从快照还原特定索引或数据流。但是，无法还原现有的打开索引。

如果要将数据还原到预先存在的群集，请使用以下方法之一来避免与现有索引和数据流发生冲突：

*删除和恢复 *恢复时重命名

#### 删除和还原

避免冲突的最简单方法是在还原现有索引或数据流之前将其删除。为了防止意外重新创建索引器数据流，我们建议您暂时停止所有索引，直到 therestore 操作完成。

如果"action.destructive_requires_name"群集设置为"false"，请不要使用删除索引 API 来定位"*"或".*"通配符模式。如果您使用 Elasticsearch 的安全功能，这将删除身份验证所需的系统索引。相反，应以"*,-.*"通配符模式为目标，以排除这些系统索引和以点 ('.) 开头的其他索引名称。

    
    
    response = client.indices.delete(
      index: 'my-index'
    )
    puts response
    
    response = client.indices.delete_data_stream(
      name: 'logs-my_app-default'
    )
    puts response
    
    
    # Delete an index
    DELETE my-index
    
    # Delete a data stream
    DELETE _data_stream/logs-my_app-default

在还原请求中，显式指定要还原的任何索引和数据流。

    
    
    response = client.snapshot.restore(
      repository: 'my_repository',
      snapshot: 'my_snapshot_2099.05.06',
      body: {
        indices: 'my-index,logs-my_app-default'
      }
    )
    puts response
    
    
    POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
    {
      "indices": "my-index,logs-my_app-default"
    }

#### 还原时重命名

如果要避免删除现有数据，可以改为重命名还原的索引和数据流。通常使用此方法将现有数据与快照中的历史数据进行比较。例如，可以使用此方法在意外更新或删除后查看文档。

在开始之前，请确保群集有足够的容量来存储现有数据和还原的数据。

以下还原快照 API 请求将"还原-"附加到任何还原的索引或数据流的名称前面。

    
    
    response = client.snapshot.restore(
      repository: 'my_repository',
      snapshot: 'my_snapshot_2099.05.06',
      body: {
        indices: 'my-index,logs-my_app-default',
        rename_pattern: '(.+)',
        rename_replacement: 'restored-$1'
      }
    )
    puts response
    
    
    POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
    {
      "indices": "my-index,logs-my_app-default",
      "rename_pattern": "(.+)",
      "rename_replacement": "restored-$1"
    }

如果重命名选项生成两个或多个具有相同名称的索引或数据流，则还原操作将失败。

如果重命名数据流，其后备索引也会重命名。例如，如果将"logs-my_app-default"数据流重命名为"rerestore-logs-my_app-default"，则支持索引".ds-logs-my_app-default-2099.03.09-000005"将重命名为".ds-rerestore-logs-my_app-default-2099.03.09-000005"。

还原操作完成后，可以比较原始数据和还原的数据。如果不再需要原始索引或数据流，可以将其删除并使用重新索引重命名其中存储的索引或数据流。

    
    
    response = client.indices.delete(
      index: 'my-index'
    )
    puts response
    
    response = client.reindex(
      body: {
        source: {
          index: 'restored-my-index'
        },
        dest: {
          index: 'my-index'
        }
      }
    )
    puts response
    
    response = client.indices.delete_data_stream(
      name: 'logs-my_app-default'
    )
    puts response
    
    response = client.reindex(
      body: {
        source: {
          index: 'restored-logs-my_app-default'
        },
        dest: {
          index: 'logs-my_app-default',
          op_type: 'create'
        }
      }
    )
    puts response
    
    
    # Delete the original index
    DELETE my-index
    
    # Reindex the restored index to rename it
    POST _reindex
    {
      "source": {
        "index": "restored-my-index"
      },
      "dest": {
        "index": "my-index"
      }
    }
    
    # Delete the original data stream
    DELETE _data_stream/logs-my_app-default
    
    # Reindex the restored data stream to rename it
    POST _reindex
    {
      "source": {
        "index": "restored-logs-my_app-default"
      },
      "dest": {
        "index": "logs-my_app-default",
        "op_type": "create"
      }
    }

### 恢复功能状态

您可以还原功能状态以从快照恢复功能的系统索引、系统数据流和其他配置数据。

如果还原快照的群集状态，则默认情况下，该操作将还原快照中的所有功能状态。同样，如果不还原快照的群集状态，则默认情况下，该操作不会还原任何功能状态。您还可以选择仅从快照还原特定功能状态，而不考虑群集状态。

要查看快照的功能状态，请使用获取快照 API。

    
    
    response = client.snapshot.get(
      repository: 'my_repository',
      snapshot: 'my_snapshot_2099.05.06'
    )
    puts response
    
    
    GET _snapshot/my_repository/my_snapshot_2099.05.06

响应的"feature_states"属性包含快照中的要素列表以及每个要素的索引。

要从快照还原特定功能状态，请在还原快照 API 的"feature_states"参数中指定响应中的"feature_name"。

当您恢复功能状态时，Elasticsearch 会关闭并覆盖该功能的现有索引。

还原"安全"功能状态将覆盖用于身份验证的系统索引。如果您使用 Elasticsearch Service，请确保在恢复"安全"功能状态之前，您有权访问 Elasticsearch Service 控制台。如果您在自己的硬件上运行 Elasticsearch，请在文件域中创建一个超级用户，以确保您仍然能够访问您的集群。

    
    
    response = client.snapshot.restore(
      repository: 'my_repository',
      snapshot: 'my_snapshot_2099.05.06',
      body: {
        feature_states: [
          'geoip'
        ],
        include_global_state: false,
        indices: '-*'
      }
    )
    puts response
    
    
    POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
    {
      "feature_states": [ "geoip" ],
      "include_global_state": false,    __"indices": "-*" __}

__

|

从还原操作中排除群集状态。   ---|---    __

|

从还原操作中排除快照中的其他索引和数据流。   ### 恢复整个群集编辑

在某些情况下，您需要从快照还原整个集群，包括集群状态和所有功能状态。这些情况应该很少见，例如在发生灾难性故障的情况下。

还原整个集群涉及删除重要的系统索引，包括用于身份验证的索引。考虑是否可以改为还原特定索引或数据流。

如果要还原到其他群集，请参阅在开始之前还原到其他群集。

1. 如果备份了群集的配置文件，则可以将它们还原到每个节点。此步骤是可选的，需要完全重启群集。

关闭节点后，将备份的配置文件复制到节点的"$ES_PATH_CONF"目录。在重新启动节点之前，请确保"elasticsearch.yml"包含适当的节点角色、节点名称和其他特定于节点的设置。

如果选择执行此步骤，则必须在群集中的每个节点上重复此过程。

2. 暂时停止索引并关闭以下功能：

    * GeoIP database downloader and ILM history store
        
                response = client.cluster.put_settings(
          body: {
            persistent: {
              "ingest.geoip.downloader.enabled": false,
              "indices.lifecycle.history_index_enabled": false
            }
          }
        )
        puts response
        
                PUT _cluster/settings
        {
          "persistent": {
            "ingest.geoip.downloader.enabled": false,
            "indices.lifecycle.history_index_enabled": false
          }
        }

    * ILM
        
                response = client.ilm.stop
        puts response
        
                POST _ilm/stop

    * Machine Learning
        
                response = client.ml.set_upgrade_mode(
          enabled: true
        )
        puts response
        
                POST _ml/set_upgrade_mode?enabled=true

    * Monitoring
        
                response = client.cluster.put_settings(
          body: {
            persistent: {
              "xpack.monitoring.collection.enabled": false
            }
          }
        )
        puts response
        
                PUT _cluster/settings
        {
          "persistent": {
            "xpack.monitoring.collection.enabled": false
          }
        }

    * Watcher
        
                response = client.watcher.stop
        puts response
        
                POST _watcher/_stop

3. * 通用分析

检查是否启用了通用性能分析索引模板管理：

        
                GET /_cluster/settings?filter_path=**.xpack.profiling.templates.enabled&include_defaults=true

如果值为"true"，请禁用通用性能分析索引模板管理：

        
                PUT _cluster/settings
        {
          "persistent": {
            "xpack.profiling.templates.enabled": false
          }
        }

如果您使用 Elasticsearch 安全功能，请登录到节点主机，导航到 Elasticsearch 安装目录，然后使用"elasticsearch-users"工具将具有"超级用户"角色的用户添加到文件领域。

例如，以下命令创建名为"restore_user"的用户。

    
        ./bin/elasticsearch-users useradd restore_user -p my_password -r superuser

使用此文件领域用户对请求进行身份验证，直到恢复操作完成。

4. 使用群集更新设置 API 将"action.destructive_requires_name"设置为"false"。这允许您使用通配符删除数据流和索引。           响应 = client.cluster.put_settings( 正文： { 持久： { "action.destructive_requires_name"： 假 } } ) 放置响应 PUT _cluster/设置 { "持久"： { "action.destructive_requires_name"： 假 } }

5. 删除集群上的所有现有数据流。           响应 = client.indices.delete_data_stream( 名称："*"，expand_wildcards："全部") 将响应删除 _data_stream/*？expand_wildcards=all

6. 删除集群上的所有现有索引。           响应 = client.index.delete( index： '*'， expand_wildcards： 'all' ) 放置响应 DELETE *？expand_wildcards=all

7. 还原整个快照，包括群集状态。默认情况下，还原群集状态也会还原快照中的任何功能状态。           响应 = client.snapshot.restore( 存储库： 'my_repository'， 快照： 'my_snapshot_2099.05.06'， 正文： { 索引： '*'， include_global_state： true } ) 放置响应 POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore { "索引"： "*"， "include_global_state"： true }

8. 还原操作完成后，恢复索引并重新启动已停止的任何功能：

    * GeoIP database downloader and ILM history store
        
                response = client.cluster.put_settings(
          body: {
            persistent: {
              "ingest.geoip.downloader.enabled": true,
              "indices.lifecycle.history_index_enabled": true
            }
          }
        )
        puts response
        
                PUT _cluster/settings
        {
          "persistent": {
            "ingest.geoip.downloader.enabled": true,
            "indices.lifecycle.history_index_enabled": true
          }
        }

    * ILM
        
                response = client.ilm.start
        puts response
        
                POST _ilm/start

    * Machine Learning
        
                response = client.ml.set_upgrade_mode(
          enabled: false
        )
        puts response
        
                POST _ml/set_upgrade_mode?enabled=false

    * Monitoring
        
                response = client.cluster.put_settings(
          body: {
            persistent: {
              "xpack.monitoring.collection.enabled": true
            }
          }
        )
        puts response
        
                PUT _cluster/settings
        {
          "persistent": {
            "xpack.monitoring.collection.enabled": true
          }
        }

    * Watcher
        
                response = client.watcher.start
        puts response
        
                POST _watcher/_start

    * Universal Profiling

如果该值最初为"true"，请再次启用通用性能分析索引模板管理，否则跳过此步骤：

        
                PUT _cluster/settings
        {
          "persistent": {
            "xpack.profiling.templates.enabled": true
          }
        }

9. 如果需要，请重置"action.destructive_requires_name"群集设置。           响应 = client.cluster.put_settings( body： { 持久： { "action.destructive_requires_name"： nil } } ) 放置响应 PUT _cluster/设置 { "持久"： { "action.destructive_requires_name"： null } }

### 监视还原

还原操作使用分片恢复过程从快照还原索引的主分片。当还原操作恢复主分片时，集群的运行状况为"黄色"。

恢复所有主分片后，复制过程会在符合条件的数据节点之间创建并分发副本。复制完成后，群集运行状况通常变为"绿色"。

在 Kibana 中启动还原后，您将导航到"**还原状态**"页面。您可以使用此页面跟踪快照中每个分片的当前状态。

您还可以使用 Elasticsearch API 监控快照恢复。若要监视群集运行状况，请使用群集运行状况 API。

    
    
    $response = $client->cluster()->health();
    
    
    resp = client.cluster.health()
    print(resp)
    
    
    response = client.cluster.health
    puts response
    
    
    res, err := es.Cluster.Health()
    fmt.Println(res, err)
    
    
    const response = await client.cluster.health()
    console.log(response)
    
    
    GET _cluster/health

要获取有关正在进行的分片恢复的详细信息，请使用索引恢复 API。

    
    
    response = client.indices.recovery(
      index: 'my-index'
    )
    puts response
    
    
    GET my-index/_recovery

要查看任何未分配的分片，请使用猫分片 API。

    
    
    response = client.cat.shards(
      v: true,
      h: 'index,shard,prirep,state,node,unassigned.reason',
      s: 'state'
    )
    puts response
    
    
    GET _cat/shards?v=true&h=index,shard,prirep,state,node,unassigned.reason&s=state

未分配的分片具有"未分配"的"状态"。对于主分片，"prirep"值为"p"，对于副本，值为"r"。"unassigned.reason"描述了为什么分片保持未分配状态。

要更深入地了解未分配分片的分配状态，请使用集群分配说明 API。

    
    
    response = client.cluster.allocation_explain(
      body: {
        index: 'my-index',
        shard: 0,
        primary: false,
        current_node: 'my-node'
      }
    )
    puts response
    
    
    GET _cluster/allocation/explain
    {
      "index": "my-index",
      "shard": 0,
      "primary": false,
      "current_node": "my-node"
    }

### 取消还原

您可以删除索引或数据流以取消其正在进行的还原。这还会删除集群中索引或数据流的任何现有数据。删除索引或数据流不会影响快照或其数据。

    
    
    response = client.indices.delete(
      index: 'my-index'
    )
    puts response
    
    response = client.indices.delete_data_stream(
      name: 'logs-my_app-default'
    )
    puts response
    
    
    # Delete an index
    DELETE my-index
    
    # Delete a data stream
    DELETE _data_stream/logs-my_app-default

### 还原到其他群集

Elasticsearch Service 可以帮助您从其他部署中恢复快照。请参阅使用快照。

快照不绑定到特定群集或群集名称。您可以在一个集群中创建快照，然后在另一个兼容集群中恢复快照。从快照还原的任何数据流或索引也必须与当前集群的版本兼容。群集的拓扑不需要匹配。

要还原快照，必须注册其存储库并可供新群集使用。如果原始集群仍对存储库具有写入权限，请将存储库注册为只读。这可以防止多个集群同时写入存储库并损坏存储库的内容。它还阻止了 Elasticsearch 缓存存储库的内容，这意味着其他集群所做的更改将立即变得可见。

在开始还原操作之前，请确保新群集具有足够的容量来存储要还原的任何数据流或索引。如果新集群的容量较小，您可以：

* 添加节点或升级硬件以增加容量。  * 恢复更少的索引和数据流。  * 减少还原索引的副本数。

例如，以下还原快照 API 请求使用"index_settings"选项将"index.number_of_replicas"设置为"1"。

    
        response = client.snapshot.restore(
      repository: 'my_repository',
      snapshot: 'my_snapshot_2099.05.06',
      body: {
        indices: 'my-index,logs-my_app-default',
        index_settings: {
          "index.number_of_replicas": 1
        }
      }
    )
    puts response
    
        POST _snapshot/my_repository/my_snapshot_2099.05.06/_restore
    {
      "indices": "my-index,logs-my_app-default",
      "index_settings": {
        "index.number_of_replicas": 1
      }
    }

如果使用分片分配过滤将原始集群中的索引或后备索引分配给特定节点，则将在新集群中强制执行相同的规则。如果新群集不包含具有可分配还原索引的适当属性的节点，则除非在还原操作期间更改了这些索引分配设置，否则将无法成功还原索引。

还原操作还会检查还原的持久设置是否与当前群集兼容，以避免意外还原不兼容的设置。如果需要还原具有不兼容持久设置的快照，请尝试在没有全局群集状态的情况下还原它。

### 排查还原错误

下面介绍了如何解决还原请求返回的常见错误。

#### 无法恢复索引 <index>]，因为集群中已存在同名的开放索引[

无法还原已存在的打开索引。若要解决此错误，请尝试还原索引或数据流中的方法之一。

#### 无法从具有 [y] 个分片的索引 [] <index>的快照中恢复具有 [x] 个<snapshot-index>分片的索引 ]

仅当现有索引已关闭且快照中的索引具有相同数量的主分片时，才能还原现有索引。此错误表示快照中的索引具有不同数量的主分片。

若要解决此错误，请尝试还原索引或数据流中的方法之一。

[« Create a snapshot](snapshots-take-snapshot.md) [Searchable snapshots
»](searchable-snapshots.md)
