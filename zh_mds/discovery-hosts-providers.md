

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Discovery and cluster formation](modules-
discovery.md)

[« Discovery and cluster formation](modules-discovery.md) [Quorum-based
decision making »](modules-discovery-quorums.md)

##Discovery

发现是集群形成模块找到其他节点以形成集群的过程。当您启动 Elasticsearch 节点或节点认为主节点发生故障时，此过程将运行，并一直持续到找到主节点或选择新的主节点为止。

此过程从来自一个或多个 seedhosts 提供程序的 _seed_ 地址列表以及最后一个已知集群中任何符合主节点条件的地址开始。该过程分两个阶段运行：首先，每个节点通过连接到每个地址并尝试识别其连接到的节点并验证其是否符合主节点资格来探测种子地址。其次，如果成功，它将与其所有已知的符合主节点条件的对等节点共享，并且远程节点依次使用 _its_ 对等节点进行响应。然后，节点探测它刚刚发现的所有新节点，请求其对等节点，依此类推。

如果节点不符合主节点条件，则它将继续此发现过程，直到发现选定的主节点。如果未发现选定的主节点，则节点将在"discovery.find_peers_interval"(默认为"1s")之后重试。

如果节点符合主节点条件，则它将继续此发现过程，直到它发现了选定的主节点，或者它发现了足够多的无主节点，以完成选择。如果这两种情况都发生得不够快，则节点将在默认为"1s"的"discovery.find_peers_interval"之后重试。

一旦选出了主人，它通常会保持当选的主人的身份，直到被故意停止为止。如果故障检测确定集群有故障，它也可能会停止充当主集群。当节点不再是选定的主节点时，它将再次开始发现过程。

有关发现问题疑难解答，请参阅发现疑难解答。

### 种子主机提供程序

默认情况下，集群形成模块提供两个种子主机提供程序来配置种子节点列表：基于 _settings_ 的种子主机提供程序和基于 _file_ 的种子主机提供程序。它可以通过发现插件扩展以支持云环境和其他形式的种子主机提供程序。种子主机提供程序使用"discovery.seed_providers"设置进行配置，该设置默认为基于 _settings_ 的主机提供程序。此设置接受不同提供程序的列表，允许您使用多种方式为群集查找这些主机。

每个种子主机提供程序生成种子节点的 IP 地址或主机名。如果它返回任何主机名，则使用 DNS 查找将这些主机名解析为 IP 地址。如果主机名解析为多个 IP 地址，则 Elasticsearch 会尝试在所有这些地址上查找种子节点。如果主机提供程序到那时没有明确提供节点的TCP端口，它将隐式使用'transport.profiles.default.port'给出的端口范围内的第一个端口，或者如果未设置'transport.profiles.default.port'，则通过'transport.port'。由"discovery.seed_resolver.max_concurrent_resolvers"控制的并发查找数(默认为"10")，每次查找的超时由默认值为"5s"的"discovery.seed_resolver.timeout"控制。请注意，DNS查找受 JVM DNS 缓存的约束。

##### 基于设置的种子主机提供程序

基于设置的种子主机提供程序使用节点设置来配置种子节点地址的非静态列表。这些地址可以作为主机名或 IP 地址提供;指定为主机名的主机在每一轮发现期间都会解析为 IP 地址。

主机列表使用"discovery.seed_hosts"静态设置进行设置。例如：

    
    
    discovery.seed_hosts:
       - 192.168.1.10:9300
       - 192.168.1.11 __- seeds.mydomain.com __

__

|

端口将默认为"transport.profiles.default.port"，如果未指定，则回退到"transport.port"。   ---|---    __

|

如果主机名解析为多个 IP 地址，Elasticsearch 将尝试连接到每个解析的地址。   ##### 基于文件的种子主机提供程序编辑

基于文件的种子主机提供程序通过外部文件配置主机列表。Elasticsearch 在更改此文件时会重新加载该文件，以便种子节点列表可以动态更改，而无需重新启动每个节点。例如，这为在 Docker 容器中运行的 Elasticsearch 实例提供了一种方便的机制，当这些 IP 地址在节点启动时可能未知时，可以动态提供要连接的 IP 地址列表。

要启用基于文件的发现，请在"elasticsearch.yml"文件中按如下方式配置"file"主机提供程序：

    
    
    discovery.seed_providers: file

然后在"$ES_PATH_CONF/unicast_hosts.txt"创建一个文件，格式如下所述。每当对"unicast_hosts.txt"文件进行更改时，Elasticsearch 都会选取新的更改，并使用新的主机列表。

请注意，基于文件的发现插件增强了"elasticsearch.yml"中的单播主机列表：如果"discovery.seed_hosts"中有有效的种子地址，则Elasticsearch除了使用"unicast_hosts.txt"中提供的地址外，还会使用这些地址。

"unicast_hosts.txt"文件每行包含一个节点条目。每个节点条目由主机(主机名或 IP 地址)和可选的传输端口号组成。如果指定了端口号，则必须紧跟在主机之后(在同一行上)，用"："分隔。如果未指定端口号，Elasticsearch 将隐式使用端口范围中的第一个端口，由 'transport.profiles.default.port' 给出，如果未设置"transport.profiles.default.port"，则由 'transport.port' 指定。

例如，对于具有参与发现的四个节点的集群，下面是一个"unicast_hosts.txt"示例，其中一些节点不在默认端口上运行：

    
    
    10.10.10.5
    10.10.10.6:9305
    10.10.10.5:10005
    # an IPv6 address
    [2001:0db8:85a3:0000:0000:8a2e:0370:7334]:9301

允许主机名而不是 IP 地址，并且如上所述由 DNS 解析。IPv6 地址必须在括号中给出，如果需要，端口位于括号之后。

您还可以向此文件添加注释。所有注释必须出现在以"#"开头的行上(即注释不能从一行中间开始)。

##### EC2 主机提供商

EC2 发现插件添加了一个主机提供程序，该提供程序使用 AWSAPI 查找种子节点列表。

##### Azure Classic hostsprovider

Azure Classic discoveryplugin addsa 主机提供程序使用 Azure Classic API 查找种子节点列表。

##### Google Compute Engine hostsprovider

GCE 发现插件添加了一个主机提供程序，该提供程序使用 GCE API 查找种子节点列表。

[« Discovery and cluster formation](modules-discovery.md) [Quorum-based
decision making »](modules-discovery-quorums.md)
