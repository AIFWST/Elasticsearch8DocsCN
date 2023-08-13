

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Secure the
Elastic Stack](secure-cluster.md) ›[User authentication](setting-up-
authentication.md)

[« User authentication](setting-up-authentication.md) [Service accounts
»](service-accounts.md)

## 内置用户

Elastic Stack 安全功能提供内置的用户凭证，帮助您启动和运行。这些用户具有一组固定的权限，在设置其密码之前无法进行身份验证。"弹性"用户可用于设置所有内置用户密码。

**创建具有最低权限的用户**

内置用户用于特定用途，不用于一般用途。特别是，除非绝对需要对集群的完全访问权限，否则不要使用"弹性"超级用户。在自我管理部署中，使用"弹性"用户创建具有其活动所需的最低角色或权限的用户。

在弹性云上，操作员权限已启用。这些权限会限制某些基础结构功能，即使角色以其他方式允许用户完成管理任务也是如此。

`elastic`

    

内置超级用户。

任何能够以"弹性"用户身份登录的人都可以直接只读访问受限索引，例如".security"。此用户还能够管理安全性并创建具有无限权限的角色。

`kibana_system`

     The user Kibana uses to connect and communicate with Elasticsearch. 
`logstash_system`

     The user Logstash uses when storing monitoring information in Elasticsearch. 
`beats_system`

     The user the Beats use when storing monitoring information in Elasticsearch. 
`apm_system`

     The user the APM server uses when storing monitoring information in Elasticsearch. 
`remote_monitoring_user`

     The user Metricbeat uses when collecting and storing monitoring information in Elasticsearch. It has the `remote_monitoring_agent` and `remote_monitoring_collector` built-in roles. 

#### 内置用户的工作原理

这些内置用户存储在一个特殊的".security"索引中，该索引由Elasticsearch管理。如果禁用内置用户或其密码更改，则更改会自动反映在群集中的每个节点上。但是，如果从快照中删除或还原".security"索引，则应用的任何更改都将丢失。

尽管它们共享相同的 API，但内置用户是独立的，并且与本机域管理的用户不同。禁用本机领域不会对内置用户产生任何影响。可以使用禁用用户 API 单独禁用内置用户。

#### 弹性引导密码

当你安装 Elasticsearch 时，如果"elastic"用户还没有密码，它使用默认的引导密码。引导密码是临时密码，可用于运行设置所有内置用户密码的工具。

缺省情况下，引导密码派生自随机化的"keystore.seed"设置，该设置在安装期间添加到密钥库中。您无需知道或更改此引导密码。但是，如果您在密钥库中定义了"bootstrap.password"设置，那么将使用该值。有关与密钥库交互的更多信息，请参阅安全设置。

为内置用户(尤其是"弹性"用户)设置密码后，引导密码将不再使用。

#### 设置内置用户密码

必须为所有内置用户设置密码。

"弹性搜索设置密码"工具是首次设置内置用户密码的最简单方法。它使用"弹性"用户的引导密码来运行用户管理 API 请求。例如，您可以在"交互式"模式下运行命令，该模式会提示您输入"弹性"、"kibana_system"、"logstash_system"、"beats_system"、"apm_system"和"remote_monitoring_user"用户的新密码：

    
    
    bin/elasticsearch-setup-passwords interactive

有关命令选项的更多信息，请参阅 elasticsearch-setup-passwords。

为"弹性"用户设置密码后，引导密码不再有效;您不能再次运行"Elasticsearch-setup-passwords"命令。

或者，您可以使用 Kibana 中的"管理>用户**"页面或更改密码 API 为内置用户设置初始密码。这些方法更复杂。您必须提供"弹性"用户及其引导密码才能登录 Kibana 或运行 API。此要求意味着您不能使用从"keystore.seed"设置派生的默认引导密码。相反，在启动 Elasticsearch 之前，您必须在密钥库中显式设置 'bootstrap.password' 设置。例如，以下命令会提示您输入新的引导密码：

    
    
    bin/elasticsearch-keystore add "bootstrap.password"

然后，您可以启动 Elasticsearch 和 Kibana，并使用"弹性"用户和引导密码登录 Kibana 并更改密码。或者，您可以为每个内置用户提交更改密码 API 请求。这些方法更适合在初始设置完成后更改密码，因为此时不再需要引导密码。

#### 将内置用户密码添加到 Kibana

设置"kibana_system"用户密码后，您需要通过在"kibana.yml"配置文件中设置"elasticsearch.password"来使用新密码更新 Kibanaserver：

    
    
    elasticsearch.password: kibanapassword

请参阅在 Kibana 中配置安全性。

#### 将内置用户密码添加到日志存储

当为 Logstash 启用监控时，"logstash_system"用户在 Logstash 内部使用。

要在 Logstash 中启用此功能，您需要通过在 'logstash.yml' 配置文件中设置"xpack.monitoring.elasticsearch.password"来使用新密码更新 Logstash 配置：

    
    
    xpack.monitoring.elasticsearch.password: logstashpassword

如果您从旧版本的 Elasticsearch 升级，出于安全原因，"logstash_system"用户可能默认为 _disabled_。更改密码后，您可以通过以下 API 调用启用用户：

    
    
    PUT _security/user/logstash_system/_enable

请参阅为日志监控配置凭证。

#### 将内置用户密码添加到 Beats

当为 Beats 启用监听时，"beats_system"用户在 Beats 内部使用。

要在 Beats 中启用此功能，您需要更新每个 Beat 的配置以引用正确的用户名和密码。例如：

    
    
    xpack.monitoring.elasticsearch.username: beats_system
    xpack.monitoring.elasticsearch.password: beatspassword

例如，请参阅 MonitorMetricbeat。

"remote_monitoring_user"用于 Metricbeat 收集和存储弹性堆栈的监控数据。请参阅productionenvironment_中的_Monitoring。

如果您从旧版本的 Elasticsearch 升级，则可能没有为"beats_system"或"remote_monitoring_user"用户设置密码。如果是这种情况，则应使用 Kibana 中的"用户管理>"页面或更改密码 API 为这些用户设置密码。

#### 将内置用户密码添加到 APM

启用监控时，"apm_system"用户在 APM 内部使用。

要在 APM 中启用此功能，您需要更新"apm-server.yml"配置文件以引用正确的用户名和密码。例如：

    
    
    xpack.monitoring.elasticsearch.username: apm_system
    xpack.monitoring.elasticsearch.password: apmserverpassword

如果您从旧版本的 Elasticsearch 升级，则可能没有为"apm_system"用户设置密码。如果是这种情况，则应使用 Kibana 中的"管理>用户**"页面或更改密码 API 为这些用户设置密码。

#### 禁用默认密码功能

此设置已弃用。弹性用户不再拥有默认密码。必须先设置密码，然后才能使用用户。请参阅 Elasticbootstrap 密码。

[« User authentication](setting-up-authentication.md) [Service accounts
»](service-accounts.md)
