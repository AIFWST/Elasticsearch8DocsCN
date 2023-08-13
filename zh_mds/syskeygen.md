

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Command
line tools](commands.md)

[« elasticsearch-shard](shard-tool.md) [elasticsearch-users »](users-
command.md)

## elasticsearch-syskeygen

'elasticsearch-syskeygen' 命令在 theelasticsearch config 目录中创建一个系统密钥文件。

###Synopsis

    
    
    bin/elasticsearch-syskeygen
    [-E <KeyValuePair>] [-h, --help]
    ([-s, --silent] | [-v, --verbose])

###Description

该命令会生成一个"system_key"文件，您可以使用该文件对敏感数据进行对称加密。例如，可以使用此密钥来防止观察程序返回和存储包含明文凭据的信息。请参阅Watcher_中的_Encrypting敏感数据。

系统密钥是对称密钥，因此必须在群集中的每个节点上使用相同的密钥。

###Parameters

'-E<KeyValuePair>'

     Configures a setting. For example, if you have a custom installation of Elasticsearch, you can use this parameter to specify the `ES_PATH_CONF` environment variable. 
`-h, --help`

     Returns all of the command parameters. 
`-s, --silent`

     Shows minimal output. 
`-v, --verbose`

     Shows verbose output. 

###Examples

以下命令在默认的"$ES_HOME/config"目录中生成一个"system_key"文件：

    
    
    bin/elasticsearch-syskeygen

[« elasticsearch-shard](shard-tool.md) [elasticsearch-users »](users-
command.md)
