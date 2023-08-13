

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Remote clusters](remote-clusters.md)

[« Connect to remote clusters](remote-clusters-connect.md) [Remote cluster
settings »](remote-clusters-settings.md)

## 为远程群集配置角色和用户

连接远程群集后，您可以在本地群集和远程群集上创建用户角色并分配必要的权限。这些角色是使用跨集群复制和跨集群搜索所必需的。

您必须在本地和远程群集上使用相同的角色名称。例如，以下跨群集复制配置在本地和远程群集上使用"远程复制"角色名称。但是，您可以在每个群集上指定不同的角色定义。

您可以通过从侧面导航栏中选择**安全>角色**，从 Kibana 的堆栈管理中管理用户和角色。您还可以使用角色管理 API 动态添加、更新、删除和检索角色。当您使用 API 来管理"本机"领域中的角色时，角色存储在内部 Elasticsearch 索引中。

以下请求使用创建或更新角色 API。您必须至少具有"manage_security"群集权限才能使用此 API。

### 配置跨群集复制的权限

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

然后，可以配置跨群集复制以跨数据中心复制数据。

### 配置跨集群搜索的权限

跨集群搜索用户需要不同的集群和索引权限以及远程集群和本地集群。以下请求在本地和远程群集上创建单独的角色，然后创建具有所需角色的用户。

##### 远程群集

在远程集群上，跨集群搜索角色需要目标索引的"读取"和"read_cross_cluster"权限。

如果使用 API 密钥对请求进行身份验证，则 API 密钥需要对 **local** 群集(而不是远程群集)具有上述权限。

如果代表其他用户发出请求，则身份验证用户必须在远程群集上具有"run_as"权限。

以下请求在远程群集上创建"远程搜索"角色：

    
    
    POST /_security/role/remote-search
    {
      "indices": [
        {
          "names": [
            "target-indices"
          ],
          "privileges": [
            "read",
            "read_cross_cluster"
          ]
        }
      ]
    }

##### 本地群集

在本地群集(用于启动跨群集搜索的群集)上，用户只需要"远程搜索"角色。角色权限可以为空。

以下请求在本地群集上创建"远程搜索"角色：

    
    
    POST /_security/role/remote-search
    {}

在每个群集上创建"远程搜索"角色后，使用创建或更新用户 API 在本地群集上创建用户并分配"远程搜索"角色。例如，以下请求将"远程搜索"角色分配给名为"交叉搜索用户"的用户：

    
    
    POST /_security/user/cross-search-user
    {
      "password" : "l0ng-r4nd0m-p@ssw0rd",
      "roles" : [ "remote-search" ]
    }

您只需在 **local** 群集上创建此用户。

然后，具有"远程搜索"角色的用户可以跨群集进行搜索。

### 配置跨集群搜索和 Kibana 的权限

使用 Kibana 跨多个集群进行搜索时，两步授权过程可确定用户是否可以访问远程集群上的数据流和索引：

* 首先，本地集群确定用户是否有权访问远程集群。本地集群是 Kibana 连接到的集群。  * 如果用户获得授权，则远程集群将确定用户是否有权访问指定的数据流和索引。

要向 Kibana 用户授予对远程集群的访问权限，请为其分配一个本地角色，该角色对远程集群上的索引具有读取权限。您可以将远程集群中的数据流和索引指定为<remote_cluster_name><target>"："。

要授予用户对远程数据流和索引的读取访问权限，您必须在远程集群上创建一个匹配角色，该角色授予"read_cross_cluster"权限，以访问相应的数据流和索引。

例如，您可能正在本地集群上主动为 Logstash 数据编制索引，并定期将较旧的基于时间的索引卸载到远程集群上的存档中。您希望跨两个集群进行搜索，因此必须在两个集群上启用 Kibana 用户。

##### 本地群集

在本地集群上，创建一个"logstash-reader"角色，该角色授予对本地"logstash-*"索引的"读取"和"view_index_metadata"权限。

如果在 Elasticsearch 中将本地集群配置为另一个远程集群，则本地集群上的"logstash-reader"角色也需要授予"read_cross_cluster"权限。

    
    
    POST /_security/role/logstash-reader
    {
      "indices": [
        {
          "names": [
            "logstash-*"
            ],
            "privileges": [
              "read",
              "view_index_metadata"
              ]
        }
      ]
    }

为您的 Kibana 用户分配一个授予 Kibana 访问权限的角色，以及您的"logstash_reader"角色。例如，以下请求创建"跨集群 kibana"用户并分配"kibana-access"和"logstash-reader"角色。

    
    
    PUT /_security/user/cross-cluster-kibana
    {
      "password" : "l0ng-r4nd0m-p@ssw0rd",
      "roles" : [
        "logstash-reader",
        "kibana-access"
        ]
    }

##### 远程群集

在远程集群上，创建一个"logstash-reader"角色，该角色授予"logstash-*"索引的"read_cross_cluster"权限以及"读取"和"view_index_metadata"权限。

    
    
    POST /_security/role/logstash-reader
    {
      "indices": [
        {
          "names": [
            "logstash-*"
            ],
            "privileges": [
              "read_cross_cluster",
              "read",
              "view_index_metadata"
              ]
        }
      ]
    }

[« Connect to remote clusters](remote-clusters-connect.md) [Remote cluster
settings »](remote-clusters-settings.md)
