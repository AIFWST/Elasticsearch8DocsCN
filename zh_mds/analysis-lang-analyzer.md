

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md) ›[Built-in analyzer reference](analysis-
analyzers.md)

[« Keyword analyzer](analysis-keyword-analyzer.md) [Pattern analyzer
»](analysis-pattern-analyzer.md)

## 语言分析器

一组旨在分析特定语言文本的分析器。支持以下类型："阿拉伯语"、"亚美尼亚语"、"巴斯克语"、"孟加拉语"、"巴西语"、"保加利亚语"、"加泰罗尼亚语"、"中日韩语"、"捷克语"、"丹麦语"、"荷兰语"、"英语"、"爱沙尼亚语"、"芬兰语"、"法语"、"加利西亚语"、"德语"、"希腊语"、"印地语"、"匈牙利语"、"印度尼西亚语"、"爱尔兰语"、"意大利语"、"拉脱维亚语"、"立陶宛语"、"挪威语"、"波斯语"、"葡萄牙语"、"罗马尼亚语"、"俄语"、"索拉尼语"、"西班牙语"、"瑞典语"、"土耳其语"、"泰语"。

### 配置语言分析器

####Stopwords

所有分析器都支持在配置内部设置自定义"停用词"，或通过设置"stopwords_path"使用外部停用词文件。有关更多详细信息，请查看停止分析器。

#### 从词干中排除单词

"stem_exclusion"参数允许您指定不应进行词干提取的小写单词数组。在内部，此功能是通过添加"keyword_marker"令牌筛选器来实现的，并将"关键字"设置为"stem_exclusion"参数的值。

以下分析器支持设置自定义"stem_exclusion"列表："阿拉伯语"、"亚美尼亚语"、"巴斯克语"、"孟加拉语"、"保加利亚语"、"加泰罗尼亚语"、"捷克语"、"荷兰语"、"英语"、"芬兰语"、"法语"、"加利西亚语"、"德语"、"印地语"、"匈牙利语"、"印度尼西亚语"、"爱尔兰语"、"意大利语"、"拉脱维亚语"、"立陶宛语"、"挪威语"、"葡萄牙语"、"罗马尼亚语"、"俄语"、"索拉尼语"、"西班牙语"、"瑞典语"、"土耳其语"。

### 重新实现语言分析器

内置语言分析器可以重新实现为"自定义"分析器(如下所述)，以便自定义其行为。

如果不打算从词干中排除单词(相当于上面的"stem_exclusion"参数)，则应从自定义分析器配置中删除"keyword_marker"令牌筛选器。

#### '阿拉伯文'分析器

