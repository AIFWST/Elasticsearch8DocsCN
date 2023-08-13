

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Manually configure security](manually-
configure-security.md)

[« Set up basic security for the Elastic Stack](security-basic-setup.md)
[Setting passwords for native and built-in users »](change-passwords-native-
users.md)

## 为弹性堆栈设置基本安全性以及安全的 HTTPS流量

在 HTTP 层上启用 TLS 时，它将提供额外的安全层，以确保与群集之间的所有通信都经过加密。

当您在"http"模式下运行"elasticsearch-certutil"工具时，该工具会询问有关您希望如何生成证书的几个问题。虽然有许多选项，但以下选择会产生适用于大多数环境的证书。

**签名证书**

"elasticsearch-certutil"工具提示的第一个问题是您是否要生成证书签名请求(CSR)。如果要签署自己的证书，请回答"n"，如果要使用中央 CA 签署证书，请回答"y"。

##### 签署您自己的证书

如果要使用在生成证书颁发机构时创建的 CA，请在询问您是否要生成 CSR 时回答"n"。然后，指定 CA 的位置，该工具使用该位置对".p12"证书进行签名和生成。此过程中的步骤遵循此工作流。

##### 使用中央 CA 签署证书

如果您在具有中央安全团队的环境中工作，他们可能会为您生成证书。组织内的基础设施可能已经配置为信任现有的 CA，因此如果您使用 CSR 并将该请求发送给控制 CA 的团队，客户端可能会更容易连接到 Elasticsearch。要使用中央 CA，请对第一个问题回答"y"。

###Prerequisites

完成为弹性堆栈设置基本安全性中的所有步骤。

### 加密 HTTP 客户端通信 Elasticsearch

1. 在集群中的每个节点上，停止 Elasticsearch 和 Kibana(如果它们正在运行)。  2. 在任何单个节点上，从您安装 Elasticsearch 的目录中，运行 Elasticsearch HTTP 证书工具以生成证书签名请求 (CSR)。           ./bin/elasticsearch-certutil http

此命令生成一个".zip"文件，其中包含要与 Elasticsearch 和 Kibana 一起使用的证书和密钥。每个文件夹都包含一个"自述文件.txt"，说明如何使用这些文件。

    1. When asked if you want to generate a CSR, enter `n`. 
    2. When asked if you want to use an existing CA, enter `y`. 
    3. Enter the path to your CA. This is the absolute path to the `elastic-stack-ca.p12` file that you generated for your cluster. 
    4. Enter the password for your CA. 
    5. Enter an expiration value for your certificate. You can enter the validity period in years, months, or days. For example, enter `90D` for 90 days. 
    6. When asked if you want to generate one certificate per node, enter `y`.

