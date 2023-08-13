

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Command
line tools](commands.md)

[« elasticsearch-node](node-tool.md) [elasticsearch-reset-password »](reset-
password.md)

## 弹性搜索-重新配置-节点

"elasticsearch-reconfigure-node"工具通过RPM或DEB软件包安装的Elasticsearch节点重新配置，以加入启用了安全功能的现有集群。

###Synopsis

    
    
    bin/elasticsearch-reconfigure-node
    [--enrollment-token] [-h, --help] [-E <KeyValuePair>]
    [-s, --silent] [-v, --verbose]

###Description

使用 DEB 或 RPM 包安装 Elasticsearch 时，假定当前节点是集群中的第一个节点。Elasticsearch在节点上启用和配置安全功能，为"弹性"超级用户生成密码，并为HTTP和传输层配置TLS。

您可以将节点添加到已启用和配置安全功能的现有群集，而不是形成单节点群集。在启动新节点之前，请使用"-s 节点"选项运行"弹性搜索-创建-注册令牌"工具，以在现有群集中的任何节点上生成注册令牌。在新节点上，运行"弹性搜索-重新配置-节点"工具，并将注册令牌作为参数传递。

此工具仅用于 Elasticsearch 的 DEB 或 RPM 发行版。

你必须使用"sudo"运行此工具，以便它可以编辑 Elasticsearch 安装配置目录中由 'root：elasticsearch' 拥有的必要文件。

###Parameters

`--enrollment-token`

     The enrollment token, which can be generated on any of the nodes in an existing, secured cluster. 
`-E <KeyValuePair>`

     Configures a standard Elasticsearch or X-Pack setting. 
`-h, --help`

     Shows help information. 
`-s, --silent`

     Shows minimal output. 
`-v, --verbose`

     Shows verbose output. 

#### JVMoptions

CLI 工具使用 64MB 的堆运行。对于大多数工具，此值都很好。但是，如果需要，可以通过设置CLI_JAVA_OPTS环境变量来覆盖它。例如，以下内容将"重新配置节点"工具使用的堆大小增加到 1GB。

    
    
    export CLI_JAVA_OPTS="-Xmx1g"
    bin/elasticsearch-reconfigure-node ...

###Examples

以下示例重新配置已安装的 Elasticsearch 节点，以便它可以在首次启动时加入现有集群。

    
    
    sudo /usr/share/elasticsearch/elasticsearch-reconfigure-node --enrollment-token eyJ2ZXIiOiI4LjAuMCIsImFkciI6WyIxOTIuMTY4LjEuMTY6OTIwMCJdLCJmZ3IiOiI4NGVhYzkyMzAyMWQ1MjcyMmQxNTFhMTQwZmM2ODI5NmE5OWNiNmU0OGVhZjYwYWMxYzljM2I3ZDJjOTg2YTk3Iiwia2V5IjoiUy0yUjFINEJrNlFTMkNEY1dVV1g6QS0wSmJxM3hTRy1haWxoQTdPWVduZyJ9

[« elasticsearch-node](node-tool.md) [elasticsearch-reset-password »](reset-
password.md)