"阿拉伯语"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'arabic_example',
      body: {
        settings: {
          analysis: {
            filter: {
              arabic_stop: {
                type: 'stop',
                stopwords: '_arabic_'
              },
              arabic_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'مثال'
                ]
              },
              arabic_stemmer: {
                type: 'stemmer',
                language: 'arabic'
              }
            },
            analyzer: {
              rebuilt_arabic: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'decimal_digit',
                  'arabic_stop',
                  'arabic_normalization',
                  'arabic_keywords',
                  'arabic_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /arabic_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "arabic_stop": {
              "type":       "stop",
              "stopwords":  "_arabic_" __},
            "arabic_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["مثال"] __},
            "arabic_stemmer": {
              "type":       "stemmer",
              "language":   "arabic"
            }
          },
          "analyzer": {
            "rebuilt_arabic": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "decimal_digit",
                "arabic_stop",
                "arabic_normalization",
                "arabic_keywords",
                "arabic_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '亚美尼亚'分析器编辑

"亚美尼亚"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'armenian_example',
      body: {
        settings: {
          analysis: {
            filter: {
              armenian_stop: {
                type: 'stop',
                stopwords: '_armenian_'
              },
              armenian_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'օրինակ'
                ]
              },
              armenian_stemmer: {
                type: 'stemmer',
                language: 'armenian'
              }
            },
            analyzer: {
              rebuilt_armenian: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'armenian_stop',
                  'armenian_keywords',
                  'armenian_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /armenian_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "armenian_stop": {
              "type":       "stop",
              "stopwords":  "_armenian_" __},
            "armenian_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["օրինակ"] __},
            "armenian_stemmer": {
              "type":       "stemmer",
              "language":   "armenian"
            }
          },
          "analyzer": {
            "rebuilt_armenian": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "armenian_stop",
                "armenian_keywords",
                "armenian_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '巴斯克语'analyzeredit。

"巴斯克"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'basque_example',
      body: {
        settings: {
          analysis: {
            filter: {
              basque_stop: {
                type: 'stop',
                stopwords: '_basque_'
              },
              basque_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'Adibidez'
                ]
              },
              basque_stemmer: {
                type: 'stemmer',
                language: 'basque'
              }
            },
            analyzer: {
              rebuilt_basque: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'basque_stop',
                  'basque_keywords',
                  'basque_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /basque_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "basque_stop": {
              "type":       "stop",
              "stopwords":  "_basque_" __},
            "basque_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["Adibidez"] __},
            "basque_stemmer": {
              "type":       "stemmer",
              "language":   "basque"
            }
          },
          "analyzer": {
            "rebuilt_basque": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "basque_stop",
                "basque_keywords",
                "basque_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '孟加拉语'analyzeredit

"孟加拉语"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'bengali_example',
      body: {
        settings: {
          analysis: {
            filter: {
              bengali_stop: {
                type: 'stop',
                stopwords: '_bengali_'
              },
              bengali_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'উদাহরণ'
                ]
              },
              bengali_stemmer: {
                type: 'stemmer',
                language: 'bengali'
              }
            },
            analyzer: {
              rebuilt_bengali: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'decimal_digit',
                  'bengali_keywords',
                  'indic_normalization',
                  'bengali_normalization',
                  'bengali_stop',
                  'bengali_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /bengali_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "bengali_stop": {
              "type":       "stop",
              "stopwords":  "_bengali_" __},
            "bengali_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["উদাহরণ"] __},
            "bengali_stemmer": {
              "type":       "stemmer",
              "language":   "bengali"
            }
          },
          "analyzer": {
            "rebuilt_bengali": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "decimal_digit",
                "bengali_keywords",
                "indic_normalization",
                "bengali_normalization",
                "bengali_stop",
                "bengali_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '巴西'分析器编辑

"巴西"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'brazilian_example',
      body: {
        settings: {
          analysis: {
            filter: {
              brazilian_stop: {
                type: 'stop',
                stopwords: '_brazilian_'
              },
              brazilian_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'exemplo'
                ]
              },
              brazilian_stemmer: {
                type: 'stemmer',
                language: 'brazilian'
              }
            },
            analyzer: {
              rebuilt_brazilian: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'brazilian_stop',
                  'brazilian_keywords',
                  'brazilian_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /brazilian_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "brazilian_stop": {
              "type":       "stop",
              "stopwords":  "_brazilian_" __},
            "brazilian_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["exemplo"] __},
            "brazilian_stemmer": {
              "type":       "stemmer",
              "language":   "brazilian"
            }
          },
          "analyzer": {
            "rebuilt_brazilian": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "brazilian_stop",
                "brazilian_keywords",
                "brazilian_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '保加利亚'分析器编辑

"保加利亚"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'bulgarian_example',
      body: {
        settings: {
          analysis: {
            filter: {
              bulgarian_stop: {
                type: 'stop',
                stopwords: '_bulgarian_'
              },
              bulgarian_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'пример'
                ]
              },
              bulgarian_stemmer: {
                type: 'stemmer',
                language: 'bulgarian'
              }
            },
            analyzer: {
              rebuilt_bulgarian: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'bulgarian_stop',
                  'bulgarian_keywords',
                  'bulgarian_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /bulgarian_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "bulgarian_stop": {
              "type":       "stop",
              "stopwords":  "_bulgarian_" __},
            "bulgarian_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["пример"] __},
            "bulgarian_stemmer": {
              "type":       "stemmer",
              "language":   "bulgarian"
            }
          },
          "analyzer": {
            "rebuilt_bulgarian": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "bulgarian_stop",
                "bulgarian_keywords",
                "bulgarian_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '加泰罗尼亚语'分析器编辑

"加泰罗尼亚语"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'catalan_example',
      body: {
        settings: {
          analysis: {
            filter: {
              catalan_elision: {
                type: 'elision',
                articles: [
                  'd',
                  'l',
                  'm',
                  'n',
                  's',
                  't'
                ],
                articles_case: true
              },
              catalan_stop: {
                type: 'stop',
                stopwords: '_catalan_'
              },
              catalan_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'example'
                ]
              },
              catalan_stemmer: {
                type: 'stemmer',
                language: 'catalan'
              }
            },
            analyzer: {
              rebuilt_catalan: {
                tokenizer: 'standard',
                filter: [
                  'catalan_elision',
                  'lowercase',
                  'catalan_stop',
                  'catalan_keywords',
                  'catalan_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /catalan_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "catalan_elision": {
              "type":       "elision",
              "articles":   [ "d", "l", "m", "n", "s", "t"],
              "articles_case": true
            },
            "catalan_stop": {
              "type":       "stop",
              "stopwords":  "_catalan_" __},
            "catalan_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["example"] __},
            "catalan_stemmer": {
              "type":       "stemmer",
              "language":   "catalan"
            }
          },
          "analyzer": {
            "rebuilt_catalan": {
              "tokenizer":  "standard",
              "filter": [
                "catalan_elision",
                "lowercase",
                "catalan_stop",
                "catalan_keywords",
                "catalan_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### 'CJK'analyzerEdit

您可能会发现 ICU 分析插件中的"icu_analyzer"比"cjk"分析器更适合 CJK 文本。试验您的文本和查询。

"cjk"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'cjk_example',
      body: {
        settings: {
          analysis: {
            filter: {
              english_stop: {
                type: 'stop',
                stopwords: [
                  'a',
                  'and',
                  'are',
                  'as',
                  'at',
                  'be',
                  'but',
                  'by',
                  'for',
                  'if',
                  'in',
                  'into',
                  'is',
                  'it',
                  'no',
                  'not',
                  'of',
                  'on',
                  'or',
                  's',
                  'such',
                  't',
                  'that',
                  'the',
                  'their',
                  'then',
                  'there',
                  'these',
                  'they',
                  'this',
                  'to',
                  'was',
                  'will',
                  'with',
                  'www'
                ]
              }
            },
            analyzer: {
              rebuilt_cjk: {
                tokenizer: 'standard',
                filter: [
                  'cjk_width',
                  'lowercase',
                  'cjk_bigram',
                  'english_stop'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /cjk_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "english_stop": {
              "type":       "stop",
              "stopwords":  [ __"a", "and", "are", "as", "at", "be", "but", "by", "for",
                "if", "in", "into", "is", "it", "no", "not", "of", "on",
                "or", "s", "such", "t", "that", "the", "their", "then",
                "there", "these", "they", "this", "to", "was", "will",
                "with", "www"
              ]
            }
          },
          "analyzer": {
            "rebuilt_cjk": {
              "tokenizer":  "standard",
              "filter": [
                "cjk_width",
                "lowercase",
                "cjk_bigram",
                "english_stop"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。默认停用词与"_English_"集几乎相同，但不完全相同。   ---|--- #### 'czech'analyzeredit

"捷克"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'czech_example',
      body: {
        settings: {
          analysis: {
            filter: {
              czech_stop: {
                type: 'stop',
                stopwords: '_czech_'
              },
              czech_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'příklad'
                ]
              },
              czech_stemmer: {
                type: 'stemmer',
                language: 'czech'
              }
            },
            analyzer: {
              rebuilt_czech: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'czech_stop',
                  'czech_keywords',
                  'czech_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /czech_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "czech_stop": {
              "type":       "stop",
              "stopwords":  "_czech_" __},
            "czech_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["příklad"] __},
            "czech_stemmer": {
              "type":       "stemmer",
              "language":   "czech"
            }
          },
          "analyzer": {
            "rebuilt_czech": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "czech_stop",
                "czech_keywords",
                "czech_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '丹麦语'analyzerEdit

"丹麦"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'danish_example',
      body: {
        settings: {
          analysis: {
            filter: {
              danish_stop: {
                type: 'stop',
                stopwords: '_danish_'
              },
              danish_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'eksempel'
                ]
              },
              danish_stemmer: {
                type: 'stemmer',
                language: 'danish'
              }
            },
            analyzer: {
              rebuilt_danish: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'danish_stop',
                  'danish_keywords',
                  'danish_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /danish_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "danish_stop": {
              "type":       "stop",
              "stopwords":  "_danish_" __},
            "danish_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["eksempel"] __},
            "danish_stemmer": {
              "type":       "stemmer",
              "language":   "danish"
            }
          },
          "analyzer": {
            "rebuilt_danish": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "danish_stop",
                "danish_keywords",
                "danish_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '荷兰语'分析器编辑

"荷兰语"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'dutch_example',
      body: {
        settings: {
          analysis: {
            filter: {
              dutch_stop: {
                type: 'stop',
                stopwords: '_dutch_'
              },
              dutch_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'voorbeeld'
                ]
              },
              dutch_stemmer: {
                type: 'stemmer',
                language: 'dutch'
              },
              dutch_override: {
                type: 'stemmer_override',
                rules: [
                  'fiets=>fiets',
                  'bromfiets=>bromfiets',
                  'ei=>eier',
                  'kind=>kinder'
                ]
              }
            },
            analyzer: {
              rebuilt_dutch: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'dutch_stop',
                  'dutch_keywords',
                  'dutch_override',
                  'dutch_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /dutch_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "dutch_stop": {
              "type":       "stop",
              "stopwords":  "_dutch_" __},
            "dutch_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["voorbeeld"] __},
            "dutch_stemmer": {
              "type":       "stemmer",
              "language":   "dutch"
            },
            "dutch_override": {
              "type":       "stemmer_override",
              "rules": [
                "fiets= >fiets",
                "bromfiets=>bromfiets",
                "ei=>eier",
                "kind=>kinder"
              ]
            }
          },
          "analyzer": {
            "rebuilt_dutch": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "dutch_stop",
                "dutch_keywords",
                "dutch_override",
                "dutch_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '英语'分析器编辑

"英语"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'english_example',
      body: {
        settings: {
          analysis: {
            filter: {
              english_stop: {
                type: 'stop',
                stopwords: '_english_'
              },
              english_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'example'
                ]
              },
              english_stemmer: {
                type: 'stemmer',
                language: 'english'
              },
              english_possessive_stemmer: {
                type: 'stemmer',
                language: 'possessive_english'
              }
            },
            analyzer: {
              rebuilt_english: {
                tokenizer: 'standard',
                filter: [
                  'english_possessive_stemmer',
                  'lowercase',
                  'english_stop',
                  'english_keywords',
                  'english_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /english_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "english_stop": {
              "type":       "stop",
              "stopwords":  "_english_" __},
            "english_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["example"] __},
            "english_stemmer": {
              "type":       "stemmer",
              "language":   "english"
            },
            "english_possessive_stemmer": {
              "type":       "stemmer",
              "language":   "possessive_english"
            }
          },
          "analyzer": {
            "rebuilt_english": {
              "tokenizer":  "standard",
              "filter": [
                "english_possessive_stemmer",
                "lowercase",
                "english_stop",
                "english_keywords",
                "english_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '爱沙尼亚'分析器编辑

"爱沙尼亚"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'estonian_example',
      body: {
        settings: {
          analysis: {
            filter: {
              estonian_stop: {
                type: 'stop',
                stopwords: '_estonian_'
              },
              estonian_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'näide'
                ]
              },
              estonian_stemmer: {
                type: 'stemmer',
                language: 'estonian'
              }
            },
            analyzer: {
              rebuilt_estonian: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'estonian_stop',
                  'estonian_keywords',
                  'estonian_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /estonian_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "estonian_stop": {
              "type":       "stop",
              "stopwords":  "_estonian_" __},
            "estonian_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["näide"] __},
            "estonian_stemmer": {
              "type":       "stemmer",
              "language":   "estonian"
            }
          },
          "analyzer": {
            "rebuilt_estonian": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "estonian_stop",
                "estonian_keywords",
                "estonian_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '芬兰语'分析器编辑

"芬兰语"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'finnish_example',
      body: {
        settings: {
          analysis: {
            filter: {
              finnish_stop: {
                type: 'stop',
                stopwords: '_finnish_'
              },
              finnish_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'esimerkki'
                ]
              },
              finnish_stemmer: {
                type: 'stemmer',
                language: 'finnish'
              }
            },
            analyzer: {
              rebuilt_finnish: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'finnish_stop',
                  'finnish_keywords',
                  'finnish_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /finnish_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "finnish_stop": {
              "type":       "stop",
              "stopwords":  "_finnish_" __},
            "finnish_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["esimerkki"] __},
            "finnish_stemmer": {
              "type":       "stemmer",
              "language":   "finnish"
            }
          },
          "analyzer": {
            "rebuilt_finnish": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "finnish_stop",
                "finnish_keywords",
                "finnish_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '法语'分析器编辑

"法语"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'french_example',
      body: {
        settings: {
          analysis: {
            filter: {
              french_elision: {
                type: 'elision',
                articles_case: true,
                articles: [
                  'l',
                  'm',
                  't',
                  'qu',
                  'n',
                  's',
                  'j',
                  'd',
                  'c',
                  'jusqu',
                  'quoiqu',
                  'lorsqu',
                  'puisqu'
                ]
              },
              french_stop: {
                type: 'stop',
                stopwords: '_french_'
              },
              french_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'Example'
                ]
              },
              french_stemmer: {
                type: 'stemmer',
                language: 'light_french'
              }
            },
            analyzer: {
              rebuilt_french: {
                tokenizer: 'standard',
                filter: [
                  'french_elision',
                  'lowercase',
                  'french_stop',
                  'french_keywords',
                  'french_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /french_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "french_elision": {
              "type":         "elision",
              "articles_case": true,
              "articles": [
                  "l", "m", "t", "qu", "n", "s",
                  "j", "d", "c", "jusqu", "quoiqu",
                  "lorsqu", "puisqu"
                ]
            },
            "french_stop": {
              "type":       "stop",
              "stopwords":  "_french_" __},
            "french_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["Example"] __},
            "french_stemmer": {
              "type":       "stemmer",
              "language":   "light_french"
            }
          },
          "analyzer": {
            "rebuilt_french": {
              "tokenizer":  "standard",
              "filter": [
                "french_elision",
                "lowercase",
                "french_stop",
                "french_keywords",
                "french_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '加利西亚语'分析器编辑

"加利西亚"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'galician_example',
      body: {
        settings: {
          analysis: {
            filter: {
              galician_stop: {
                type: 'stop',
                stopwords: '_galician_'
              },
              galician_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'exemplo'
                ]
              },
              galician_stemmer: {
                type: 'stemmer',
                language: 'galician'
              }
            },
            analyzer: {
              rebuilt_galician: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'galician_stop',
                  'galician_keywords',
                  'galician_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /galician_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "galician_stop": {
              "type":       "stop",
              "stopwords":  "_galician_" __},
            "galician_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["exemplo"] __},
            "galician_stemmer": {
              "type":       "stemmer",
              "language":   "galician"
            }
          },
          "analyzer": {
            "rebuilt_galician": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "galician_stop",
                "galician_keywords",
                "galician_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '德语'分析器编辑

"德国"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'german_example',
      body: {
        settings: {
          analysis: {
            filter: {
              german_stop: {
                type: 'stop',
                stopwords: '_german_'
              },
              german_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'Beispiel'
                ]
              },
              german_stemmer: {
                type: 'stemmer',
                language: 'light_german'
              }
            },
            analyzer: {
              rebuilt_german: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'german_stop',
                  'german_keywords',
                  'german_normalization',
                  'german_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /german_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "german_stop": {
              "type":       "stop",
              "stopwords":  "_german_" __},
            "german_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["Beispiel"] __},
            "german_stemmer": {
              "type":       "stemmer",
              "language":   "light_german"
            }
          },
          "analyzer": {
            "rebuilt_german": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "german_stop",
                "german_keywords",
                "german_normalization",
                "german_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '希腊语'分析器编辑

"希腊"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'greek_example',
      body: {
        settings: {
          analysis: {
            filter: {
              greek_stop: {
                type: 'stop',
                stopwords: '_greek_'
              },
              greek_lowercase: {
                type: 'lowercase',
                language: 'greek'
              },
              greek_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'παράδειγμα'
                ]
              },
              greek_stemmer: {
                type: 'stemmer',
                language: 'greek'
              }
            },
            analyzer: {
              rebuilt_greek: {
                tokenizer: 'standard',
                filter: [
                  'greek_lowercase',
                  'greek_stop',
                  'greek_keywords',
                  'greek_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /greek_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "greek_stop": {
              "type":       "stop",
              "stopwords":  "_greek_" __},
            "greek_lowercase": {
              "type":       "lowercase",
              "language":   "greek"
            },
            "greek_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["παράδειγμα"] __},
            "greek_stemmer": {
              "type":       "stemmer",
              "language":   "greek"
            }
          },
          "analyzer": {
            "rebuilt_greek": {
              "tokenizer":  "standard",
              "filter": [
                "greek_lowercase",
                "greek_stop",
                "greek_keywords",
                "greek_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '印地语'分析器编辑

"印地语"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'hindi_example',
      body: {
        settings: {
          analysis: {
            filter: {
              hindi_stop: {
                type: 'stop',
                stopwords: '_hindi_'
              },
              hindi_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'उदाहरण'
                ]
              },
              hindi_stemmer: {
                type: 'stemmer',
                language: 'hindi'
              }
            },
            analyzer: {
              rebuilt_hindi: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'decimal_digit',
                  'hindi_keywords',
                  'indic_normalization',
                  'hindi_normalization',
                  'hindi_stop',
                  'hindi_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /hindi_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "hindi_stop": {
              "type":       "stop",
              "stopwords":  "_hindi_" __},
            "hindi_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["उदाहरण"] __},
            "hindi_stemmer": {
              "type":       "stemmer",
              "language":   "hindi"
            }
          },
          "analyzer": {
            "rebuilt_hindi": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "decimal_digit",
                "hindi_keywords",
                "indic_normalization",
                "hindi_normalization",
                "hindi_stop",
                "hindi_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '匈牙利'分析器编辑

"匈牙利"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'hungarian_example',
      body: {
        settings: {
          analysis: {
            filter: {
              hungarian_stop: {
                type: 'stop',
                stopwords: '_hungarian_'
              },
              hungarian_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'példa'
                ]
              },
              hungarian_stemmer: {
                type: 'stemmer',
                language: 'hungarian'
              }
            },
            analyzer: {
              rebuilt_hungarian: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'hungarian_stop',
                  'hungarian_keywords',
                  'hungarian_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /hungarian_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "hungarian_stop": {
              "type":       "stop",
              "stopwords":  "_hungarian_" __},
            "hungarian_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["példa"] __},
            "hungarian_stemmer": {
              "type":       "stemmer",
              "language":   "hungarian"
            }
          },
          "analyzer": {
            "rebuilt_hungarian": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "hungarian_stop",
                "hungarian_keywords",
                "hungarian_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '印尼语'分析器编辑

"印度尼西亚"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'indonesian_example',
      body: {
        settings: {
          analysis: {
            filter: {
              indonesian_stop: {
                type: 'stop',
                stopwords: '_indonesian_'
              },
              indonesian_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'contoh'
                ]
              },
              indonesian_stemmer: {
                type: 'stemmer',
                language: 'indonesian'
              }
            },
            analyzer: {
              rebuilt_indonesian: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'indonesian_stop',
                  'indonesian_keywords',
                  'indonesian_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /indonesian_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "indonesian_stop": {
              "type":       "stop",
              "stopwords":  "_indonesian_" __},
            "indonesian_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["contoh"] __},
            "indonesian_stemmer": {
              "type":       "stemmer",
              "language":   "indonesian"
            }
          },
          "analyzer": {
            "rebuilt_indonesian": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "indonesian_stop",
                "indonesian_keywords",
                "indonesian_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '爱尔兰'分析器编辑

"爱尔兰"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'irish_example',
      body: {
        settings: {
          analysis: {
            filter: {
              irish_hyphenation: {
                type: 'stop',
                stopwords: [
                  'h',
                  'n',
                  't'
                ],
                ignore_case: true
              },
              irish_elision: {
                type: 'elision',
                articles: [
                  'd',
                  'm',
                  'b'
                ],
                articles_case: true
              },
              irish_stop: {
                type: 'stop',
                stopwords: '_irish_'
              },
              irish_lowercase: {
                type: 'lowercase',
                language: 'irish'
              },
              irish_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'sampla'
                ]
              },
              irish_stemmer: {
                type: 'stemmer',
                language: 'irish'
              }
            },
            analyzer: {
              rebuilt_irish: {
                tokenizer: 'standard',
                filter: [
                  'irish_hyphenation',
                  'irish_elision',
                  'irish_lowercase',
                  'irish_stop',
                  'irish_keywords',
                  'irish_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /irish_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "irish_hyphenation": {
              "type":       "stop",
              "stopwords":  [ "h", "n", "t" ],
              "ignore_case": true
            },
            "irish_elision": {
              "type":       "elision",
              "articles":   [ "d", "m", "b" ],
              "articles_case": true
            },
            "irish_stop": {
              "type":       "stop",
              "stopwords":  "_irish_" __},
            "irish_lowercase": {
              "type":       "lowercase",
              "language":   "irish"
            },
            "irish_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["sampla"] __},
            "irish_stemmer": {
              "type":       "stemmer",
              "language":   "irish"
            }
          },
          "analyzer": {
            "rebuilt_irish": {
              "tokenizer":  "standard",
              "filter": [
                "irish_hyphenation",
                "irish_elision",
                "irish_lowercase",
                "irish_stop",
                "irish_keywords",
                "irish_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### 'Italian'analyzeredit

"意大利语"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'italian_example',
      body: {
        settings: {
          analysis: {
            filter: {
              italian_elision: {
                type: 'elision',
                articles: [
                  'c',
                  'l',
                  'all',
                  'dall',
                  'dell',
                  'nell',
                  'sull',
                  'coll',
                  'pell',
                  'gl',
                  'agl',
                  'dagl',
                  'degl',
                  'negl',
                  'sugl',
                  'un',
                  'm',
                  't',
                  's',
                  'v',
                  'd'
                ],
                articles_case: true
              },
              italian_stop: {
                type: 'stop',
                stopwords: '_italian_'
              },
              italian_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'esempio'
                ]
              },
              italian_stemmer: {
                type: 'stemmer',
                language: 'light_italian'
              }
            },
            analyzer: {
              rebuilt_italian: {
                tokenizer: 'standard',
                filter: [
                  'italian_elision',
                  'lowercase',
                  'italian_stop',
                  'italian_keywords',
                  'italian_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /italian_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "italian_elision": {
              "type": "elision",
              "articles": [
                    "c", "l", "all", "dall", "dell",
                    "nell", "sull", "coll", "pell",
                    "gl", "agl", "dagl", "degl", "negl",
                    "sugl", "un", "m", "t", "s", "v", "d"
              ],
              "articles_case": true
            },
            "italian_stop": {
              "type":       "stop",
              "stopwords":  "_italian_" __},
            "italian_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["esempio"] __},
            "italian_stemmer": {
              "type":       "stemmer",
              "language":   "light_italian"
            }
          },
          "analyzer": {
            "rebuilt_italian": {
              "tokenizer":  "standard",
              "filter": [
                "italian_elision",
                "lowercase",
                "italian_stop",
                "italian_keywords",
                "italian_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '拉脱维亚'分析器编辑

"拉脱维亚"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'latvian_example',
      body: {
        settings: {
          analysis: {
            filter: {
              latvian_stop: {
                type: 'stop',
                stopwords: '_latvian_'
              },
              latvian_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'piemērs'
                ]
              },
              latvian_stemmer: {
                type: 'stemmer',
                language: 'latvian'
              }
            },
            analyzer: {
              rebuilt_latvian: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'latvian_stop',
                  'latvian_keywords',
                  'latvian_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /latvian_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "latvian_stop": {
              "type":       "stop",
              "stopwords":  "_latvian_" __},
            "latvian_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["piemērs"] __},
            "latvian_stemmer": {
              "type":       "stemmer",
              "language":   "latvian"
            }
          },
          "analyzer": {
            "rebuilt_latvian": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "latvian_stop",
                "latvian_keywords",
                "latvian_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '立陶宛'分析器编辑

"立陶宛"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'lithuanian_example',
      body: {
        settings: {
          analysis: {
            filter: {
              lithuanian_stop: {
                type: 'stop',
                stopwords: '_lithuanian_'
              },
              lithuanian_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'pavyzdys'
                ]
              },
              lithuanian_stemmer: {
                type: 'stemmer',
                language: 'lithuanian'
              }
            },
            analyzer: {
              rebuilt_lithuanian: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'lithuanian_stop',
                  'lithuanian_keywords',
                  'lithuanian_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /lithuanian_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "lithuanian_stop": {
              "type":       "stop",
              "stopwords":  "_lithuanian_" __},
            "lithuanian_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["pavyzdys"] __},
            "lithuanian_stemmer": {
              "type":       "stemmer",
              "language":   "lithuanian"
            }
          },
          "analyzer": {
            "rebuilt_lithuanian": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "lithuanian_stop",
                "lithuanian_keywords",
                "lithuanian_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '挪威语'analyzeredit

"挪威"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'norwegian_example',
      body: {
        settings: {
          analysis: {
            filter: {
              norwegian_stop: {
                type: 'stop',
                stopwords: '_norwegian_'
              },
              norwegian_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'eksempel'
                ]
              },
              norwegian_stemmer: {
                type: 'stemmer',
                language: 'norwegian'
              }
            },
            analyzer: {
              rebuilt_norwegian: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'norwegian_stop',
                  'norwegian_keywords',
                  'norwegian_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /norwegian_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "norwegian_stop": {
              "type":       "stop",
              "stopwords":  "_norwegian_" __},
            "norwegian_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["eksempel"] __},
            "norwegian_stemmer": {
              "type":       "stemmer",
              "language":   "norwegian"
            }
          },
          "analyzer": {
            "rebuilt_norwegian": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "norwegian_stop",
                "norwegian_keywords",
                "norwegian_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '波斯语'分析器编辑

"波斯语"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'persian_example',
      body: {
        settings: {
          analysis: {
            char_filter: {
              zero_width_spaces: {
                type: 'mapping',
                mappings: [
                  '\\u200C=>\\u0020'
                ]
              }
            },
            filter: {
              persian_stop: {
                type: 'stop',
                stopwords: '_persian_'
              }
            },
            analyzer: {
              rebuilt_persian: {
                tokenizer: 'standard',
                char_filter: [
                  'zero_width_spaces'
                ],
                filter: [
                  'lowercase',
                  'decimal_digit',
                  'arabic_normalization',
                  'persian_normalization',
                  'persian_stop'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /persian_example
    {
      "settings": {
        "analysis": {
          "char_filter": {
            "zero_width_spaces": {
                "type":       "mapping",
                "mappings": [ "\\u200C=>\\u0020"] __}
          },
          "filter": {
            "persian_stop": {
              "type":       "stop",
              "stopwords":  "_persian_" __}
          },
          "analyzer": {
            "rebuilt_persian": {
              "tokenizer":     "standard",
              "char_filter": [ "zero_width_spaces" ],
              "filter": [
                "lowercase",
                "decimal_digit",
                "arabic_normalization",
                "persian_normalization",
                "persian_stop"
              ]
            }
          }
        }
      }
    }

__

|

将零宽度的非连接符替换为 ASCII 空格。   ---|---    __

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   #### '葡萄牙语'分析器编辑

"葡萄牙语"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'portuguese_example',
      body: {
        settings: {
          analysis: {
            filter: {
              portuguese_stop: {
                type: 'stop',
                stopwords: '_portuguese_'
              },
              portuguese_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'exemplo'
                ]
              },
              portuguese_stemmer: {
                type: 'stemmer',
                language: 'light_portuguese'
              }
            },
            analyzer: {
              rebuilt_portuguese: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'portuguese_stop',
                  'portuguese_keywords',
                  'portuguese_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /portuguese_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "portuguese_stop": {
              "type":       "stop",
              "stopwords":  "_portuguese_" __},
            "portuguese_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["exemplo"] __},
            "portuguese_stemmer": {
              "type":       "stemmer",
              "language":   "light_portuguese"
            }
          },
          "analyzer": {
            "rebuilt_portuguese": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "portuguese_stop",
                "portuguese_keywords",
                "portuguese_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '罗马尼亚语'分析器编辑

"罗马尼亚"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'romanian_example',
      body: {
        settings: {
          analysis: {
            filter: {
              romanian_stop: {
                type: 'stop',
                stopwords: '_romanian_'
              },
              romanian_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'exemplu'
                ]
              },
              romanian_stemmer: {
                type: 'stemmer',
                language: 'romanian'
              }
            },
            analyzer: {
              rebuilt_romanian: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'romanian_stop',
                  'romanian_keywords',
                  'romanian_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /romanian_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "romanian_stop": {
              "type":       "stop",
              "stopwords":  "_romanian_" __},
            "romanian_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["exemplu"] __},
            "romanian_stemmer": {
              "type":       "stemmer",
              "language":   "romanian"
            }
          },
          "analyzer": {
            "rebuilt_romanian": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "romanian_stop",
                "romanian_keywords",
                "romanian_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '俄语'分析器编辑

"俄罗斯"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'russian_example',
      body: {
        settings: {
          analysis: {
            filter: {
              russian_stop: {
                type: 'stop',
                stopwords: '_russian_'
              },
              russian_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'пример'
                ]
              },
              russian_stemmer: {
                type: 'stemmer',
                language: 'russian'
              }
            },
            analyzer: {
              rebuilt_russian: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'russian_stop',
                  'russian_keywords',
                  'russian_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /russian_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "russian_stop": {
              "type":       "stop",
              "stopwords":  "_russian_" __},
            "russian_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["пример"] __},
            "russian_stemmer": {
              "type":       "stemmer",
              "language":   "russian"
            }
          },
          "analyzer": {
            "rebuilt_russian": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "russian_stop",
                "russian_keywords",
                "russian_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### 'sorani'analyzeredit

"sorani"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'sorani_example',
      body: {
        settings: {
          analysis: {
            filter: {
              sorani_stop: {
                type: 'stop',
                stopwords: '_sorani_'
              },
              sorani_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'mînak'
                ]
              },
              sorani_stemmer: {
                type: 'stemmer',
                language: 'sorani'
              }
            },
            analyzer: {
              rebuilt_sorani: {
                tokenizer: 'standard',
                filter: [
                  'sorani_normalization',
                  'lowercase',
                  'decimal_digit',
                  'sorani_stop',
                  'sorani_keywords',
                  'sorani_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /sorani_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "sorani_stop": {
              "type":       "stop",
              "stopwords":  "_sorani_" __},
            "sorani_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["mînak"] __},
            "sorani_stemmer": {
              "type":       "stemmer",
              "language":   "sorani"
            }
          },
          "analyzer": {
            "rebuilt_sorani": {
              "tokenizer":  "standard",
              "filter": [
                "sorani_normalization",
                "lowercase",
                "decimal_digit",
                "sorani_stop",
                "sorani_keywords",
                "sorani_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '西班牙语'分析器编辑

"西班牙语"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'spanish_example',
      body: {
        settings: {
          analysis: {
            filter: {
              spanish_stop: {
                type: 'stop',
                stopwords: '_spanish_'
              },
              spanish_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'ejemplo'
                ]
              },
              spanish_stemmer: {
                type: 'stemmer',
                language: 'light_spanish'
              }
            },
            analyzer: {
              rebuilt_spanish: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'spanish_stop',
                  'spanish_keywords',
                  'spanish_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /spanish_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "spanish_stop": {
              "type":       "stop",
              "stopwords":  "_spanish_" __},
            "spanish_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["ejemplo"] __},
            "spanish_stemmer": {
              "type":       "stemmer",
              "language":   "light_spanish"
            }
          },
          "analyzer": {
            "rebuilt_spanish": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "spanish_stop",
                "spanish_keywords",
                "spanish_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '瑞典语'analyzeredit

"瑞典"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'swedish_example',
      body: {
        settings: {
          analysis: {
            filter: {
              swedish_stop: {
                type: 'stop',
                stopwords: '_swedish_'
              },
              swedish_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'exempel'
                ]
              },
              swedish_stemmer: {
                type: 'stemmer',
                language: 'swedish'
              }
            },
            analyzer: {
              rebuilt_swedish: {
                tokenizer: 'standard',
                filter: [
                  'lowercase',
                  'swedish_stop',
                  'swedish_keywords',
                  'swedish_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /swedish_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "swedish_stop": {
              "type":       "stop",
              "stopwords":  "_swedish_" __},
            "swedish_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["exempel"] __},
            "swedish_stemmer": {
              "type":       "stemmer",
              "language":   "swedish"
            }
          },
          "analyzer": {
            "rebuilt_swedish": {
              "tokenizer":  "standard",
              "filter": [
                "lowercase",
                "swedish_stop",
                "swedish_keywords",
                "swedish_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '土耳其语'分析器编辑

"土耳其"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'turkish_example',
      body: {
        settings: {
          analysis: {
            filter: {
              turkish_stop: {
                type: 'stop',
                stopwords: '_turkish_'
              },
              turkish_lowercase: {
                type: 'lowercase',
                language: 'turkish'
              },
              turkish_keywords: {
                type: 'keyword_marker',
                keywords: [
                  'örnek'
                ]
              },
              turkish_stemmer: {
                type: 'stemmer',
                language: 'turkish'
              }
            },
            analyzer: {
              rebuilt_turkish: {
                tokenizer: 'standard',
                filter: [
                  'apostrophe',
                  'turkish_lowercase',
                  'turkish_stop',
                  'turkish_keywords',
                  'turkish_stemmer'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /turkish_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "turkish_stop": {
              "type":       "stop",
              "stopwords":  "_turkish_" __},
            "turkish_lowercase": {
              "type":       "lowercase",
              "language":   "turkish"
            },
            "turkish_keywords": {
              "type":       "keyword_marker",
              "keywords":   ["örnek"] __},
            "turkish_stemmer": {
              "type":       "stemmer",
              "language":   "turkish"
            }
          },
          "analyzer": {
            "rebuilt_turkish": {
              "tokenizer":  "standard",
              "filter": [
                "apostrophe",
                "turkish_lowercase",
                "turkish_stop",
                "turkish_keywords",
                "turkish_stemmer"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|---    __

|

应删除此过滤器，除非存在应从词干中排除的单词。   #### '泰语'分析器编辑

"泰式"分析器可以重新实现为"自定义"分析器，如下所示：

    
    
    response = client.indices.create(
      index: 'thai_example',
      body: {
        settings: {
          analysis: {
            filter: {
              thai_stop: {
                type: 'stop',
                stopwords: '_thai_'
              }
            },
            analyzer: {
              rebuilt_thai: {
                tokenizer: 'thai',
                filter: [
                  'lowercase',
                  'decimal_digit',
                  'thai_stop'
                ]
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT /thai_example
    {
      "settings": {
        "analysis": {
          "filter": {
            "thai_stop": {
              "type":       "stop",
              "stopwords":  "_thai_" __}
          },
          "analyzer": {
            "rebuilt_thai": {
              "tokenizer":  "thai",
              "filter": [
                "lowercase",
                "decimal_digit",
                "thai_stop"
              ]
            }
          }
        }
      }
    }

__

|

默认停用词可以用"停用词"或"stopwords_path"参数覆盖。   ---|--- « 关键字分析器 模式分析器»