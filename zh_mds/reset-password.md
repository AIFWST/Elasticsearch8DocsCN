

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Command
line tools](commands.md)

[« elasticsearch-reconfigure-node](reconfigure-node.md) [elasticsearch-saml-
metadata »](saml-metadata.md)

## 弹性搜索-重置-密码

"弹性搜索-重置-密码"命令重置本机领域中的用户和内置用户的密码。

###Synopsis

    
    
    bin/elasticsearch-reset-password
    [-a, --auto] [-b, --batch] [-E <KeyValuePair]
    [-f, --force] [-h, --help] [-i, --interactive]
    [-s, --silent] [-u, --username] [--url] [-v, --verbose]

###Description

使用此命令可重置本机域中的任何用户或任何内置用户的密码。默认情况下，会为您生成一个强密码。要显式设置密码，请使用"-i"在交互模式下运行该工具。该命令在 filerealm 中生成(并随后删除)一个临时用户来运行更改用户密码的请求。

如果在"弹性搜索.yml"文件中禁用了文件领域，则无法使用此工具。

此命令使用 HTTP 连接连接到群集并运行用户管理请求。该命令自动尝试通过使用"elasticsearch.yml"文件中的"xpack.security.http.ssl"设置通过HTTPS建立连接。如果不使用默认的配置目录位置，请确保在运行"弹性搜索-重置密码"命令之前，"ES_PATH_CONF"环境变量返回正确的路径。您可以使用"-E"命令选项覆盖"elasticsearch.yml"文件中的设置。有关调试连接失败的详细信息，请参阅安装密码命令由于连接失败而失败。

###Parameters

'-a， --auto'

     Resets the password of the specified user to an auto-generated strong password. (Default) 
`-b, --batch`

     Runs the reset password process without prompting the user for verification. 
`-E <KeyValuePair>`

     Configures a standard Elasticsearch or X-Pack setting. 
`-f, --force`

     Forces the command to run against an unhealthy cluster. 
`-h, --help`

     Returns all of the command parameters. 
`-i, --interactive`

     Prompts for the password of the specified user. Use this option to explicitly set a password. 
`-s --silent`

     Shows minimal output in the console. 
`-u, --username`

     The username of the native realm user or built-in user. 
`--url`

     Specifies the base URL (hostname and port of the local node) that the tool uses to submit API requests to Elasticsearch. The default value is determined from the settings in your `elasticsearch.yml` file. If `xpack.security.http.ssl.enabled` is set to `true`, you must specify an HTTPS URL. 
`-v --verbose`

     Shows verbose output in the console. 

###Examples

以下示例将"弹性"用户的密码重置为自动生成的值，并在控制台中打印新密码：

    
    
    bin/elasticsearch-reset-password -u elastic

以下示例在终端中提示输入所需密码后，使用用户名"user1"重置本机用户的密码：

    
    
    bin/elasticsearch-reset-password --username user1 -i

以下示例将用户名为"user2"的本机用户的密码重置为自动生成的值，以在控制台中打印新密码。指定的 URL 指示弹性搜索重置密码工具尝试访问本地 Elasticsearch 节点的位置：

    
    
    bin/elasticsearch-reset-password --url "https://172.0.0.3:9200" --username user2 -i

[« elasticsearch-reconfigure-node](reconfigure-node.md) [elasticsearch-saml-
metadata »](saml-metadata.md)
