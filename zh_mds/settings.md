

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md)

[« Run Elasticsearch locally](run-elasticsearch-locally.md) [Important
Elasticsearch configuration »](important-settings.md)

## 配置ElasticSearch

Elasticsearch提供了良好的默认值，并且需要很少的配置。大多数设置都可以使用群集更新设置 API 在正在运行的群集上更改。

配置文件应包含特定于节点的设置(例如"node.name"和路径)，或者节点加入群集所需的设置，例如"cluster.name"和"network.host"。

### 配置文件位置

Elasticsearch 有三个配置文件：

* 'elasticsearch.yml' 用于配置 Elasticsearch ;
* 'jvm.options' 用于配置 Elasticsearch JVM 设置 ;
* 'log4j2.properties' 用于配置 Elasticsearch 日志记录

这些文件位于 config 目录中，其默认位置取决于安装是来自归档发行版('tar.gz 或 'zip')还是软件包发行版(Debian 或 RPM 软件包)。

对于归档分发，配置目录位置默认为"$ES_HOME/config"。配置目录的位置可以通过"ES_PATH_CONF"环境变量更改，如下所示：

    
    
    ES_PATH_CONF=/path/to/my/config 
    ./bin/elasticsearch

或者，您可以通过命令行或通过 shell 配置文件"导出""ES_PATH_CONF"环境变量。

对于软件包发行版，配置目录位置默认为'/etc/elasticsearch'。配置目录的位置也可以通过"ES_PATH_CONF"环境变量进行更改，但请注意，在 shell 中设置此位置是不够的。相反，这个变量来源于'/etc/default/elasticsearch'(对于Debian软件包)和'/etc/sysconfig/elasticsearch'(对于RPM软件包)。您需要相应地编辑其中一个文件中的"ES_PATH_CONF=/etc/elasticsearch"条目以更改配置目录位置。

### 配置文件格式

配置格式为 YAML。下面是更改数据和日志目录路径的示例：
    
    path:
        data: /var/lib/elasticsearch
        logs: /var/log/elasticsearch

还可以按如下方式拼合设置：
    
    path.data: /var/lib/elasticsearch
    path.logs: /var/log/elasticsearch

在 YAML 中，可以将非标量值的格式设置为序列：
    discovery.seed_hosts:
       - 192.168.1.10:9300
       - 192.168.1.11
       - seeds.mydomain.com

虽然不太常见，但您也可以将非标量值格式化为数组：

    
    
    discovery.seed_hosts: ["192.168.1.10:9300", "192.168.1.11", "seeds.mydomain.com"]

### 环境变量替换

使用 '${...} 引用的环境变量配置文件中的 ' 表示法将替换为环境变量的值。例如：

    
    
    node.name:    ${HOSTNAME}
    network.host: ${ES_NETWORK_HOST}

环境变量的值必须是简单字符串。使用逗号分隔的字符串来提供 Elasticsearch 将解析为列表的值。例如，Elasticsearch 会将以下字符串拆分为"${HOSTNAME}"环境变量的值列表：

    
    
    export HOSTNAME="host1,host2"

### 群集和节点设置类型

群集和节点设置可以根据其配置方式进行分类：

Dynamic

    

您可以使用群集更新设置 API 在正在运行的群集上配置和更新动态设置。您还可以使用"elasticsearch.yml"在未启动或关闭节点上本地配置动态设置。

使用群集更新设置 API 进行的更新可以是 _persistent_ (适用于群集重新启动)或 _transient_ (在群集重新启动后重置)。您还可以通过使用 API 为其分配"null"值来重置瞬态或持久性设置。

如果使用多种方法配置相同的设置，则 Elasticsearch 将按以下优先级顺序应用这些设置：

1. 瞬态设置 2.持久设置 3."弹性搜索.yml"设置 4.默认设置值

例如，您可以应用瞬态设置来覆盖持久性设置或"弹性搜索.yml"设置。但是，对"elasticsearch.yml"设置的更改不会覆盖定义的瞬态或持久性设置。

如果使用 Elasticsearch Service，请使用用户设置功能配置所有集群设置。此方法允许 Elasticsearch Service 自动拒绝可能破坏集群的不安全设置。

如果您在自己的硬件上运行 Elasticsearch，请使用集群更新设置 API 来配置动态集群设置。仅使用"elasticsearch.yml"作为静态群集设置和节点设置。API 不需要重启，并确保设置的值在所有节点上都相同。

不再建议使用瞬态群集设置。请改用持久群集设置。如果群集变得不稳定，则暂时性设置可能会意外清除，从而导致可能不需要的群集配置。请参阅瞬态设置迁移指南。

Static

    

静态设置只能在未启动或关闭的节点上使用'elasticsearch.yml'进行配置。

必须在群集中的每个相关节点上设置静态设置。

[« Run Elasticsearch locally](run-elasticsearch-locally.md) [Important
Elasticsearch configuration »](important-settings.md)
