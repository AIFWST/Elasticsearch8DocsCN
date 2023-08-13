

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Installing Elasticsearch](install-
elasticsearch.md)

[« Installing Elasticsearch](install-elasticsearch.md) [Install
Elasticsearch with `.zip` on Windows »](zip-windows.md)

## 在 Linux 或 MacOS 上从存档安装 Elasticsearch

Elasticsearch作为Linux和MacOS的".tar.gz"存档提供。

此软件包包含免费和订阅功能。开始 30 天试用以试用所有功能。

Elasticsearch 的最新稳定版本可以在 DownloadElasticsearch 页面上找到。其他版本可以在"过去的版本"页面上找到。

Elasticsearch包括来自JDK维护者(GPLv2 + CE)的OpenJDK捆绑版本。要使用自己的 Java 版本，请参阅 JVM 版本要求版本")

### 下载并安装适用于 Linux 的存档

Elasticsearch v8.9.0 的 Linux 存档可以按如下方式下载和安装：

    
    
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.9.0-linux-x86_64.tar.gz
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.9.0-linux-x86_64.tar.gz.sha512
    shasum -a 512 -c elasticsearch-8.9.0-linux-x86_64.tar.gz.sha512 __tar -xzf elasticsearch-8.9.0-linux-x86_64.tar.gz
    cd elasticsearch-8.9.0/ __

__

|

比较下载的".tar.gz"存档的 SHA 和已发布的校验和，后者应输出"elasticsearch-{version}-linux-x86_64.tar.gz：OK"。   ---|---    __

|

此目录称为"$ES_HOME"。   ### 下载并安装适用于 MacOS 的存档编辑

Elasticsearch v8.9.0 的 MacOS 存档可以按如下方式下载和安装：

    
    
    curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.9.0-darwin-x86_64.tar.gz
    curl https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.9.0-darwin-x86_64.tar.gz.sha512 | shasum -a 512 -c - __tar -xzf elasticsearch-8.9.0-darwin-x86_64.tar.gz
    cd elasticsearch-8.9.0/ __

__

|

比较下载的".tar.gz"存档和已发布的校验和，后者应输出"elasticsearch-{version}-darwin-x86_64.tar.gz：OK"。   ---|---    __

|

此目录称为"$ES_HOME"。   ### 启用自动创建系统索引编辑

一些商业功能会在 Elasticsearch 中自动创建索引。默认情况下，Elasticsearch 配置为允许自动创建索引，不需要额外的步骤。但是，如果您在 Elasticsearch 中禁用了自动索引创建，则必须在 'elasticsearch.yml' 中配置"action.auto_create_index"以允许商业功能创建以下索引：

    
    
    action.auto_create_index: .monitoring*,.watches,.triggered_watches,.watcher-history*,.ml*

如果您使用的是 Logstash 或 Beats，那么您很可能需要在"action.auto_create_index"设置中使用其他索引名称，确切的值将取决于您的本地配置。如果您不确定环境的正确值，则可以考虑将该值设置为"*"，这将允许自动创建所有索引。

### 从命令行运行 Elasticsearch

运行以下命令，从命令行启动 Elasticsearch：

    
    
    ./bin/elasticsearch

首次启动 Elasticsearch 时，安全功能默认处于启用状态并进行配置。以下安全配置会自动发生：

* 启用身份验证和授权，并为"弹性"内置超级用户生成密码。  * TLS 的证书和密钥是为传输层和 HTTP 层生成的，并且使用这些密钥和证书启用和配置 TLS。  * 将为 Kibana 生成注册令牌，有效期为 30 分钟。

