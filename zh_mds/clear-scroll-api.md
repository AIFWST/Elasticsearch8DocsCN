

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Search APIs](search.md)

[« Scroll API](scroll-api.md) [Search template API »](search-template-
api.md)

## 清除滚动接口

清除滚动搜索的搜索上下文和结果。

    
    
    response = client.clear_scroll(
      body: {
        scroll_id: 'DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ=='
      }
    )
    puts response
    
    
    res, err := es.ClearScroll(
    	es.ClearScroll.WithBody(strings.NewReader(`{
    	  "scroll_id": "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ=="
    	}`)),
    )
    fmt.Println(res, err)
    
    
    DELETE /_search/scroll
    {
      "scroll_id" : "DXF1ZXJ5QW5kRmV0Y2gBAAAAAAAAAD4WYm9laVYtZndUQlNsdDcwakFMNjU1QQ=="
    }

###Request

"删除/_search/滚动/" [7.0.0<scroll_id>] 在 7.0.0 中已弃用。

"删除/_search/滚动"

### 路径参数

`<scroll_id>`

    

[7.0.0] 在 7.0.0 中已弃用。 (可选，字符串)要清除的滚动 ID 的逗号分隔列表。要清除所有滚动 ID，请使用"_all"。

滚动 ID 可以很长。我们建议仅使用"scroll_id"请求正文参数指定滚动 ID。

### 查询参数

`scroll_id`

    

[7.0.0] 在 7.0.0 中已弃用。 (可选，字符串)要清除的滚动 ID 的逗号分隔列表。要清除所有滚动 ID，请使用"_all"。

滚动 ID 可以很长。我们建议仅使用"scroll_id"请求正文参数指定滚动 ID。

### 请求正文

`scroll_id`

     (Required, string or array of strings) Scroll IDs to clear. To clear all scroll IDs, use `_all`. 

### 响应正文

`succeeded`

     (Boolean) If `true`, the request succeeded. This does not indicate whether any scrolling search requests were cleared. 
`num_freed`

     (integer) Number of scrolling search requests cleared. 

[« Scroll API](scroll-api.md) [Search template API »](search-template-
api.md)
