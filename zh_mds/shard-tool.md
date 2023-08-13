

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Command
line tools](commands.md)

[« elasticsearch-setup-passwords](setup-passwords.md) [elasticsearch-
syskeygen »](syskeygen.md)

## 弹性搜索分片

在某些情况下，分片副本的 Lucene 索引或 Translog 可能会损坏。"elasticsearch-shard"命令使您能够在无法自动恢复或从备份中恢复分片的良好副本时删除分片的损坏部分。

当您运行"弹性搜索分片"时，您将丢失损坏的数据。仅当无法从分片的另一个副本恢复或还原快照时，才应将此工具用作最后的手段。

###Synopsis

    
    
    bin/elasticsearch-shard remove-corrupted-data
      ([--index <Index>] [--shard-id <ShardId>] | [--dir <IndexPath>])
      [--truncate-clean-translog]
      [-E <KeyValuePair>]
      [-h, --help] ([-s, --silent] | [-v, --verbose])

###Description

当 Elasticsearch 检测到分片的数据已损坏时，它会失败该分片复制并拒绝使用它。在正常情况下，分片会自动从另一个副本中恢复。如果没有可用的分片的良好副本，并且您无法从快照中恢复一个副本，则可以使用"elasticsearch-shard"删除损坏的数据并恢复对未受影响段中任何剩余数据的访问。

在运行"elasticsearch-shard"之前停止Elasticsearch。

要删除损坏的分片数据，请使用"删除损坏的数据"子命令。

有两种方法可以指定路径：

* 使用"--index"和"--shard-id"选项指定索引名称和分片名称。  * 使用"--dir"选项指定损坏的索引或 translog 文件的完整路径。

#### JVMoptions

CLI 工具使用 64MB 的堆运行。对于大多数工具，此值都很好。但是，如果需要，可以通过设置CLI_JAVA_OPTS环境变量来覆盖它。例如，以下内容将"分片"工具使用的堆大小增加到 1GB。

    
    
    export CLI_JAVA_OPTS="-Xmx1g"
    bin/elasticsearch-shard ...

#### 删除损坏的数据

"Elasticsearch-shard"分析分片副本，并提供发现的损坏的概述。要继续，您必须确认要删除损坏的数据。

在运行"弹性搜索分片"之前备份您的数据。这是一种破坏性操作，可从分片中删除损坏的数据。

    
    
    $ bin/elasticsearch-shard remove-corrupted-data --index my-index-000001 --shard-id 0
    
    
        WARNING: Elasticsearch MUST be stopped before running this tool.
    
      Please make a complete backup of your index before using this tool.
    
    
    Opening Lucene index at /var/lib/elasticsearchdata/indices/P45vf_YQRhqjfwLMUvSqDw/0/index/
    
     >> Lucene index is corrupted at /var/lib/elasticsearchdata/indices/P45vf_YQRhqjfwLMUvSqDw/0/index/
    
    Opening translog at /var/lib/elasticsearchdata/indices/P45vf_YQRhqjfwLMUvSqDw/0/translog/
    
    
     >> Translog is clean at /var/lib/elasticsearchdata/indices/P45vf_YQRhqjfwLMUvSqDw/0/translog/
    
    
      Corrupted Lucene index segments found - 32 documents will be lost.
    
                WARNING:              YOU WILL LOSE DATA.
    
    Continue and remove docs from the index ? Y
    
    WARNING: 1 broken segments (containing 32 documents) detected
    Took 0.056 sec total.
    Writing...
    OK
    Wrote new segments file "segments_c"
    Marking index with the new history uuid : 0pIBd9VTSOeMfzYT6p0AsA
    Changing allocation id V8QXk-QXSZinZMT-NvEq4w to tjm9Ve6uTBewVFAlfUMWjA
    
    You should run the following command to allocate this shard:
    
    POST /_cluster/reroute?metric=none
    {
      "commands" : [
        {
          "allocate_stale_primary" : {
            "index" : "index42",
            "shard" : 0,
            "node" : "II47uXW2QvqzHBnMcl2o_Q",
            "accept_data_loss" : false
          }
        }
      ]
    }
    
    You must accept the possibility of data loss by changing the `accept_data_loss` parameter to `true`.
    
    Deleted corrupt marker corrupted_FzTSBSuxT7i3Tls_TgwEag from /var/lib/elasticsearchdata/indices/P45vf_YQRhqjfwLMUvSqDw/0/index/

当您使用"弹性搜索分片"删除损坏的数据时，分片的分配 ID 会发生变化。重启节点后，必须使用 clusterreroute API 告诉 Elasticsearch 使用新的 ID。'elasticsearch-shard' 命令显示您需要提交的请求。

您还可以使用"-h"选项来获取"弹性搜索分片"工具支持的所有选项和参数的列表。

最后，您可以使用"--truncate-clean-translog"选项来截断分片的Translog，即使它看起来没有损坏。

[« elasticsearch-setup-passwords](setup-passwords.md) [elasticsearch-
syskeygen »](syskeygen.md)