"弹性"用户的密码和 Kibana 的注册令牌将输出到您的终端。例如：

    
    
    The generated password for the elastic built-in superuser is:
    <password>
    
    The enrollment token for Kibana instances, valid for the next 30 minutes:
    <enrollment-token>
    
    The hex-encoded SHA-256 fingerprint of the generated HTTPS CA DER-encoded certificate:
    <fingerprint>
    
    You can complete the following actions at any time:
    Reset the password of the elastic built-in superuser with
    'bin/elasticsearch-reset-password -u elastic'.
    
    Generate an enrollment token for Kibana instances with
    'bin/elasticsearch-create-enrollment-token -s kibana'.
    
    Generate an enrollment token for Elasticsearch nodes with
    'bin/elasticsearch-create-enrollment-token -s node'.

如果您已对 Elasticsearch 密钥库进行密码保护，系统将提示您输入密钥库的密码。有关更多详细信息，请参阅安全设置。

默认情况下，Elasticsearch 将其日志打印到控制台("stdout")和日志目录中的"集群名称>.log"文件<。Elasticsearch在启动时会记录一些信息，但是在完成初始化后，它将继续在前台运行，并且不会进一步记录任何内容，直到发生值得记录的事情。当Elasticsearch运行时，你可以通过它的HTTP接口与它进行交互，该接口默认位于端口"9200"上。

要停止 Elasticsearch，请按"Ctrl-C"。

所有用Elasticsearch打包的脚本都需要一个支持数组的Bash版本，并假设Bash在'/bin/bash'中可用。因此，Bash 应该直接或通过符号链接在此路径上可用。

#### 在现有群集中注册节点

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

### 检查 Elasticsearch 是否正在运行

您可以通过向"localhost"上的端口"9200"发送HTTPS请求来测试您的Elasticsearch节点是否正在运行：

    
    
    curl --cacert $ES_HOME/config/certs/http_ca.crt -u elastic https://localhost:9200 __

__

|

确保在调用中使用"https"，否则请求将失败。

`--cacert`

     Path to the generated `http_ca.crt` certificate for the HTTP layer.   
  
---|---  
  
Enter the password for the `elastic` user that was generated during
installation, which should return a response like this:

    
    
    {
      "name" : "Cp8oag6",
      "cluster_name" : "elasticsearch",
      "cluster_uuid" : "AT69_T_DTp-1qgIJlatQqA",
      "version" : {
        "number" : "8.9.0",
        "build_type" : "tar",
        "build_hash" : "f27399d",
        "build_flavor" : "default",
        "build_date" : "2016-03-30T09:51:41.449Z",
        "build_snapshot" : false,
        "lucene_version" : "9.7.0",
        "minimum_wire_compatibility_version" : "1.2.3",
        "minimum_index_compatibility_version" : "1.2.3"
      },
      "tagline" : "You Know, for Search"
    }

可以使用命令行上的"-q"或"--quiet"选项禁用日志打印到"stdout"。

### 以 adaemon 身份运行

要将 Elasticsearch 作为守护进程运行，请在命令行上指定"-d"，并使用"-p"选项将进程 ID 记录在文件中：

    
    
    ./bin/elasticsearch -d -p pid

如果您已对 Elasticsearch 密钥库进行密码保护，系统将提示您输入密钥库的密码。有关更多详细信息，请参阅安全设置。

日志消息可以在'$ES_HOME/logs/'目录中找到。

要关闭 Elasticsearch，请终止 'pid' 文件中记录的进程 ID：

    
    
    pkill -F pid

Elasticsearch '.tar.gz' 包不包含 'systemd' 模块。要将 Elasticsearch 作为服务进行管理，请改用 Debian 或 RPM 软件包。

### 在命令行上配置 Elasticsearch

默认情况下，Elasticsearch从'$ES_HOME/config/elasticsearch.yml'文件加载其配置。此配置文件的格式在_Configuring Elasticsearch_中进行了说明。

也可以在命令行上使用"-E"语法在命令行上指定配置文件中指定的任何设置，如下所示：

    
    
    ./bin/elasticsearch -d -Ecluster.name=my_cluster -Enode.name=node_1

通常，任何集群范围的设置(如"cluster.name")都应添加到"elasticsearch.yml"配置文件中，而任何特定于节点的设置(如"node.name")都可以在命令行上指定。

### 将客户端连接到弹性搜索

