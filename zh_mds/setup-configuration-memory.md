

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Important system configuration](system-
config.md)

[« Configuring system settings](setting-system-settings.md) [File
Descriptors »](file-descriptors.md)

## 禁用交换

大多数操作系统尝试将尽可能多的内存用于文件系统缓存，并急切地交换未使用的应用程序内存。这可能导致 JVM 堆的某些部分甚至其可执行页面被换出到磁盘。

交换对性能和节点稳定性非常不利，应不惜一切代价避免交换。它可能导致垃圾回收持续**分钟**而不是毫秒，并可能导致节点响应缓慢，甚至与群集断开连接。在弹性分布式系统中，让操作系统杀死节点更有效。

有三种方法可以禁用交换。首选选项是完全禁用交换。如果这不是一个选项，是否首选最小化交换与内存锁定取决于您的环境。

### 禁用所有交换文件

通常 Elasticsearch 是唯一在机器上运行的服务，它的内存使用由 JVM 选项控制。应该不需要启用交换。

在 Linux 系统上，您可以通过运行以下命令暂时禁用交换：

    
    
    sudo swapoff -a

这不需要重新启动 Elasticsearch。

要永久禁用它，您需要编辑"/etc/fstab"文件并注释掉任何包含"swap"一词的行。

在Windows上，可以通过"系统属性→高级→性能→高级→虚拟内存"完全禁用分页文件来实现等效。

### 配置"交换"

Linux 系统上可用的另一个选项是确保 sysctl 值"vm.swappiness"设置为"1"。这减少了内核的交换倾向，并且在正常情况下不会导致交换，同时仍然允许整个系统在紧急情况下交换。

### 启用"bootstrap.memory_lock"

另一种选择是使用Linux/Unix系统上的mlockall或Windows上的VirtualLock，尝试将进程地址空间锁定到RAM中，防止任何Elasticsearch堆内存被换出。

使用内存锁时，某些平台仍会交换堆外内存。要防止堆外内存交换，请改为禁用所有交换文件。

要启用内存锁定，请在"elasticsearch.yml"中将"bootstrap.memory_lock"设置为"true"：

    
    
    bootstrap.memory_lock: true

'mlockall' 可能会导致 JVM 或 shell 会话退出，如果它尝试分配的内存多于可用内存！

启动 Elasticsearch 后，您可以通过检查此请求输出中的 'mlockall' 值来查看此设置是否成功应用：

    
    
    response = client.nodes.info(
      filter_path: '**.mlockall'
    )
    puts response
    
    
    GET _nodes?filter_path=**.mlockall

如果您看到"mlockall"是"false"，则表示"mlockall"请求失败。您还将在日志中看到一行包含更多信息的行，其中包含"无法锁定 JVM 内存"字样。

在Linux/Unix系统上，最可能的原因是运行Elasticsearch的用户没有锁定内存的权限。可以按以下方式授予：

".zip"和".tar.gz"

    

在启动 Elasticsearch 之前设置 'ulimit -l unlimited' asroot。或者，在"/etc/security/limits.conf"中将"memlock"设置为"unlimited"：

    
    
    # allow user 'elasticsearch' mlockall
    elasticsearch soft memlock unlimited
    elasticsearch hard memlock unlimited

RPM 和 Debian

     Set `LimitMEMLOCK` to `infinity` in the [systemd configuration](setting-system-settings.html#systemd "Systemd configuration"). 

"mlockall"失败的另一个可能原因是JNA临时目录(通常是"/tmp"的子目录)使用"noexec"选项挂载。这可以通过使用"ES_JAVA_OPTS"环境变量为 JNA 指定一个新的临时目录来解决：

    
    
    export ES_JAVA_OPTS="$ES_JAVA_OPTS -Djna.tmpdir=<path>"
    ./bin/elasticsearch

或在 jvm.options 配置文件中设置此 JVM 标志。

[« Configuring system settings](setting-system-settings.md) [File
Descriptors »](file-descriptors.md)
