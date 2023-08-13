

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md)

[« Auditing search queries](auditing-search-queries.md) [Securing clients
and integrations »](security-clients-integrations.md)

## 使用 IP 过滤限制连接

除了尝试加入群集的其他节点之外，还可以将 IP 过滤应用于应用程序客户机、节点客户机或传输客户机。

如果节点的 IP 地址在黑名单上，Elasticsearch 安全功能允许连接到 Elasticsearch，但会立即丢弃该地址，并且不会处理任何请求。

Elasticsearch 安装不是为了通过互联网公开访问而设计的。IP 过滤和 Elasticsearchsecurity 功能的其他功能不会改变这种情况。

### 启用 IP 过滤

Elasticsearch 安全功能包含允许或拒绝主机、域或子网的访问控制功能。如果启用了操作员权限功能，则只有操作员用户可以更新这些设置。

您可以通过在"elasticsearch.yml"中指定"xpack.security.transport.filter.allow"和"xpack.security.transport.filter.deny"设置来配置 IP 过滤。允许规则优先于拒绝规则。

除非明确指定，否则"xpack.security.http.filter.*"设置默认为相应的"xpack.security.transport.filter.*"设置的值。

    
    
    xpack.security.transport.filter.allow: "192.168.0.1"
    xpack.security.transport.filter.deny: "192.168.0.0/24"

"_all"关键字可用于拒绝所有未明确允许的连接。

    
    
    xpack.security.transport.filter.allow: [ "192.168.0.1", "192.168.0.2", "192.168.0.3", "192.168.0.4" ]
    xpack.security.transport.filter.deny: _all

IP 过滤配置还支持 IPv6 地址。

    
    
    xpack.security.transport.filter.allow: "2001:0db8:1234::/48"
    xpack.security.transport.filter.deny: "1234:0db8:85a3:0000:0000:8a2e:0370:7334"

您还可以在 DNS 查找可用时按主机名进行筛选。

    
    
    xpack.security.transport.filter.allow: localhost
    xpack.security.transport.filter.deny: '*.google.com'

### 禁用 IP 漏洞

在某些情况下，禁用 IP 筛选可以略微提高性能。要完全禁用 IP 过滤，请将"elasticsearch.yml"配置文件中的"xpack.security.transport.filter.enabled"设置的值设置为"false"。

    
    
    xpack.security.transport.filter.enabled: false

您还可以禁用传输协议的 IP 过滤，但仅对 HTTP 启用它。

    
    
    xpack.security.transport.filter.enabled: false
    xpack.security.http.filter.enabled: true

### 指定 TCP 传输配置文件

TCP 传输配置文件使 Elasticsearch 能够在多个主机上绑定。Elasticsearchsecurity功能使您能够对不同的配置文件应用不同的IP过滤。

    
    
    xpack.security.transport.filter.allow: 172.16.0.0/24
    xpack.security.transport.filter.deny: _all
    transport.profiles.client.xpack.security.filter.allow: 192.168.0.0/24
    transport.profiles.client.xpack.security.filter.deny: _all

如果未指定配置文件，则会自动使用"默认"。

### HTTP过滤

您可能希望对传输和 HTTP 协议进行不同的 IP 过滤。

    
    
    xpack.security.transport.filter.allow: localhost
    xpack.security.transport.filter.deny: '*.google.com'
    xpack.security.http.filter.allow: 172.16.0.0/16
    xpack.security.http.filter.deny: _all

#### 动态更新 IP 筛选器设置

如果在具有高度动态 IP 地址的环境中运行，例如基于云的托管，则在预配计算机时很难预先知道 IP 地址。您可以使用"_Cluster更新设置"API_，而不是更改配置文件并重新启动节点。例如：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "xpack.security.transport.filter.allow": '172.16.0.0/24'
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "persistent" : {
        "xpack.security.transport.filter.allow" : "172.16.0.0/24"
      }
    }

您还可以完全动态禁用过滤：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "xpack.security.transport.filter.enabled": false
        }
      }
    )
    puts response
    
    
    PUT /_cluster/settings
    {
      "persistent" : {
        "xpack.security.transport.filter.enabled" : false
      }
    }

为了避免将自己锁定在集群之外，默认边界传输地址永远不会被拒绝。这意味着您始终可以通过 SSH 连接到系统并使用 curl 来应用更改。

[« Auditing search queries](auditing-search-queries.md) [Securing clients
and integrations »](security-clients-integrations.md)
