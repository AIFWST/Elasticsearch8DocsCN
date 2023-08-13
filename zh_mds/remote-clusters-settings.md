

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Remote clusters](remote-clusters.md)

[« Configure roles and users for remote clusters](remote-clusters-
privileges.md) [Plugins »](modules-plugins.md)

## 远程群集设置

以下设置适用于嗅探模式和代理模式。特定于嗅探模式和代理模式的设置分别描述。

`cluster.remote.<cluster_alias>.mode`

     The mode used for a remote cluster connection. The only supported modes are `sniff` and `proxy`. 
`cluster.remote.initial_connect_timeout`

     The time to wait for remote connections to be established when the node starts. The default is `30s`. 
`remote_cluster_client` [role](modules-node.html#node-roles "Node roles")

     By default, any node in the cluster can act as a cross-cluster client and connect to remote clusters. To prevent a node from connecting to remote clusters, specify the [node.roles](modules-node.html#node-roles "Node roles") setting in `elasticsearch.yml` and exclude `remote_cluster_client` from the listed roles. Search requests targeting remote clusters must be sent to a node that is allowed to act as a cross-cluster client. Other features such as machine learning [data feeds](ml-settings.html#general-ml-settings "General machine learning settings"), [transforms](transform-settings.html#general-transform-settings "General transforms settings"), and [cross-cluster replication](ccr-getting-started-tutorial.html "Tutorial: Set up cross-cluster replication") require the `remote_cluster_client` role. 
`cluster.remote.<cluster_alias>.skip_unavailable`

     Per cluster boolean setting that allows to skip specific clusters when no nodes belonging to them are available and they are the target of a remote cluster request. Default is `false`, meaning that all clusters are mandatory by default, but they can selectively be made optional by setting this setting to `true`. 
`cluster.remote.<cluster_alias>.transport.ping_schedule`

     Sets the time interval between regular application-level ping messages that are sent to try and keep remote cluster connections alive. If set to `-1`, application-level ping messages to this remote cluster are not sent. If unset, application-level ping messages are sent according to the global `transport.ping_schedule` setting, which defaults to `-1` meaning that pings are not sent. It is preferable to correctly configure TCP keep-alives instead of configuring a `ping_schedule`, because TCP keep-alives are handled by the operating system and not by Elasticsearch. By default Elasticsearch enables TCP keep-alives on remote cluster connections. Remote cluster connections are transport connections so the `transport.tcp.*` [advanced settings](modules-network.html#transport-settings "Advanced transport settings") regarding TCP keep-alives apply to them. 
`cluster.remote.<cluster_alias>.transport.compress`

     Per cluster setting that enables you to configure compression for requests to a specific remote cluster. This setting impacts only requests sent to the remote cluster. If the inbound request is compressed, Elasticsearch compresses the response. The setting options are `true`, `indexing_data`, and `false`. If unset, the global `transport.compress` is used as the fallback setting. 
`cluster.remote.<cluster_alias>.transport.compression_scheme`

     Per cluster setting that enables you to configure compression scheme for requests to a specific remote cluster. This setting impacts only requests sent to the remote cluster. If an inbound request is compressed, Elasticsearch compresses the response using the same compression scheme. The setting options are `deflate` and `lz4`. If unset, the global `transport.compression_scheme` is used as the fallback setting. 

### 嗅探模式远程群集设置

`cluster.remote.<cluster_alias>.seeds`

     The list of seed nodes used to sniff the remote cluster state. 
`cluster.remote.<cluster_alias>.node_connections`

     The number of gateway nodes to connect to for this remote cluster. The default is `3`. 

`cluster.remote.node.attr`

     A node attribute to filter out nodes that are eligible as a gateway node in the remote cluster. For instance a node can have a node attribute `node.attr.gateway: true` such that only nodes with this attribute will be connected to if `cluster.remote.node.attr` is set to `gateway`. 

### 代理模式远程群集设置

`cluster.remote.<cluster_alias>.proxy_address`

     The address used for all remote connections. 
`cluster.remote.<cluster_alias>.proxy_socket_connections`

     The number of socket connections to open per remote cluster. The default is `18`. 

`cluster.remote.<cluster_alias>.server_name`

     An optional hostname string which is sent in the `server_name` field of the TLS Server Name Indication extension if [TLS is enabled](security-basic-setup.html#encrypt-internode-communication "Encrypt internode communications with TLS"). The TLS transport will fail to open remote connections if this field is not a valid hostname as defined by the TLS SNI specification. 

[« Configure roles and users for remote clusters](remote-clusters-
privileges.md) [Plugins »](modules-plugins.md)
