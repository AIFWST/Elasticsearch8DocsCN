

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Watcher settings in Elasticsearch](notification-settings.md) [Important
system configuration »](system-config.md)

## 高级配置

通常不建议修改高级设置，这可能会对性能和稳定性产生负面影响。在大多数情况下，建议使用 Elasticsearch 提供的默认值。

### 设置 JVM选项

如果需要，您可以通过添加定制选项文件(首选)或设置"ES_JAVA_OPTS"环境变量来覆盖缺省 JVM 选项。

JVM 选项文件必须具有后缀_.options_，并包含 JVM 参数的行分隔列表。JVM按字典顺序处理选项文件。

JVM 选项文件的放置位置取决于安装类型：

* tar.gz 或 .zip：将自定义 JVM 选项文件添加到 'config/jvm.options.d/'。  Debian 或 RPM：将自定义 JVM 选项文件添加到 '/etc/elasticsearch/jvm.options.d/'。  * Docker：将挂载自定义 JVM 选项文件绑定到"/usr/share/elasticsearch/config/jvm.options.d/"中。

不要修改根 'jvm.options' 文件。改用 'jvm.options.d/' 中的文件。

#### JVM 选项语法

JVM 选项文件包含以行分隔的 JVM 参数列表。参数前面有短划线 ('-')。若要将设置应用于特定版本，请在版本或版本范围前面加上冒号。

* 将设置应用于所有版本：-Xmx2g

* 将设置应用于特定版本：17：-Xmx2g

* 将设置应用于一系列版本：17-18：-Xmx2g

若要将设置应用于特定版本和任何更高版本，请省略范围的上限。例如，此设置适用于 Java 8 及更高版本：

    
        17-:-Xmx2g

空白行将被忽略。以"#"开头的行被视为注释并被忽略。未注释掉且未被识别为有效 JVMarguments 的行将被拒绝，Elasticsearch 将无法启动。

#### 使用环境变量设置 JVM选项

在生产中，使用 JVM 选项文件覆盖默认设置。在测试和开发环境中，您还可以通过"ES_JAVA_OPTS"环境变量设置 JVM 选项。

    
    
    export ES_JAVA_OPTS="$ES_JAVA_OPTS -Djava.io.tmpdir=/path/to/temp/dir"
    ./bin/elasticsearch

如果您使用的是 RPM 或 Debian 软件包，您可以在系统配置文件中指定"ES_JAVA_OPTS"。

Elasticsearch 忽略了"JAVA_TOOL_OPTIONS"和"JAVA_OPTS"环境变量。

### 设置 JVM 堆大小

默认情况下，Elasticsearch 会根据阳极的角色和总内存自动设置 JVM 堆大小。对于大多数生产环境，建议使用默认大小调整。

要覆盖默认堆大小，请设置最小和最大堆大小设置"Xms"和"Xmx"。最小值和最大值必须相同。

堆大小应基于可用 RAM：

*将"Xms"和"Xmx"设置为不超过总内存的50%。Elasticsearch 需要内存用于 JVM 堆以外的目的。例如，Elasticsearch 使用堆外缓冲区进行高效的网络通信，并依靠操作系统的文件系统缓存来高效访问文件。JVM本身也需要一些内存。Elasticsearch 使用的内存超过通过"Xmx"设置配置的限制是正常的。

在容器(如 Docker)中运行时，总内存定义为容器可见的内存量，而不是主机上的总系统内存量。

* 将"Xms"和"Xmx"设置为不超过压缩普通对象指针 (oops) 的阈值。确切的阈值各不相同，但 26GB 在大多数系统上是安全的，在某些系统上可以高达 30GB。要验证您是否低于阈值，请检查 Elasticsearch 日志中是否有如下条目：堆大小 [1.9GB]，压缩的普通对象指针 [true]

或者使用节点信息 API 检查节点的"jvm.using_compressed_ordinary_object_pointers"值：

    
        response = client.nodes.info(
      node_id: '_all',
      metric: 'jvm'
    )
    puts response
    
        GET _nodes/_all/jvm

Elasticsearch 可用的堆越多，它可用于内部缓存的内存就越多。这为操作系统留给文件系统缓存的内存更少。较大的堆也可能导致更长的垃圾回收暂停。

要配置堆大小，请将"Xms"和"Xmx"JVM 参数添加到扩展名为".options"的自定义 JVM 选项文件中，并将其存储在"jvm.options.d/"目录中。例如，要将最大堆大小设置为 2GB，请将"Xms"和"Xmx"都设置为"2g"：

    
    
    -Xms2g
    -Xmx2g

为了进行测试，您还可以使用"ES_JAVA_OPTS"环境变量设置堆大小：

    
    
    ES_JAVA_OPTS="-Xms2g -Xmx2g" ./bin/elasticsearch

"ES_JAVA_OPTS"变量覆盖所有其他 JVM 选项。我们不建议在生产中使用"ES_JAVA_OPTS"。

如果您将 Elasticsearch 作为 Windows 服务运行，则可以使用服务管理器更改堆大小。请参阅在 Windows 上安装和运行 Elasticsearch as aservice。

#### 启用 Elasticsearch TCP readinessport

此功能为技术预览版，可能会在将来的版本中进行更改或删除。Elastic 将尽最大努力修复任何问题，但技术预览版中的功能不受官方 GA 功能的 SLA 支持的约束。

如果已配置，节点可以在节点处于就绪状态时打开 TCP 端口。当阳极成功加入集群时，它被视为准备就绪。在单节点配置中，当节点能够接受请求时，它被称为准备就绪。

要启用就绪 TCP 端口，请使用"readyiness.port"设置。就绪服务将绑定到所有主机地址。

如果节点离开群集，或者使用关闭 API 将节点标记为关闭，则就绪端口将立即关闭。

成功连接到就绪 TCP 端口表示弹性搜索节点已准备就绪。当客户端连接到就绪端口时，服务器只是终止套接字连接。不会将任何数据发送回客户端。如果客户端无法连接到就绪端口，则节点未就绪。

[« Watcher settings in Elasticsearch](notification-settings.md) [Important
system configuration »](system-config.md)
