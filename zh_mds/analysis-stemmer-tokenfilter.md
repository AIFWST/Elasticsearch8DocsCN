

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Token filter reference](analysis-tokenfilters.md)

[« Snowball token filter](analysis-snowball-tokenfilter.md) [Stemmer
override token filter »](analysis-stemmer-override-tokenfilter.md)

## 词干筛选器

为多种语言提供算法词干提取，其中一些语言具有其他变体。有关支持的语言列表，请参阅"语言"参数。

如果未自定义，筛选器将使用英语的波特词干提取算法。

###Example

以下分析 API 请求使用"词干分析器"过滤器的默认波特词干算法将"狐狸快速跳跃"阻止为"狐狸跳跃快速"：

    
    
    response = client.indices.analyze(
      body: {
        tokenizer: 'standard',
        filter: [
          'stemmer'
        ],
        text: 'the foxes jumping quickly'
      }
    )
    puts response
    
    
    GET /_analyze
    {
      "tokenizer": "standard",
      "filter": [ "stemmer" ],
      "text": "the foxes jumping quickly"
    }

筛选器生成以下标记：

    
    
    [ the, fox, jump, quickli ]

### 添加到分析器

以下创建索引 APIrequest 使用"词干分析器"筛选器来配置新的自定义分析器。

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'whitespace',
                filter: [
                  'stemmer'
                ]
              }
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
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "whitespace",
              "filter": [ "stemmer" ]
            }
          }
        }
      }
    }

### 可配置参数

`language`

    

(可选，字符串)用于词干标记的依赖于语言的词干提取算法。如果同时指定了此参数和"name"参数，则使用"语言"参数参数。

"语言"的有效值

有效值按语言排序。默认为**'英语'**。推荐的算法为粗体。

