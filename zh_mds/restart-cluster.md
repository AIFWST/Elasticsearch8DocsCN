

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md)

[« Add and remove nodes in your cluster](add-elasticsearch-nodes.md) [Remote
clusters »](remote-clusters.md)

## 全集群重启和滚动重启

在某些情况下，您可能需要执行完全群集重新启动或滚动重新启动。在全集群重启的情况下，您关闭并重启集群中的所有节点，而在滚动重启的情况下，一次只关闭一个节点，因此服务不会中断。

超过低水位线阈值的节点重启速度将很慢。在重新启动节点之前，将磁盘使用率降低到低水位线以下。

### 全集群重启

1. **禁用分片分配。

关闭数据节点时，分配过程会等待 'index.unassigned.node_left.delayed_timeout'(默认为 1 分钟)，然后再开始将该节点上的分片复制到集群中的其他节点，这可能涉及大量 I/O。由于节点即将重新启动，因此不需要此 I/O。您可以通过在关闭数据节点之前禁用副本分配来避免争分夺秒：

    
        response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.routing.allocation.enable": 'primaries'
        }
      }
    )
    puts response
    
        PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.enable": "primaries"
      }
    }

2. **停止索引并执行刷新。

执行刷新可加快分片恢复速度。

    
        response = client.indices.flush
    puts response
    
        POST /_flush

1. **暂时停止与活动机器学习作业和数据馈送关联的任务。 (可选)

机器学习功能需要特定订阅。

关闭集群时，有两个选项可用于处理机器学习作业和数据馈送：

    * Temporarily halt the tasks associated with your machine learning jobs and datafeeds and prevent new jobs from opening by using the [set upgrade mode API](ml-set-upgrade-mode.html "Set upgrade mode API"):
        
                response = client.ml.set_upgrade_mode(
          enabled: true
        )
        puts response
        
                POST _ml/set_upgrade_mode?enabled=true

禁用升级模式时，作业将使用自动保存的最后一个模型状态恢复。此选项避免了在关闭期间管理活动作业的开销，并且比显式停止数据馈送和关闭作业更快。

    * [Stop all datafeeds and close all jobs](/guide/en/machine-learning/8.9/stopping-ml.html). This option saves the model state at the time of closure. When you reopen the jobs after the cluster restart, they use the exact same model. However, saving the latest model state takes longer than using upgrade mode, especially if you have a lot of jobs or jobs with large model states. 

2. **关闭所有节点。

    * If you are running Elasticsearch with `systemd`:
        
                sudo systemctl stop elasticsearch.service

    * If you are running Elasticsearch with SysV `init`:
        
                sudo -i service elasticsearch stop

    * If you are running Elasticsearch as a daemon:
        
                kill $(cat pid)

3. **执行任何所需的更改。 4.**重新启动节点。

如果您有专用主节点，请先启动它们并等待它们形成集群并选择主节点，然后再继续处理数据节点。您可以通过查看日志来检查进度。

一旦有足够多的主节点相互发现，它们就会形成一个集群并选择一个主节点。此时，您可以使用 cat 运行状况和 cat 节点 API 来监控加入集群的节点：

    
        response = client.cat.health
    puts response
    
    response = client.cat.nodes
    puts response
    
        GET _cat/health
    
    GET _cat/nodes

"_cat/health"返回的"状态"列显示群集中每个节点的运行状况："红色"、"黄色"或"绿色"。

5. **等待所有节点加入群集并报告黄色状态。

当节点加入集群时，它将开始恢复本地存储的任何主分片。"_cat/运行状况"API 最初报告的"状态"为"红色"，表示并非所有主分片都已分配。

节点恢复其本地分片后，集群"状态"将切换为"黄色"，表示已恢复所有主分片，但未分配所有副本分片。这是意料之中的，因为您尚未重新启用分配。延迟副本的分配，直到所有节点都为"黄色"，允许主节点将副本分配给已经具有本地分片副本的节点。

6. **重新启用分配。

当所有节点都加入集群并恢复其主分片时，通过将"cluster.routing.allocation.enable"恢复为其默认值来重新启用分配：

    
        response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.routing.allocation.enable": nil
        }
      }
    )
    puts response
    
        PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.enable": null
      }
    }

重新启用分配后，集群将开始向数据节点分配副本分片。此时，恢复索引和搜索是安全的，但如果您可以等到所有主分片和副本分片都成功分配并且所有节点的状态为"绿色"，您的集群将恢复得更快。

