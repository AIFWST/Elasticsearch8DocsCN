

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[Index lifecycle actions](ilm-actions.md)

[« Delete](ilm-delete.md) [Migrate »](ilm-migrate.md)

## 强制合并

允许的阶段：热，暖。

强制将索引合并到指定的最大段数中。

"强制合并"操作是尽力而为。可能会发生某些分片正在重新定位的情况，在这种情况下，它们将不会合并。

要在"热"阶段使用"强制合并"操作，必须存在"翻转"操作**。如果未配置滚动更新操作，ILM 将拒绝该策略。

**性能注意事项**

强制合并是一项资源密集型操作。如果一次触发的强制合并过多，可能会对集群产生负面影响。当您将包含强制合并操作的 ILM 策略应用于现有索引时，可能会发生这种情况。如果他们符合"min_age"标准，他们可以立即进行多个阶段。您可以通过增加"min_age"或设置"index.lifecycle.origination_date"来更改指数年龄的计算方式来防止这种情况。

如果遇到强制合并任务队列积压，则可能需要增加强制合并线程池的大小，以便可以并行强制合并索引。为此，请配置"thread_pool.force_merge.size"群集设置。

这可能会产生级联性能影响。监控集群性能并缓慢增加线程池的大小以减少积压。

强制合并将由索引当前阶段内的节点执行。"热"阶段的强制合并将使用节点可能更快的热节点，同时对摄取的影响更大。"暖"阶段的强制合并将使用暖节点，并且可能需要更长的时间来执行，但不会影响"热"层中的引入。

###Options

`max_num_segments`

     (Required, integer) Number of segments to merge to. To fully merge the index, set to `1`. 
`index_codec`

    

(可选，字符串)用于压缩文档存储的编解码器。唯一接受的值是"best_compression"，它使用 DEFLATE 获得更高的压缩比，但存储字段性能较慢。要使用默认的 LZ4 编解码器，请省略此参数。

如果使用"best_compression"，ILM 将在强制合并之前关闭索引，然后重新打开索引。关闭时，索引将不可用于读取器写入操作。

###Example

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            warm: {
              actions: {
                forcemerge: {
                  max_num_segments: 1
                }
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/my_policy
    {
      "policy": {
        "phases": {
          "warm": {
            "actions": {
              "forcemerge" : {
                "max_num_segments": 1
              }
            }
          }
        }
      }
    }

[« Delete](ilm-delete.md) [Migrate »](ilm-migrate.md)
