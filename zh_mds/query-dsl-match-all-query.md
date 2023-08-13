

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« Parent ID query](query-dsl-parent-id-query.md) [Span queries »](span-
queries.md)

## 匹配所有查询

最简单的查询，它匹配所有文档，为它们提供"_score""1.0"。

    
    
    $params = [
        'body' => [
            'query' => [
                'match_all' => [
                ],
            ],
        ],
    ];
    $response = $client->search($params);
    
    
    resp = client.search(body={"query": {"match_all": {}}})
    print(resp)
    
    
    response = client.search(
      body: {
        query: {
          match_all: {}
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match_all": {}
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    const response = await client.search({
      body: {
        query: {
          match_all: {}
        }
      }
    })
    console.log(response)
    
    
    GET /_search
    {
        "query": {
            "match_all": {}
        }
    }

可以使用"boost"参数更改"_score"：

    
    
    response = client.search(
      body: {
        query: {
          match_all: {
            boost: 1.2
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match_all": {
    	      "boost": 1.2
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "match_all": { "boost" : 1.2 }
      }
    }

## 匹配无查询

这是"match_all"查询的反面，它与任何文档都不匹配。

    
    
    response = client.search(
      body: {
        query: {
          match_none: {}
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "match_none": {}
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "match_none": {}
      }
    }

[« Parent ID query](query-dsl-parent-id-query.md) [Span queries »](span-
queries.md)
