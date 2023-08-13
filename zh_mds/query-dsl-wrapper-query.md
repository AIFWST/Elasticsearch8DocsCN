

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Specialized queries](specialized-queries.md)

[« Script score query](query-dsl-script-score-query.md) [Pinned Query
»](query-dsl-pinned-query.md)

## 包装器查询

接受任何其他查询作为 base64 编码字符串的查询。

    
    
    response = client.search(
      body: {
        query: {
          wrapper: {
            query: 'eyJ0ZXJtIiA6IHsgInVzZXIuaWQiIDogImtpbWNoeSIgfX0='
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "wrapper": {
          "query": "eyJ0ZXJtIiA6IHsgInVzZXIuaWQiIDogImtpbWNoeSIgfX0=" __}
      }
    }

__

|

Base64 编码字符串： '{"term" ： { "user.id" ： "kimchy" }}' ---|--- 此查询在 Spring Data Elasticsearch 的上下文中更有用。这是用户在使用 Spring 数据存储库时添加自定义查询的方式。用户可以将 @Query() 注释添加到存储库方法中。当调用这样的方法时，我们在注释的查询参数中进行参数替换，然后将其作为搜索请求的查询部分发送。

[« Script score query](query-dsl-script-score-query.md) [Pinned Query
»](query-dsl-pinned-query.md)