当您第一次启动 Elasticsearch 时，TLS 会自动为 HTTP 层配置。CA 证书生成并存储在磁盘上：

    
    
    $ES_HOME/config/certs/http_ca.crt

此证书的十六进制编码 SHA-256 指纹也会输出到终端。任何连接到 Elasticsearch 的客户端，例如 Elasticsearch Client、Beats、Independent Elastic Agents 和 Logstash，都必须验证它们是否信任 Elasticsearch 用于 HTTPS 的证书。队列服务器和队列管理的弹性代理会自动配置为信任 CA 证书。其他客户端可以使用 CA 证书的指纹或 CA 证书本身来建立信任。

如果自动配置过程已经完成，您仍然可以获取安全证书的指纹。您还可以将 CA 证书复制到您的计算机，并将客户端配置为使用它。

##### 使用 CA 指纹

复制 Elasticsearch 启动时输出到终端的指纹值，并将客户端配置为在连接到 Elasticsearch 时使用此指纹建立信任。

如果自动配置过程已经完成，您仍可以通过运行以下命令获取安全证书的指纹。路径是 HTTP 层自动生成的 CA 证书的路径。

    
    
    openssl x509 -fingerprint -sha256 -in config/certs/http_ca.crt

该命令返回安全证书，包括指纹。"颁发者"应该是"Elasticsearch security auto-configuration HTTP CA"。

    
    
    issuer= /CN=Elasticsearch security auto-configuration HTTP CA
    SHA256 Fingerprint=<fingerprint>

##### 使用 CA 证书

如果您的库不支持验证指纹的方法，则会在每个 Elasticsearch 节点上的以下目录中创建自动生成的 CA 证书：

    
    
    $ES_HOME/config/certs/http_ca.crt

将"http_ca.crt"文件复制到您的计算机，并将客户端配置为在连接到 Elasticsearch 时使用此证书建立信任。

### 档案目录布局

存档分发是完全独立的。默认情况下，所有文件和目录都包含在"$ES_HOME"中 - 解压缩存档时创建的目录。

这非常方便，因为您不必创建任何目录即可开始使用 Elasticsearch，卸载 Elasticsearch 就像删除 '$ES_HOME' 目录一样简单。但是，建议更改配置目录、数据目录和日志目录的默认位置，以便以后不会删除重要数据。

类型 |描述 |默认位置 |设置---|---|---|--- **首页**

|

Elasticsearch 主目录或 '$ES_HOME'

|

通过解压缩存档创建的目录

|   **.bin**

|

二进制脚本，包括用于启动节点的"elasticsearch"和用于安装插件的"elasticsearch-plugin"

|

`$ES_HOME/bin`

|   **会议**

|

包含"elasticsearch.yml"的配置文件

|

`$ES_HOME/config`

|

"ES_PATH_CONF" **conf**

|

为传输层和 HTTP 层生成 TLS 密钥和证书。

|

`$ES_HOME/config/certs`

|   **数据**

|

节点上分配的每个索引/分片的数据文件的位置。

|

`$ES_HOME/data`

|

'path.data' **logs**

|

日志文件位置。

|

`$ES_HOME/logs`

|

'path.logs' **plugins**

|

插件文件位置。每个插件将包含在一个子目录中。

|

`$ES_HOME/plugins`

|   **回购**

|

共享文件系统存储库位置。可以容纳多个位置。文件系统存储库可以放置在此处指定的任何目录的任何子目录中。

|

未配置

|

'path.repo' #### 安全证书和密钥编辑

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

### 后续步骤

您现在已经设置了一个测试Elasticsearch环境。在开始使用 Elasticsearch 进行认真开发或投入生产之前，您必须进行一些额外的设置：

* 了解如何配置 Elasticsearch。  * 配置重要的 Elasticsearch 设置。  * 配置重要的系统设置。

[« Installing Elasticsearch](install-elasticsearch.md) [Install
Elasticsearch with `.zip` on Windows »](zip-windows.md)
