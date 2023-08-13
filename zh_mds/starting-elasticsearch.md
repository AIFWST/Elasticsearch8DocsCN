

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md)

[« Bootstrap Checks for X-Pack](bootstrap-checks-xpack.md) [Stopping
Elasticsearch »](stopping-elasticsearch.md)

## 启动弹性搜索

启动 Elasticsearch 的方法因安装方式而异。

### 存档包('.tar.gz')

如果您安装了带有".tar.gz"包的 Elasticsearch，则可以从命令行启动 Elasticsearch。

#### 从命令行运行 Elasticsearch

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

#### 运行方式为 adaemon

要将 Elasticsearch 作为守护进程运行，请在命令行上指定"-d"，并使用"-p"选项将进程 ID 记录在文件中：

    
    
    ./bin/elasticsearch -d -p pid

如果您已对 Elasticsearch 密钥库进行密码保护，系统将提示您输入密钥库的密码。有关更多详细信息，请参阅安全设置。

日志消息可以在'$ES_HOME/logs/'目录中找到。

要关闭 Elasticsearch，请终止 'pid' 文件中记录的进程 ID：

    
    
    pkill -F pid

Elasticsearch '.tar.gz' 包不包含 'systemd' 模块。要将 Elasticsearch 作为服务进行管理，请改用 Debian 或 RPM 软件包。

### 存档包('.zip')

如果你在Windows上安装了带有".zip"包的Elasticsearch，你可以从命令行启动Elasticsearch。如果您希望 Elasticsearch 在启动时自动启动，无需任何用户交互，请安装Elasticsearch 作为服务。

#### 从命令行运行 Elasticsearch

运行以下命令，从命令行启动 Elasticsearch：

    
    
    .\bin\elasticsearch.bat

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
    'bin\elasticsearch-reset-password -u elastic'.
    
    Generate an enrollment token for Kibana instances with
    'bin\elasticsearch-create-enrollment-token -s kibana'.
    
    Generate an enrollment token for Elasticsearch nodes with
    'bin\elasticsearch-create-enrollment-token -s node'.

如果您已对 Elasticsearch 密钥库进行密码保护，系统将提示您输入密钥库的密码。有关更多详细信息，请参阅安全设置。

默认情况下，Elasticsearch 将其日志打印到控制台("STDOUT")和日志目录中的"集群名称>.log"<"文件。Elasticsearch在启动时会记录一些信息，但是在完成初始化后，它将继续在前台运行，并且不会进一步记录任何内容，直到发生值得记录的事情。当Elasticsearch运行时，你可以通过它的HTTP接口与它进行交互，该接口默认位于端口"9200"上。

要停止 Elasticsearch，请按"Ctrl-C"。

#### 在现有群集中注册节点

当 Elasticsearch 首次启动时，安全自动配置过程会将 HTTP 层绑定到 '0.0.0.0'，但只将传输层绑定到 localhost。此预期行为可确保您可以在默认情况下启用安全性的情况下启动单节点群集，而无需任何其他配置。

在注册新节点之前，在生产集群中通常需要执行其他操作，例如绑定到地址而不是"localhost"或满足引导程序检查。在此期间，自动生成的注册令牌可能会过期，这就是不会自动生成注册令牌的原因。

此外，只有同一主机上的节点才能加入群集，而无需其他配置。如果您希望来自其他主机的节点加入您的集群，则需要将"transport.host"设置为支持的值(例如取消注释建议值"0.0.0.0")，或者绑定到其他主机可以访问的接口的 IP 地址。有关详细信息，请参阅传输设置。

要在群集中注册新节点，请在群集中的任何现有节点上使用"弹性搜索-创建-注册令牌"工具创建注册令牌。然后，您可以使用"--enrollment-token"参数启动新节点，以便它加入现有集群。

1. 在运行 Elasticsearch 的单独终端中，导航到安装 Elasticsearch 的目录，然后运行"elasticsearch-create-enrollment-token"工具，为您的新节点生成注册令牌。           bin\elasticsearch-create-enrollment-token -s 节点

复制注册令牌，您将使用该令牌向 Elasticsearch 集群注册新节点。

2. 在新节点的安装目录中，启动 Elasticsearch 并使用"--enrollment-token"参数传递注册令牌。           bin\elasticsearch --enrollment-token <enrollment-token>

Elasticsearch 会在以下目录中自动生成证书和密钥：

    
        config\certs

3. 对要注册的任何新节点重复上一步。

### Debian软件包

#### 使用 'systemd' 运行 Elasticsearch

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

### Dockerimages

如果你安装了 Docker 镜像，你可以从命令行启动 Elasticsearch。根据使用的是开发模式还是生产模式，有不同的方法。请参阅使用 Docker 启动单节点群集。

### RPM包

#### 使用 'systemd' 运行 Elasticsearch

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

[« Bootstrap Checks for X-Pack](bootstrap-checks-xpack.md) [Stopping
Elasticsearch »](stopping-elasticsearch.md)
