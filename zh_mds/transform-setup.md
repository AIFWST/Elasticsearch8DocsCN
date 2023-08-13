

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Roll up or
transform your data](data-rollup-transform.md) ›[Transforming
data](transforms.md)

[« Transform overview](transform-overview.md) [When to use transforms
»](transform-usage.md)

## 设置升级转换

#### 要求概述

若要使用转换，必须具有：

* 至少一个转换节点，* 在 Kibana 空间中可见的管理功能，以及 * 安全权限：

    * grant use of transforms, and 
    * grant access to source and destination indices 

#### 安全特权

分配安全权限会影响用户访问转换的方式。考虑两个主要类别：

* Elasticsearch API user** ：使用 Elasticsearch 客户端、cURL 或 Kibana **Dev Tools** 通过 Elasticsearch API 访问转换。此场景需要 Elasticsearch 安全权限。  * **Kibana 用户** ：在 Kibana 中使用变换。此场景需要 Kibana 功能权限 _and_ Elasticsearch 安全权限。

##### Elasticsearch APIuser

若要_manage_ 转换，必须满足以下所有要求：

* "transform_admin"内置角色或"manage_transform"集群权限，* 源索引的"读取"和"view_index_metadata"索引权限，以及目标索引的 * "create_index"、"索引"、"管理"和"读取"索引权限。如果配置了"retention_policy"，则还需要对目标索引具有"删除"索引权限。

若要仅查看转换的配置和状态，必须具有：

* "transform_user"内置角色或"monitor_transform"群集权限

有关 Elasticsearch 角色和权限的更多信息，请参阅内置角色和安全权限。

##### Kibanauser

在 Kibana 空间中，要完全访问转换，您必须满足以下所有要求：

* Kibana 空间中可见的管理功能，包括"数据视图管理"和"堆栈监控"、* "monitoring_user"内置角色、* "transform_admin"内置角色或"manage_transform"集群权限、* "kibana_admin"内置角色或具有"数据视图管理"功能的"读取"或"全部"Kibana 权限的自定义角色(取决于目标索引是否已存在数据视图)，   * 源索引的数据视图，* 源索引的"读取"和"view_index_metadata"索引权限，以及目标索引的"create_index"、"索引"、"管理"和"读取"索引权限。此外，使用"retention_policy"时，目标索引需要"删除"索引权限。  * "read_pipeline"群集权限(如果转换使用采集管道)

在 Kibana 空间中，要对转换进行只读访问，您必须满足以下所有要求：

* Kibana 空间中可见的管理功能，包括"堆栈监控"、"monitoring_user"内置角色、* "transform_user"内置角色或"monitor_transform"集群权限、* "kibana_admin"内置角色或对空间中至少一个功能具有"读取"Kibana 权限的自定义角色，* 源索引和目标索引的数据视图，以及 * 源索引和目标索引的"读取"和"view_index_metadata"索引权限

有关更多信息和 Kibana 安全功能，请参阅 Kibana 角色管理和 Kibanaprivileges。

#### 木花空间

使用空间，您可以在 Kibana 中组织源索引和目标索引以及其他已保存的对象，并仅查看属于空间的对象。但是，转换是一个长时间运行的任务，在群集级别进行管理，因此不限于某些空间的范围。可以在 Kibana** 的堆栈管理**下为数据视图实现空间感知>这允许对转换目标索引的权限。

要在 Kibana 中成功创建转换，您必须登录到源索引可见且"数据视图管理"和"堆栈监控"功能可见的空间。

[« Transform overview](transform-overview.md) [When to use transforms
»](transform-usage.md)
