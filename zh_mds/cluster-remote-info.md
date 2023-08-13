

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Pending cluster tasks API](cluster-pending.md) [Task management API
»](tasks.md)

## 远程集群信息接口

返回已配置的远程群集信息。

###Request

"获取/_remote/信息"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

群集远程信息 API 允许您检索所有已配置的远程群集信息。它返回由配置的远程群集别名键入的连接和终结点信息。

### 响应正文

`mode`

     Connection mode for the remote cluster. Returned values are `sniff` and `proxy`. 
`connected`

     True if there is at least one connection to the remote cluster. 
`initial_connect_timeout`

     The initial connect timeout for remote cluster connections. 

`skip_unavailable`

     Whether a cross-cluster search skips the remote cluster if its nodes are unavailable during the search. If `true`, a cross-cluster search also ignores errors returned by the remote cluster. Refer to [Optional remote clusters](modules-cross-cluster-search.html#skip-unavailable-clusters "Optional remote clusters"). 
`seeds`

     Initial seed transport addresses of the remote cluster when sniff mode is configured. 
`num_nodes_connected`

     Number of connected nodes in the remote cluster when sniff mode is configured. 
`max_connections_per_cluster`

     Maximum number of connections maintained for the remote cluster when sniff mode is configured. 
`proxy_address`

     Address for remote connections when proxy mode is configured. 
`num_proxy_sockets_connected`

     Number of open socket connections to the remote cluster when proxy mode is configured. 
`max_proxy_socket_connections`

     The maximum number of socket connections to the remote cluster when proxy mode is configured. 

[« Pending cluster tasks API](cluster-pending.md) [Task management API
»](tasks.md)
