

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Node](modules-node.md) [Node query cache settings »](query-cache.md)

##Networking

每个 Elasticsearch 节点都有两个不同的网络接口。客户端使用其 HTTP 接口向 Elasticsearch 的 REST API 发送请求，但节点使用传输接口与其他节点通信。传输接口还用于与远程群集进行通信。

您可以使用"network.*"设置同时配置这两个接口。如果您的网络更复杂，则可能需要使用"http.*"和"transport.*"设置单独配置接口。如果可能，请使用适用于这两个接口的"network.*"设置来简化配置并减少重复。

默认情况下，Elasticsearch仅绑定到"localhost"，这意味着它无法远程访问。此配置对于由一个或多个节点组成的本地开发群集(全部在同一主机上运行)来说已足够。要跨多个主机或远程客户端可访问的集群形成集群，必须调整一些网络设置，例如"network.host"。

### 小心网络配置！

切勿将未受保护的节点暴露给公共互联网。如果这样做，则允许世界上的任何人下载、修改或删除群集中的任何数据。

将 Elasticsearch 配置为绑定到非本地地址会将一些警告转换为致命异常。如果节点在配置其网络设置后拒绝启动，则必须在继续之前解决记录的异常。

### 常用网络设置

大多数用户只需要配置以下网络设置。

`network.host`

    

(静态，字符串)为 HTTP 和传输流量设置此节点的地址。节点将绑定到此地址，并将其用作其发布地址。接受 IP 地址、主机名或特殊值。

默认为"_local_"。

`http.port`

    

(静态，整数)要绑定用于 HTTP 客户端通信的端口。接受单个值或范围。如果指定了范围，则节点将绑定到该范围中的第一个可用端口。

默认为"9200-9300"。

`transport.port`

    

(静态，整数)用于节点之间通信的绑定端口。接受单个值或范围。如果指定了范围，则节点将绑定到该范围中的第一个可用端口。将此设置设置为每个符合主节点条件的节点上的单个端口，而不是范围。

默认为"9300-9400"。

### 网络地址的特殊值

您可以将 Elasticsearch 配置为使用以下特殊值自动确定其地址。在配置"network.host"、"network.bind_host"、"network.publish_host"以及 HTTP 和传输接口的相应设置时，请使用这些值。

`_local_`

     Any loopback addresses on the system, for example `127.0.0.1`. 
`_site_`

     Any site-local addresses on the system, for example `192.168.0.1`. 
`_global_`

     Any globally-scoped addresses on the system, for example `8.8.8.8`. 
`_[networkInterface]_`

     Use the addresses of the network interface called `[networkInterface]`. For example if you wish to use the addresses of an interface called `en0` then set `network.host: _en0_`. 
`0.0.0.0`

     The addresses of all available network interfaces. 

在某些系统中，这些特殊值解析为多个地址。如果是这样，Elasticsearch 将选择其中一个作为其发布地址，并可能在每次节点重新启动时更改其选择。确保您的节点可以在每个可能的地址访问。

任何包含"："的值(例如 IPv6 地址或某些特殊值)都必须用引号括起来，因为"："是 YAML 中的特殊字符。

#### IPv4 vsIPv6

默认情况下，这些特殊值同时生成 IPv4 和 IPv6 地址，但您也可以添加"：ipv4"或"：ipv6"后缀，以分别将它们限制为仅 IPv4 或 IPv6 地址。例如，"network.host："_en0：ipv4_"会将此节点的地址设置为接口"en0"的 IPv4 地址。

### 云中的发现

在云中运行时，可以使用 EC2 发现插件或安装了 Google Compute Engine 发现插件来运行更多特殊设置。

### 绑定和发布

Elasticsearch 将网络地址用于两个不同的目的，即绑定和发布。大多数节点将使用相同的地址进行所有操作，但更复杂的设置可能需要为不同的目的配置不同的地址。

当像Elasticsearch这样的应用程序希望接收网络通信时，它必须向操作系统指示它应该接收其流量的地址或地址。这称为 _binding_ 到这些地址。如果需要，Elasticsearch 可以绑定到多个地址，但大多数节点只绑定到一个地址。Elasticsearch 只能在具有具有该地址的网络接口的主机上运行时绑定到该地址。如有必要，您可以将传输接口和 HTTP 接口配置为绑定到不同的地址。

每个 Elasticsearch 节点都有一个客户端和其他节点可以联系它的地址，称为其_publish address_。每个节点都有一个用于其 HTTP 接口的发布地址和一个用于其传输接口的发布地址。这两个地址可以是任何内容，并且不需要是主机上网络接口的地址。唯一的要求是每个节点必须：

* 所有将使用嗅探发现它的客户端都可以在其 HTTP 发布地址访问它。  * 可通过其集群中的所有其他节点以及将使用嗅探模式发现它的任何远程集群在其传输发布地址访问。

