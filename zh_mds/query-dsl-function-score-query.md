

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md) ›[Compound queries](compound-queries.md)

[« Disjunction max query](query-dsl-dis-max-query.md) [Full text queries
»](full-text-queries.md)

## 函数得分查询

"function_score"允许您修改查询检索的文档的分数。例如，如果分数函数的计算成本很高，并且足以计算筛选的文档集的分数，则这可能很有用。

要使用"function_score"，用户必须定义一个查询和一个或多个函数，为查询返回的每个文档计算新的分数。

"function_score"只能与一个函数一起使用，如下所示：

    
    
    response = client.search(
      body: {
        query: {
          function_score: {
            query: {
              match_all: {}
            },
            boost: '5',
            random_score: {},
            boost_mode: 'multiply'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "function_score": {
    	      "query": {
    	        "match_all": {}
    	      },
    	      "boost": "5",
    	      "random_score": {},
    	      "boost_mode": "multiply"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "function_score": {
          "query": { "match_all": {} },
          "boost": "5",
          "random_score": {}, __"boost_mode": "multiply"
        }
      }
    }

__

|

有关支持函数的列表，请参阅函数分数。   ---|--- 此外，还可以组合多个功能。在这种情况下，可以选择仅在文档与给定的筛选查询匹配时才应用该函数

    
    
    response = client.search(
      body: {
        query: {
          function_score: {
            query: {
              match_all: {}
            },
            boost: '5',
            functions: [
              {
                filter: {
                  match: {
                    test: 'bar'
                  }
                },
                random_score: {},
                weight: 23
              },
              {
                filter: {
                  match: {
                    test: 'cat'
                  }
                },
                weight: 42
              }
            ],
            max_boost: 42,
            score_mode: 'max',
            boost_mode: 'multiply',
            min_score: 42
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "function_score": {
    	      "query": {
    	        "match_all": {}
    	      },
    	      "boost": "5",
    	      "functions": [
    	        {
    	          "filter": {
    	            "match": {
    	              "test": "bar"
    	            }
    	          },
    	          "random_score": {},
    	          "weight": 23
    	        },
    	        {
    	          "filter": {
    	            "match": {
    	              "test": "cat"
    	            }
    	          },
    	          "weight": 42
    	        }
    	      ],
    	      "max_boost": 42,
    	      "score_mode": "max",
    	      "boost_mode": "multiply",
    	      "min_score": 42
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "function_score": {
          "query": { "match_all": {} },
          "boost": "5", __"functions": [
            {
              "filter": { "match": { "test": "bar" } },
              "random_score": {}, __"weight": 23
            },
            {
              "filter": { "match": { "test": "cat" } },
              "weight": 42
            }
          ],
          "max_boost": 42,
          "score_mode": "max",
          "boost_mode": "multiply",
          "min_score": 42
        }
      }
    }

__

|

提升整个查询。   ---|---    __

|

有关支持函数的列表，请参阅函数分数。   每个函数的筛选查询生成的分数无关紧要。

如果没有给出带有函数的过滤器，则等效于指定""match_all"：{}'

首先，每个文档都由定义的函数评分。参数"score_mode"指定如何组合计算的分数：

`multiply`

|

分数乘以(默认)---|---"总和"

|

分数相加为"平均"

|

分数平均为"第一"

|

具有匹配过滤器的第一个函数应用"max"

|

最高分使用"最低"

|

使用最低分数 由于分数可以采用不同的量表(例如，在 0 到 1 个 fordecay 函数之间，但对于"field_value_factor"是任意的)，并且还因为有时函数对分数的不同影响是需要的，因此可以使用用户定义的"权重"调整每个函数的分数。"权重"可以在"函数"数组(上面的例子)中为每个函数定义，并与相应函数计算的分数相乘。如果在没有任何其他函数声明的情况下给出权重，则"weight"充当仅返回"weight"的函数。

如果"score_mode"设置为"平均"，则各个分数将按**加权**平均值合并。例如，如果两个函数返回分数 1 和 2，并且它们各自的权重为 3 和 4，则它们的分数将合并为 '(1*3+2*4)/(3+4)' 和 **not** '(1*3+2*4)/2'。

可以通过设置"max_boost"参数将新分数限制为不超过特定限制。"max_boost"的默认值为 FLT_MAX。

新计算的分数与查询的分数相结合。参数"boost_mode"定义如何：

`multiply`

|

查询分数和函数分数乘以(默认值)---|---"替换"

|

仅使用函数分数，忽略查询分数"总和"

|

查询分数和函数分数添加"平均"

|

平均"最大值"

|

查询分数和函数分数的最大值"最小"

|

最小查询分数和函数分数 默认情况下，修改分数不会更改匹配的文档。要排除未达到特定分数阈值的文档，可以将"min_score"参数设置为所需的分数阈值。

要使"min_score"正常工作，查询返回的**所有**文档都需要进行评分，然后逐个筛选掉。

"function_score"查询提供多种类型的分数函数。

* "script_score" * "重量" * "random_score" * "field_value_factor" * 衰减函数："高斯"、"线性"、"EXP"

### 脚本分数

"script_score"函数允许您包装另一个查询，并使用脚本表达式从文档中的其他数值字段值派生的计算来自定义其评分。下面是一个简单的示例：

    
    
    response = client.search(
      body: {
        query: {
          function_score: {
            query: {
              match: {
                message: 'elasticsearch'
              }
            },
            script_score: {
              script: {
                source: "Math.log(2 + doc['my-int'].value)"
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "function_score": {
          "query": {
            "match": { "message": "elasticsearch" }
          },
          "script_score": {
            "script": {
              "source": "Math.log(2 + doc['my-int'].value)"
            }
          }
        }
      }
    }

在 Elasticsearch 中，所有文档分数都是正 32 位浮点数。

如果"script_score"函数生成更高精度的分数，则会将其转换为最接近的 32 位浮点数。

同样，分数必须是非负的。否则，Elasticsearch 会返回错误。

除了不同的脚本字段值和表达式之外，"_score"script 参数可用于根据包装的查询检索分数。

缓存脚本编译以加快执行速度。如果脚本具有需要考虑的参数，则最好重用同一脚本，并为其提供参数：

    
    
    response = client.search(
      body: {
        query: {
          function_score: {
            query: {
              match: {
                message: 'elasticsearch'
              }
            },
            script_score: {
              script: {
                params: {
                  a: 5,
                  b: 1.2
                },
                source: "params.a / Math.pow(params.b, doc['my-int'].value)"
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "function_score": {
          "query": {
            "match": { "message": "elasticsearch" }
          },
          "script_score": {
            "script": {
              "params": {
                "a": 5,
                "b": 1.2
              },
              "source": "params.a / Math.pow(params.b, doc['my-int'].value)"
            }
          }
        }
      }
    }

请注意，与"custom_score"查询不同，查询的分数乘以脚本评分的结果。如果要禁止此操作，请设置"boost_mode"："替换"

###Weight

"权重"分数允许您将分数乘以提供的"权重"。这有时是需要的，因为在特定查询上设置的提升值被规范化，而对于此分数函数，它不需要。数值的类型为 float。

    
    
    "weight" : number

###Random

"random_score"生成的分数均匀分布，从 0 到但不包括 1。默认情况下，它使用内部 Lucene 文档 ID 作为随机性的来源，这非常有效，但不幸的是不可重现，因为文档可能会通过合并重新编号。

如果您希望分数可重复，则可以提供"种子"和"字段"。然后，最终分数将根据此种子、所考虑文档的"field"的最小值以及基于索引名称和分片 id 计算的盐计算，以便具有相同值但存储在不同索引中的文档获得不同的分数。请注意，位于同一分片中且具有相同"字段"值的文档将获得相同的分数，因此通常需要使用对所有文档具有唯一值的字段。一个不错的默认选择可能是使用"_seq_no"字段，其唯一的缺点是，如果更新文档，分数会发生变化，因为更新操作也会更新"_seq_no"字段的值。

可以在不设置字段的情况下设置种子，但这已被弃用，因为这需要在"_id"字段上加载字段数据，这会消耗大量内存。

    
    
    response = client.search(
      body: {
        query: {
          function_score: {
            random_score: {
              seed: 10,
              field: '_seq_no'
            }
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "function_score": {
    	      "random_score": {
    	        "seed": 10,
    	        "field": "_seq_no"
    	      }
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "function_score": {
          "random_score": {
            "seed": 10,
            "field": "_seq_no"
          }
        }
      }
    }

### 字段价值因子

"field_value_factor"功能允许您使用文档中的字段来影响分数。它类似于使用"script_score"函数，但是，它避免了脚本的开销。如果用于多值字段，则在计算中仅使用该字段的第一个值。

例如，假设您有一个使用数字"my-int"字段编制索引的文档，并希望使用此字段影响文档的分数，这样做的示例如下所示：

    
    
    response = client.search(
      body: {
        query: {
          function_score: {
            field_value_factor: {
              field: 'my-int',
              factor: 1.2,
              modifier: 'sqrt',
              missing: 1
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "function_score": {
          "field_value_factor": {
            "field": "my-int",
            "factor": 1.2,
            "modifier": "sqrt",
            "missing": 1
          }
        }
      }
    }

这将转化为以下评分公式：

'sqrt(1.2 * doc['my-int'].value)'

"field_value_factor"功能有许多选项：

`field`

|

要从文档中提取的字段。   ---|---"因素"

|

将字段值乘以的可选因子默认为"1"。   "修饰符"

|

应用于字段值的修饰符可以是以下之一："无"、"日志"、"log1p"、"log2p"、"ln"、"ln1p"、"ln2p"、"square"、"sqrt"或"倒数"。默认为"无"。   修饰符 |含义 ---|--- "无"

|

不要对字段值"log"应用任何乘数

|

取字段值的公共对数。由于此函数将返回负值，如果对 0 到 1 之间的值使用会导致错误，因此建议改用"log1p"。   'log1p'

|

字段值加 1 并取公共对数 'log2p'

|

将 2 加到字段值并取公共对数 'ln'

|

取字段值的自然对数。由于此函数将返回负值，如果对 0 到 1 之间的值使用会导致错误，因此建议改用"ln1p"。   'LN1P'

|

字段值加 1 并取自然对数 'ln2p'

|

字段值加 2 并取自然对数"平方"

|

对字段值进行平方(将其乘以自身)'sqrt'

|

取字段值"倒数"的平方根

|

对字段值进行复复，与"1/x"相同，其中"x"是字段的值"缺失"

     Value used if the document doesn't have that field. The modifier and factor are still applied to it as though it were read from the document. 

"field_value_score"函数产生的分数必须是非负的，否则将抛出错误。如果将 'log' 和 'ln' 修饰符用于 0 到 1 之间的值，将产生负值。请务必使用范围筛选器限制字段的值以避免这种情况，或使用"log1p"和"ln1p"。

请记住，取 log() 的 0 或负数的平方根是非法操作，并且会引发异常。请务必使用范围过滤器限制字段的值以避免这种情况，或使用"log1p"和"ln1p"。

### 衰减函数

衰减函数使用一个函数对文档进行评分，该函数根据文档的数值字段值与用户给定原点的距离进行衰减。这类似于范围查询，但使用平滑边缘而不是框。

若要对具有数值字段的查询使用距离评分，用户必须为每个字段定义"原点"和"比例"。需要"原点"来定义计算距离的"中心点"，需要"尺度"来定义衰减率。衰减函数指定为

    
    
    "DECAY_FUNCTION": { __"FIELD_NAME": { __"origin": "11, 12",
              "scale": "2km",
              "offset": "0km",
              "decay": 0.33
        }
    }

__

|

"DECAY_FUNCTION"应该是"线性"、"exp"或"高斯"之一。   ---|---    __

|

指定的字段必须是数值、日期或地理点字段。   在上面的示例中，字段是"geo_point"，原点可以以地理格式提供。在这种情况下，"比例"和"偏移"必须用单位给出。如果您的字段是日期字段，则可以将"小数位数"和"偏移量"设置为天、周等。例：

    
    
    response = client.search(
      body: {
        query: {
          function_score: {
            gauss: {
              "@timestamp": {
                origin: '2013-09-17',
                scale: '10d',
                offset: '5d',
                decay: 0.5
              }
            }
          }
        }
      }
    )
    puts response
    
    
    GET /_search
    {
      "query": {
        "function_score": {
          "gauss": {
            "@timestamp": {
              "origin": "2013-09-17", __"scale": "10d",
              "offset": "5d", __"decay": 0.5 __}
          }
        }
      }
    }

__

|

原点的日期格式取决于映射中定义的"格式"。如果未定义原点，则使用当前时间。   ---|---    __

|

"偏移"和"衰减"参数是可选的。   "起源"

|

用于计算距离的原点。对于数值字段，必须以数字形式提供，对于日期字段，必须以日期形式提供，对于地理字段，必须以地理点形式提供。对于地理和数值字段是必需的。对于日期字段，默认值为"现在"。原点支持日期数学(例如"now-1h")。   ---|---"规模"

|

所有类型都需要。定义与原点的距离 + 偏移量，在该距离处计算的分数将等于"衰减"参数。对于地理字段：可以定义为数字+单位(1公里，12米,...)。默认单位为米。对于日期字段：可以定义为数字+单位("1h"、"10d",...)。默认单位为毫秒。fornumeric 字段：任何数字。   "偏移"

|

如果定义了"偏移量"，则衰减函数将仅计算距离大于定义的"偏移量"的文档的衰减函数。默认值为 0。   "腐烂"

|

"衰减"参数定义了如何在"比例"上给出的距离对文档进行评分。如果未定义"衰减"，则距离"量表"的文档将获得 0.5 分。   在第一个示例中，您的文档可能代表酒店并包含地理位置字段。您希望根据酒店距给定位置的距离来计算衰减函数。您可能不会立即看到为高斯函数选择什么比例，但您可以这样说："在距离所需位置 2 公里处，分数应减少到三分之一。然后，参数"scale"将自动调整，以确保 score 函数计算距离所需位置 2 公里的酒店的分数为 0.33。

在第二个示例中，字段值介于 2013-09-12 和 2013-09-22 之间的文档的权重为 1.0，自该日期起 15 天的文档的权重为 0.5。

#### 支持的衰减函数

"DECAY_FUNCTION"决定了衰变的形状：

`gauss`

    

正态衰减，计算公式为：

![Gaussian](images/Gaussian.png)

其中计算 ！sigma 以确保分数在距离"原点"+-"偏移量"的距离"尺度"上取值"衰减"

西格玛计算

请参阅正态衰减，关键字"高斯"，以获取演示由"高斯"函数生成的曲线的图形。

`exp`

    

指数衰减，计算公式为：

![Exponential](images/Exponential.png)

再次计算参数 ！lambda 以确保分数在距离"原点"+-"偏移量"的距离"尺度"处取值"衰减"

！λ计算

请参阅指数衰减，关键字"exp"，用于演示由"exp"函数生成的曲线的图形。

`linear`

    

线性衰减，计算公式为：

![Linear](images/Linear.png).

再次计算参数"s"以确保分数在距离"原点"+-"偏移量"的距离"尺度"上取值"衰减"

！

与正态衰减和指数衰减相反，如果字段值超过用户给定比例值的两倍，则此函数实际上将分数设置为 0。

对于单个函数，三个衰减函数及其参数可以像这样可视化(此示例中的字段称为"age")：

！衰减 2D

#### 多值字段

如果用于计算衰减的字段包含多个值，则默认情况下选择最接近原点的值来确定距离。这可以通过设置"multi_value_mode"来更改。

`min`

|

距离是最小距离---|---"最大"

|

距离是最大距离"平均"

|

距离是平均距离"总和"

|

距离是所有距离的总和 示例：

    
    
        "DECAY_FUNCTION": {
            "FIELD_NAME": {
                  "origin": ...,
                  "scale": ...
            },
            "multi_value_mode": "avg"
        }

### 详细示例

假设您正在某个城镇寻找一家酒店。您的预算是有限的。此外，您希望酒店靠近镇中心，因此酒店离所需位置越远，您办理入住手续的可能性就越小。

您希望根据到市中心的距离和价格对与您的条件(例如，"酒店、南锡、非吸烟者")匹配的查询结果进行评分。

直觉上，您想将市中心定义为原点，也许您愿意从酒店步行 2 公里到市中心。 在本例中，位置字段的原点是市中心，比例尺为 ~2 公里。

如果您的预算很低，您可能更喜欢便宜的东西而不是昂贵的东西。对于价格字段，**原产地**将为0欧元，**比例**取决于您愿意支付的金额，例如20欧元。

在此示例中，对于酒店的价格，这些字段可能称为"价格"，对于此酒店的坐标，这些字段可能称为"位置"。

在这种情况下，"价格"的函数将是

    
    
    "gauss": { __"price": {
              "origin": "0",
              "scale": "20"
        }
    }

__

|

这个衰减函数也可以是"线性"或"exp"。   ---|--- 和"位置"：

    
    
    "gauss": { __"location": {
              "origin": "11, 12",
              "scale": "2km"
        }
    }

__

|

这个衰减函数也可以是"线性"或"exp"。   ---|--- 假设你想在原始分数上将这两个函数相乘，请求将如下所示：

    
    
    response = client.search(
      body: {
        query: {
          function_score: {
            functions: [
              {
                gauss: {
                  price: {
                    origin: '0',
                    scale: '20'
                  }
                }
              },
              {
                gauss: {
                  location: {
                    origin: '11, 12',
                    scale: '2km'
                  }
                }
              }
            ],
            query: {
              match: {
                properties: 'balcony'
              }
            },
            score_mode: 'multiply'
          }
        }
      }
    )
    puts response
    
    
    res, err := es.Search(
    	es.Search.WithBody(strings.NewReader(`{
    	  "query": {
    	    "function_score": {
    	      "functions": [
    	        {
    	          "gauss": {
    	            "price": {
    	              "origin": "0",
    	              "scale": "20"
    	            }
    	          }
    	        },
    	        {
    	          "gauss": {
    	            "location": {
    	              "origin": "11, 12",
    	              "scale": "2km"
    	            }
    	          }
    	        }
    	      ],
    	      "query": {
    	        "match": {
    	          "properties": "balcony"
    	        }
    	      },
    	      "score_mode": "multiply"
    	    }
    	  }
    	}`)),
    	es.Search.WithPretty(),
    )
    fmt.Println(res, err)
    
    
    GET /_search
    {
      "query": {
        "function_score": {
          "functions": [
            {
              "gauss": {
                "price": {
                  "origin": "0",
                  "scale": "20"
                }
              }
            },
            {
              "gauss": {
                "location": {
                  "origin": "11, 12",
                  "scale": "2km"
                }
              }
            }
          ],
          "query": {
            "match": {
              "properties": "balcony"
            }
          },
          "score_mode": "multiply"
        }
      }
    }

接下来，我们展示三个可能的衰减函数中每个函数的计算分数的外观。

#### 正常衰减，关键词"高斯"

在上面的例子中选择"高斯"作为衰减函数时，乘数的轮廓和曲面图如下所示：

！CD0e18A6 e898 11e2 9b3cf0145078bd6f

！ec43c928 e898 11e2 8e0df3c4519dbd89

假设您的原始搜索结果与三家酒店匹配：

* "Backback Nap" * "Drink n Drive" * "BnB Bellevue"。

"Drink n Drive"离您定义的位置(近2公里)很远，而且不太便宜(约13欧元)，因此它的系数很低，为0.56倍。"BnBBellevue"和"Backback Nap"都非常接近定义的位置，但"BnB Bellevue"更便宜，因此它的乘数为0.86，而"BackpackNap"的值为0.66。

#### 指数衰减，关键字"exp"

在上面的例子中选择"exp"作为衰减函数时，乘数的轮廓和曲面图如下所示：

！082975c0 e899 11e2 86f7174c3a729d64

！0b606884 e899 11e2 907baefc77eefef6

#### 线性衰减，关键词"线性"

在上面的例子中选择"线性"作为衰减函数时，乘数的轮廓和曲面图如下所示：

！1775b0ca e899 11e2 9f4a776b406305c6

！19d8b1aa e899 11e2 91bc6b0553e8d722

### 衰减函数支持的字段

仅支持数值、日期和地理点字段。

### 如果缺少字段怎么办？

如果文档中缺少数值字段，则该函数将返回 1。

[« Disjunction max query](query-dsl-dis-max-query.md) [Full text queries
»](full-text-queries.md)
