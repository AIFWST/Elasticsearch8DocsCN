

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md)

[« Elasticsearch security principles](es-security-principles.md) [Manually
configure security »](manually-configure-security.md)

## 在自动启用安全性的情况下启动弹性堆栈

首次启动 Elasticsearch 时，会自动进行以下安全配置：

* TLS 的证书和密钥是为传输层和 HTTP 层生成的。  * TLS 配置设置将写入 'elasticsearch.yml'。  * 为"弹性"用户生成密码。  * 将为 Kibana 生成注册令牌。

然后，您可以启动 Kibana 并输入注册令牌，该令牌的有效期为 30 分钟。此令牌会自动应用来自 Elasticsearch 集群的安全设置，使用内置的"kibana"服务帐户向 Elasticsearch 进行身份验证，并将安全配置写入"kibana.yml"。

在某些情况下，无法自动配置安全性，因为节点启动过程检测到节点已是群集的一部分，或者安全性已配置或显式禁用。

###Prerequisites

* 下载并解压缩适用于您环境的"elasticsearch"软件包发行版。  * 下载并解压缩适用于您环境的"kibana"软件包发行版。

### 启动 Elasticsearch 并在启用安全性的情况下注册 Kibana

1. 从安装目录中，启动 Elasticsearch。将为"弹性"用户生成一个密码并输出到终端，以及用于注册 Kibana 的注册令牌。           bin/elasticsearch

您可能需要在终端中向后滚动一点才能查看密码和注册令牌。

2. 复制生成的密码和注册令牌，并将其保存在安全的位置。这些值仅在您第一次启动 Elasticsearch 时显示。

如果您需要重置"弹性"用户或其他内置用户的密码，请运行"弹性搜索重置密码"工具。要为 Kibana 或 Elasticsearch 节点生成新的注册令牌，请运行"elasticsearch-create-enrollment-token"工具。这些工具可以在 Elasticsearch 'bin' 目录中找到。

3. (可选)打开一个新终端，并验证您是否可以通过进行经过身份验证的调用来连接到您的 Elasticsearch 集群。出现提示时，输入"弹性"用户的密码：curl --cacert config/certs/http_ca.crt -u 弹性 https://localhost:9200

4. 从安装 Kibana 的目录中，启动 Kibana。           宾/木花

5. 使用交互模式或分离模式注册 Kibana。

    * **Interactive mode** (browser)

      1. In your terminal, click the generated link to open Kibana in your browser. 
      2. In your browser, paste the enrollment token that you copied and click the button to connect your Kibana instance with Elasticsearch.

如果 Kibana 检测到 Elasticsearch 的现有凭据("elasticsearch.username"和"elasticsearch.password")或"elasticsearch.hosts"的现有 URL，则不会进入交互模式。

    * **Detached mode** (non-browser)

运行"kibana-setup"工具，并使用"--注册令牌"参数传递生成的注册令牌。

        
                bin/kibana-setup --enrollment-token <enrollment-token>

### 在群集中注册其他节点

当 Elasticsearch 首次启动时，安全自动配置过程会将 HTTP 层绑定到 '0.0.0.0'，但只将传输层绑定到 localhost。此预期行为可确保您可以在默认情况下启用安全性的情况下启动单节点群集，而无需任何其他配置。

在注册新节点之前，在生产集群中通常需要执行其他操作，例如绑定到地址而不是"localhost"或满足引导程序检查。在此期间，自动生成的注册令牌可能会过期，这就是不会自动生成注册令牌的原因。

此外，只有同一主机上的节点才能加入群集，而无需其他配置。如果您希望来自其他主机的节点加入您的集群，则需要将"transport.host"设置为支持的值(例如取消注释建议值"0.0.0.0")，或者绑定到其他主机可以访问的接口的 IP 地址。有关详细信息，请参阅传输设置。

要在群集中注册新节点，请在群集中的任何现有节点上使用"弹性搜索-创建-注册令牌"工具创建注册令牌。然后，您可以使用"--enrollment-token"参数启动新节点，以便它加入现有集群。

1. 在运行 Elasticsearch 的单独终端中，导航到安装 Elasticsearch 的目录，然后运行"elasticsearch-create-enrollment-token"工具，为您的新节点生成注册令牌。           bin/elasticsearch-create-enrollment-token -s 节点

复制注册令牌，您将使用该令牌向 Elasticsearch 集群注册新节点。

2. 在新节点的安装目录中，启动 Elasticsearch 并使用"--enrollment-token"参数传递注册令牌。           bin/elasticsearch --enrollment-token <enrollment-token>

Elasticsearch 会在以下目录中自动生成证书和密钥：

    
        config/certs

3. 对要注册的任何新节点重复上一步。

### 将客户端连接到弹性搜索

当您第一次启动 Elasticsearch 时，TLS 会自动为 HTTP 层配置。CA 证书生成并存储在磁盘上：

    
    
    /etc/elasticsearch/certs/http_ca.crt

此证书的十六进制编码 SHA-256 指纹也会输出到终端。任何连接到 Elasticsearch 的客户端，例如 Elasticsearch Client、Beats、Independent Elastic Agents 和 Logstash，都必须验证它们是否信任 Elasticsearch 用于 HTTPS 的证书。队列服务器和队列管理的弹性代理会自动配置为信任 CA 证书。其他客户端可以使用 CA 证书的指纹或 CA 证书本身来建立信任。

如果自动配置过程已经完成，您仍然可以获取安全证书的指纹。您还可以将 CA 证书复制到您的计算机，并将客户端配置为使用它。

