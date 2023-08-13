

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Important system configuration](system-
config.md)

[« Important system configuration](system-config.md) [Disable swapping
»](setup-configuration-memory.md)

## 配置系统设置

在何处配置系统设置取决于您用于安装 Elasticsearch 的软件包以及您使用的操作系统。

使用".zip"或".tar.gz"软件包时，可以配置系统设置：

* 暂时使用"ulimit"。  * 永久在 '/etc/security/limits.conf' 中。

使用 RPM 或 Debian 软件包时，大多数系统设置都在系统配置文件中设置。但是，使用 systemd 的系统要求在 systemd 配置文件中指定系统限制。

###'ulimit'

在 Linux 系统上，"ulimit"可用于临时更改资源限制。在切换到将运行 Elasticsearch 的用户之前，通常需要将限制设置为"root"。例如，要将打开文件句柄 ('ulimit -n') 的数量设置为 65，536，您可以执行以下操作：

    
    
    sudo su  __ulimit -n 65535 __su elasticsearch __

__

|

成为"根"。   ---|---    __

|

更改打开文件的最大数量。   __

|

成为"elasticsearch"用户以启动Elasticsearch。   新限制仅在当前会话期间应用。

您可以使用"ulimit -a"查阅所有当前应用的限制。

###'/etc/security/limits.conf'

在 Linux 系统上，可以通过编辑"/etc/security/limits.conf"文件为特定用户设置持久限制。要将 'elasticsearch' 用户的最大打开文件数设置为 65，535，请将以下行添加到 'limits.conf' 文件中：

    
    
    elasticsearch  -  nofile  65535

此更改仅在"弹性搜索"用户下次打开新会话时生效。

### Ubuntu 和 'limits.conf'

Ubuntu 忽略了由 'init.d' 启动的进程的 'limits.conf' 文件。要启用"limits.conf"文件，请编辑"/etc/pam.d/su"并取消注释以下行：

    
    
    # session    required   pam_limits.so

### 系统配置文件

使用 RPM 或 Debian 软件包时，可以在系统配置文件中指定环境变量，该文件位于：

RPM

|

'/etc/sysconfig/elasticsearch' ---|--- Debian

|

'/etc/default/elasticsearch' 但是，系统限制需要通过 systemd 指定。

### 系统配置

在使用 systemd 的系统上使用 RPM 或 Debian 软件包时，必须通过 systemd 指定系统限制。

systemd 服务文件 ('/usr/lib/systemd/system/elasticsearch.service')包含默认应用的限制。

要覆盖它们，请添加一个名为'/etc/systemd/system/elasticsearch.service.d/override.conf'的文件(或者，你可以运行'sudo systemctl edit elasticsearch'，它会在默认编辑器中自动打开文件)。设置此文件中的任何更改，例如：

    
    
    [Service]
    LimitMEMLOCK=infinity

完成后，运行以下命令以重新加载单元：

    
    
    sudo systemctl daemon-reload

[« Important system configuration](system-config.md) [Disable swapping
»](setup-configuration-memory.md)