Arabic

     [**`arabic`**](https://lucene.apache.org/core/9_7_0/analysis/common/org/apache/lucene/analysis/ar/ArabicStemmer.html)
Armenian

     [**`armenian`**](https://snowballstem.org/algorithms/armenian/stemmer.html)
Basque

     [**`basque`**](https://snowballstem.org/algorithms/basque/stemmer.html)
Bengali

     [**`bengali`**](https://www.tandfonline.com/doi/abs/10.1080/02564602.1993.11437284)
Brazilian Portuguese

     [**`brazilian`**](https://lucene.apache.org/core/9_7_0/analysis/common/org/apache/lucene/analysis/br/BrazilianStemmer.html)
Bulgarian

     [**`bulgarian`**](http://members.unine.ch/jacques.savoy/Papers/BUIR.pdf)
Catalan

     [**`catalan`**](https://snowballstem.org/algorithms/catalan/stemmer.html)
Czech

     [**`czech`**](https://dl.acm.org/doi/10.1016/j.ipm.2009.06.001)
Danish

     [**`danish`**](https://snowballstem.org/algorithms/danish/stemmer.html)
Dutch

     [**`dutch`**](https://snowballstem.org/algorithms/dutch/stemmer.html), [`dutch_kp`](https://snowballstem.org/algorithms/kraaij_pohlmann/stemmer.html)
English

     [**`english`**](https://snowballstem.org/algorithms/porter/stemmer.html), [`light_english`](https://ciir.cs.umass.edu/pubfiles/ir-35.pdf), [`lovins`](https://snowballstem.org/algorithms/lovins/stemmer.html), [`minimal_english`](https://www.researchgate.net/publication/220433848_How_effective_is_suffixing), [`porter2`](https://snowballstem.org/algorithms/english/stemmer.html), [`possessive_english`](https://lucene.apache.org/core/9_7_0/analysis/common/org/apache/lucene/analysis/en/EnglishPossessiveFilter.html)
Estonian

     [**`estonian`**](https://lucene.apache.org/core/9_7_0/analyzers-common/org/tartarus/snowball/ext/EstonianStemmer.html)
Finnish

     [**`finnish`**](https://snowballstem.org/algorithms/finnish/stemmer.html), [`light_finnish`](http://clef.isti.cnr.it/2003/WN_web/22.pdf)
French

     [**`light_french`**](https://dl.acm.org/citation.cfm?id=1141523), [`french`](https://snowballstem.org/algorithms/french/stemmer.html), [`minimal_french`](https://dl.acm.org/citation.cfm?id=318984)
Galician

     [**`galician`**](http://bvg.udc.es/recursos_lingua/stemming.jsp), [`minimal_galician`](http://bvg.udc.es/recursos_lingua/stemming.jsp) (Plural step only) 
German

     [**`light_german`**](https://dl.acm.org/citation.cfm?id=1141523), [`german`](https://snowballstem.org/algorithms/german/stemmer.html), [`german2`](https://snowballstem.org/algorithms/german2/stemmer.html), [`minimal_german`](http://members.unine.ch/jacques.savoy/clef/morpho.pdf)
Greek

     [**`greek`**](https://sais.se/mthprize/2007/ntais2007.pdf)
Hindi

     [**`hindi`**](http://computing.open.ac.uk/Sites/EACLSouthAsia/Papers/p6-Ramanathan.pdf)
Hungarian

     [**`hungarian`**](https://snowballstem.org/algorithms/hungarian/stemmer.html), [`light_hungarian`](https://dl.acm.org/citation.cfm?id=1141523&dl=ACM&coll=DL&CFID=179095584&CFTOKEN=80067181)
Indonesian

     [**`indonesian`**](http://www.illc.uva.nl/Publications/ResearchReports/MoL-2003-02.text.pdf)
Irish

     [**`irish`**](https://snowballstem.org/otherapps/oregan/)
Italian

     [**`light_italian`**](https://www.ercim.eu/publication/ws-proceedings/CLEF2/savoy.pdf), [`italian`](https://snowballstem.org/algorithms/italian/stemmer.html)
Kurdish (Sorani)

     [**`sorani`**](https://lucene.apache.org/core/9_7_0/analysis/common/org/apache/lucene/analysis/ckb/SoraniStemmer.html)
Latvian

     [**`latvian`**](https://lucene.apache.org/core/9_7_0/analysis/common/org/apache/lucene/analysis/lv/LatvianStemmer.html)
Lithuanian

     [**`lithuanian`**](https://svn.apache.org/viewvc/lucene/dev/branches/lucene_solr_5_3/lucene/analysis/common/src/java/org/apache/lucene/analysis/lt/stem_ISO_8859_1.sbl?view=markup)
Norwegian (Bokmål)

     [**`norwegian`**](https://snowballstem.org/algorithms/norwegian/stemmer.html), [**`light_norwegian`**](https://lucene.apache.org/core/9_7_0/analysis/common/org/apache/lucene/analysis/no/NorwegianLightStemmer.html), [`minimal_norwegian`](https://lucene.apache.org/core/9_7_0/analysis/common/org/apache/lucene/analysis/no/NorwegianMinimalStemmer.html)
Norwegian (Nynorsk)

     [**`light_nynorsk`**](https://lucene.apache.org/core/9_7_0/analysis/common/org/apache/lucene/analysis/no/NorwegianLightStemmer.html), [`minimal_nynorsk`](https://lucene.apache.org/core/9_7_0/analysis/common/org/apache/lucene/analysis/no/NorwegianMinimalStemmer.html)
Portuguese

     [**`light_portuguese`**](https://dl.acm.org/citation.cfm?id=1141523&dl=ACM&coll=DL&CFID=179095584&CFTOKEN=80067181), [`minimal_portuguese`](http://www.inf.ufrgs.br/~buriol/papers/Orengo_CLEF07.pdf), [`portuguese`](https://snowballstem.org/algorithms/portuguese/stemmer.html), [`portuguese_rslp`](https://www.inf.ufrgs.br/\\~viviane/rslp/index.htm)
Romanian

     [**`romanian`**](https://snowballstem.org/algorithms/romanian/stemmer.html)
Russian

     [**`russian`**](https://snowballstem.org/algorithms/russian/stemmer.html), [`light_russian`](https://doc.rero.ch/lm.php?url=1000%2C43%2C4%2C20091209094227-CA%2FDolamic_Ljiljana_-_Indexing_and_Searching_Strategies_for_the_Russian_20091209.pdf)
Spanish

     [**`light_spanish`**](https://www.ercim.eu/publication/ws-proceedings/CLEF2/savoy.pdf), [`spanish`](https://snowballstem.org/algorithms/spanish/stemmer.html)
Swedish

     [**`swedish`**](https://snowballstem.org/algorithms/swedish/stemmer.html), [`light_swedish`](http://clef.isti.cnr.it/2003/WN_web/22.pdf)
Turkish

     [**`turkish`**](https://snowballstem.org/algorithms/turkish/stemmer.html)

`name`

     An alias for the [`language`](analysis-stemmer-tokenfilter.html#analysis-stemmer-tokenfilter-language-parm) parameter. If both this and the `language` parameter are specified, the `language` parameter argument is used. 

###Customize

要自定义"词干分析器"过滤器，请复制它以创建新的自定义令牌过滤器的基础。您可以使用过滤器的可配置参数修改过滤器。

例如，以下请求创建一个自定义的"词干分析器"筛选器，该筛选器使用"light_german"算法对单词进行词干提取：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          analysis: {
            analyzer: {
              my_analyzer: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'my_stemmer'
                ]
              }
            },
            filter: {
              my_stemmer: {
                type: 'stemmer',
                language: 'light_german'
              }
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
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "standard",
              "filter": [
                "lowercase",
                "my_stemmer"
              ]
            }
          },
          "filter": {
            "my_stemmer": {
              "type": "stemmer",
              "language": "light_german"
            }
          }
        }
      }
    }

[« Snowball token filter](analysis-snowball-tokenfilter.md) [Stemmer
override token filter »](analysis-stemmer-override-tokenfilter.md)