#### 使用 CA 指纹

复制 Elasticsearch 启动时输出到终端的指纹值，并将客户端配置为在连接到 Elasticsearch 时使用此指纹建立信任。

如果自动配置过程已经完成，您仍可以通过运行以下命令获取安全证书的指纹。路径是 HTTP 层自动生成的 CA 证书的路径。

    
    
    openssl x509 -fingerprint -sha256 -in config/certs/http_ca.crt

该命令返回安全证书，包括指纹。"颁发者"应该是"Elasticsearch security auto-configuration HTTP CA"。

    
    
    issuer= /CN=Elasticsearch security auto-configuration HTTP CA
    SHA256 Fingerprint=<fingerprint>

#### 使用 CA 证书

如果您的库不支持验证指纹的方法，则会在每个 Elasticsearch 节点上的以下目录中创建自动生成的 CA 证书：

    
    
    /etc/elasticsearch/certs/http_ca.crt

将"http_ca.crt"文件复制到您的计算机，并将客户端配置为在连接到 Elasticsearch 时使用此证书建立信任。

### 下一步是什么？

祝贺！您已成功启动启用了安全性的弹性堆栈。Elasticsearch 和 Kibana 在 HTTP 层使用 TLS 进行保护，并且节点间通信是加密的。如果要为网络流量启用 HTTPS，可以加密浏览器和 Kibana 之间的流量。

### 安全证书和密钥

安装 Elasticsearch 时，会在 Elasticsearch 配置目录中生成以下证书和密钥，用于将 Kibana 实例连接到安全的 Elasticsearch 集群并加密节点间通信。此处列出了这些文件以供参考。

`http_ca.crt`

     The CA certificate that is used to sign the certificates for the HTTP layer of this Elasticsearch cluster. 
`http.p12`

     Keystore that contains the key and certificate for the HTTP layer for this node. 
`transport.p12`

     Keystore that contains the key and certificate for the transport layer for all the nodes in your cluster. 

'http.p12' 和 'transport.p12' 是受密码保护的 PKCS#12 密钥库。Elasticsearch 将这些密钥库的密码存储为 securesettings。要检索密码以便检查或更改密钥库内容，请使用"bin/elasticsearch-keystore"工具。

使用以下命令检索"http.p12"的密码：

    
    
    bin/elasticsearch-keystore show xpack.security.http.ssl.keystore.secure_password

使用以下命令检索"transport.p12"的密码：

    
    
    bin/elasticsearch-keystore show xpack.security.transport.ssl.keystore.secure_password

此外，当您使用注册令牌将 Kibana 连接到安全的 Elasticsearch 集群时，将从 Elasticsearch 检索 HTTP 层 CA 证书，并将其存储在 Kibana '/data' 目录中。此文件在 Kibana 和 Elasticsearch Certificate Authority(CA) 之间建立 HTTP 层的信任。

### 跳过安全自动配置的情况

首次启动 Elasticsearch 时，节点启动过程会尝试自动为您配置安全性。该过程运行一些检查以确定：

* 如果这是节点第一次启动 * 是否已配置安全性 * 如果启动过程可以修改节点配置

如果这些检查中的任何一项失败，则表明您手动配置了安全性，或者不希望自动配置安全性。在这些情况下，节点使用现有配置正常启动。

如果将 Elasticsearch 输出重定向到文件，则会跳过安全性自动配置。自动配置的凭证只能在您第一次启动 Elasticsearch 时在终端上查看。如果需要将输出重定向到文件，请在第一次启动 Elasticsearch 而不进行重定向，并在所有后续启动时使用重定向。

#### 检测到现有环境

如果某些目录已经存在，则强烈表明该节点以前已启动。同样，如果某些文件_don t_存在，或者我们无法读取或写入特定文件或目录，那么我们可能不会以安装 Elasticsearch 的用户或管理员施加的限制身份运行。如果以下任何环境检查为真，则不会自动配置安全性。

Elasticsearch '/data' 目录存在且不为空

     The existence of this directory is a strong indicator that the node was started previously, and might already be part of a cluster. 
The `elasticsearch.yml` file doesn't exist (or isn't readable), or the
`elasticsearch.keystore` isn't readable

     If either of these files aren't readable, we can't determine whether Elasticsearch security features are already enabled. This state can also indicate that the node startup process isn't running as a user with sufficient privileges to modify the node configuration. 
The Elasticsearch configuration directory isn't writable

     This state likely indicates that an administrator made this directory read-only, or that the user who is starting Elasticsearch is not the user that installed Elasticsearch. 

#### 检测到现有设置

以下设置与安全自动配置不兼容。如果存在这些设置中的任何一个，节点启动过程将自动跳过配置安全性，节点将正常启动。

* "node.roles"设置为节点不能被选为"master"的值，或者节点无法保存数据 * "xpack.security.autoconfiguration.enabled"设置为"false" * "xpack.security.enabled"设置了一个值 * 任何"xpack.security.transport.ssl.*"或"xpack.security.http.ssl.*"设置都有一个值在"elasticsearch.yml"配置文件或"elasticsearch.keystore"中设置的值 * 任何"discovery.type"，"discovery.seed_hosts"， 或"cluster.initial_master_nodes"发现和集群形成设置具有值集

例外情况是当"discovery.type"设置为"单节点"时，或者当"cluster.initial_master_nodes"存在但仅包含当前节点的名称时。

[« Elasticsearch security principles](es-security-principles.md) [Manually
configure security »](manually-configure-security.md)
