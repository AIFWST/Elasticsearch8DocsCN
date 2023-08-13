

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authorization](authorization.md)

[« User authorization](authorization.md) [Defining roles »](defining-
roles.md)

## 内置角色

Elastic Stack 安全功能将默认角色应用于所有用户，包括匿名用户。默认角色使用户能够访问身份验证终结点、更改自己的密码以及获取有关自己的信息。

还可以将一组内置角色显式分配给用户。这些角色具有一组固定的权限，无法更新。

`apm_system`

     Grants access necessary for the APM system user to send system-level data (such as monitoring) to Elasticsearch. 
`apm_user`

     Grants the privileges required for APM users (such as `read` and `view_index_metadata` privileges on the `apm-*` and `.ml-anomalies*` indices).  [7.13.0]  Deprecated in 7.13.0. See [APM app users and privileges](/guide/en/kibana/8.9/apm-app-users.html) for alternatives.  . 
`beats_admin`

     Grants access to the `.management-beats` index, which contains configuration information for the Beats. 
`beats_system`

    

授予 Beats 系统用户向 Elasticsearch 发送系统级数据(如监控)所需的访问权限。

* 不应将此角色分配给用户，因为授予的权限可能会在版本之间更改。  * 此角色不提供对 beats 索引的访问，也不适合将 beats 输出写入 Elasticsearch。