如果使用主机名指定传输发布地址，则 Elasticsearch 会在启动期间将此主机名解析为 IP 地址一次，其他节点将使用生成的 IP 地址，而不是自己再次解析该名称。为避免混淆，请使用解析为所有网络位置中节点地址的主机名。

#### 使用单个地址

最常见的配置是让 Elasticsearch 绑定到客户端和其他节点可以访问的单个地址。在此配置中，您只需将"network.host"设置为该地址。不应单独设置任何绑定或发布地址，也不应单独配置 HTTP 或传输接口的地址。

#### 使用多个地址

如果您希望将 Elasticsearch 绑定到多个地址，或者发布与您绑定的地址不同的地址，请使用高级网络设置。将"network.bind_host"设置为绑定地址，将"network.publish_host"设置为公开此节点的地址。在复杂的配置中，您可以为 HTTP 和传输接口以不同的方式配置这些地址。

### 高级网络设置

这些高级设置允许您绑定到多个地址，或使用不同的地址进行绑定和发布。在大多数情况下，它们不是必需的，如果可以使用常用设置，则不应使用它们。

`network.bind_host`

     ([Static](settings.html#static-cluster-setting), string) The network address(es) to which the node should bind in order to listen for incoming connections. Accepts a list of IP addresses, hostnames, and [special values](modules-network.html#network-interface-values "Special values for network addresses"). Defaults to the address given by `network.host`. Use this setting only if binding to multiple addresses or using different addresses for publishing and binding. 
`network.publish_host`

     ([Static](settings.html#static-cluster-setting), string) The network address that clients and other nodes can use to contact this node. Accepts an IP address, a hostname, or a [special value](modules-network.html#network-interface-values "Special values for network addresses"). Defaults to the address given by `network.host`. Use this setting only if binding to multiple addresses or using different addresses for publishing and binding. 

您可以为"network.host"和"network.publish_host"指定地址列表。您还可以指定一个或多个解析为多个地址的主机名或特殊值。如果这样做，那么Elasticsearch会选择一个地址作为其发布地址。此选项使用基于 IPv4/IPv6 堆栈首选项和可访问性的启发式方法，并且可能会在节点重新启动时更改。确保每个节点都可以在所有可能的发布地址上访问。

#### 高级 TCP 设置

使用以下设置来控制 HTTP 接口和传输接口使用的 TCP 连接的低级别参数。

`network.tcp.keep_alive`

     ([Static](settings.html#static-cluster-setting), boolean) Configures the `SO_KEEPALIVE` option for network sockets, which determines whether each connection sends TCP keepalive probes. Defaults to `true`. 
`network.tcp.keep_idle`

     ([Static](settings.html#static-cluster-setting), integer) Configures the `TCP_KEEPIDLE` option for network sockets, which determines the time in seconds that a connection must be idle before starting to send TCP keepalive probes. Defaults to `-1`, which means to use the system default. This value cannot exceed `300` seconds. Only applicable on Linux and macOS. 
`network.tcp.keep_interval`

     ([Static](settings.html#static-cluster-setting), integer) Configures the `TCP_KEEPINTVL` option for network sockets, which determines the time in seconds between sending TCP keepalive probes. Defaults to `-1`, which means to use the system default. This value cannot exceed `300` seconds. Only applicable on Linux and macOS. 
`network.tcp.keep_count`

     ([Static](settings.html#static-cluster-setting), integer) Configures the `TCP_KEEPCNT` option for network sockets, which determines the number of unacknowledged TCP keepalive probes that may be sent on a connection before it is dropped. Defaults to `-1`, which means to use the system default. Only applicable on Linux and macOS. 
`network.tcp.no_delay`

     ([Static](settings.html#static-cluster-setting), boolean) Configures the `TCP_NODELAY` option on network sockets, which determines whether [TCP no delay](https://en.wikipedia.org/wiki/Nagle%27s_algorithm) is enabled. Defaults to `true`. 
`network.tcp.reuse_address`

     ([Static](settings.html#static-cluster-setting), boolean) Configures the `SO_REUSEADDR` option for network sockets, which determines whether the address can be reused or not. Defaults to `false` on Windows and `true` otherwise. 
`network.tcp.send_buffer_size`

     ([Static](settings.html#static-cluster-setting), [byte value](api-conventions.html#byte-units "Byte size units")) Configures the size of the TCP send buffer for network sockets. Defaults to `-1` which means to use the system default. 
`network.tcp.receive_buffer_size`

     ([Static](settings.html#static-cluster-setting), [byte value](api-conventions.html#byte-units "Byte size units")) Configures the size of the TCP receive buffer. Defaults to `-1` which means to use the system default. 

### 高级 HTTPsettings

使用以下高级设置独立于传输接口配置 HTTP 接口。您还可以使用网络设置同时配置这两个接口。

`http.host`

    

(静态，字符串)为 HTTP 流量设置此节点的地址。节点将绑定到此地址，并将其用作其 HTTP 发布地址。接受 IP 地址、主机名或特殊值。仅当传输接口和 HTTP 接口需要不同的配置时，才使用此设置。

默认为"network.host"给出的地址。

`http.bind_host`

     ([Static](settings.html#static-cluster-setting), string) The network address(es) to which the node should bind in order to listen for incoming HTTP connections. Accepts a list of IP addresses, hostnames, and [special values](modules-network.html#network-interface-values "Special values for network addresses"). Defaults to the address given by `http.host` or `network.bind_host`. Use this setting only if you require to bind to multiple addresses or to use different addresses for publishing and binding, and you also require different binding configurations for the transport and HTTP interfaces. 
`http.publish_host`

     ([Static](settings.html#static-cluster-setting), string) The network address for HTTP clients to contact the node using sniffing. Accepts an IP address, a hostname, or a [special value](modules-network.html#network-interface-values "Special values for network addresses"). Defaults to the address given by `http.host` or `network.publish_host`. Use this setting only if you require to bind to multiple addresses or to use different addresses for publishing and binding, and you also require different binding configurations for the transport and HTTP interfaces. 
`http.publish_port`

     ([Static](settings.html#static-cluster-setting), integer) The port of the [HTTP publish address](modules-network.html#modules-network-binding-publishing "Binding and publishing"). Configure this setting only if you need the publish port to be different from `http.port`. Defaults to the port assigned via `http.port`. 
`http.max_content_length`

     ([Static](settings.html#static-cluster-setting), [byte value](api-conventions.html#byte-units "Byte size units")) Maximum size of an HTTP request body. If the body is compressed, the limit applies to the HTTP request body size before compression. Defaults to `100mb`. Configuring this setting to greater than `100mb` can cause cluster instability and is not recommended. If you hit this limit when sending a request to the [Bulk](docs-bulk.html "Bulk API") API, configure your client to send fewer documents in each bulk request. If you wish to index individual documents that exceed `100mb`, pre-process them into smaller documents before sending them to Elasticsearch. For instance, store the raw data in a system outside Elasticsearch and include a link to the raw data in the documents that Elasticsearch indexes. 
`http.max_initial_line_length`

     ([Static](settings.html#static-cluster-setting), [byte value](api-conventions.html#byte-units "Byte size units")) Maximum size of an HTTP URL. Defaults to `4kb`. 
`http.max_header_size`

     ([Static](settings.html#static-cluster-setting), [byte value](api-conventions.html#byte-units "Byte size units")) Maximum size of allowed headers. Defaults to `16kb`. 

'http.compression' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

    

(静态，布尔值)尽可能支持压缩(使用接受编码)。如果启用了 HTTPS，则默认为"false"。否则，默认为"true"。

禁用 HTTPS 压缩可缓解潜在的安全风险，例如 BREACH 攻击。要压缩HTTPStraffic，您必须明确地将"http.compression"设置为"true"。

`http.compression_level`

     ([Static](settings.html#static-cluster-setting), integer) Defines the compression level to use for HTTP responses. Valid values are in the range of 1 (minimum compression) and 9 (maximum compression). Defaults to `3`. 

'http.cors.enabled' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

    

(静态，布尔值)启用或禁用跨源资源共享，这决定了其他源上的浏览器是否可以执行针对 Elasticsearch 的请求。设置为 'true' 以启用 Elasticsearch 来处理预检 CORS 请求。如果"http.cors.allow-origin"列表允许请求中发送的"Origin"，Elasticsearch 将使用"Access-Control-Allow-Origin"标头响应这些请求。设置为 'false'(默认值)可使 Elasticsearch 忽略 'Origin' 请求标头，从而有效地禁用 CORSrequests，因为 Elasticsearch 永远不会响应 'Access-Control-Allow-Origin' 响应标头。

如果客户端未发送带有"Origin"标头的预检请求，或者未检查来自服务器的响应标头以验证"访问控制-允许源"响应标头，则跨源安全性会受到损害。如果未在 Elasticsearch 上启用 CORS，则客户端知道的唯一方法是发送预检请求并意识到缺少所需的响应标头。

'http.cors.allow-origin' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

    

(静态，字符串)哪个起源允许。如果在值前面加上正斜杠 ('/')，这将被视为正则表达式，允许您支持 HTTP 和 HTTP。例如，使用 '/https？：\/\/localhost(：[0-9]+)？/' 在这两种情况下都会适当地返回请求标头。默认为不允许源。

通配符 ('*') 是一个有效值，但被视为安全风险，因为您的 Elasticsearch 实例对来自 **任何地方** 的跨源请求开放。

'http.cors.max-age' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Static](settings.html#static-cluster-setting), integer) Browsers send a "preflight" OPTIONS-request to determine CORS settings. `max-age` defines for how long, in seconds, the result should be cached. Defaults to `1728000` (20 days). 

'http.cors.allow-methods' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Static](settings.html#static-cluster-setting), string) Which methods to allow. Defaults to `OPTIONS, HEAD, GET, POST, PUT, DELETE`. 

'http.cors.allow-headers' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Static](settings.html#static-cluster-setting), string) Which headers to allow. Defaults to `X-Requested-With, Content-Type, Content-Length, Authorization, Accept, User-Agent, X-Elastic-Client-Meta`. 

'http.cors.expose-headers' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Static](settings.html#static-cluster-setting)) Which response headers to expose in the client. Defaults to `X-elastic-product`. 

'http.cors.allow-credentials' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

    

(静态，布尔值)是否应返回"访问控制允许凭据"标头。默认为"假"。

仅当设置设置为"true"时，才会返回此标头。

`http.detailed_errors.enabled`

     ([Static](settings.html#static-cluster-setting), boolean) Configures whether detailed error reporting in HTTP responses is enabled. Defaults to `true`, which means that HTTP requests that include the [`?error_trace` parameter](common-options.html#common-options-error-options "Enabling stack traces") will return a detailed error message including a stack trace if they encounter an exception. If set to `false`, requests with the `?error_trace` parameter are rejected. 
`http.pipelining.max_events`

     ([Static](settings.html#static-cluster-setting), integer) The maximum number of events to be queued up in memory before an HTTP connection is closed, defaults to `10000`. 
`http.max_warning_header_count`

     ([Static](settings.html#static-cluster-setting), integer) The maximum number of warning headers in client HTTP responses. Defaults to `-1` which means the number of warning headers is unlimited. 
`http.max_warning_header_size`

     ([Static](settings.html#static-cluster-setting), [byte value](api-conventions.html#byte-units "Byte size units")) The maximum total size of warning headers in client HTTP responses. Defaults to `-1` which means the size of the warning headers is unlimited. 
`http.tcp.keep_alive`

     ([Static](settings.html#static-cluster-setting), boolean) Configures the `SO_KEEPALIVE` option for this socket, which determines whether it sends TCP keepalive probes. Defaults to `network.tcp.keep_alive`. 
`http.tcp.keep_idle`

     ([Static](settings.html#static-cluster-setting), integer) Configures the `TCP_KEEPIDLE` option for HTTP sockets, which determines the time in seconds that a connection must be idle before starting to send TCP keepalive probes. Defaults to `network.tcp.keep_idle`, which uses the system default. This value cannot exceed `300` seconds. Only applicable on Linux and macOS. 
`http.tcp.keep_interval`

     ([Static](settings.html#static-cluster-setting), integer) Configures the `TCP_KEEPINTVL` option for HTTP sockets, which determines the time in seconds between sending TCP keepalive probes. Defaults to `network.tcp.keep_interval`, which uses the system default. This value cannot exceed `300` seconds. Only applicable on Linux and macOS. 
`http.tcp.keep_count`

     ([Static](settings.html#static-cluster-setting), integer) Configures the `TCP_KEEPCNT` option for HTTP sockets, which determines the number of unacknowledged TCP keepalive probes that may be sent on a connection before it is dropped. Defaults to `network.tcp.keep_count`, which uses the system default. Only applicable on Linux and macOS. 
`http.tcp.no_delay`

     ([Static](settings.html#static-cluster-setting), boolean) Configures the `TCP_NODELAY` option on HTTP sockets, which determines whether [TCP no delay](https://en.wikipedia.org/wiki/Nagle%27s_algorithm) is enabled. Defaults to `true`. 
`http.tcp.reuse_address`

     ([Static](settings.html#static-cluster-setting), boolean) Configures the `SO_REUSEADDR` option for HTTP sockets, which determines whether the address can be reused or not. Defaults to `false` on Windows and `true` otherwise. 
`http.tcp.send_buffer_size`

     ([Static](settings.html#static-cluster-setting), [byte value](api-conventions.html#byte-units "Byte size units")) The size of the TCP send buffer for HTTP traffic. Defaults to `network.tcp.send_buffer_size`. 
`http.tcp.receive_buffer_size`

     ([Static](settings.html#static-cluster-setting), [byte value](api-conventions.html#byte-units "Byte size units")) The size of the TCP receive buffer for HTTP traffic. Defaults to `network.tcp.receive_buffer_size`. 
`http.client_stats.enabled`

     ([Dynamic](settings.html#dynamic-cluster-setting), boolean) Enable or disable collection of HTTP client stats. Defaults to `true`. 
`http.client_stats.closed_channels.max_count`

     ([Static](settings.html#static-cluster-setting), integer) When `http.client_stats.enabled` is `true`, sets the maximum number of closed HTTP channels for which Elasticsearch reports statistics. Defaults to `10000`. 
`http.client_stats.closed_channels.max_age`

     ([Static](settings.html#static-cluster-setting), [time value](api-conventions.html#time-units "Time units")) When `http.client_stats.enabled` is `true`, sets the maximum length of time after closing a HTTP channel that Elasticsearch will report that channel's statistics. Defaults to `5m`. 

### 高级传输设置

使用以下高级设置独立于 HTTP 接口配置传输接口。使用网络设置一起配置两个接口。

`transport.host`

    

(静态，字符串)为传输流量设置此节点的地址。节点将绑定到此地址，并将其用作其传输发布地址。接受 IP 地址、主机名或特殊值。仅当传输接口和 HTTP 接口需要不同的配置时，才使用此设置。

默认为"network.host"给出的地址。

`transport.bind_host`

     ([Static](settings.html#static-cluster-setting), string) The network address(es) to which the node should bind in order to listen for incoming transport connections. Accepts a list of IP addresses, hostnames, and [special values](modules-network.html#network-interface-values "Special values for network addresses"). Defaults to the address given by `transport.host` or `network.bind_host`. Use this setting only if you require to bind to multiple addresses or to use different addresses for publishing and binding, and you also require different binding configurations for the transport and HTTP interfaces. 
`transport.publish_host`

     ([Static](settings.html#static-cluster-setting), string) The network address at which the node can be contacted by other nodes. Accepts an IP address, a hostname, or a [special value](modules-network.html#network-interface-values "Special values for network addresses"). Defaults to the address given by `transport.host` or `network.publish_host`. Use this setting only if you require to bind to multiple addresses or to use different addresses for publishing and binding, and you also require different binding configurations for the transport and HTTP interfaces. 
`transport.publish_port`

     ([Static](settings.html#static-cluster-setting), integer) The port of the [transport publish address](modules-network.html#modules-network-binding-publishing "Binding and publishing"). Set this parameter only if you need the publish port to be different from `transport.port`. Defaults to the port assigned via `transport.port`. 
`transport.connect_timeout`

     ([Static](settings.html#static-cluster-setting), [time value](api-conventions.html#time-units "Time units")) The connect timeout for initiating a new connection (in time setting format). Defaults to `30s`. 
`transport.compress`

     ([Static](settings.html#static-cluster-setting), string) Set to `true`, `indexing_data`, or `false` to configure transport compression between nodes. The option `true` will compress all data. The option `indexing_data` will compress only the raw index data sent between nodes during ingest, ccr following (excluding bootstrap), and operations based shard recovery (excluding transferring lucene files). Defaults to `indexing_data`. 
`transport.compression_scheme`

     ([Static](settings.html#static-cluster-setting), string) Configures the compression scheme for `transport.compress`. The options are `deflate` or `lz4`. If `lz4` is configured and the remote node has not been upgraded to a version supporting `lz4`, the traffic will be sent uncompressed. Defaults to `lz4`. 
`transport.tcp.keep_alive`

     ([Static](settings.html#static-cluster-setting), boolean) Configures the `SO_KEEPALIVE` option for transport sockets, which determines whether they send TCP keepalive probes. Defaults to `network.tcp.keep_alive`. 
`transport.tcp.keep_idle`

     ([Static](settings.html#static-cluster-setting), integer) Configures the `TCP_KEEPIDLE` option for transport sockets, which determines the time in seconds that a connection must be idle before starting to send TCP keepalive probes. Defaults to `network.tcp.keep_idle` if set, or the system default otherwise. This value cannot exceed `300` seconds. In cases where the system default is higher than `300`, the value is automatically lowered to `300`. Only applicable on Linux and macOS. 
`transport.tcp.keep_interval`

     ([Static](settings.html#static-cluster-setting), integer) Configures the `TCP_KEEPINTVL` option for transport sockets, which determines the time in seconds between sending TCP keepalive probes. Defaults to `network.tcp.keep_interval` if set, or the system default otherwise. This value cannot exceed `300` seconds. In cases where the system default is higher than `300`, the value is automatically lowered to `300`. Only applicable on Linux and macOS. 
`transport.tcp.keep_count`

     ([Static](settings.html#static-cluster-setting), integer) Configures the `TCP_KEEPCNT` option for transport sockets, which determines the number of unacknowledged TCP keepalive probes that may be sent on a connection before it is dropped. Defaults to `network.tcp.keep_count` if set, or the system default otherwise. Only applicable on Linux and macOS. 
`transport.tcp.no_delay`

     ([Static](settings.html#static-cluster-setting), boolean) Configures the `TCP_NODELAY` option on transport sockets, which determines whether [TCP no delay](https://en.wikipedia.org/wiki/Nagle%27s_algorithm) is enabled. Defaults to `true`. 
`transport.tcp.reuse_address`

     ([Static](settings.html#static-cluster-setting), boolean) Configures the `SO_REUSEADDR` option for network sockets, which determines whether the address can be reused or not. Defaults to `network.tcp.reuse_address`. 
`transport.tcp.send_buffer_size`

     ([Static](settings.html#static-cluster-setting), [byte value](api-conventions.html#byte-units "Byte size units")) The size of the TCP send buffer for transport traffic. Defaults to `network.tcp.send_buffer_size`. 
`transport.tcp.receive_buffer_size`

     ([Static](settings.html#static-cluster-setting), [byte value](api-conventions.html#byte-units "Byte size units")) The size of the TCP receive buffer for transport traffic. Defaults to `network.tcp.receive_buffer_size`. 
`transport.ping_schedule`

     ([Static](settings.html#static-cluster-setting), [time value](api-conventions.html#time-units "Time units")) Configures the time between sending application-level pings on all transport connections to promptly detect when a transport connection has failed. Defaults to `-1` meaning that application-level pings are not sent. You should use TCP keepalives (see `transport.tcp.keep_alive`) instead of application-level pings wherever possible. 

#### 传输配置文件

Elasticsearch 允许您通过使用传输配置文件绑定到不同接口上的多个端口。请参阅此示例配置

    
    
    transport.profiles.default.port: 9300-9400
    transport.profiles.default.bind_host: 10.0.0.1
    transport.profiles.client.port: 9500-9600
    transport.profiles.client.bind_host: 192.168.0.1
    transport.profiles.dmz.port: 9700-9800
    transport.profiles.dmz.bind_host: 172.16.1.2

"默认"配置文件很特殊。它用作任何其他配置文件的回退(如果这些配置文件没有设置特定的配置设置)，以及此节点连接到群集中其他节点的方式。其他配置文件可以具有任何名称，并可用于为传入连接设置特定终结点。

可以在每个传输配置文件上配置以下参数，如上例所示：

* "端口"：要绑定到的端口。  * "bind_host"：要绑定到的主机。  * "publish_host"：在信息性 API 中发布的主机。

配置文件还支持传输设置部分中指定的所有其他传输设置，并将这些设置用作默认值。例如，可以显式配置"transport.profiles.client.tcp.reuse_address"，否则默认配置为"transport.tcp.reuse_address"。

#### 长期空闲连接

两个节点之间的传输连接由许多长期存在的 TCP 连接组成，其中一些连接可能会长时间处于空闲状态。尽管如此，Elasticsearch 要求这些连接保持打开状态，如果任何节点间连接被外部影响(如防火墙)关闭，它可能会中断集群的运行。配置网络以保留 Elasticsearch 节点之间的长期空闲连接非常重要，例如，启用"*.tcp.keep_alive"并确保保持连接间隔短于可能导致空闲连接关闭的任何超时，或者如果无法配置激活，则设置"transport.ping_schedule"。在达到一定年龄时断开连接的设备是 Elasticsearch 集群常见的问题来源，不得使用。

#### 请求压缩

默认的"transport.compress"配置选项"indexing_data"将仅压缩与节点之间原始索引源数据传输相关的请求。此选项主要压缩在摄取、ccr 和分片恢复期间发送的数据。此默认值通常对本地群集通信有意义，因为压缩原始文档往往会显著降低节点间网络使用量，同时将 CPU 影响降至最低。

"transport.compress"设置始终配置本地群集请求压缩，并且是远程群集请求压缩的回退设置。如果要以不同于本地请求压缩的方式配置远程请求压缩，则可以使用"cluster.remote.${cluster_alias}.transport.compress"设置在每个远程群集的基础上进行设置。

#### 响应压缩

压缩设置不配置响应的压缩。如果入站请求被压缩，Elasticsearch 将压缩响应 - 即使未启用压缩也是如此。同样，如果入站请求未压缩，Elasticsearch 也不会压缩响应 - 即使启用了压缩也是如此。用于压缩响应的压缩方案与用于压缩请求的远程节点的方案相同。

### 请求跟踪

您可以跟踪在 HTTP 和传输层上发出的单个请求。

跟踪可能会生成极高的日志量，从而破坏集群的稳定性。不要在繁忙或重要的集群上启用请求跟踪。

#### REST 请求跟踪器

HTTP 层有一个专用的跟踪器，用于记录传入请求和相应的传出响应。通过将"org.elasticsearch.http.HttpTracer"记录器的级别设置为"TRACE"来激活跟踪器：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "logger.org.elasticsearch.http.HttpTracer": 'TRACE'
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
       "persistent" : {
          "logger.org.elasticsearch.http.HttpTracer" : "TRACE"
       }
    }

您还可以使用一组包含和排除通配符模式来控制将跟踪哪些 URI。默认情况下，将跟踪每个请求。

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "http.tracer.include": '*',
          "http.tracer.exclude": ''
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
       "persistent" : {
          "http.tracer.include" : "*",
          "http.tracer.exclude" : ""
       }
    }

默认情况下，跟踪器记录与这些筛选器匹配的每个请求和响应的摘要。要记录每个请求和响应的正文，请将系统属性"es.insecure_network_trace_enabled"设置为"true"，然后将"org.elasticsearch.http.HttpTracer"和"org.elasticsearch.http.HttpBodyTracer"记录器的级别设置为"TRACE"：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "logger.org.elasticsearch.http.HttpTracer": 'TRACE',
          "logger.org.elasticsearch.http.HttpBodyTracer": 'TRACE'
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
       "persistent" : {
          "logger.org.elasticsearch.http.HttpTracer" : "TRACE",
          "logger.org.elasticsearch.http.HttpBodyTracer" : "TRACE"
       }
    }

每个消息正文都经过压缩、编码并拆分为块以避免截断：

    
    
    [TRACE][o.e.h.HttpBodyTracer     ] [master] [276] response body [part 1]: H4sIAAAAAAAA/9...
    [TRACE][o.e.h.HttpBodyTracer     ] [master] [276] response body [part 2]: 2oJ93QyYLWWhcD...
    [TRACE][o.e.h.HttpBodyTracer     ] [master] [276] response body (gzip compressed, base64-encoded, and split into 2 parts on preceding log lines)

每个区块都使用内部请求 ID(在本例中为"[276]")进行批注，您应该使用该 ID 将区块与相应的摘要行相关联。要重建输出，base64-解码数据并使用"gzip"解压缩它。例如，在类Unix系统上：

    
    
    cat httptrace.log | sed -e 's/.*://' | base64 --decode | gzip --decompress

HTTP 请求和响应正文可能包含凭据和密钥等敏感信息，因此默认情况下禁用 HTTP 正文跟踪。您必须通过将系统属性"es.insecure_network_trace_enabled"设置为"true"在每个节点上显式启用它。此功能主要用于不包含任何敏感信息的测试系统。如果在包含敏感信息的系统上设置此属性，则必须保护日志免受未经授权的访问。

#### 传输跟踪器

传输层有一个专用的跟踪器，用于记录传入和传出的请求和响应。通过将"org.elasticsearch.transport.TransportService.tracer"记录器的级别设置为"TRACE"来激活跟踪器：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "logger.org.elasticsearch.transport.TransportService.tracer": 'TRACE'
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
       "persistent" : {
          "logger.org.elasticsearch.transport.TransportService.tracer" : "TRACE"
       }
    }

您还可以使用一组包含和排除通配符模式来控制将跟踪哪些操作。默认情况下，将跟踪每个请求，但故障检测 ping 除外：

    
    
    response = client.cluster.put_settings(
      body: {
        persistent: {
          "transport.tracer.include": '*',
          "transport.tracer.exclude": 'internal:coordination/fault_detection/*'
        }
      }
    )
    puts response
    
    
    PUT _cluster/settings
    {
       "persistent" : {
          "transport.tracer.include" : "*",
          "transport.tracer.exclude" : "internal:coordination/fault_detection/*"
       }
    }

### 网络线程模型

本节介绍网络子系统在 Elasticsearch 中使用的线程模型。此信息不是使用 Elasticsearch 所必需的，但对于诊断集群中的网络问题的高级用户可能很有用。

Elasticsearch节点通过一组TCP通道进行通信，这些通道共同形成传输连接。Elasticsearch 客户端通过 HTTP 与集群通信，集群也使用一个或多个 TCP 通道。这些TCP通道中的每一个都由节点中的一个"transport_worker"线程拥有。此拥有线程在通道打开时选择，并在通道的生存期内保持不变。

每个"transport_worker"线程全权负责通过其拥有的通道发送和接收数据。此外，每个 http 和传输服务器套接字都分配给其中一个"transport_worker"线程。该工作线程负责接受到其拥有的服务器套接字的新传入连接。

如果 Elasticsearch 中的线程想要通过特定通道发送数据，它会将数据传递给拥有的"transport_worker"线程进行实际传输。

通常，"transport_worker"线程不会完全处理它们收到的消息。相反，他们将进行少量的初步处理，然后将消息分派(移交)到不同的线程池以进行其余处理。例如，批量消息被调度到"write"线程池，搜索被调度到"搜索"线程池之一，并且对统计信息和其他管理任务的请求主要被调度到"管理"线程池。然而，在某些情况下，消息的处理预计会非常快，以至于 Elasticsearch 将在"transport_worker"线程上完成所有处理，而不是产生将其调度到其他地方的开销。

默认情况下，每个 CPU 有一个"transport_worker"线程。相比之下，有时可能有数万个TCP通道。如果数据到达 TCPchannel 并且其所属的"transport_worker"线程繁忙，则在线程完成它正在执行的任何操作之前，不会处理数据。同样，在拥有的"transport_worker"线程空闲之前，传出数据不会通过通道发送。这意味着我们要求每个"transport_worker"线程经常处于空闲状态。空闲的"transport_worker"在堆栈转储中如下所示：

    
    
    "elasticsearch[instance-0000000004][transport_worker][T#1]" #32 daemon prio=5 os_prio=0 cpu=9645.94ms elapsed=501.63s tid=0x00007fb83b6307f0 nid=0x1c4 runnable  [0x00007fb7b8ffe000]
       java.lang.Thread.State: RUNNABLE
    	at sun.nio.ch.EPoll.wait(java.base@17.0.2/Native Method)
    	at sun.nio.ch.EPollSelectorImpl.doSelect(java.base@17.0.2/EPollSelectorImpl.java:118)
    	at sun.nio.ch.SelectorImpl.lockAndDoSelect(java.base@17.0.2/SelectorImpl.java:129)
    	- locked <0x00000000c443c518> (a sun.nio.ch.Util$2)
    	- locked <0x00000000c38f7700> (a sun.nio.ch.EPollSelectorImpl)
    	at sun.nio.ch.SelectorImpl.select(java.base@17.0.2/SelectorImpl.java:146)
    	at io.netty.channel.nio.NioEventLoop.select(NioEventLoop.java:813)
    	at io.netty.channel.nio.NioEventLoop.run(NioEventLoop.java:460)
    	at io.netty.util.concurrent.SingleThreadEventExecutor$4.run(SingleThreadEventExecutor.java:986)
    	at io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74)
    	at java.lang.Thread.run(java.base@17.0.2/Thread.java:833)

在节点热线程 API 中，空闲的"transport_worker"线程报告如下：

    
    
       0.0% [cpu=0.0%, idle=100.0%] (500ms out of 500ms) cpu usage by thread 'elasticsearch[instance-0000000004][transport_worker][T#1]'
         10/10 snapshots sharing following 9 elements
           java.base@17.0.2/sun.nio.ch.EPoll.wait(Native Method)
           java.base@17.0.2/sun.nio.ch.EPollSelectorImpl.doSelect(EPollSelectorImpl.java:118)
           java.base@17.0.2/sun.nio.ch.SelectorImpl.lockAndDoSelect(SelectorImpl.java:129)
           java.base@17.0.2/sun.nio.ch.SelectorImpl.select(SelectorImpl.java:146)
           io.netty.channel.nio.NioEventLoop.select(NioEventLoop.java:813)
           io.netty.channel.nio.NioEventLoop.run(NioEventLoop.java:460)
           io.netty.util.concurrent.SingleThreadEventExecutor$4.run(SingleThreadEventExecutor.java:986)
           io.netty.util.internal.ThreadExecutorMap$2.run(ThreadExecutorMap.java:74)
           java.base@17.0.2/java.lang.Thread.run(Thread.java:833)

请注意，"transport_worker"线程应始终处于"RUNNABLE"状态，即使在等待输入时也是如此，因为它们在本机"EPoll#wait"方法中阻塞。"idle="时间报告线程等待输入所花费的时间比例，而"cpu="时间报告线程处理其接收的输入所花费的时间比例。

如果"transport_worker"线程不经常空闲，则可能会积压工作。这可能会导致在其拥有的通道上处理消息时出现延迟。很难准确预测哪些工作会被推迟：

* 通道比线程多得多。如果与一个通道相关的工作导致其工作线程延迟，则该线程拥有的所有其他通道也将遭受延迟。  * 从 TCP 通道到工作线程的映射是固定的，但任意的。打开通道时，以循环方式为每个通道分配一个所属线程。每个工作线程负责许多不同类型的通道。  * 每对节点之间有许多通道开放。对于每个请求，Elasticsearch 将以循环方式从适当的通道中进行选择。某些请求最终可能会在延迟工作线程拥有的通道上，而其他相同的请求将在运行平稳的通道上发送。

如果积压工作积累得太远，某些消息可能会延迟数秒。该节点甚至可能无法通过其运行状况检查并从集群中删除。有时，您可以使用 Nodes 热线程 API 找到繁忙的"transport_worker"线程的证据。但是，此 API 本身会发送网络消息，因此如果"transport_worker"线程太忙，则可能无法正常工作。使用"jstack"获取堆栈转储或使用 Java Flight Recorder 获取分析跟踪更可靠。这些工具独立于 JVM 正在执行的任何工作。

[« Node](modules-node.md) [Node query cache settings »](query-cache.md)
