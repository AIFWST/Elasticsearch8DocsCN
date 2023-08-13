

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Snapshot lifecycle management APIs](snapshot-
lifecycle-management-api.md)

[« Get snapshot lifecycle management status API](slm-api-get-status.md)
[Start snapshot lifecycle management API »](slm-api-start.md)

## 获取快照生命周期统计信息API

返回有关快照生命周期管理所执行操作的全局和策略级统计信息。

###Request

"获取/_slm/统计数据"

###Prerequisites

如果启用了 Elasticsearch 安全功能，您必须具有"manage_slm"集群权限才能使用此 API。有关详细信息，请参阅安全权限。

###Examples

    
    
    response = client.slm.get_stats
    puts response
    
    
    GET /_slm/stats

API 返回以下响应：

    
    
    {
      "retention_runs": 13,
      "retention_failed": 0,
      "retention_timed_out": 0,
      "retention_deletion_time": "1.4s",
      "retention_deletion_time_millis": 1404,
      "policy_stats": [ ],
      "total_snapshots_taken": 1,
      "total_snapshots_failed": 1,
      "total_snapshots_deleted": 0,
      "total_snapshot_deletion_failures": 0
    }

[« Get snapshot lifecycle management status API](slm-api-get-status.md)
[Start snapshot lifecycle management API »](slm-api-start.md)
