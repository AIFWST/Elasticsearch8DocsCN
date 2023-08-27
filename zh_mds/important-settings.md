

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Configuring Elasticsearch](settings.md) [Secure settings »](secure-
settings.md)

## 重要的弹性搜索配置

Elasticsearch 只需要很少的配置即可开始，但在使用集群生产之前，必须考虑的项目数量：

* 路径设置
* 群集名称设置
* 节点名称设置
* 网络主机设置 
* 发现设置
* 堆大小设置 
* JVM 堆转储路径设置 
* GC 日志记录设置
* 临时目录设置
* JVM 致命错误日志设置 
* 群集备份

我们的 Elastic 云服务会自动配置这些项目，默认情况下使您的集群可用于生产。

#### 路径设置

Elasticsearch 将索引到索引的数据写入，并将数据流写入"data"目录。Elasticsearch 将自己的应用程序日志(其中包含有关集群运行状况和操作的信息)写入"logs"目录。

对于macOS".tar.gz"，Linux".tar.gz"和Windows".zip"安装，默认情况下，"data"和"logs"是"$ES_HOME"的子目录。但是，"$ES_HOME"中的文件在升级过程中有删除的风险。

在生产环境中，我们强烈建议您将"elasticsearch.yml"中的"path.data"和"path.logs"设置为"$ES_HOME"之外的位置。默认情况下，Docker、Debian 和 RPM 安装将数据和日志写入 '$ES_HOME' 之外的位置。

支持的"path.data"和"path.logs"值因平台而异：

类Unix系统窗口

Linux 和 macOS 安装支持 Unix 样式的路径：

    
    
    path:
      data: /var/data/elasticsearch
      logs: /var/log/elasticsearch

Windows 安装支持带有转义反斜杠的 DOS 路径：
   
    path:
      data: "C:\\Elastic\\Elasticsearch\\data"
      logs: "C:\\Elastic\\Elasticsearch\\logs"

不要修改数据目录中的任何内容，也不要运行可能干扰其内容的进程。如果 Elasticsearch 以外的内容修改了数据目录的内容，那么 Elasticsearch 可能会失败，报告损坏或其他数据不一致，或者看起来工作正常，因为静默丢失了一些数据。不要尝试对数据目录进行文件系统备份;没有受支持的方法来还原此类备份。请改用快照和还原来安全地进行备份。不要在数据目录上运行病毒扫描程序。病毒扫描程序可能会阻止 Elasticsearch 正常工作，并可能修改数据目录的内容。数据目录不包含可执行文件，因此病毒扫描只会发现误报。

#### 多个数据路径

在 7.13.0 中已弃用。

如果需要，您可以在"path.data"中指定多个路径。Elasticsearch 将节点的数据存储在所有提供的路径上，但将每个分片的数据保留在同一路径上。

Elasticsearch 不会在节点的数据路径之间平衡分片。单个路径中的高磁盘使用率可能会触发整个节点的高磁盘使用率水线。如果触发，Elasticsearch 将不会向节点添加分片，即使节点的其他路径有可用磁盘空间也是如此。如果需要额外的磁盘空间，我们建议您添加新节点而不是额外的数据路径。

类Unix系统窗口

Linux 和 macOS 安装支持"path.data"中的多个 Unix 样式路径：

    
    
    path:
      data:
        - /mnt/elasticsearch_1
        - /mnt/elasticsearch_2
        - /mnt/elasticsearch_3

Windows安装支持"path.data"中的多个DOS路径：

    
    
    path:
      data:
        - "C:\\Elastic\\Elasticsearch_1"
        - "E:\\Elastic\\Elasticsearch_1"
        - "F:\\Elastic\\Elasticsearch_3"

#### 从多个数据路径迁移

对多个数据路径的支持在 7.13 中已弃用，并将在将来的版本中删除。

作为多个数据路径的替代方法，您可以创建一个跨多个磁盘的文件系统，其中包含硬件虚拟化层(如 RAID)或软件虚拟化层(如 Linux 上的逻辑卷管理器 (LVM)或 Windows 上的存储空间)。如果您希望在一台计算机上使用多个数据路径，则必须为每个数据路径运行一个节点。

