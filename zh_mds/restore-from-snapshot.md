

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Start Snapshot Lifecycle Management](start-slm.md) [Multiple deployments
writing to the same snapshot repository »](add-repository.md)

## 从快照还原

Elasticsearch 使用快照将数据副本存储在集群之外。您可以恢复快照以恢复集群中没有分片副本的索引和数据流。如果删除了数据(索引或数据流)，或者群集成员身份已更改，并且系统中的当前节点不再包含数据的副本，则可能会发生这种情况。

恢复丢失的数据需要您备份受影响的索引和数据流，该备份对于您的使用案例来说足够最新。请不要在未确认的情况下继续。

弹性搜索服务 自我管理

要恢复缺少数据的索引和数据流：

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧边导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **开发工具>控制台**。

!木花控制台

4. 使用 cat 索引 API 查看受影响的索引。           响应 = client.cat.indices( v： true， health： 'red'， h： 'index，status，health' ) put response GET _cat/indices？v&health=red&h=index，status，health

响应将如下所示：

    
        index                                status health
    .ds-my-data-stream-2022.06.17-000001 open   red
    kibana_sample_data_flights           open   red

上述索引的"红色"运行状况表明这些索引缺少主分片，这意味着它们缺少数据。

5. 为了恢复数据，我们需要找到包含这两个索引的快照。若要查找此类快照，请使用获取快照 API。           响应 = client.snapshot.get( 存储库： 'my_repository'， 快照： '*'， 详细： false ) 放置响应 GET _snapshot/my_repository/*？verbose=false

响应将如下所示：

    
        {
      "snapshots" : [
        {
          "snapshot" : "snapshot-20200617",                                     __"uuid" : "dZyPs1HyTwS-cnKdH08EPg",
          "repository" : "my_repository", __"indices" : [ __".apm-agent-configuration",
            ".apm-custom-link",
            ".ds-ilm-history-5-2022.06.17-000001",
            ".ds-my-data-stream-2022.06.17-000001",
            ".geoip_databases",
            ".kibana-event-log-8.2.2-000001",
            ".kibana_8.2.2_001",
            ".kibana_task_manager_8.2.2_001",
            "kibana_sample_data_ecommerce",
            "kibana_sample_data_flights",
            "kibana_sample_data_logs"
          ],
          "data_streams" : [ ],
          "state" : "SUCCESS" __}
      ],
      "total" : 1,
      "remaining" : 0
    }

__

|

快照的名称。   ---|---    __

|

快照的存储库。   __

|

快照中备份的索引。   __

|

如果快照成功。     6. 快照"快照-20200617"包含我们要恢复的两个索引。您可能有多个快照，您可以从中还原目标索引。选择最新快照。  7.现在我们找到了快照，我们将继续准备数据流以恢复丢失的数据。我们将检查索引元数据以查看是否有任何索引是数据流的一部分：响应 = client.indices.get( 索引："kibana_sample_data_flights，.ds-my-data-stream-2022.06.17-000001"，功能："设置"，flat_settings：true ) 将响应 GET kibana_sample_data_flights，.ds-my-data-stream-2022.06.17-000001？features=settings&flat_settings

响应将如下所示：

    
        {
      ".ds-my-data-stream-2022.06.17-000001" : {                                __"aliases" : { },
        "mappings" : { },
        "settings" : { __"index.creation_date" : "1658406121699",
          "index.hidden" : "true",
          "index.lifecycle.name" : "my-lifecycle-policy",
          "index.number_of_replicas" : "1",
          "index.number_of_shards" : "1",
          "index.provided_name" : ".ds-my-data-stream-2022.06.17-000001",
          "index.routing.allocation.include._tier_preference" : "data_hot",
          "index.uuid" : "HmlFXp6VSu2XbQ-O3hVrwQ",
          "index.version.created" : "8020299"
        },
        "data_stream" : "my-data-stream" __},
      "kibana_sample_data_flights" : { __"aliases" : { },
        "mappings" : { },
        "settings" : {
          "index.creation_date" : "1655121541454",
          "index.number_of_replicas" : "0",
          "index.number_of_shards" : "1",
          "index.provided_name" : "kibana_sample_data_flights",
          "index.routing.allocation.include._tier_preference" : "data_content",
          "index.uuid" : "jMOlwKPPSzSraeeBWyuoDA",
          "index.version.created" : "8020299"
        }
      }
    }

__

|

索引的名称。   ---|---    __

|

包含我们正在寻找的元数据的此索引的设置。   __

|

这表示此索引是数据流的一部分，并显示数据流名称。   __

|

我们请求的其他索引的名称。   上面的响应显示"kibana_sample_data_flights"不是 adata 流的一部分，因为它在设置中没有名为"data_stream"的字段。

相反，".ds-my-data-stream-2022.06.17-000001"是称为"my-data-stream"的数据流的一部分。当你找到像这样的索引，它属于数据流时，你需要检查数据是否仍在被索引。您可以通过检查"设置"看到，如果可以找到此属性："index.lifecycle.indexing_complete"："true"，则表示在此索引中已完成索引，您可以继续下一步。

如果"index.lifecycle.indexing_complete"不存在或配置为"false"，则需要滚动更新数据流，以便可以恢复丢失的数据，而不会阻止引入新数据。以下命令将实现这一点。

    
        response = client.indices.rollover(
      alias: 'my-data-stream'
    )
    puts response
    
        POST my-data-stream/_rollover

8. 现在数据流准备已完成，我们将使用关闭索引 API 关闭目标索引。           响应 = client.index.close( index： 'kibana_sample_data_flights，.ds-my-data-stream-2022.06.17-000001' ) 将响应 POST kibana_sample_data_flights，.ds-my-data-stream-2022.06.17-000001/_close

您可以使用猫索引 API 确认它们已关闭。

    
        response = client.cat.indices(
      v: true,
      health: 'red',
      h: 'index,status,health'
    )
    puts response
    
        GET _cat/indices?v&health=red&h=index,status,health

响应将如下所示：

    
        index                                status health
    .ds-my-data-stream-2022.06.17-000001 close   red
    kibana_sample_data_flights           close   red

9. 索引已关闭，现在我们可以使用还原快照 API 从快照还原它们而不会造成任何复杂性：响应 = client.snapshot.restore( 存储库："my_repository"，快照："快照-20200617"，正文：{ 索引："kibana_sample_data_flights，.ds-my-data-stream-2022.06.17-000001"，include_aliases：true } ) 将响应 POST _snapshot/my_repository/snapshot-20200617/_restore { "索引"： "kibana_sample_data_flights，.ds-my-data-stream-2022.06.17-000001"， __"include_aliases"： true __}

__

|

要还原的索引。   ---|---    __

|

我们还想恢复别名。   如果需要恢复任何功能状态，我们需要使用"feature_states"字段指定它们，并且属于我们还原的功能状态的索引不得在"索引"下指定。运行状况 API 返回需要还原的"索引"和"feature_states"，以便从快照诊断还原。例如：

    
        response = client.snapshot.restore(
      repository: 'my_repository',
      snapshot: 'snapshot-20200617',
      body: {
        feature_states: [
          'geoip'
        ],
        indices: 'kibana_sample_data_flights,.ds-my-data-stream-2022.06.17-000001',
        include_aliases: true
      }
    )
    puts response
    
        POST _snapshot/my_repository/snapshot-20200617/_restore
    {
      "feature_states": [ "geoip" ],
      "indices": "kibana_sample_data_flights,.ds-my-data-stream-2022.06.17-000001",
      "include_aliases": true
    }

10. 最后，我们可以通过 cat 索引 API 验证索引运行状况现在是否为"绿色"。           响应 = client.cat.indices( v： true， index： '.ds-my-data-stream-2022.06.17-000001，kibana_sample_data_flightsh=index，status，health' ) 把响应 GET _cat/indices？v&index=.ds-my-data-stream-2022.06.17-000001，kibana_sample_data_flightsh=index，status，health

响应将如下所示：

    
        index                                status health
    .ds-my-data-stream-2022.06.17-000001 open   green
    kibana_sample_data_flights           open   green

正如我们在上面看到的，指数是"绿色"和开放的。问题已解决。

有关创建和还原快照的更多指导，请参阅本指南。

要恢复缺少分片的索引：

1. 使用 cat 索引 API 查看受影响的索引。           响应 = client.cat.indices( v： true， health： 'red'， h： 'index，status，health' ) put response GET _cat/indices？v&health=red&h=index，status，health

响应将如下所示：

    
        index                                status health
    .ds-my-data-stream-2022.06.17-000001 open   red
    kibana_sample_data_flights           open   red

上述索引的"红色"运行状况表明这些索引缺少主分片，这意味着它们缺少数据。

2. 为了恢复数据，我们需要找到包含这两个索引的快照。若要查找此类快照，请使用获取快照 API。           响应 = client.snapshot.get( 存储库： 'my_repository'， 快照： '*'， 详细： false ) 放置响应 GET _snapshot/my_repository/*？verbose=false

响应将如下所示：

    
        {
      "snapshots" : [
        {
          "snapshot" : "snapshot-20200617",                                     __"uuid" : "dZyPs1HyTwS-cnKdH08EPg",
          "repository" : "my_repository", __"indices" : [ __".apm-agent-configuration",
            ".apm-custom-link",
            ".ds-ilm-history-5-2022.06.17-000001",
            ".ds-my-data-stream-2022.06.17-000001",
            ".geoip_databases",
            ".kibana-event-log-8.2.2-000001",
            ".kibana_8.2.2_001",
            ".kibana_task_manager_8.2.2_001",
            "kibana_sample_data_ecommerce",
            "kibana_sample_data_flights",
            "kibana_sample_data_logs"
          ],
          "data_streams" : [ ],
          "state" : "SUCCESS" __}
      ],
      "total" : 1,
      "remaining" : 0
    }

__

|

快照的名称。   ---|---    __

|

快照的存储库。   __

|

快照中备份的索引。   __

|

如果快照成功。     3. 快照"快照-20200617"包含我们要恢复的两个索引。您可能有多个快照，您可以从中还原目标索引。选择最新快照。  4.现在我们找到了快照，我们将继续准备数据流以恢复丢失的数据。我们将检查索引元数据以查看是否有任何索引是数据流的一部分：响应 = client.indices.get( 索引："kibana_sample_data_flights，.ds-my-data-stream-2022.06.17-000001"，功能："设置"，flat_settings：true ) 将响应 GET kibana_sample_data_flights，.ds-my-data-stream-2022.06.17-000001？features=settings&flat_settings

响应将如下所示：

    
        {
      ".ds-my-data-stream-2022.06.17-000001" : {                                __"aliases" : { },
        "mappings" : { },
        "settings" : { __"index.creation_date" : "1658406121699",
          "index.hidden" : "true",
          "index.lifecycle.name" : "my-lifecycle-policy",
          "index.number_of_replicas" : "1",
          "index.number_of_shards" : "1",
          "index.provided_name" : ".ds-my-data-stream-2022.06.17-000001",
          "index.routing.allocation.include._tier_preference" : "data_hot",
          "index.uuid" : "HmlFXp6VSu2XbQ-O3hVrwQ",
          "index.version.created" : "8020299"
        },
        "data_stream" : "my-data-stream" __},
      "kibana_sample_data_flights" : { __"aliases" : { },
        "mappings" : { },
        "settings" : {
          "index.creation_date" : "1655121541454",
          "index.number_of_replicas" : "0",
          "index.number_of_shards" : "1",
          "index.provided_name" : "kibana_sample_data_flights",
          "index.routing.allocation.include._tier_preference" : "data_content",
          "index.uuid" : "jMOlwKPPSzSraeeBWyuoDA",
          "index.version.created" : "8020299"
        }
      }
    }

__

|

索引的名称。   ---|---    __

|

包含我们正在寻找的元数据的此索引的设置。   __

|

这表示此索引是数据流的一部分，并显示数据流名称。   __

|

我们请求的其他索引的名称。   上面的响应显示"kibana_sample_data_flights"不是 adata 流的一部分，因为它在设置中没有名为"data_stream"的字段。

相反，".ds-my-data-stream-2022.06.17-000001"是称为"my-data-stream"的数据流的一部分。当你找到像这样的索引，它属于数据流时，你需要检查数据是否仍在被索引。您可以通过检查"设置"看到，如果可以找到此属性："index.lifecycle.indexing_complete"："true"，则表示在此索引中已完成索引，您可以继续下一步。

如果"index.lifecycle.indexing_complete"不存在或配置为"false"，则需要滚动更新数据流，以便可以恢复丢失的数据，而不会阻止引入新数据。以下命令将实现这一点。

    
        response = client.indices.rollover(
      alias: 'my-data-stream'
    )
    puts response
    
        POST my-data-stream/_rollover

5. 现在数据流准备已完成，我们将使用关闭索引 API 关闭目标索引。           响应 = client.index.close( index： 'kibana_sample_data_flights，.ds-my-data-stream-2022.06.17-000001' ) 将响应 POST kibana_sample_data_flights，.ds-my-data-stream-2022.06.17-000001/_close

您可以使用猫索引 API 确认它们已关闭。

    
        response = client.cat.indices(
      v: true,
      health: 'red',
      h: 'index,status,health'
    )
    puts response
    
        GET _cat/indices?v&health=red&h=index,status,health

响应将如下所示：

    
        index                                status health
    .ds-my-data-stream-2022.06.17-000001 close   red
    kibana_sample_data_flights           close   red

6. 索引已关闭，现在我们可以使用还原快照 API 从快照还原它们而不会造成任何复杂性：响应 = client.snapshot.restore( 存储库："my_repository"，快照："快照-20200617"，正文：{ 索引："kibana_sample_data_flights，.ds-my-data-stream-2022.06.17-000001"，include_aliases：true } ) 将响应 POST _snapshot/my_repository/snapshot-20200617/_restore { "索引"： "kibana_sample_data_flights，.ds-my-data-stream-2022.06.17-000001"， __"include_aliases"： true __}

__

|

要还原的索引。   ---|---    __

|

我们还想恢复别名。   如果需要恢复任何功能状态，我们需要使用"feature_states"字段指定它们，并且属于我们还原的功能状态的索引不得在"索引"下指定。运行状况 API 返回需要还原的"索引"和"feature_states"，以便从快照诊断还原。例如：

    
        response = client.snapshot.restore(
      repository: 'my_repository',
      snapshot: 'snapshot-20200617',
      body: {
        feature_states: [
          'geoip'
        ],
        indices: 'kibana_sample_data_flights,.ds-my-data-stream-2022.06.17-000001',
        include_aliases: true
      }
    )
    puts response
    
        POST _snapshot/my_repository/snapshot-20200617/_restore
    {
      "feature_states": [ "geoip" ],
      "indices": "kibana_sample_data_flights,.ds-my-data-stream-2022.06.17-000001",
      "include_aliases": true
    }

7. 最后，我们可以通过 cat 索引 API 验证索引运行状况现在是否为"绿色"。           响应 = client.cat.indices( v： true， index： '.ds-my-data-stream-2022.06.17-000001，kibana_sample_data_flightsh=index，status，health' ) 把响应 GET _cat/indices？v&index=.ds-my-data-stream-2022.06.17-000001，kibana_sample_data_flightsh=index，status，health

响应将如下所示：

    
        index                                status health
    .ds-my-data-stream-2022.06.17-000001 open   green
    kibana_sample_data_flights           open   green

正如我们在上面看到的，指数是"绿色"和开放的。问题已解决。

有关创建和还原快照的更多指导，请参阅本指南。

[« Start Snapshot Lifecycle Management](start-slm.md) [Multiple deployments
writing to the same snapshot repository »](add-repository.md)