您可以使用"_cat/运行状况"和"_cat/恢复"API 监视进度：

    
        response = client.cat.health
    puts response
    
    response = client.cat.recovery
    puts response
    
        GET _cat/health
    
    GET _cat/recovery

7. **重新启动机器学习作业。 (可选)

如果暂时停止了与机器学习作业关联的任务，请使用设置升级模式 API 将其返回到活动状态：

    
        response = client.ml.set_upgrade_mode(
      enabled: false
    )
    puts response
    
        POST _ml/set_upgrade_mode?enabled=false

如果您在停止节点之前关闭了所有机器学习作业，请打开作业并从 Kibana 或使用打开的作业启动数据馈送并启动数据馈送 API。

### 滚动重启

1. **禁用分片分配。

关闭数据节点时，分配过程会等待 'index.unassigned.node_left.delayed_timeout'(默认为 1 分钟)，然后再开始将该节点上的分片复制到集群中的其他节点，这可能涉及大量 I/O。由于节点即将重新启动，因此不需要此 I/O。您可以通过在关闭数据节点之前禁用副本分配来避免争分夺秒：

    
        response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.routing.allocation.enable": 'primaries'
        }
      }
    )
    puts response
    
        PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.enable": "primaries"
      }
    }

2. **停止不必要的索引并执行刷新。**(可选)

虽然您可以在滚动重启期间继续编制索引，但如果暂时停止不必要的索引并执行刷新，则分片恢复可能会更快。

    
        response = client.indices.flush
    puts response
    
        POST /_flush

3. **暂时停止与活动机器学习作业和数据馈送关联的任务。 (可选)

机器学习功能需要特定订阅。

关闭集群时，有两个选项可用于处理机器学习作业和数据馈送：

    * Temporarily halt the tasks associated with your machine learning jobs and datafeeds and prevent new jobs from opening by using the [set upgrade mode API](ml-set-upgrade-mode.html "Set upgrade mode API"):
        
                response = client.ml.set_upgrade_mode(
          enabled: true
        )
        puts response
        
                POST _ml/set_upgrade_mode?enabled=true

禁用升级模式时，作业将使用自动保存的最后一个模型状态恢复。此选项避免了在关闭期间管理活动作业的开销，并且比显式停止数据馈送和关闭作业更快。

    * [Stop all datafeeds and close all jobs](/guide/en/machine-learning/8.9/stopping-ml.html). This option saves the model state at the time of closure. When you reopen the jobs after the cluster restart, they use the exact same model. However, saving the latest model state takes longer than using upgrade mode, especially if you have a lot of jobs or jobs with large model states. 

    * If you perform a rolling restart, you can also leave your machine learning jobs running. When you shut down a machine learning node, its jobs automatically move to another node and restore the model states. This option enables your jobs to continue running during the shutdown but it puts increased load on the cluster. 

4. **在滚动重启的情况下关闭单个节点。

    * If you are running Elasticsearch with `systemd`:
        
                sudo systemctl stop elasticsearch.service

    * If you are running Elasticsearch with SysV `init`:
        
                sudo -i service elasticsearch stop

    * If you are running Elasticsearch as a daemon:
        
                kill $(cat pid)

5. **执行任何所需的更改。 6.**重新启动您更改的节点。

启动节点并通过检查日志文件或提交"_cat/节点"请求来确认它已加入群集：

    
        response = client.cat.nodes
    puts response
    
        GET _cat/nodes

7. **重新启用分片分配。

对于数据节点，节点加入集群后，删除"cluster.routing.allocation.enable"设置以启用分片分配并开始使用节点：

    
        response = client.cluster.put_settings(
      body: {
        persistent: {
          "cluster.routing.allocation.enable": nil
        }
      }
    )
    puts response
    
        PUT _cluster/settings
    {
      "persistent": {
        "cluster.routing.allocation.enable": null
      }
    }

8. **滚动重启时重复此操作。

当节点恢复且群集稳定时，对需要更改的每个节点重复这些步骤。

9. **重新启动机器学习作业。 (可选)

如果暂时停止了与机器学习作业关联的任务，请使用设置升级模式 API 将其返回到活动状态：

    
        response = client.ml.set_upgrade_mode(
      enabled: false
    )
    puts response
    
        POST _ml/set_upgrade_mode?enabled=false

如果您在停止节点之前关闭了所有机器学习作业，请打开作业并从 Kibana 或使用打开的作业启动数据馈送并启动数据馈送 API。

[« Add and remove nodes in your cluster](add-elasticsearch-nodes.md) [Remote
clusters »](remote-clusters.md)