如果您当前在高可用性群集中使用多个数据路径，则可以迁移到对每个节点使用单个路径而不会停机的设置，使用类似于滚动重启的过程：依次关闭每个节点并将其替换为一个或多个节点，每个节点配置为使用单个数据路径。更详细地说，对于当前具有多个数据路径的每个节点，应遵循以下过程。原则上，您可以在滚动升级到 8.0 期间执行此迁移，但我们建议在开始升级之前迁移到单数据路径设置。

1. 拍摄快照以在发生灾难时保护您的数据。  2. (可选)使用分配过滤器将数据从目标节点迁移出去： 响应 = client.cluster.put_settings( 正文： { 持久： { "cluster.routing.allocation.exclude._name"： '目标节点名称' } } ) 放置响应 放置 _cluster/设置 { "持久"： { "cluster.routing.allocation.exclude._name"： "目标节点名称" } }

您可以使用 cat 分配 API 来跟踪此数据迁移的进度。如果某些分片没有迁移，则集群分配解释API将帮助您确定原因。

3. 按照滚动重启过程中的步骤操作，包括关闭目标节点。  4. 确保您的集群运行状况为"黄色"或"绿色"，以便将每个分片的副本分配给集群中的至少一个其他节点。  5. 如果适用，请删除在上一步中应用的分配筛选器。           响应 = client.cluster.put_settings( body： { 持久： { "cluster.routing.allocation.exclude._name"： nil } } ) 放置响应 PUT _cluster/设置 { "持久"： { "cluster.routing.allocation.exclude._name"： null } }

6. 通过删除其数据路径的内容来丢弃停止节点持有的数据。  7. 重新配置您的存储。例如，使用 LVM 或存储空间将磁盘合并到单个文件系统中。确保重新配置的存储有足够的空间来容纳它将保存的数据。  8. 通过调整节点"elasticsearch.yml"文件中的"path.data"设置来重新配置节点。如果需要，请安装更多节点，每个节点都有自己的"path.data"设置，指向单独的数据路径。  9. 启动新节点，然后执行滚动重启过程的其余部分。  10. 确保您的集群运行状况为"绿色"，以便分配每个分片。

您也可以将一定数量的单数据路径节点添加到群集，使用分配筛选器将所有数据迁移到这些新节点，然后从群集中删除旧节点。此方法将暂时将群集的大小加倍，因此仅当您有能力像这样扩展群集时，此方法才有效。

如果您当前使用多个数据路径，但您的集群可用性不高，则可以通过拍摄快照、创建具有所需配置的新集群并将快照还原到其中来迁移到未弃用的配置。

#### 群集名称设置

节点只有在与集群中的所有其他节点共享其"cluster.name"时才能加入集群。默认名称是"elasticsearch"，但您应该将其更改为描述集群用途的适当名称。

    
    
    cluster.name: logging-prod

不要在不同的环境中重复使用相同的集群名称。否则，节点可能会加入错误的群集。

更改群集的名称需要完全重新启动群集。

#### 节点名称设置

Elasticsearch 使用"node.name"作为 Elasticsearch 特定实例的人类可读标识符。节点名称默认为Elasticsearch启动时机器的主机名，但可以在"elasticsearch.yml"中显式配置：

    
    
    node.name: prod-data-2

#### 网络主机设置