`data_frame_transforms_admin`

     Grants `manage_data_frame_transforms` cluster privileges, which enable you to manage transforms. This role also includes all [Kibana privileges](/guide/en/kibana/8.9/kibana-privileges.html) for the machine learning features.  [7.5.0]  Deprecated in 7.5.0. Replaced by [`transform_admin`](built-in-roles.html#built-in-roles-transform-admin) . 
`data_frame_transforms_user`

     Grants `monitor_data_frame_transforms` cluster privileges, which enable you to use transforms. This role also includes all [Kibana privileges](/guide/en/kibana/8.9/kibana-privileges.html) for the machine learning features.  [7.5.0]  Deprecated in 7.5.0. Replaced by [`transform_user`](built-in-roles.html#built-in-roles-transform-user) . 
`editor`

    

授予对 Kibana 中所有功能(包括解决方案)的完全访问权限和对数据索引的只读访问权限。

* 此角色提供对未以点为前缀的任何索引的读取访问权限。  * 此角色会在 Kibana 新功能发布后立即自动授予对这些功能的完全访问权限。  * 某些 Kibana 功能可能还需要创建或写入数据索引的访问权限。机器学习数据帧分析作业就是一个例子。对于此类功能，必须在单独的角色中定义这些权限。

`enrich_user`

     Grants access to manage **all** enrich indices (`.enrich-*`) and **all** operations on ingest pipelines. 
`ingest_admin`

    

授予管理**所有**索引模板和**全部**摄取管道配置的访问权限。

此角色不提供创建索引的功能;这些特权必须在单独的角色中定义。

`kibana_dashboard_only_user`

     (This role is deprecated, please use [Kibana feature privileges](/guide/en/kibana/8.9/kibana-privileges.html#kibana-feature-privileges) instead). Grants read-only access to the Kibana Dashboard in every [space in Kibana](/guide/en/kibana/8.9/xpack-spaces.html). This role does not have access to editing tools in Kibana. 
`kibana_system`

    

授予 Kibana 系统用户读取和写入 Kibana 索引、管理索引模板和令牌以及检查 Elasticsearch 集群可用性所需的访问权限。它还允许激活、搜索和检索用户配置文件，以及更新"kibana-*"命名空间的用户配置文件数据。此角色授予对".monitoring-*"索引的读取访问权限以及对".reporting-*"索引的读写访问权限。有关更多信息，请参阅在 Kibana 中配置安全性。

不应将此角色分配给用户，因为授予的权限可能会在版本之间更改。

`kibana_admin`

     Grants access to all features in Kibana. For more information on Kibana authorization, see [Kibana authorization](/guide/en/kibana/8.9/xpack-security-authorization.html). 
`kibana_user`

     (This role is deprecated, please use the [`kibana_admin`](built-in-roles.html#built-in-roles-kibana-admin) role instead.) Grants access to all features in Kibana. For more information on Kibana authorization, see [Kibana authorization](/guide/en/kibana/8.9/xpack-security-authorization.html). 
`logstash_admin`

     Grants access to the `.logstash*` indices for managing configurations, and grants necessary access for logstash-specific APIs exposed by the logstash x-pack plugin. 
`logstash_system`

    

授予 Logstash 系统用户向 Elasticsearch 发送系统级数据(如监控)所需的访问权限。有关更多信息，请参阅在 Logstash 中配置安全性。

* 不应将此角色分配给用户，因为授予的权限可能会在版本之间更改。  * 此角色不提供对 logstash 索引的访问权限，不适合在 Logstash 管道中使用。

`machine_learning_admin`

     Provides all of the privileges of the `machine_learning_user` role plus the full use of the machine learning APIs. Grants `manage_ml` cluster privileges, read access to `.ml-anomalies*`, `.ml-notifications*`, `.ml-state*`, `.ml-meta*` indices and write access to `.ml-annotations*` indices. Machine learning administrators also need index privileges for source and destination indices and roles that grant access to Kibana. See [Machine learning security privileges](/guide/en/machine-learning/8.9/setup.html#setup-privileges). 
`machine_learning_user`

     Grants the minimum privileges required to view machine learning configuration, status, and work with results. This role grants `monitor_ml` cluster privileges, read access to the `.ml-notifications` and `.ml-anomalies*` indices (which store machine learning results), and write access to `.ml-annotations*` indices. Machine learning users also need index privileges for source and destination indices and roles that grant access to Kibana. See [Machine learning security privileges](/guide/en/machine-learning/8.9/setup.html#setup-privileges). 
`manage_enrich`

     Grants privileges to access and use all of the [enrich APIs](/guide/en/elasticsearch/reference/8.9/enrich-apis.html). Users with this role can manage enrich policies that add data from your existing indices to incoming documents during ingest. 
`monitoring_user`

     Grants the minimum privileges required for any user of X-Pack monitoring other than those required to use Kibana. This role grants access to the monitoring indices and grants privileges necessary for reading basic cluster information. This role also includes all [Kibana privileges](/guide/en/kibana/8.9/kibana-privileges.html) for the Elastic Stack monitoring features. Monitoring users should also be assigned the `kibana_admin` role, or another role with [access to the Kibana instance](/guide/en/kibana/8.9/xpack-security-authorization.html). 
`remote_monitoring_agent`

     Grants the minimum privileges required to write data into the monitoring indices (`.monitoring-*`). This role also has the privileges necessary to create Metricbeat indices (`metricbeat-*`) and write data into them. 
`remote_monitoring_collector`

     Grants the minimum privileges required to collect monitoring data for the Elastic Stack. 
`reporting_user`

     Grants the specific privileges required for users of X-Pack reporting other than those required to use Kibana. This role grants access to the reporting indices; each user has access to only their own reports. Reporting users should also be assigned additional roles that grant [access to Kibana](/guide/en/kibana/8.9/xpack-security-authorization.html) as well as read access to the [indices](defining-roles.html#roles-indices-priv "Indices Privileges") that will be used to generate reports. 
`rollup_admin`

     Grants `manage_rollup` cluster privileges, which enable you to manage and execute all rollup actions. 
`rollup_user`

     Grants `monitor_rollup` cluster privileges, which enable you to perform read-only operations related to rollups. 
`snapshot_user`

     Grants the necessary privileges to create snapshots of **all** the indices and to view their metadata. This role enables users to view the configuration of existing snapshot repositories and snapshot details. It does not grant authority to remove or add repositories or to restore snapshots. It also does not enable to change index settings or to read or update data stream or index data. 
`superuser`

    

授予对集群管理和数据索引的完全访问权限。此角色还授予对受限索引(如".security")的直接只读访问权限。具有"超级用户"角色的用户可以模拟系统中的任何其他用户。

在 Elastic Cloud 上，所有标准用户(包括具有"超级用户"角色的用户)都被限制执行仅限操作员的操作。

此角色可以管理安全性并创建具有无限权限的角色。将其分配给用户时要格外小心。

`transform_admin`

     Grants `manage_transform` cluster privileges, which enable you to manage transforms. This role also includes all [Kibana privileges](/guide/en/kibana/8.9/kibana-privileges.html) for the machine learning features. 
`transform_user`

     Grants `monitor_transform` cluster privileges, which enable you to perform read-only operations related to transforms. This role also includes all [Kibana privileges](/guide/en/kibana/8.9/kibana-privileges.html) for the machine learning features. 
`transport_client`

    

授予通过 JavaTransport 客户机访问集群所需的特权。Java 传输客户机使用_Node活动API_和_Cluster状态API_(启用嗅探时)获取有关集群中节点的信息。如果用户使用传输客户端，请为其分配此角色。

有效地使用传输客户端意味着向用户授予对群集状态的访问权限。这意味着用户可以查看所有索引、索引模板、映射、节点以及有关集群的基本上所有内容的元数据。但是，此角色不授予查看所有索引中的数据的权限。

`viewer`

    

授予对 Kibana 中所有功能(包括解决方案)和数据索引的只读访问权限。

* 此角色提供对未以点为前缀的任何索引的读取访问权限。  * 一旦 Kibana 新功能可用，此角色就会自动授予对这些功能的只读访问权限。

`watcher_admin`

    

允许用户创建和执行所有观察程序操作。授予对".watches"索引的读取访问权限。还授予对监视历史记录和触发的监视索引的读取访问权限。

`watcher_user`

    

授予对".watches"索引、获取监视操作和观察者统计信息的读取访问权限。

[« User authorization](authorization.md) [Defining roles »](defining-
roles.md)
