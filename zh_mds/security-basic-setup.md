

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Manually configure security](manually-
configure-security.md)

[« Set up minimal security for Elasticsearch](security-minimal-setup.md)
[Set up basic security for the Elastic Stack plus secured HTTPS traffic
»](security-basic-setup-https.md)

## 为 ElasticStack 设置基本安全性

当您第一次启动 Elasticsearch 时，系统会为"弹性"用户生成密码，并自动为您配置 TLS。如果您在启动 Elasticsearch 节点之前手动配置安全性，则自动配置过程将遵循您的安全配置。您可以随时调整 TLS 配置，例如更新节点证书。

如果群集有多个节点，则必须在节点之间配置 TLS。如果不启用 TLS，生产模式群集将不会启动。

传输层依赖于双向 TLS 进行节点的加密和身份验证。正确应用 TLS 可确保恶意节点无法加入群集并与其他节点交换数据。虽然在 HTTP 层实现用户名和密码身份验证对于保护本地群集很有用，但节点之间通信的安全性需要 TLS。

在节点之间配置 TLS 是防止未经授权的节点访问群集的基本安全设置。

**了解传输上下文**

传输层安全性 (TLS) 是用于将安全控制(如加密)应用于网络通信的行业标准协议的名称。TLS 是过去称为安全套接字层 (SSL) 的现代名称。Elasticsearch 文档可以互换使用术语 TLS 和 SSL。

传输协议是 Elasticsearch 节点用来相互通信的协议的名称。此名称特定于 Elasticsearch，用于区分传输端口(默认为"9300")和 HTTP 端口(默认为"9200")。节点使用传输端口相互通信，REST客户端使用 HTTP 端口与 Elasticsearch 通信。

尽管单词 _transport_ 出现在两种上下文中，但它们的含义不同。可以将TLS应用于Elasticsearch传输端口和HTTP端口。我们知道这些重叠的术语可能会令人困惑，因此需要澄清的是，在这种情况下，我们将TLS应用于Elasticsearch传输端口。在下一个场景中，我们将 TLS 应用于 Elasticsearch HTTP 端口。

### 生成证书颁发机构

您可以在群集中添加任意数量的节点，但它们必须能够相互通信。集群中节点之间的通信由传输模块处理。要保护您的集群，您必须确保节点间通信经过加密和验证，这是通过双向 TLS 实现的。

在安全的集群中，Elasticsearch 节点在与其他节点通信时使用证书来识别自己。

群集必须验证这些证书的真实性。建议的方法是信任特定的证书颁发机构 (CA)。将节点添加到群集时，它们必须使用由 sameCA 签名的证书。

对于传输层，我们建议使用单独的专用 CA，而不是现有的、可能共享的 CA，以便严格控制节点成员身份。使用"elasticsearch-certutil"工具为您的集群生成 CA。

1. 在启动 Elasticsearch 之前，请在任何单个节点上使用"elasticsearch-certutil"工具为您的集群生成 CA。           ./bin/elasticsearch-certutil ca

    1. When prompted, accept the default file name, which is `elastic-stack-ca.p12`. This file contains the public certificate for your CA and the private key used to sign certificates for each node. 
    2. Enter a password for your CA. You can choose to leave the password blank if you're not deploying to a production environment. 

2. 在任何单个节点上，为群集中的节点生成证书和私钥。您可以包括在上一步中生成的"弹性堆栈-ca.p12"输出文件。           ./bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12

'--<ca_file>ca '

    

用于签署证书的 CA 文件的名称。"elasticsearch-certutil"工具的默认文件名是"elastic-stack-ca.p12"。

    1. Enter the password for your CA, or press **Enter** if you did not configure one in the previous step. 
    2. Create a password for the certificate and accept the default file name.

输出文件是名为"弹性证书.p12"的密钥库。此文件包含节点证书、节点密钥和 CA 证书。

3. 在群集中的每个节点上，将"弹性证书.p12"文件复制到"$ES_PATH_CONF"目录。

### 使用 TLS 加密节点间通信

传输网络层用于集群中节点之间的内部通信。启用安全功能后，必须使用 TLS 来确保节点之间的通信已加密。

生成证书颁发机构和证书后，您将更新集群以使用这些文件。

Elasticsearch 监控所有文件，例如配置为 TLS 相关节点设置值的证书、密钥、密钥库或信任库。如果您更新了其中任何一个文件，例如当您的主机名更改或您的证书即将过期时，Elasticsearch 会重新加载它们。这些文件以全局 Elasticsearch'resource.reload.interval.high' 设置(默认为 5 秒)确定的频率轮询更改。

针对群集中的每个节点完成以下步骤。要加入同一群集，所有节点必须共享相同的"cluster.name"值。

1. 打开"$ES_PATH_CONF/elasticsearch.yml"文件并进行以下更改：

    1. Add the [`cluster-name`](important-settings.html#cluster-name "Cluster name setting") setting and enter a name for your cluster:
        
                cluster.name: my-cluster

    2. Add the [`node.name`](important-settings.html#node-name "Node name setting") setting and enter a name for the node. The node name defaults to the hostname of the machine when Elasticsearch starts.
        
                node.name: node-1

    3. Add the following settings to enable internode communication and provide access to the node's certificate.

由于您在集群中的每个节点上使用相同的"弹性证书.p12"文件，因此请将验证模式设置为"证书"：

        
                xpack.security.transport.ssl.enabled: true
        xpack.security.transport.ssl.verification_mode: certificate __xpack.security.transport.ssl.client_authentication: required
        xpack.security.transport.ssl.keystore.path: elastic-certificates.p12
        xpack.security.transport.ssl.truststore.path: elastic-certificates.p12

__

|

如果要使用主机名验证，请将验证模式设置为"完整"。应为每个主机生成与 DNS 或 IP 地址匹配的不同证书。请参阅 TLS 设置中的"xpack.security.transport.ssl.verification_mode"参数。   ---|--- 2.如果您在创建节点证书时输入了密码，请运行以下命令将密码存储在 Elasticsearch 密钥库中：./bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password ./bin/elasticsearch-keystore add xpack.security.transport.ssl.truststore.secure_password

3. 为群集中的每个节点完成前面的步骤。  4. 在集群中的每个节点上，启动 Elasticsearch。启动和停止 Elasticsearch 的方法因安装方式而异。

例如，如果您使用归档发行版('tar.gz'或'.zip')安装了 Elasticsearch，则可以在命令行中输入 'Ctrl+C' 来停止 Elasticsearch。

您必须执行完全群集重新启动。配置为使用 TLSfor 传输的节点无法与使用未加密传输连接的节点通信(反之亦然)。

### 下一步是什么？

祝贺！您已加密群集中节点之间的通信，可以通过 TLS 引导程序检查。

要添加另一层安全性，请为 Elastic Stackplus 安全 HTTPS 流量设置基本安全性。除了在 Elasticsearch 集群的传输接口上配置 TLS 之外，您还可以在 HTTP 接口上为 Elasticsearch 和 Kibana 配置 TLS。

[« Set up minimal security for Elasticsearch](security-minimal-setup.md)
[Set up basic security for the Elastic Stack plus secured HTTPS traffic
»](security-basic-setup-https.md)
