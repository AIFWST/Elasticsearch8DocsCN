

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Command
line tools](commands.md)

[« elasticsearch-certutil](certutil.md) [elasticsearch-croneval
»](elasticsearch-croneval.md)

## 弹性搜索-创建-注册-令牌

'elasticsearch-create-enrollment-token' 命令为 Elasticsearch 节点和 Kibana 实例创建注册令牌。

###Synopsis

    
    
    bin/elasticsearch-create-enrollment-token
    [-f, --force] [-h, --help] [-E <KeyValuePair>] [-s, --scope] [--url]

###Description

"elasticsearch-create-enrollment-token"只能与自动配置安全性的 Elasticsearchclusters 一起使用。

使用此命令创建注册令牌，您可以使用这些令牌将 newElasticsearch 节点注册到现有集群，或配置 Kibana 实例以与启用了安全功能的现有 Elasticsearch 集群进行通信。该命令在文件域中生成(并随后删除)一个临时用户，以运行创建注册令牌的请求。

如果在"弹性搜索.yml"文件中禁用了文件领域，则无法使用此工具。

此命令使用 HTTP 连接连接到群集并运行用户管理请求。该命令自动尝试通过使用"elasticsearch.yml"文件中的"xpack.security.http.ssl"设置通过HTTPS建立连接。如果不使用默认配置目录，请确保在运行"弹性搜索-创建-注册-令牌"命令之前，"ES_PATH_CONF"环境变量返回正确的路径。您可以使用"-E"命令选项覆盖"elasticsearch.yml"文件中的设置。有关调试连接失败的详细信息，请参阅安装密码命令由于连接失败而失败。

###Parameters

'-E<KeyValuePair>'

     Configures a standard Elasticsearch or X-Pack setting. 
`-f, --force`

     Forces the command to run against an unhealthy cluster. 
`-h, --help`

     Returns all of the command parameters. 
`-s, --scope`

     Specifies the scope of the generated token. Supported values are `node` and `kibana`. 
`--url`

     Specifies the base URL (hostname and port of the local node) that the tool uses to submit API requests to Elasticsearch. The default value is determined from the settings in your `elasticsearch.yml` file. If `xpack.security.http.ssl.enabled` is set to `true`, you must specify an HTTPS URL. 

###Examples

以下命令创建一个注册令牌，用于将 Elasticsearch 节点注册到集群中：

    
    
    bin/elasticsearch-create-enrollment-token -s node

以下命令创建用于将 Kibanainstance 注册到集群中的注册令牌。指定的 URL 指示弹性搜索-创建-注册-令牌工具尝试访问本地 Elasticsearch 节点的位置：

    
    
    bin/elasticsearch-create-enrollment-token -s kibana --url "https://172.0.0.3:9200"

[« elasticsearch-certutil](certutil.md) [elasticsearch-croneval
»](elasticsearch-croneval.md)
