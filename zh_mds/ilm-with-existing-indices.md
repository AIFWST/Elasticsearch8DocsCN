

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md)

[« Start and stop index lifecycle management](start-stop-ilm.md) [Skip
rollover »](skipping-rollover.md)

## 管理现有索引

如果您一直在使用 Curator 或其他机制来管理周期索引，则在迁移到 ILM 时，您有几个选项：

* 设置索引模板以使用 ILM 策略来管理新索引。一旦 ILM 管理了当前的写入索引，您就可以对旧索引应用适当的策略。  * 重新索引为 ILM 管理的索引。

从 Curator 版本 5.7 开始，Curator 将忽略 ILM 托管索引。

### 将策略应用于现有时序索引

过渡到使用 ILM 管理定期索引的最简单方法是配置索引模板以将生命周期策略应用于新索引。一旦要写入的索引由 ILM 管理，您就可以手动将策略应用于较旧的索引。

为旧索引定义一个单独的策略，以省略滚动更新操作。滚动更新用于管理新数据的去向，因此不适用。

请记住，应用于现有索引的策略会将每个阶段的"min_age"与索引的原始创建日期进行比较，并且可能会立即进行多个阶段。如果您的策略执行资源密集型操作(如强制合并)，则在切换到 ILM 时，您不希望让大量索引同时执行这些操作。

您可以在用于现有索引的策略中指定不同的"min_age"值，或设置"index.lifecycle.origination_date"来控制索引年龄的计算方式。

一旦所有 ILM 之前的索引都已老化并被删除，您就可以删除用于管理它们的策略。

如果您使用的是 Beats 或 Logstash，则在 7.0 及更高版本中启用 ILM 将设置 ILM 以自动管理新索引。如果您使用的是 Beatsthrough Logstash，则可能需要更改 Logstash 输出配置并调用 Beats 安装程序以将 ILM 用于新数据。

### 重新索引为托管索引

将策略应用于现有索引的替代方法是将数据重新索引到 ILM 管理的索引中。如果创建具有非常少量数据的定期索引导致分片计数过多，或者连续索引到同一索引中导致大型分片和性能问题，则可能需要执行此操作。

首先，您需要设置新的 ILM 管理的索引：

1. 更新索引模板以包含必要的 ILM 设置。  2. 引导初始索引作为写入索引。  3. 停止写入旧索引，并使用指向引导索引的别名为新文档编制索引。

重新索引到托管索引中：

1. 如果您不想在 ILM 管理的索引中混合使用新旧数据，请暂停为新文档编制索引。在一个索引中混合新旧数据是安全的，但需要保留组合索引，直到您准备好删除新数据为止。  2. 缩短 ILM 轮询间隔，以确保在等待滚动更新检查时索引不会变得太大。默认情况下，ILM 会检查每 10 分钟需要执行哪些操作。           响应 = client.cluster.put_settings( body： { persistent： { "indices.lifecycle.poll_interval"： '1m' } } ) put response PUT _cluster/settings { "persistent"： { "indices.lifecycle.poll_interval"： "1m" __} }

__

|

每分钟检查一次，查看是否需要执行 ILM 操作(如滚动更新)。   ---|--- 3.使用重新索引 API 重新索引数据。如果要按最初编制索引的顺序对数据进行分区，可以运行单独的重新索引请求。

文档保留其原始 ID。如果您不使用自动生成的文档 ID，并且从多个源索引重新编制索引，则可能需要执行其他处理以确保文档 ID 不会冲突。执行此操作的一种方法是在重新索引调用中使用脚本将原始索引名追加到文档 ID。

    
        response = client.reindex(
      body: {
        source: {
          index: 'mylogs-*'
        },
        dest: {
          index: 'mylogs',
          op_type: 'create'
        }
      }
    )
    puts response
    
        POST _reindex
    {
      "source": {
        "index": "mylogs-*" __},
      "dest": {
        "index": "mylogs", __"op_type": "create" __}
    }

__

|

匹配现有索引。使用新索引的前缀可以更轻松地使用此索引模式。   ---|---    __

|

指向引导索引的别名。   __

|

如果多个文档具有相同的 ID，则停止重新编制索引。建议这样做是为了防止在不同源索引中的文档具有相同 ID 时意外覆盖文档。     4. 重新索引完成后，将 ILM 轮询间隔设置回其默认值，以防止主节点上不必要的负载： 响应 = client.cluster.put_settings( 正文： { 持久： { "indices.lifecycle.poll_interval"： nil } } } ) 放置响应 PUT _cluster/设置 { "持久"： { "indices.lifecycle.poll_interval"： 空 } }

5. 继续使用相同的别名为新数据编制索引。

使用此别名进行查询现在将搜索新数据和所有索引数据。

6. 确认所有重新编制索引的数据在新托管索引中可用后，可以安全地删除旧索引。

[« Start and stop index lifecycle management](start-stop-ilm.md) [Skip
rollover »](skipping-rollover.md)
