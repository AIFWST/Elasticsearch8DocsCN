

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Command
line tools](commands.md)

[« elasticsearch-create-enrollment-token](create-enrollment-token.md)
[elasticsearch-keystore »](elasticsearch-keystore.md)

## elasticsearch-croneval

验证和计算 cron 表达式。

###Synopsis

    
    
    bin/elasticsearch-croneval <expression>
    [-c, --count <integer>] [-h, --help]
    ([-s, --silent] | [-v, --verbose])

###Description

此命令使您能够验证您的 cron 表达式是否适用于 Elasticsearch 并生成预期的结果。

此命令在 '$ES_HOME/bin' 目录中提供。

###Parameters

'-c， --count' <Integer>

     The number of future times this expression will be triggered. The default value is `10`. 
`-d, --detail`

     Shows detail for invalid cron expression. It will print the stacktrace if the expression is not valid. 
`-h, --help`

     Returns all of the command parameters. 
`-s, --silent`

     Shows minimal output. 
`-v, --verbose`

     Shows verbose output. 

###Example

如果 cron 表达式有效，以下命令将显示接下来 20 次将触发计划：

    
    
    bin/elasticsearch-croneval "0 0/1 * * * ?" -c 20

[« elasticsearch-create-enrollment-token](create-enrollment-token.md)
[elasticsearch-keystore »](elasticsearch-keystore.md)
