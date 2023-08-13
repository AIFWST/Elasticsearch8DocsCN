

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Snapshot
and restore](snapshot-restore.md)

[« Source-only repository](snapshots-source-only-repository.md) [Restore a
snapshot »](snapshots-restore-snapshot.md)

## 创建快照

本指南介绍如何拍摄正在运行的集群的快照。您可以稍后还原快照以恢复或传输其数据。

在本指南中，你将了解如何：

* 使用快照生命周期管理 (SLM) 自动创建和保留快照 * 手动拍摄快照 * 监控快照的进度 * 删除或取消快照 * 备份群集配置文件

本指南还提供了有关创建专用集群状态快照和以不同时间间隔拍摄快照的提示。

###Prerequisites

* 要使用 Kibana 的"快照和还原"功能，您必须具有以下权限：

    * [Cluster privileges](security-privileges.html#privileges-list-cluster "Cluster privileges"): `monitor`, `manage_slm`, `cluster:admin/snapshot`, and `cluster:admin/repository`
    * [Index privilege](security-privileges.html#privileges-list-indices "Indices privileges"): `all` on the `monitor` index 

* 您只能从具有选定主节点的正在运行的集群中拍摄快照。  * 快照存储库必须注册并可供群集使用。  * 集群的全局元数据必须是可读的。要在快照中包含索引，索引及其元数据也必须是可读的。确保没有任何阻止读取访问的群集块或索引块。

###Considerations

* 每个快照在其存储库中必须具有唯一的名称。尝试创建与现有快照同名的快照将失败。  * 快照会自动删除重复数据。您可以频繁拍摄快照，而对存储开销的影响很小。  * 每个快照在逻辑上都是独立的。您可以删除快照，而不会影响其他快照。  * 拍摄快照可以暂时暂停分片分配。请参阅快照和分片分配。  * 拍摄快照不会阻止索引或其他请求。但是，快照不会包括在快照过程启动后所做的更改。  *您可以同时拍摄多个快照。"快照.max_并发_操作"群集设置限制并发快照操作的最大数量。  * 如果在快照中包含数据流，则快照还包括流的后备索引和元数据。

您还可以在快照中仅包含特定的后备索引。但是，快照不会包含数据流的元数据或其其他支持索引。

* 快照可以包含数据流，但不包括特定的后备索引。还原此类数据流时，它将仅包含快照中的后备索引。如果流的原始写入索引不在快照中，则快照中的最新后备索引将成为流的写入索引。

### 使用 SLM 自动创建快照

快照生命周期管理 (SLM) 是定期备份集群的最简单方法。SLM 策略会按照预设的计划自动拍摄快照。该策略还可以根据您定义的保留规则删除快照。

Elasticsearch Service 部署会自动包含"云快照策略"SLM 策略。Elasticsearch Service 使用此策略为您的集群拍摄定期快照。有关更多信息，请参阅 ElasticsearchService 快照文档。

#### SLM安全性

以下集群权限控制在启用 Elasticsearch 安全功能时对 SLM 操作的访问：

`manage_slm`

     Allows a user to perform all SLM actions, including creating and updating policies and starting and stopping SLM. 
`read_slm`

     Allows a user to perform all read-only SLM actions, such as getting policies and checking the SLM status. 
`cluster:admin/snapshot/*`

     Allows a user to take and delete snapshots of any index, whether or not they have access to that index. 

您可以创建和管理角色以通过 KibanaManagement 分配这些权限。

要授予创建和管理 SLM 策略和快照所需的权限，您可以设置具有"manage_slm"和"cluster：admin/snapshot/*"集群权限以及对 SLMhistory 索引的完全访问权限的角色。

例如，以下请求创建一个"slm-admin"角色：

    
    
    POST _security/role/slm-admin
    {
      "cluster": [ "manage_slm", "cluster:admin/snapshot/*" ],
      "indices": [
        {
          "names": [ ".slm-history-*" ],
          "privileges": [ "all" ]
        }
      ]
    }

要授予对 SLM 策略和快照历史记录的只读访问权限，您可以设置具有"read_slm"集群特权和对快照生命周期管理历史记录索引的读取访问权限的角色。

例如，以下请求创建一个"slm 只读"角色：

    
    
    POST _security/role/slm-read-only
    {
      "cluster": [ "read_slm" ],
      "indices": [
        {
          "names": [ ".slm-history-*" ],
          "privileges": [ "read" ]
        }
      ]
    }

#### 创建 SLM 策略

要在 Kibana 中管理 SLM，请转到主菜单并单击"堆栈管理">"快照和还原">"策略"。若要创建策略，请单击"**创建策略**"。

您还可以使用 SLM API 管理 SLM。若要创建策略，请使用创建 SLM 策略 API。

以下请求创建一个策略，用于在每天凌晨 1：30 UTC 备份集群状态、所有数据流和所有索引。

    
    
    PUT _slm/policy/nightly-snapshots
    {
      "schedule": "0 30 1 * * ?",       __"name": " <nightly-snap-{now/d}>", __"repository": "my_repository", __"config": {
        "indices": "*", __"include_global_state": true __},
      "retention": { __"expire_after": "30d",
        "min_count": 5,
        "max_count": 50
      }
    }

__

|

何时拍摄快照，用 Cron 语法编写。   ---|---    __

|

快照名称。支持日期数学。为防止命名冲突，该策略还会将 UUID 附加到每个快照名称。   __

|

用于存储策略快照的已注册快照存储库。   __

|

要包含在策略快照中的数据流和索引。   __

|

如果为"true"，则策略的快照包括群集状态。默认情况下，这也包括所有功能状态。若要仅包含特定功能状态，请参阅备份特定功能状态。   __

|

可选的保留规则。此配置将快照保留 30 天，无论使用期限如何，至少保留 5 个快照且不超过 50 个快照。请参见 SLMretention和快照保留限制。   #### 手动运行 SLM策略编辑

您可以手动运行 SLM 策略以立即创建快照。这对于测试新策略或在升级前拍摄快照非常有用。手动运行策略不会影响其快照计划。

要在 Kibana 中运行策略，请转到"策略"页面，然后单击"操作"列下的运行图标。您还可以使用执行 SLM 策略 API。

    
    
    POST _slm/policy/nightly-snapshots/_execute

快照过程在后台运行。若要监视其进度，请参阅监视快照。

#### SLM保留

SLM 快照保留是独立于策略的快照计划运行的集群级任务。要控制 SLM 保留任务的运行时间，请配置"slm.retention_schedule"群集设置。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "slm.retention_schedule": '0 30 1 * * ?'
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
      "persistent" : {
        "slm.retention_schedule" : "0 30 1 * * ?"
      }
    }

若要立即运行保留任务，请使用执行 SLM 保留策略 API。

    
    
    response = client.slm.execute_retention
    puts response
    
    
    POST _slm/_execute_retention

SLM 策略的保留规则仅适用于使用该策略创建的快照。其他快照不计入策略的保留限制。

#### 快照保留限制

我们建议您在 SLM 策略中包含保留规则，以删除不再需要的快照。

快照存储库可以安全地扩展到数千个快照。但是，要管理其元数据，大型存储库在主节点上需要更多内存。保留规则可确保存储库的元数据不会增长到可能破坏主节点稳定性的大小。

### 手动创建快照

要在没有 SLM 策略的情况下拍摄快照，请使用创建快照 API。快照名称支持日期数学。

    
    
    response = client.snapshot.create(
      repository: 'my_repository',
      snapshot: '<my_snapshot_{now/d}>'
    )
    puts response
    
    
    # PUT _snapshot/my_repository/<my_snapshot_{now/d}>
    PUT _snapshot/my_repository/%3Cmy_snapshot_%7Bnow%2Fd%7D%3E

根据其大小，快照可能需要一段时间才能完成。默认情况下，创建快照 API 仅启动快照进程，在后台运行。若要在快照完成之前阻止客户端，请将"wait_for_completion"查询参数设置为"true"。

    
    
    response = client.snapshot.create(
      repository: 'my_repository',
      snapshot: 'my_snapshot',
      wait_for_completion: true
    )
    puts response
    
    
    PUT _snapshot/my_repository/my_snapshot?wait_for_completion=true

您还可以使用克隆快照 API 克隆现有快照。

### 监视快照

要监控任何当前正在运行的快照，请将获取快照 API 与"_current"请求路径参数一起使用。

    
    
    response = client.snapshot.get(
      repository: 'my_repository',
      snapshot: '_current'
    )
    puts response
    
    
    GET _snapshot/my_repository/_current

要获取参与任何当前运行的快照的每个分片的完整细分，请使用获取快照状态 API。

    
    
    response = client.snapshot.status
    puts response
    
    
    GET _snapshot/_status

#### 检查 SLM 历史记录

要获取有关集群的 SLM 执行历史记录的详细信息(包括每个 SLM 策略的统计信息)，请使用获取 SLM 统计信息 API。API 还返回有关群集快照保留任务历史记录的信息。

    
    
    response = client.slm.get_stats
    puts response
    
    
    GET _slm/stats

若要获取有关特定 SLM 策略的执行历史记录的信息，请使用获取 SLM 策略 API。响应包括：

* 下一次计划策略执行。  * 策略上次成功启动快照过程的时间(如果适用)。成功启动并不能保证快照完成。  * 上次策略执行失败的时间(如果适用)以及关联的错误。

    
    
    response = client.slm.get_lifecycle(
      policy_id: 'nightly-snapshots'
    )
    puts response
    
    
    GET _slm/policy/nightly-snapshots

### 删除或取消快照

要在 Kibana 中删除快照，请转到"**快照**"页面，然后单击"操作**"列下的垃圾桶图标。您还可以使用删除快照 API。

    
    
    response = client.snapshot.delete(
      repository: 'my_repository',
      snapshot: 'my_snapshot_2099.05.06'
    )
    puts response
    
    
    DELETE _snapshot/my_repository/my_snapshot_2099.05.06

如果您删除正在进行的快照，Elasticsearch 会取消它。快照进程将停止并删除为快照创建的任何文件。删除快照不会删除其他快照使用的文件。

### 备份配置文件

如果您在自己的硬件上运行 Elasticsearch，我们建议您除了备份之外，还使用您选择的文件备份软件定期备份每个节点的 '$ES_PATH_CONF' 目录中的文件。快照不会备份这些文件。另请注意，这些文件在每个节点上会有所不同，因此每个节点的文件应单独备份。

'elasticsearch.keystore'、TLS 密钥以及 SAML、OIDC 和 Kerberos 领域私钥文件包含敏感信息。请考虑加密这些文件的备份。

### 备份特定功能状态

默认情况下，包含群集状态的快照还包括所有功能状态。同样，默认情况下，排除集群状态的快照会排除所有功能状态。

您还可以将快照配置为仅包含特定功能状态，而不考虑群集状态。

若要获取可用功能的列表，请使用获取功能 API。

    
    
    response = client.features.get_features
    puts response
    
    
    GET _features

该 API 返回：

    
    
    {
      "features": [
        {
          "name": "tasks",
          "description": "Manages task results"
        },
        {
          "name": "kibana",
          "description": "Manages Kibana configuration and reports"
        },
        {
          "name": "security",
          "description": "Manages configuration for Security features, such as users and roles"
        },
        ...
      ]
    }

要在快照中包含特定功能状态，请在"feature_states"数组中指定功能"name"。

例如，以下 SLM 策略在其快照中仅包含 Kibana 和 Elasticsearch 安全功能的功能状态。

    
    
    PUT _slm/policy/nightly-snapshots
    {
      "schedule": "0 30 2 * * ?",
      "name": "<nightly-snap-{now/d}>",
      "repository": "my_repository",
      "config": {
        "indices": "*",
        "include_global_state": true,
        "feature_states": [
          "kibana",
          "security"
        ]
      },
      "retention": {
        "expire_after": "30d",
        "min_count": 5,
        "max_count": 50
      }
    }

属于要素状态的任何索引或数据流都将显示在快照的内容中。例如，如果备份"安全"功能状态，则"security-*"系统索引将显示在获取快照 API 的响应中的"索引"和"feature_states"下。

### 专用集群状态快照

某些功能状态包含敏感数据。例如，"安全"功能状态包括可能包含用户名和加密密码哈希的系统索引。由于密码是使用加密哈希存储的，因此泄露快照不会自动使第三方能够作为您的用户之一进行身份验证或使用 API 密钥。但是，它会泄露机密信息，如果第三方可以修改快照，他们可以安装后门。

为了更好地保护此数据，请考虑为群集状态的快照创建专用存储库和 SLM策略。这使您可以严格限制和审核对存储库的访问。

例如，以下 SLM 策略仅备份群集状态。策略将这些快照存储在专用存储库中。

    
    
    PUT _slm/policy/nightly-cluster-state-snapshots
    {
      "schedule": "0 30 2 * * ?",
      "name": "<nightly-cluster-state-snap-{now/d}>",
      "repository": "my_secure_repository",
      "config": {
        "include_global_state": true,                 __"indices": "-*" __},
      "retention": {
        "expire_after": "30d",
        "min_count": 5,
        "max_count": 50
      }
    }

__

|

包括群集状态。默认情况下，这还包括所有功能状态。   ---|---    __

|

不包括常规数据流和索引。   如果拍摄群集状态的专用快照，则需要从其他快照中排除群集状态。例如：

    
    
    PUT _slm/policy/nightly-snapshots
    {
      "schedule": "0 30 2 * * ?",
      "name": "<nightly-snap-{now/d}>",
      "repository": "my_repository",
      "config": {
        "include_global_state": false,    __"indices": "*" __},
      "retention": {
        "expire_after": "30d",
        "min_count": 5,
        "max_count": 50
      }
    }

__

|

排除群集状态。默认情况下，这也排除了所有功能状态。   ---|---    __

|

包括所有常规数据流和索引。   ### 以不同的时间间隔创建快照编辑

如果仅使用单个 SLM 策略，则可能很难频繁拍摄快照并保留时间间隔较长的快照。

例如，每 30 分钟拍摄一次快照(最多 100 个快照)的策略将仅将快照保留大约两天。虽然此设置非常适合备份最近的更改，但它不允许您从前一周或上个月还原数据。

要解决此问题，您可以使用按不同计划运行的同一快照存储库创建多个 SLM 策略。由于策略的保留规则仅适用于其快照，因此策略不会删除由其他策略创建的快照。

例如，以下 SLM 策略每小时拍摄一次快照，最多 24 个快照。该策略将其快照保留一天。

    
    
    PUT _slm/policy/hourly-snapshots
    {
      "name": "<hourly-snapshot-{now/d}>",
      "schedule": "0 0 * * * ?",
      "repository": "my_repository",
      "config": {
        "indices": "*",
        "include_global_state": true
      },
      "retention": {
        "expire_after": "1d",
        "min_count": 1,
        "max_count": 24
      }
    }

以下策略在同一快照存储库中获取夜间快照。该策略将其快照保留一个月。

    
    
    PUT _slm/policy/daily-snapshots
    {
      "name": "<daily-snapshot-{now/d}>",
      "schedule": "0 45 23 * * ?",          __"repository": "my_repository",
      "config": {
        "indices": "*",
        "include_global_state": true
      },
      "retention": {
        "expire_after": "30d",
        "min_count": 1,
        "max_count": 31
      }
    }

__

|

每天晚上 11：45 UTC 运行。   ---|--- 以下策略在同一存储库中创建每月快照。该策略将其快照保留一年。

    
    
    PUT _slm/policy/monthly-snapshots
    {
      "name": "<monthly-snapshot-{now/d}>",
      "schedule": "0 56 23 1 * ?",            __"repository": "my_repository",
      "config": {
        "indices": "*",
        "include_global_state": true
      },
      "retention": {
        "expire_after": "366d",
        "min_count": 1,
        "max_count": 12
      }
    }

__

|

在每月的第一天晚上 11：56(UTC) 运行。   ---|--- « 仅源存储库 恢复快照 »