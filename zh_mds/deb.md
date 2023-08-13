

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Installing Elasticsearch](install-
elasticsearch.md)

[« Install Elasticsearch with `.zip` on Windows](zip-windows.md) [Install
Elasticsearch with RPM »](rpm.md)

## 使用 DebianPackage 安装 Elasticsearch

Elasticsearch 的 Debian 软件包可以从我们的网站或我们的 APT 存储库下载。它可用于在任何基于 Debian 的系统(如 Debian 和 Ubuntu)上安装 Elasticsearch。

此软件包包含免费和订阅功能。开始 30 天试用以试用所有功能。

Elasticsearch 的最新稳定版本可以在 DownloadElasticsearch 页面上找到。其他版本可以在"过去的版本"页面上找到。

Elasticsearch包括来自JDK维护者(GPLv2 + CE)的OpenJDK捆绑版本。要使用自己的 Java 版本，请参阅 JVM 版本要求版本")

### 导入 Elasticsearch PGPKey

我们使用带有指纹的 Elasticsearch 签名密钥(PGP keyD88E42B4，可从 <https://pgp.mit.edu> 处获得)对所有软件包进行签名：

    
    
    4609 5ACC 8548 582C 1A26 99A9 D27D 666C D88E 42B4

下载并安装公共签名密钥：

    
    
    wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

### 从 APT 存储库安装

在继续之前，您可能需要在 Debian 上安装 'apt-transport-https' 软件包：

    
    
    sudo apt-get install apt-transport-https

将存储库定义保存到"/etc/apt/sources.list.d/elastic-8.x.list"：

    
    
    echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list

这些说明不使用"add-apt-repository"，原因如下：

1. "add-apt-repository"将条目添加到系统"/etc/apt/sources.list"文件中，而不是"/etc/apt/sources.list.d"中干净的每个存储库文件 2."add-apt-repository"不是许多发行版上默认安装的一部分，需要许多非默认依赖项。  3. 旧版本的"add-apt-repository"总是添加一个"deb-src"条目，这将导致错误，因为我们不提供源码包。如果您添加了"deb-src"条目，您将看到如下错误，直到删除"deb-src"行： 无法在发布文件中找到预期的条目"主/源/源"(错误的源列表条目或格式不正确的文件)

您可以使用以下命令安装 Elasticsearch Debian 软件包：

    
    
    sudo apt-get update && sudo apt-get install elasticsearch

如果同一个 Elasticsearch 仓库存在两个条目，您将在"apt-get update"期间看到如下错误：

    
    
    Duplicate sources.list entry https://artifacts.elastic.co/packages/8.x/apt/ ...`

检查"/etc/apt/sources.list.d/elasticsearch-8.x.list"中的重复条目，或在"/etc/apt/sources.list.d/"和"/etc/apt/sources.list"文件中找到重复条目。

在基于 systemd 的发行版上，安装脚本将尝试设置内核参数(例如，'vm.max_map_count');您可以通过屏蔽 systemd-sysctl.service 单元来跳过此操作。

### 手动下载并安装 Debian 软件包

Debian 软件包 Elasticsearch v8.9.0 可以从网站下载并安装如下：

    
    
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.9.0-amd64.deb
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.9.0-amd64.deb.sha512
    shasum -a 512 -c elasticsearch-8.9.0-amd64.deb.sha512 __sudo dpkg -i elasticsearch-8.9.0-amd64.deb

__

|

比较下载的 Debian 软件包的 SHA 和已发布的校验和，它应该输出 'elasticsearch-{version}-amd64.deb： OK'。   ---|--- ### 使用 securityenablededit 启动 Elasticsearch

安装 Elasticsearch 时，默认情况下会启用和配置安全功能。安装 Elasticsearch 时，将自动进行以下安全配置：

* 启用身份验证和授权，并为"弹性"内置超级用户生成密码。  * TLS 的证书和密钥是为传输层和 HTTP 层生成的，并且使用这些密钥和证书启用和配置 TLS。

密码、证书和密钥将输出到您的终端。例如：

    
    
                -------Security autoconfiguration information-------
    
    Authentication and authorization are enabled.
    TLS for the transport and HTTP layers is enabled and configured.
    
    The generated password for the elastic built-in superuser is : <password>
    
    If this node should join an existing cluster, you can reconfigure this with
    '/usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token <token-here>'
    after creating an enrollment token on your existing cluster.
    
    You can complete the following actions at any time:
    
    Reset the password of the elastic built-in superuser with
    '/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic'.
    
    Generate an enrollment token for Kibana instances with
     '/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana'.
    
    Generate an enrollment token for Elasticsearch nodes with
    '/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node'.

#### 重新配置节点以加入现有群集

安装 Elasticsearch 时，安装过程默认配置单节点集群。如果您希望节点加入现有群集，请在首次启动新节点之前_在现有节点上生成注册令牌。

1. 在现有集群中的任何节点上，生成节点注册令牌：/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s 节点

2. 复制注册令牌，该令牌将输出到您的终端。  3. 在新的 Elasticsearch 节点上，将注册令牌作为参数传递给"elasticsearch-reconfigure-node"工具：/usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token <enrollment-token>

Elasticsearch 现在配置为加入现有集群。

4. 使用"systemd"启动新节点。

### 启用系统索引的自动创建

一些商业功能会在 Elasticsearch 中自动创建索引。默认情况下，Elasticsearch 配置为允许自动创建索引，不需要额外的步骤。但是，如果您在 Elasticsearch 中禁用了自动索引创建，则必须在 'elasticsearch.yml' 中配置"action.auto_create_index"以允许商业功能创建以下索引：

    
    
    action.auto_create_index: .monitoring*,.watches,.triggered_watches,.watcher-history*,.ml*

如果您使用的是 Logstash 或 Beats，那么您很可能需要在"action.auto_create_index"设置中使用其他索引名称，确切的值将取决于您的本地配置。如果您不确定环境的正确值，则可以考虑将该值设置为"*"，这将允许自动创建所有索引。

### 使用 'systemd' 运行 Elasticsearch

要将 Elasticsearch 配置为在系统启动时自动启动，请运行以下命令：

    
    
    sudo /bin/systemctl daemon-reload
    sudo /bin/systemctl enable elasticsearch.service

Elasticsearch可以按如下方式启动和停止：

    
    
    sudo systemctl start elasticsearch.service
    sudo systemctl stop elasticsearch.service

这些命令不提供关于 Elasticsearch 是否成功启动的反馈。相反，此信息将写入位于"/var/log/elasticsearch/"中的日志文件中。

如果您的 Elasticsearch 密钥库受密码保护，则需要使用本地文件和 systemdenvironment 变量向"systemd"提供密钥库密码。此本地文件在存在时应受到保护，并且可以在 Elasticsearch 启动并运行后安全删除。

    
    
    echo "keystore_password" > /path/to/my_pwd_file.tmp
    chmod 600 /path/to/my_pwd_file.tmp
    sudo systemctl set-environment ES_KEYSTORE_PASSPHRASE_FILE=/path/to/my_pwd_file.tmp
    sudo systemctl start elasticsearch.service

默认情况下，Elasticsearch 服务不会在 'systemd' 日志中记录信息。要启用"journalctl"日志记录，必须从"elasticsearch.service"文件的"ExecStart"命令行中删除"--quiet"选项。

启用"systemd"日志记录后，可以使用"journalctl"命令获得日志记录信息：

跟踪日志：

    
    
    sudo journalctl -f

列出弹性搜索服务的日志条目：

    
    
    sudo journalctl --unit elasticsearch

列出从给定时间开始的 elasticsearch 服务的日志条目：

    
    
    sudo journalctl --unit elasticsearch --since  "2016-10-30 18:17:16"

检查"man journalctl"或<https://www.freedesktop.org/software/systemd/man/journalctl.html>以获取更多命令行选项。

### 旧"systemd"版本的启动超时

默认情况下，Elasticsearch 将 'TimeoutStartSec' 参数设置为 'systemd' 到 '900s'。如果您运行的是至少 238 版的 'systemd'，那么 Elasticsearch 可以自动延长启动超时，并且即使启动时间超过 900 秒，也会重复执行此操作，直到启动完成。

238 之前的 'systemd' 版本不支持超时扩展机制，如果 Elasticsearch 进程未在配置的超时内完全启动，它将终止该进程。如果发生这种情况，Elasticsearch 将在其日志中报告它在启动后不久就正常关闭了：

    
    
    [2022-01-31T01:22:31,077][INFO ][o.e.n.Node               ] [instance-0000000123] starting ...
    ...
    [2022-01-31T01:37:15,077][INFO ][o.e.n.Node               ] [instance-0000000123] stopping ...

但是，"systemd"日志将报告启动超时：

    
    
    Jan 31 01:22:30 debian systemd[1]: Starting Elasticsearch...
    Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Start operation timed out. Terminating.
    Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Main process exited, code=killed, status=15/TERM
    Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Failed with result 'timeout'.
    Jan 31 01:37:15 debian systemd[1]: Failed to start Elasticsearch.

为避免这种情况，请将您的"systemd"至少升级到版本 238。您还可以通过扩展"超时开始秒"参数来临时解决此问题。

### 检查 Elasticsearch 是否正在运行

您可以通过向"localhost"上的端口"9200"发送HTTPS请求来测试您的Elasticsearch节点是否正在运行：

    
    
    curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic https://localhost:9200 __

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

### 配置弹性搜索

'/etc/elasticsearch' 目录包含 Elasticsearch 的默认运行时配置。在软件包安装中，此目录和所有包含的文件的所有权设置为"root：elasticsearch"。

"setgid"标志在"/etc/elasticsearch"目录上应用组权限，以确保Elasticsearch可以读取任何包含的文件和子目录。所有文件和子目录都继承了"root：elasticsearch"的所有权。从此目录或任何子目录(如 elasticsearch-keystore 工具)运行命令需要"root：elasticsearch"权限。

默认情况下，Elasticsearch 从 '/etc/elasticsearch/elasticsearch.yml' 文件加载其配置。此配置文件的格式在_Configuring Elasticsearch_中解释。

Debian 软件包还有一个系统配置文件('/etc/default/elasticsearch')，它允许你设置以下参数：

`ES_JAVA_HOME`

|

设置要使用的自定义 Java 路径。   ---|--- "ES_PATH_CONF"

|

配置文件目录(需要包含"elasticsearch.yml"，"jvm.options"和"log4j2.properties"文件);默认为'/etc/elasticsearch'。   "ES_JAVA_OPTS"

|

您可能要应用的任何其他 JVM 系统属性。   "RESTART_ON_UPGRADE"

|

配置包升级时重新启动，默认为"false"。这意味着您必须在手动安装软件包后重新启动 Elasticsearch 实例。这样做的原因是为了确保集群中的升级不会导致持续的分片重新分配，从而导致高网络流量并缩短集群的响应时间。   使用"systemd"的发行版要求通过"systemd"而不是通过"/etc/sysconfig/elasticsearch"文件配置系统资源限制。有关详细信息，请参阅 Systemd 配置。

### 将客户端连接到弹性搜索

当您第一次启动 Elasticsearch 时，TLS 会自动为 HTTP 层配置。CA 证书生成并存储在磁盘上：

    
    
    /etc/elasticsearch/certs/http_ca.crt

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

    
    
    /etc/elasticsearch/certs/http_ca.crt

将"http_ca.crt"文件复制到您的计算机，并将客户端配置为在连接到 Elasticsearch 时使用此证书建立信任。

### Debianpackage 的目录布局

Debian 软件包将配置文件、日志和数据目录放在基于 Debian 的系统的正确位置：

类型 |描述 |默认位置 |设置---|---|---|--- **首页**

|

Elasticsearch 主目录或 '$ES_HOME'

|

`/usr/share/elasticsearch`

|   **.bin**

|

二进制脚本，包括用于启动节点的"elasticsearch"和用于安装插件的"elasticsearch-plugin"

|

`/usr/share/elasticsearch/bin`

|   **会议**

|

包含"elasticsearch.yml"的配置文件

|

`/etc/elasticsearch`

|

"ES_PATH_CONF" **conf**

|

环境变量，包括堆大小、文件描述符。

|

`/etc/default/elasticsearch`

|   **会议**

|

为传输层和 http 层生成 TLS 密钥和证书。

|

`/etc/elasticsearch/certs`

|   **数据**

|

节点上分配的每个索引/分片的数据文件的位置。

|

`/var/lib/elasticsearch`

|

'path.data' **jdk**

|

捆绑的Java开发工具包用于运行Elasticsearch。可以通过在"/etc/default/elasticsearch"中设置"ES_JAVA_HOME"环境变量来覆盖。

|

`/usr/share/elasticsearch/jdk`

|   **原木**

|

日志文件位置。

|

`/var/log/elasticsearch`

|

'path.logs' **plugins**

|

插件文件位置。每个插件将包含在一个子目录中。

|

`/usr/share/elasticsearch/plugins`

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

[« Install Elasticsearch with `.zip` on Windows](zip-windows.md) [Install
Elasticsearch with RPM »](rpm.md)