默认情况下，Elasticsearch 只绑定到环回地址，例如 '127.0.0.1' 和 '：：1]'。这足以在单个服务器上运行一个或多个节点的群集以进行开发和测试，但 [弹性生产群集必须涉及其他服务器上的节点。有许多网络设置，但通常您只需要配置"network.host"：

    
    
    network.host: 192.168.1.10

当您为"network.host"提供值时，Elasticsearch 假定您正在从开发模式切换到生产模式，并将许多系统启动检查从警告升级到异常。查看开发和生产模式之间的差异。

#### 发现和集群形成设置

在进入生产环境之前配置两个重要的发现和集群形成设置，以便集群中的节点可以相互发现并选择主节点。

#####'discovery.seed_hosts'

开箱即用，无需任何网络配置，Elasticsearch 将绑定到可用的环回地址，并扫描本地端口"9300"到"9305"，以与在同一服务器上运行的其他节点连接。此行为提供自动群集体验，而无需执行任何配置。

如果要与其他主机上的节点形成群集，请使用静态"discovery.seed_hosts"设置。此设置提供群集中符合主节点条件的其他节点的列表，这些节点可能处于活动状态并可联系以设定发现过程的种子。此设置接受群集中所有符合主节点条件的地址的 YAML 序列或数组。每个地址可以是 IP 地址，也可以是通过 DNS 解析为一个或多个 IP 地址的主机名。

    
    
    discovery.seed_hosts:
       - 192.168.1.10:9300
       - 192.168.1.11 __- seeds.mydomain.com __- [0:0:0:0:0:ffff:c0a8:10c]:9301 __

__

|

该端口是可选的，默认为"9300"，但可以覆盖。   ---|---    __

|

如果主机名解析为多个 IP 地址，则节点将尝试发现所有解析地址的其他节点。   __

|

IPv6 地址必须括在方括号中。   如果符合主节点条件的节点没有固定的名称或地址，请使用备用主机提供程序动态查找其地址。

#####'cluster.initial_master_nodes'

首次启动 Elasticsearch 集群时，集群引导步骤会确定一组符合主节点条件的节点，这些节点的选票在第一次选举中计算。在开发模式下，配置了无发现设置后，此步骤由节点本身自动执行。

由于自动引导本质上是不安全的，因此在启动新的集群生产模式时，必须明确列出应在第一次选举中计入的主节点。您可以使用"cluster.initial_master_nodes"设置设置此列表。

首次成功形成群集后，从每个节点的配置中删除"cluster.initial_master_nodes"设置。重新启动群集或向现有群集添加新节点时，请勿使用此设置。

    
    
    discovery.seed_hosts:
       - 192.168.1.10:9300
       - 192.168.1.11
       - seeds.mydomain.com
       - [0:0:0:0:0:ffff:c0a8:10c]:9301
    cluster.initial_master_nodes: __- master-node-a
       - master-node-b
       - master-node-c

__

|

通过默认为主机名的"node.name"标识初始主节点。确保"cluster.initial_master_nodes"中的值与"node.name"完全匹配。如果使用完全限定域名 (FQDN)，例如"主节点 a.example.com"作为节点名称，则必须在此列表中使用 FQDN。相反，如果"node.name"是没有任何尾随限定符的裸主机名，则还必须省略 'cluster.initial_master_nodes' 中的尾随限定符。   ---|--- 请参阅引导集群和发现和集群形成设置。

#### 堆大小设置

默认情况下，Elasticsearch 会根据阳极的角色和总内存自动设置 JVM 堆大小。我们建议对大多数生产环境使用默认大小调整。

如果需要，您可以通过手动设置 JVMheap 大小来覆盖默认大小。

#### JVM 堆转储路径设置

默认情况下，Elasticsearch 将 JVM 配置为将堆转储到内存不足异常到默认数据目录。在 RPM 和 Debian 软件包上，数据目录是 '/var/lib/elasticsearch'。在Linux和MacOS以及Windows发行版中，"data"目录位于Elasticsearch安装的根目录下。

如果此路径不适合接收堆转储，请修改"jvm.options"中的"-XX：HeapDumpPath=..."条目：

* 如果指定目录，JVM 将根据正在运行的实例的 PID 为堆转储生成文件名。  * 如果指定固定文件名而不是目录，那么当 JVM 需要对内存不足异常执行堆转储时，该文件必须不存在。否则，堆转储将失败。

#### GC 日志记录设置

默认情况下，Elasticsearch 启用垃圾回收 (GC) 日志。它们在"jvm.options"中配置，并输出到与Elasticsearchlogs相同的默认位置。默认配置每 64 MB 轮换一次日志，最多可占用 2 GB 磁盘空间。

您可以使用 JEP 158：统一 JVM 日志记录中所述的命令行选项重新配置 JVM 日志记录。除非您直接更改默认的"jvm.options"文件，否则除了您自己的设置之外，还会应用 Elasticsearch 默认配置。要禁用默认配置，请首先通过提供"-Xlog：disable"选项禁用日志记录，然后提供您自己的命令行选项。这将禁用_all_ JVMlogging，因此请务必查看可用选项并启用所需的所有内容。

要查看原始 JEP 中未包含的更多选项，请参阅使用 JVM 统一日志记录框架启用日志记录。

####Examples

通过使用一些示例选项创建"$ES_HOME/config/jvm.options.d/gc.options"，将默认的 GC 日志输出位置更改为"/opt/my-app/gc.log"：

    
    
    # Turn off all previous logging configuratons
    -Xlog:disable
    
    # Default settings from JEP 158, but with `utctime` instead of `uptime` to match the next line
    -Xlog:all=warning:stderr:utctime,level,tags
    
    # Enable GC logging to a custom location with a variety of options
    -Xlog:gc*,gc+age=trace,safepoint:file=/opt/my-app/gc.log:utctime,level,pid,tags:filecount=32,filesize=64m

配置 Elasticsearch Docker 容器以将 GC 调试日志发送到标准错误('stderr')。这允许容器业务流程协调程序处理输出。如果使用"ES_JAVA_OPTS"环境变量，请指定：

    
    
    MY_OPTS="-Xlog:disable -Xlog:all=warning:stderr:utctime,level,tags -Xlog:gc=debug:stderr:utctime"
    docker run -e ES_JAVA_OPTS="$MY_OPTS" # etc

#### 临时目录设置

默认情况下，Elasticsearch 使用一个私有临时目录，启动脚本会在系统临时目录下方立即创建该目录。

在某些 Linux 发行版上，如果最近没有访问过文件和目录，系统实用程序将从"/tmp"中清除它们。如果长时间不使用需要临时目录的功能，则此行为可能会导致在 Elasticsearch 运行时删除私有临时目录。如果随后使用需要此目录的功能，则删除专用临时目录会导致问题。

如果您使用 '.deb' 或 '.rpm' 软件包安装 Elasticsearch，并在 'systemd' 下运行它，那么 Elasticsearch 使用的私有临时目录将被排除在定期清理之外。

如果您打算在 Linux 或 MacOS 上运行".tar.gz"发行版，请考虑为 Elasticsearch 创建一个专用的临时目录，该目录不在将从中清除旧文件和目录的路径下。此目录应设置权限，以便只有运行 Elasticsearch 的用户才能访问它。然后，在启动 Elasticsearch 之前，将 '$ES_TMPDIR' 环境变量设置为指向此目录。

#### JVM 致命错误日志设置

默认情况下，Elasticsearch 将 JVM 配置为将致命错误日志写入默认日志记录目录。在 RPM和 Debian 软件包上，这个目录是 '/var/log/elasticsearch'。在 Linux 和 MacOS 以及 Windows 发行版上，"logs"目录位于 Elasticsearch 安装的根目录下。

这些是 JVM 在遇到致命错误(例如分段错误)时生成的日志。如果此路径不适合接收日志，请修改"jvm.options"中的"-XX：ErrorFile=..."条目。

#### 群集备份

在灾难中，快照可以防止永久性数据丢失。快照生命周期管理是定期备份集群的最简单方法。有关详细信息，see_Create snapshot_。

**拍摄快照是备份集群的唯一可靠且受支持的方法。 您无法通过复制 Elasticsearch 集群节点的数据目录来备份集群。没有支持的方法可以从文件系统级备份恢复任何数据。如果尝试从此类备份还原群集，则群集可能会失败，并报告损坏或丢失文件或其他数据不一致，或者看起来已成功丢失某些数据。

[« Configuring Elasticsearch](settings.md) [Secure settings »](secure-
settings.md)
