

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Term-level queries](term-level-queries.md)

[« Exists query](query-dsl-exists-query.md) [IDs »](query-dsl-ids-
query.md)

## 模糊查询

返回包含与搜索词类似的术语的文档，由 Levenshtein 编辑距离度量。

编辑距离是将一个术语转换为另一个术语所需的一个字符更改的数量。这些更改可能包括：

* 更改字符 ( **b** 牛 → **f** 牛) * 删除字符 ( **b** 缺少 → 缺少) * 插入一个字符 (原文如此 → 原文如此 **k** ) * 转置两个相邻字符 ( **ac** t → **ca** t)

为了查找类似的字词，"模糊"查询会在指定的编辑距离内创建一组搜索词的所有可能变体或扩展。然后，查询将返回每个扩展的完全匹配项。

### 示例请求

#### 简单示例

    
    
    response = client.search(
      body: {
        query: {
          fuzzy: {
            "user.id": {
              value: 'ki'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "fuzzy": {
          "user.id": {
            "value": "ki"
          }
        }
      }
    }

#### 使用高级参数的示例

    
    
    response = client.search(
      body: {
        query: {
          fuzzy: {
            "user.id": {
              value: 'ki',
              fuzziness: 'AUTO',
              max_expansions: 50,
              prefix_length: 0,
              transpositions: true,
              rewrite: 'constant_score'
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "fuzzy": {
          "user.id": {
            "value": "ki",
            "fuzziness": "AUTO",
            "max_expansions": 50,
            "prefix_length": 0,
            "transpositions": true,
            "rewrite": "constant_score"
          }
        }
      }
    }

### "模糊"的顶级参数

`<field>`

     (Required, object) Field you wish to search. 

### 参数 '<field>'

`value`

     (Required, string) Term you wish to find in the provided `<field>`. 
`fuzziness`

     (Optional, string) Maximum edit distance allowed for matching. See [Fuzziness](common-options.html#fuzziness "Fuzziness") for valid values and more information. 
`max_expansions`

    

(可选，整数)创建的最大变体数。默认为"50"。

避免在"max_expansions"参数中使用较高的值，尤其是在"prefix_length"参数值为"0"的情况下。"max_expansions"参数中的高值可能会导致性能不佳，因为检查的变体数量很多。

`prefix_length`

     (Optional, integer) Number of beginning characters left unchanged when creating expansions. Defaults to `0`. 
`transpositions`

     (Optional, Boolean) Indicates whether edits include transpositions of two adjacent characters (ab → ba). Defaults to `true`. 
`rewrite`

     (Optional, string) Method used to rewrite the query. For valid values and more information, see the [`rewrite` parameter](query-dsl-multi-term-rewrite.html "rewrite parameter"). 

###Notes

如果"search.allow_expensive_queries"设置为 false，则不会执行模糊查询。

[« Exists query](query-dsl-exists-query.md) [IDs »](query-dsl-ids-
query.md)
