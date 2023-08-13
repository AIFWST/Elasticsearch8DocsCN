

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[SQL REST API](sql-rest.md)

[« Use runtime fields](sql-runtime-fields.md) [SQL Translate API »](sql-
translate.md)

## 运行异步 SQL搜索

默认情况下，SQL 搜索是同步的。它们在返回响应之前等待完整的结果。但是，跨大型数据集或冻结数据的搜索结果可能需要更长的时间。

若要避免长时间等待，请运行异步 SQL 搜索。将"wait_for_completion_timeout"设置为要等待同步结果的持续时间。

    
    
    response = client.sql.query(
      format: 'json',
      body: {
        wait_for_completion_timeout: '2s',
        query: 'SELECT * FROM library ORDER BY page_count DESC',
        fetch_size: 5
      }
    )
    puts response
    
    
    POST _sql?format=json
    {
      "wait_for_completion_timeout": "2s",
      "query": "SELECT * FROM library ORDER BY page_count DESC",
      "fetch_size": 5
    }

如果搜索未在此时间段内完成，则搜索将变为异步。该 API 返回：

* 搜索的"ID"。  * "is_partial"值为"true"，表示搜索结果不完整。  * "is_running"值为"true"，表示搜索仍在后台运行。

对于 CSV、TSV 和 TXT 响应，API 会在各自的"异步 ID"、"部分异步"和"异步运行"HTTP 标头中返回这些值。

    
    
    {
      "id": "FnR0TDhyWUVmUmVtWXRWZER4MXZiNFEad2F5UDk2ZVdTVHV1S0xDUy00SklUdzozMTU=",
      "is_partial": true,
      "is_running": true,
      "rows": [ ]
    }

若要检查异步搜索的进度，请将搜索 ID 与 getasync SQL 搜索状态 API 配合使用。

    
    
    response = client.sql.get_async_status(
      id: 'FnR0TDhyWUVmUmVtWXRWZER4MXZiNFEad2F5UDk2ZVdTVHV1S0xDUy00SklUdzozMTU='
    )
    puts response
    
    
    GET _sql/async/status/FnR0TDhyWUVmUmVtWXRWZER4MXZiNFEad2F5UDk2ZVdTVHV1S0xDUy00SklUdzozMTU=

如果"is_running"和"is_partial"为"false"，则异步搜索已完成并具有完整的结果。

    
    
    {
      "id": "FnR0TDhyWUVmUmVtWXRWZER4MXZiNFEad2F5UDk2ZVdTVHV1S0xDUy00SklUdzozMTU=",
      "is_running": false,
      "is_partial": false,
      "expiration_time_in_millis": 1611690295000,
      "completion_status": 200
    }

若要获取结果，请将搜索 ID 与获取异步 SQL 搜索 API 一起使用。如果搜索仍在运行，请使用"wait_for_completion_timeout"指定要等待的时间。您还可以指定响应"格式"。

    
    
    response = client.sql.get_async(
      id: 'FnR0TDhyWUVmUmVtWXRWZER4MXZiNFEad2F5UDk2ZVdTVHV1S0xDUy00SklUdzozMTU=',
      wait_for_completion_timeout: '2s',
      format: 'json'
    )
    puts response
    
    
    GET _sql/async/FnR0TDhyWUVmUmVtWXRWZER4MXZiNFEad2F5UDk2ZVdTVHV1S0xDUy00SklUdzozMTU=?wait_for_completion_timeout=2s&format=json

#### 更改搜索保留期

默认情况下，Elasticsearch 会将异步 SQL 搜索存储五天。在此期限之后，Elasticsearch 会删除搜索及其结果，即使搜索仍在运行。要更改此保留期，请使用"keep_alive"参数。

    
    
    response = client.sql.query(
      format: 'json',
      body: {
        keep_alive: '2d',
        wait_for_completion_timeout: '2s',
        query: 'SELECT * FROM library ORDER BY page_count DESC',
        fetch_size: 5
      }
    )
    puts response
    
    
    POST _sql?format=json
    {
      "keep_alive": "2d",
      "wait_for_completion_timeout": "2s",
      "query": "SELECT * FROM library ORDER BY page_count DESC",
      "fetch_size": 5
    }

可以使用获取异步 SQL 搜索 API 的"keep_alive"参数稍后更改保留期。新时间段在请求运行后开始。

    
    
    response = client.sql.get_async(
      id: 'FmdMX2pIang3UWhLRU5QS0lqdlppYncaMUpYQ05oSkpTc3kwZ21EdC1tbFJXQToxOTI=',
      keep_alive: '5d',
      wait_for_completion_timeout: '2s',
      format: 'json'
    )
    puts response
    
    
    GET _sql/async/FmdMX2pIang3UWhLRU5QS0lqdlppYncaMUpYQ05oSkpTc3kwZ21EdC1tbFJXQToxOTI=?keep_alive=5d&wait_for_completion_timeout=2s&format=json

使用删除异步 SQL 搜索 API 在"keep_alive"句点结束之前删除异步搜索。如果搜索仍在运行，Elasticsearch 会取消它。

    
    
    response = client.sql.delete_async(
      id: 'FmdMX2pIang3UWhLRU5QS0lqdlppYncaMUpYQ05oSkpTc3kwZ21EdC1tbFJXQToxOTI='
    )
    puts response
    
    
    DELETE _sql/async/delete/FmdMX2pIang3UWhLRU5QS0lqdlppYncaMUpYQ05oSkpTc3kwZ21EdC1tbFJXQToxOTI=

#### 存储同步 SQL 搜索

默认情况下，Elasticsearch 只存储异步 SQL 搜索。要保存异步搜索，请指定"wait_for_completion_timeout"并将"keep_on_completion"设置为"true"。

    
    
    response = client.sql.query(
      format: 'json',
      body: {
        keep_on_completion: true,
        wait_for_completion_timeout: '2s',
        query: 'SELECT * FROM library ORDER BY page_count DESC',
        fetch_size: 5
      }
    )
    puts response
    
    
    POST _sql?format=json
    {
      "keep_on_completion": true,
      "wait_for_completion_timeout": "2s",
      "query": "SELECT * FROM library ORDER BY page_count DESC",
      "fetch_size": 5
    }

如果"is_partial"和"is_running"为"false"，则搜索是同步的并返回完整的结果。

    
    
    {
      "id": "Fnc5UllQdUVWU0NxRFNMbWxNYXplaFEaMUpYQ05oSkpTc3kwZ21EdC1tbFJXQTo0NzA=",
      "is_partial": false,
      "is_running": false,
      "rows": ...,
      "columns": ...,
      "cursor": ...
    }

稍后可以使用搜索 ID 和获取异步 SQLsearch API 获得相同的结果。

保存的同步搜索仍受"keep_alive"保留期的限制。当此期限结束时，Elasticsearch 将删除搜索结果。您还可以使用删除异步 SQL 搜索 API 删除保存的搜索。

[« Use runtime fields](sql-runtime-fields.md) [SQL Translate API »](sql-
translate.md)
