

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Lowercase token filter](analysis-lowercase-tokenfilter.md) [Multiplexer
token filter »](analysis-multiplexer-tokenfilter.md)

## 最小哈希令牌筛选器

使用 MinHash 技术为令牌流生成签名。您可以使用 MinHash 签名来估计文档的相似性。请参阅使用"min_hash"令牌过滤器进行相似性搜索。

"min_hash"筛选器对令牌流顺序执行以下操作：

1. 对流中的每个令牌进行哈希处理。  2. 将哈希分配给存储桶，仅保留每个存储桶的最小哈希。  3. 将每个存储桶中的最小哈希作为令牌流输出。

此过滤器使用 Lucene 的 MinHashFilter。

### 可配置参数

`bucket_count`

     (Optional, integer) Number of buckets to which hashes are assigned. Defaults to `512`. 
`hash_count`

     (Optional, integer) Number of ways to hash each token in the stream. Defaults to `1`. 
`hash_set_size`

    

(可选，整数)要保留的每个存储桶的哈希数。默认为"1"。

哈希按大小升序保留，首先从存储桶的最小哈希开始。

`with_rotation`

     (Optional, Boolean) If `true`, the filter fills empty buckets with the value of the first non-empty bucket to its circular right if the `hash_set_size` is `1`. If the `bucket_count` argument is greater than `1`, this parameter defaults to `true`. Otherwise, this parameter defaults to `false`. 

### 配置"min_hash"过滤器的提示

* "min_hash"过滤器输入标记通常应是由带状疱疹令牌过滤器生成的 k 字带状疱疹。您应该选择足够大的"k"，以便文档中出现任何给定带状疱疹的可能性较低。同时，由于内部每个带状疱疹都被散列为 128 位散列，因此您应该选择足够小的"k"，以便所有可能的不同 k 字带状疱疹都可以散列为 128 位散列，并且冲突最小。  * 我们建议您测试"hash_count"、"bucket_count"和"hash_set_size"参数的不同参数：

    * To improve precision, increase the `bucket_count` or `hash_set_size` arguments. Higher `bucket_count` and `hash_set_size` values increase the likelihood that different tokens are indexed to different buckets. 
    * To improve the recall, increase the value of the `hash_count` argument. For example, setting `hash_count` to `2` hashes each token in two different ways, increasing the number of potential candidates for search. 

* 默认情况下，"min_hash"过滤器为每个文档生成 512 个令牌。每个令牌的大小为 16 个字节。这意味着每个文档的大小将增加约 8Kb。  * "min_hash"过滤器用于杰卡德相似性。这意味着文档包含某个令牌的次数并不重要，重要的是它是否包含它。

### 使用"min_hash"令牌过滤器进行相似性搜索

"min_hash"令牌过滤器允许您对文档进行哈希处理以进行相似性搜索。相似性搜索或最近邻搜索是一个复杂的问题。分析解决方案需要在查询文档和索引中的每个文档之间进行详尽的成对比较。如果索引很大，则这是一个禁止的操作。已经开发了许多近似最近邻搜索解决方案，以使相似性搜索更加实用和计算可行。这些解决方案之一涉及文档的哈希处理。

文档的哈希方式是，相似的文档更有可能产生相同的哈希代码并放入相同的哈希桶中，而不同的文档更有可能被哈希到不同的哈希桶中。这种类型的哈希称为局部敏感哈希 (LSH)。

根据文档之间相似性的构成，已经提出了各种LSH功能。对于Jaccardsimilarity，一个流行的LSH函数是MinHash。MinHash 为文档生成签名的一般想法是对整个索引词汇表应用随机排列(词汇表的随机编号)，并记录文档此排列的最小值(文档中存在的词汇字的最小值)。排列运行多次;合并所有这些的最小值将构成文档的签名。

在实践中，不是随机排列，而是选择许多哈希函数。哈希函数计算文档的每个令牌的哈希代码，并从中选择最小哈希代码。来自 allhash 函数的最小哈希代码组合在一起以形成文档的签名。

### 自定义并添加到分析器

要自定义"min_hash"过滤器，请复制它，为新的自定义令牌过滤器创建基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下创建索引 API 请求使用以下自定义令牌筛选器来配置新的自定义分析器：

*"my_shingle_filter"，一个自定义的"瓦片"过滤器。"my_shingle_filter"仅输出五个字的带状疱疹。  *"my_minhash_filter"，自定义"min_hash"过滤器。"my_minhash_filter"将每个五个字的瓦片散列一次。然后，它将哈希分配到 512 个存储桶中，仅保留每个存储桶中的最小哈希。

该请求还将自定义分析器分配给"指纹"字段映射。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            filter: {
              my_shingle_filter: {
                type: 'shingle',
                min_shingle_size: 5,
                max_shingle_size: 5,
                output_unigrams: false
              },
              my_minhash_filter: {
                type: 'min_hash',
                hash_count: 1,
                bucket_count: 512,
                hash_set_size: 1,
                with_rotation: true
              }
            },
            analyzer: {
              my_analyzer: {
                tokenizer: 'standard',
                filter: [
                  'my_shingle_filter',
                  'my_minhash_filter'
                ]
              }
            }
          }
        },
        mappings: {
          properties: {
            fingerprint: {
              type: 'text',
              analyzer: 'my_analyzer'
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "settings": {
        "analysis": {
          "filter": {
            "my_shingle_filter": {      __"type": "shingle",
              "min_shingle_size": 5,
              "max_shingle_size": 5,
              "output_unigrams": false
            },
            "my_minhash_filter": {
              "type": "min_hash",
              "hash_count": 1, __"bucket_count": 512, __"hash_set_size": 1, __"with_rotation": true __}
          },
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "standard",
              "filter": [
                "my_shingle_filter",
                "my_minhash_filter"
              ]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "fingerprint": {
            "type": "text",
            "analyzer": "my_analyzer"
          }
        }
      }
    }

__

|

将自定义带状疱疹过滤器配置为仅输出五个字的带状疱疹。   ---|---    __

|

流中的每个五个字的瓦片都会散列一次。   __

|

哈希分配给 512 个存储桶。   __

|

仅保留每个存储桶中的最小哈希。   __

|

筛选器使用相邻存储桶的值填充空存储桶。   « 小写令牌过滤器 多路复用令牌过滤器 »