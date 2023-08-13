

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Command
line tools](commands.md)

[« elasticsearch-service-tokens](service-tokens-command.md) [elasticsearch-
shard »](shard-tool.md)

## 弹性搜索设置密码

### 在 8.0 中已弃用。

"elasticsearch-setup-passwords"工具已被弃用，并将在未来的版本中删除。要手动重置内置用户(包括"弹性"用户)的密码，请使用"弹性搜索-重置-密码"工具、弹性搜索更改密码 API 或 Kibana 中的用户管理功能。

"弹性搜索设置密码"命令为内置用户设置密码。

###Synopsis

    
    
    bin/elasticsearch-setup-passwords auto|interactive
    [-b, --batch] [-h, --help] [-E <KeyValuePair>]
    [-s, --silent] [-u, --url "<URL>"] [-v, --verbose]

###Description

此命令仅用于在初始配置Elasticsearch安全功能期间使用。它使用"弹性"引导密码来运行用户管理 API 请求。如果您的 Elasticsearch 密钥库受密码保护，那么在为内置用户设置密码之前，必须先输入密钥库密码。为"弹性"用户设置密码后，引导密码不再有效，并且不能使用此命令。相反，您可以使用 Kibana 中的"用户管理>**管理**"UI 或更改密码 API 来更改密码。

此命令使用 HTTP 连接连接到群集并运行用户管理请求。如果您的集群在 HTTP 层上使用 TLS/SSL，则该命令会自动尝试使用 HTTPS 协议建立连接。它通过使用"elasticsearch.yml"文件中的"xpack.security.http.ssl"设置来配置连接。如果不使用默认的 configdirectory 位置，请确保在运行 'elasticsearch-setup-passwords' 命令之前，**ES_PATH_CONF** 环境变量返回正确的路径。您可以使用"-E"命令选项覆盖"elasticsearch.yml"文件中的设置。有关调试连接失败的详细信息，请参阅安装密码命令由于连接失败而失败。

###Parameters

`auto`

     Outputs randomly-generated passwords to the console. 
`-b, --batch`

     If enabled, runs the change password process without prompting the user. 
`-E <KeyValuePair>`

     Configures a standard Elasticsearch or X-Pack setting. 
`-h, --help`

     Shows help information. 
`interactive`

     Prompts you to manually enter passwords. 
`-s, --silent`

     Shows minimal output. 
`-u, --url "<URL>"`

     Specifies the URL that the tool uses to submit the user management API requests. The default value is determined from the settings in your `elasticsearch.yml` file. If `xpack.security.http.ssl.enabled` is set to `true`, you must specify an HTTPS URL. 
`-v, --verbose`

     Shows verbose output. 

###Examples

以下示例使用"-u"参数告知工具将其用户管理 API 请求提交到何处：

    
    
    bin/elasticsearch-setup-passwords auto -u "http://localhost:9201"

[« elasticsearch-service-tokens](service-tokens-command.md) [elasticsearch-
shard »](shard-tool.md)
