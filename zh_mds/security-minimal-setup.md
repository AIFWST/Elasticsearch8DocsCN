

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[Manually configure security](manually-
configure-security.md)

[« Manually configure security](manually-configure-security.md) [Set up
basic security for the Elastic Stack »](security-basic-setup.md)

## 为弹性搜索设置最低安全性

如果您正在运行现有的不安全集群并希望启用 Elasticsearch 安全功能，则只需完成以下步骤。

在 Elasticsearch 8.0 及更高版本中，首次启动 Elasticsearch 时会自动启用安全性。

如果您运行的是禁用安全性的现有 Elasticsearch 集群，则可以手动启用 Elasticsearch 安全功能，然后为内置用户创建密码。您可以稍后添加更多用户，但使用内置用户可以简化为群集启用安全性的过程。

最低安全方案不足以满足生产模式群集的需求。如果群集具有多个节点，则必须启用最低安全性，然后在节点之间配置传输层安全性 (TLS)。

### 启用 Elasticsearch 安全功能

启用 Elasticsearch 安全功能可提供基本身份验证，以便您可以使用用户名和密码身份验证运行本地集群。

1. 在集群中的每个节点上，停止 Kibana 和 Elasticsearch(如果它们正在运行)。  2. 在集群中的每个节点上，将"xpack.security.enabled"设置添加到"$ES_PATH_CONF/elasticsearch.yml"文件，并将值设置为"true"：xpack.security.enabled：true

'$ES_PATH_CONF' 变量是 Elasticsearch 配置文件的路径。如果你使用归档发行版('zip'或'tar.gz')安装了Elasticsearch，则变量默认为'$ES_HOME/config'。如果您使用的是软件包发行版(Debian 或 RPM)，变量默认为 '/etc/elasticsearch'。

3. 如果您的集群具有单个节点，请在"$ES_PATH_CONF/elasticsearch.yml"文件中添加"discovery.type"设置，并将值设置为"单节点"。此设置可确保您的节点不会无意中连接到可能正在您的网络上运行的其他集群。           发现类型：单节点

### 为内置用户设置密码

要与集群通信，您必须为"弹性"和"kibana_system"内置用户配置密码。除非启用匿名访问(不推荐)，否则将拒绝所有不包含凭据的请求。

启用最低或基本安全性时，您只需为"弹性"和"kibana_system"用户设置密码。

1. 在集群中的每个节点上，启动 Elasticsearch。例如，如果您安装了带有".tar.gz"包的 Elasticsearch，请从"ES_HOME"目录运行以下命令：./bin/elasticsearch

2. 在集群中的任何节点上，打开另一个终端窗口，并通过运行"弹性搜索-重置密码"实用程序为"弹性"内置用户设置密码。此命令将密码重置为自动生成的值。           ./bin/elasticsearch-reset-password -u elastic

如果要将密码设置为特定值，请使用交互式 ('-i') 参数运行命令。

    
        ./bin/elasticsearch-reset-password -i -u elastic

3. 为"kibana_system"内置用户设置密码。           ./bin/elasticsearch-reset-password -u kibana_system

4. 保存新密码。在下一步中，您需要将"kibana_system"用户的密码添加到 Kibana。

**下一页** ： 配置 Kibana 以使用密码连接到 Elasticsearch

### 配置 Kibana 以使用密码连接到 Elasticsearch

启用 Elasticsearch 安全功能后，用户必须使用有效的用户名和密码登录 toKibana。

您需要将 Kibana 配置为使用您之前创建的内置"kibana_system"用户和密码。Kibana 执行一些需要使用"kibana_system"用户的后台任务。

此帐户不适用于个人用户，并且没有从浏览器登录 Kibana 的权限。相反，您将以"弹性"超级用户的身份登录 Kibana。

1. 将"elasticsearch.username"设置添加到"KIB_PATH_CONF/kibana.yml"文件中，并将值设置为"kibana_system"用户：elasticsearch.username："kibana_system"

"KIB_PATH_CONF"变量是 Kibana 配置文件的路径。如果您使用归档发行版("zip"或"tar.gz")安装了 Kibana，则变量默认为"KIB_HOME/config"。如果您使用软件包发行版(Debian 或 RPM)，变量默认为 '/etc/kibana'。

2. 在安装 Kibana 的目录中，运行以下命令以创建 Kibana 密钥库并添加安全设置：

    1. Create the Kibana keystore:
        
                ./bin/kibana-keystore create

    2. Add the password for the `kibana_system` user to the Kibana keystore:
        
                ./bin/kibana-keystore add elasticsearch.password

出现提示时，输入"kibana_system"用户的密码。

3. 重新启动 Kibana。例如，如果您安装了带有".tar.gz"软件包的 Kibana，请从 Kibana 目录运行以下命令：./bin/kibana

4. 以"弹性"用户身份登录 Kibana。使用此超级用户帐户可以管理空间、创建新用户和分配角色。如果您在本地运行 Kibana，请转到"http://localhost:5601"以查看登录页面。

### 下一步是什么？

祝贺！您为本地群集启用了密码保护，以防止未经授权的访问。您可以以"弹性"用户身份安全地登录 Kibana，并创建其他用户和角色。如果您运行的是单节点群集，则可以在此处停止。

如果群集有多个节点，则必须在节点之间配置传输层安全性 (TLS)。如果不启用 TLS，生产模式群集将不会启动。

为 Elastic Stack 设置基本安全性，以保护集群中节点之间的所有内部通信。

[« Manually configure security](manually-configure-security.md) [Set up
basic security for the Elastic Stack »](security-basic-setup.md)