每个证书都有自己的私钥，并将针对特定的主机名或 IP 地址颁发。

    7. When prompted, enter the name of the first node in your cluster. Use the same node name that you used when [generating node certificates](security-basic-setup.html#generate-certificates "Generate the certificate authority"). 
    8. Enter all hostnames used to connect to your first node. These hostnames will be added as DNS names in the Subject Alternative Name (SAN) field in your certificate.

列出用于通过 HTTPS 连接到集群的每个主机名和变体。

    9. Enter the IP addresses that clients can use to connect to your node. 
    10. Repeat these steps for each additional node in your cluster. 

3. 为每个节点生成证书后，在出现提示时输入私钥的密码。  4. 解压缩生成的"elasticsearch-ssl-http.zip"文件。这个压缩文件包含一个用于Elasticsearch和Kibana的目录。           /elasticsearch |_ README.txt |_ http.p12 |_ sample-elasticsearch.yml /kibana |_ README.txt |_ elasticsearch-ca.pem |_ sample-kibana.yml

5. 在集群中的**每个**节点上，完成以下步骤：

    1. Copy the relevant `http.p12` certificate to the `$ES_PATH_CONF` directory. 
    2. Edit the `elasticsearch.yml` file to enable HTTPS security and specify the location of the `http.p12` security certificate.
        
                xpack.security.http.ssl.enabled: true
        xpack.security.http.ssl.keystore.path: http.p12

    3. Add the password for your private key to the secure settings in Elasticsearch.
        
                ./bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password

    4. Start Elasticsearch. 

**下一页**：加密 Kibana 的 HTTP 客户端通信

### 为 Kibana 加密 HTTP 客户端通信

浏览器将流量发送到 Kibana，Kibana 将流量发送到 Elasticsearch。这些通信通道单独配置为使用 TLS。您加密 Kibana 和 Elasticsearch 之间的流量，然后加密浏览器和 Kibana 之间的流量。

#### 加密 Kibana 和 Elasticsearch 之间的流量

当你使用"http"选项运行"elasticsearch-certutil"工具时，它创建了一个包含"elasticsearch-ca.pem"文件的"/kibana"目录。您可以使用此文件将 Kibana 配置为信任 HTTPlayer 的 Elasticsearch CA。

1. 将 'elasticsearch-ca.pem' 文件复制到 Kibana 配置目录，如 '$KBN_PATH_CONF' 路径所定义。  2. 打开"kibana.yml"并添加以下行以指定 HTTP 层的安全证书的位置。           elasticsearch.ssl.certificateAuthority： $KBN_PATH_CONF/elasticsearch-ca.pem

3. 添加以下行以指定 Elasticsearch 集群的 HTTPS URL。           elasticsearch.hosts： <your_elasticsearch_host>https://：9200

4. 重新启动 Kibana。

**连接到安全监控群集**

如果启用了弹性监控功能，并且您配置了单独的 Elasticsearch 监控集群，您还可以将 Kibana 配置为通过 HTTPS 连接到监控集群。步骤相同，但每个设置都以"监视"为前缀。例如，"monitoring.ui.elasticsearch.hosts"和"monitoring.ui.elasticsearch.ssl.truststore.path"。

您必须为监控集群创建单独的"弹性搜索-ca.pem"安全文件。

**下一页**：加密浏览器与 Kibana 之间的流量

#### 加密浏览器和 Kibana 之间的流量

您可以为 Kibana 创建服务器证书和私钥。Kibana 在从 Web 浏览器接收连接时使用此服务器证书和相应的私钥。

获取服务器证书时，必须正确设置其使用者可选名称 (SAN)，以确保浏览器信任它。您可以将一个或多个 SAN 设置为 Kibana 服务器的完全限定域名 (FQDN)、主机名或 IP 地址。选择 SAN 时，请在浏览器中选择用于连接到 Kibana 的属性，这可能是 FQDN。

以下说明为 Kibana 创建证书签名请求 (CSR)。CSR 包含 CA 用于生成和签署安全证书的信息。证书可以是受信任的(由受信任的公共 CA 签名)或不受信任的(由内部 CA 签名)。自签名或内部签名证书可用于开发环境和构建概念证明，但不应在生产环境中使用。

在投入生产之前，请使用受信任的 CA(如 Let'sEncrypt)或组织的内部 CA 对证书进行签名。使用签名证书为与 Kibana 的连接建立浏览器信任，以便进行内部访问或在公共互联网上。

1. 为 Kibana 生成服务器证书和私钥。           ./bin/elasticsearch-certutil csr -name kibana-server -DNS example.com，www.example.com

CSR 的通用名称 (CN) 为"kibana-server"，SAN 为 "example.com"，另一个 SAN 为 "www.example.com"。

此命令默认生成一个包含以下内容的"csr-bundle.zip"文件：

    
        /kibana-server
    |_ kibana-server.csr
    |_ kibana-server.key

2. 解压缩"csr-bundle.zip"文件，获取"kibana-server.csr"未签名安全证书和"kibana-server.key"未加密私钥。  3. 将"kibana-server.csr"证书签名请求发送到您的内部 CA 或受信任的 CA 进行签名，以获取签名证书。签名文件可以采用不同的格式，例如".crt"文件，如"kibana-server.crt"。  4. 打开"kibana.yml"并添加以下行以配置 Kibana 以访问服务器证书和未加密的私钥。           server.ssl.certificate： $KBN_PATH_CONF/kibana-server.crt server.ssl.key： $KBN_PATH_CONF/kibana-server.key

'$KBN_PATH_CONF' 包含 Kibana 配置文件的路径。如果您使用归档发行版("zip"或"tar.gz")安装了 Kibana，则路径默认为"$KBN_HOME/config"。如果您使用的是软件包发行版(Debian 或 RPM)，则路径默认为 '/etc/kibana'。

5. 将以下行添加到"kibana.yml"，为入站连接启用 TLS。           server.ssl.enabled： true

6. 启动木花。

进行这些更改后，您必须始终通过 HTTPS 访问 Kibana。例如，"https://<your_kibana_host>.com"。

**下一页**：配置 Beats 安全性

### 配置 Beatssecurity

Beats 是开源数据托运器，您可以将其作为代理安装在服务器上，用于将操作数据发送到 Elasticsearch。每个节拍都是可单独安装的产品。以下步骤介绍如何为 Metricbeat 配置安全性。对于要为其配置安全性的每个附加 Beat 执行以下步骤。

####Prerequisites

使用您的首选方法安装 Metricbeat。

在完成以下步骤之前，您无法连接到弹性堆栈或为 Metricbeat 配置资产。

#### 为 Metricbeat 创建角色

通常，您需要创建以下单独的角色：

* **设置**角色，用于设置索引模板和其他依赖项 * **监视**角色，用于发送监视信息 * **编写器**角色，用于发布 Metricbeat 收集的事件 * **读取者角色，适用于需要查看和创建访问 Metricbeat 数据的可视化的 Kibana 用户

这些说明假定您使用的是 Metricbeatindex 的默认名称。如果未列出指示的索引名称，或者您使用的是自定义名称，请在定义角色时手动输入该名称并修改权限以匹配索引命名模式。

要从 Kibana 中的堆栈管理创建用户和角色，请从侧面导航栏中选择**角色**或**用户**。

**下一步**：创建安装角色

###### 创建安装角色和用户

设置 Metricbeat 的管理员通常需要将用于索引数据的映射、仪表板和其他对象加载到 Elasticsearch 中，并在 Kibana 中可视化。

设置 Metricbeat 是一项需要额外权限的管理员级任务。最佳做法是仅向管理员授予安装角色，并对事件发布使用限制性更强的角色。

1. 创建设置角色： 2. 输入 **metricbeat_setup** 作为角色名称。  3. 选择**监控**和**manage_ilm**集群权限。  4. 在 **metricbeat-\** * 索引上，选择 **管理** 和 **写入** 权限。

如果未列出 **metricbeat-\** * 索引，请将该模式输入到索引列表中。

5. 创建设置用户： 6. 输入 **metricbeat_setup** 作为用户名。  7. 输入用户名、密码和其他用户详细信息。  8. 将以下角色分配给 **metricbeat_setup** 用户：

角色 |目的 ---|--- "metricbeat_setup"

|

设置指标节拍。   "kibana_admin"

|

将依赖项(例如示例仪表板(如果可用)加载到 Kibana "ingest_admin"中

|

设置索引模板并引入管道(如果可用)

下一篇：创建监控角色

###### 创建监视角色和用户

要安全地发送监控数据，请创建监控用户并向其授予必要的权限。

您可以使用内置的"beats_system"用户(如果它在您的环境中可用)。由于内置用户在弹性云中不可用，因此这些说明会创建一个明确用于监控 Metricbeat 的用户。

1. 如果您使用的是内置的"beats_system"用户，请在集群中的任何节点上运行"弹性搜索重置密码"实用程序以设置该用户的密码：

此命令将"beats_system"用户的密码重置为自动生成的值。

    
        ./bin/elasticsearch-reset-password -u beats_system

如果要将密码设置为特定值，请使用交互式 ('-i') 参数运行命令。

    
        ./bin/elasticsearch-reset-password -i -u beats_system

2. 创建监控角色： 3. 输入 **metricbeat_monitoring** 作为角色名称。  4. 选择**监控**集群权限。  5. 在 **.monitoring-beats-\** * 索引上，选择 **create_index** 和 **create_doc** 权限。  6. 创建监控用户： 7. 输入 **metricbeat_monitoring** 作为用户名。  8. 输入用户名、密码和其他用户详细信息。  9. 将以下角色分配给 **metricbeat_monitoring** 用户：

角色 |目的 ---|--- "metricbeat_monitoring"

|

监控指标节拍。   "kibana_admin"

|

使用 Kibana "monitoring_user"

|

在 Kibana 中使用堆栈监控来监控 Metricbeat

**下一页**：创建编写器角色

###### 创建编写器角色和用户

将事件发布到 Elasticsearch 的用户需要创建并写入 Metricbeat 索引。若要最大程度地减少编写器角色所需的特权，请使用安装角色预加载依赖项。本部分假定你已创建安装角色。

1. 创建编写者角色： 2. 输入 **metricbeat_writer** 作为角色名称。  3. 选择**监控**和**read_ilm**集群权限。  4. 在 **metricbeat-\** * 索引上，选择 **create_doc** 、 **create_index** 和 **view_index_metadata** 权限。  5. 创建编写器用户： 6. 输入 **metricbeat_writer** 作为用户名。  7. 输入用户名、密码和其他用户详细信息。  8. 将以下角色分配给 **metricbeat_writer** 用户：

角色 |目的 ---|--- "metricbeat_writer"

|

监控指标节拍"remote_monitoring_collector"

|

从 Metricbeat 'remote_monitoring_agent' 收集监控指标

|

将监控数据发送到监控集群

**下一页**：创建读取者角色

###### 创建读取者角色和用户

Kibana 用户通常需要查看包含 Metricbeat 数据的仪表板和可视化效果。这些用户可能还需要创建和编辑仪表板和可视化效果。创建读取者角色以向这些用户分配适当的权限。

1. 创建读取者角色： 2. 输入 **metricbeat_reader** 作为角色名称。  3. 在 **metricbeat-\** * 索引上，选择 ** 读取 ** 权限。  4. 在 **Kibana** 下，单击 **添加 Kibana 权限**。

    * Under **Spaces** , choose **Default**. 
    * Choose **Read** or **All** for Discover, Visualize, Dashboard, and Metrics. 

5. 创建读取器用户： 6. 输入 **metricbeat_reader** 作为用户名。  7. 输入用户名、密码和其他用户详细信息。  8. 将以下角色分配给 **metricbeat_reader** 用户：

角色 |目的 ---|--- "metricbeat_reader"

|

读取指标节拍数据。   "monitoring_user"

|

允许用户监控 Metricbeat 本身的运行状况。仅将此角色分配给管理 Metricbeat "beats_admin"的用户

|

在 Beats 集中管理中创建和管理配置。仅将此角色分配给需要使用 Beats 中央管理的用户。   

**下一页**：将 Metricbeat 配置为使用 TLS

##### 配置 Metricbeat 以使用 TLS

在启动 Metricbeat 之前，您需要配置与 Elasticsearch 和 Kibana 的连接。您可以配置身份验证以使用基本身份验证、API 密钥身份验证或公钥基础结构 (PKI) 证书将数据发送到安全群集。

以下说明使用您创建的"metricbeat_writer"和"metricbeat_setup"用户的凭据。如果需要更高级别的安全性，我们建议使用 PKI 证书。

配置与 Elasticsearch 和 Kibana 的连接后，您将启用"elasticsearch-xpack"模块并将该模块配置为使用 HTTPS。

在生产环境中，我们强烈建议使用单独的集群(称为监控集群)来存储数据。使用单独的监控集群可防止生产集群中断影响您访问监控数据的能力。它还可以防止监视活动影响生产群集的性能。

1. 在为 HTTP 层生成证书的节点上，导航到"/kibana"目录。  2. 将"elasticsearch-ca.pem"证书复制到安装 Metricbeat 的目录。  3. 打开"metricbeat.yml"配置文件并配置与 Elasticsearch 的连接。

在"output.elasticsearch"下，指定以下字段：

    
        output.elasticsearch:
     hosts: ["<your_elasticsearch_host>:9200"]
     protocol: "https"
     username: "metricbeat_writer"
     password: "<password>"
     ssl:
       certificate_authorities: ["elasticsearch-ca.pem"]
       verification_mode: "certificate"

`hosts`

     Specifies the host where your Elasticsearch cluster is running. 
`protocol`

     Indicates the protocol to use when connecting to Elasticsearch. This value must be `https`. 
`username`

     Name of the user with privileges required to publish events to Elasticsearch. The `metricbeat_writer` user that you created has these privileges. 
`password`

     Password for the indicated `username`. 
`certificate_authorities`

     Indicates the path to the local `.pem` file that contains your CA's certificate. 

4. 配置与 Kibana 的连接。

在"setup.kibana"下，指定以下字段：

    
        setup.kibana
     host: "https://<your_elasticsearch_host>:5601"
     ssl.enabled: true
     username: "metricbeat_setup"
     password: "p@ssw0rd"

`hosts`

     The URLs of the Elasticsearch instances to use for all your queries. Ensure that you include `https` in the URL. 
`username`

     Name of the user with privileges required to set up dashboards in Kibana. The `metricbeat_setup` user that you created has these privileges. 
`password`

     Password for the indicated `username`. 

5. 启用 'elasticsearch-xpack' 模块。           ./metricbeat 模块支持 elasticsearch-xpack

6. 修改 'elasticsearch-xpack' 模块以使用 HTTPS。此模块收集有关 Elasticsearch 的指标。

打开"/modules.d/elasticsearch-xpack.yml"并指定以下字段：

    
        - module: elasticsearch
     xpack.enabled: true
     period: 10s
     hosts: ["https://<your_elasticsearch_host>:9200"]
     username: "remote_monitoring_user"
     password: "<password>"
     ssl:     __enabled: true
       certificate_authorities: ["elasticsearch-ca.pem"]
       verification_mode: "certificate"

__

|

使用加密流量监控节点时，需要配置 SSL。请参阅为 Metricbeat配置 SSL。

`hosts`

     Specifies the host where your Elasticsearch cluster is running. Ensure that you include `https` in the URL. 
`username`

     Name of the user with privileges to collect metric data. The built-in `monitoring_user` user has these privileges. Alternatively, you can create a user and assign it the `monitoring_user` role. 
`password`

     Password for the indicated `username`. 
`certificate_authorities`

     Indicates the path to the local `.pem` file that contains your CA's certificate.   
  
---|---  
  
  7. If you want to use the predefined assets for parsing, indexing, and visualizing your data, run the following command to load these assets:
    
        ./metricbeat setup -e

8. 启动 Elasticsearch，然后启动 Metricbeat。           ./metricbeat -e

"-e"是可选的，它将输出发送到标准错误而不是配置的日志输出。

9. 登录 Kibana，打开主菜单，然后单击"堆栈监控**"。

您将看到需要您注意的集群警报，以及 Elasticsearch 可用监控指标的摘要。单击可用卡片上的任意标题链接以查看其他信息。

[« Set up basic security for the Elastic Stack](security-basic-setup.md)
[Setting passwords for native and built-in users »](change-passwords-native-
users.md)
