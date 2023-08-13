

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md) ›[Bucket aggregations](search-
aggregations-bucket.md)

[« Date histogram aggregation](search-aggregations-bucket-datehistogram-
aggregation.md) [Diversified sampler aggregation »](search-aggregations-
bucket-diversified-sampler-aggregation.md)

## 日期范围聚合

专用于日期值的范围聚合。此聚合与正常范围聚合之间的主要区别在于，"from"和"to"值可以在日期数学表达式中表示，并且还可以指定返回"from"和"to"响应字段的日期格式。请注意，此聚合包括"from"值，并排除每个范围的"to"值。

Example:

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          range: {
            date_range: {
              field: 'date',
              format: 'MM-yyyy',
              ranges: [
                {
                  to: 'now-10M/M'
                },
                {
                  from: 'now-10M/M'
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "range": {
          "date_range": {
            "field": "date",
            "format": "MM-yyyy",
            "ranges": [
              { "to": "now-10M/M" },  __{ "from": "now-10M/M" } __]
          }
        }
      }
    }

__

|

<现在减去 10 个月，四舍五入到月初。   ---|---    __

|

>= 现在减去 10 个月，四舍五入到月初。   在上面的示例中，我们创建了两个范围存储桶，第一个将"存储桶"日期在 10 个月前之前的所有文档，第二个将"存储桶"自 10 个月前以来的所有文档

Response:

    
    
    {
      ...
      "aggregations": {
        "range": {
          "buckets": [
            {
              "to": 1.4436576E12,
              "to_as_string": "10-2015",
              "doc_count": 7,
              "key": "*-10-2015"
            },
            {
              "from": 1.4436576E12,
              "from_as_string": "10-2015",
              "doc_count": 0,
              "key": "10-2015-*"
            }
          ]
        }
      }
    }

如果格式或日期值不完整，则日期范围聚合会将任何缺少的组件替换为默认值。请参阅缺少日期组件。

### 缺失值

"missing"参数定义应如何处理缺少值的文档。默认情况下，它们将被忽略，但也可以将它们视为具有值。这是通过添加一组字段名称：值映射来指定每个字段的默认值来完成的。

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          range: {
            date_range: {
              field: 'date',
              missing: '1976/11/30',
              ranges: [
                {
                  key: 'Older',
                  to: '2016/02/01'
                },
                {
                  key: 'Newer',
                  from: '2016/02/01',
                  to: 'now/d'
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
       "aggs": {
           "range": {
               "date_range": {
                   "field": "date",
                   "missing": "1976/11/30",
                   "ranges": [
                      {
                        "key": "Older",
                        "to": "2016/02/01"
                      }, __{
                        "key": "Newer",
                        "from": "2016/02/01",
                        "to" : "now/d"
                      }
                  ]
              }
          }
       }
    }

__

|

"日期"字段中没有值的文档将被添加到"旧"存储桶中，就像它们的日期值为"1976-11-30"一样。   ---|--- ### 日期格式/模式编辑

此信息是从日期时间格式化程序复制的

所有 ASCII 字母都保留为格式模式字母，定义如下：

符号 |含义 |简报 |示例 ---|---|---|--- G

|

era

|

text

|

广告;公元;一 u

|

year

|

year

|

2004;04 y

|

year-of-era

|

year

|

2004;04 D

|

day-of-year

|

number

|

189 米/升

|

month-of-year

|

number/text

|

7;07;七月;七月;J d

|

day-of-month

|

number

|

10 季度/季度

|

quarter-of-year

|

number/text

|

3;03;问3;第三季度 Y

|

week-based-year

|

year

|

1996;96 瓦

|

week-of-week-based-year

|

number

|

27 瓦

|

week-of-month

|

number

|

4 E

|

day-of-week

|

text

|

星期二;星期二;T e/c

|

本地化的星期几

|

number/text

|

2;22年星期二;星期二;T F

|

week-of-month

|

number

|

3 安培

|

am-pm-of-day

|

text

|

下午 h

|

上午一小时下午时钟 (1-12)

|

number

|

12 千米

|

下午一小时 (0-11)

|

number

|

0 千米

|

下午一小时时钟 (1-24)

|

number

|

0 小时

|

一天中的小时 (0-23)

|

number

|

0 米

|

minute-of-hour

|

number

|

30 秒

|

second-of-minute

|

number

|

55 秒

|

fraction-of-second

|

fraction

|

978 安培

|

milli-of-day

|

number

|

1234 北

|

nano-of-second

|

number

|

987654321 N

|

nano-of-day

|

number

|

1234000000 V

|

时区标识

|

zone-id

|

美洲/Los_Angeles;Z;-08：30 兹

|

时区名称

|

zone-name

|

太平洋标准时间;太平洋标准时间 O

|

局部区域偏移

|

offset-O

|

格林威治标准时间+8;格林威治标准时间+08：00;世界协调时-08：00;   X

|

区域偏移量 _Z_ 表示零

|

offset-X

|

Z;-08;-0830;-08:30;-083015;-08:30:15;   x

|

zone-offset

|

offset-x

|

+0000;-08;-0830;-08:30;-083015;-08:30:15;   Z

|

zone-offset

|

offset-Z

|

+0000;-0800;-08:00;   p

|

垫下一个

|

焊盘改性剂

|

1    '

|

文本转义

|

delimiter

|

'' 单引号

|

literal

|

'

|

[ 可选部分开始

|

]

|

可选节端

|

# 保留供将来使用

|

{

|

保留供将来使用

|

} 图案字母的数量决定了格式。

Text

     The text style is determined based on the number of pattern letters used. Less than 4 pattern letters will use the short form. Exactly 4 pattern letters will use the full form. Exactly 5 pattern letters will use the narrow form. Pattern letters `L`, `c`, and `q` specify the stand-alone form of the text styles. 
Number

     If the count of letters is one, then the value is output using the minimum number of digits and without padding. Otherwise, the count of digits is used as the width of the output field, with the value zero-padded as necessary. The following pattern letters have constraints on the count of letters. Only one letter of `c` and `F` can be specified. Up to two letters of `d`, `H`, `h`, `K`, `k`, `m`, and `s` can be specified. Up to three letters of `D` can be specified. 
Number/Text

     If the count of pattern letters is 3 or greater, use the Text rules above. Otherwise use the Number rules above. 
Fraction

     Outputs the nano-of-second field as a fraction-of-second. The nano-of-second value has nine digits, thus the count of pattern letters is from 1 to 9. If it is less than 9, then the nano-of-second value is truncated, with only the most significant digits being output. 
Year

     The count of letters determines the minimum field width below which padding is used. If the count of letters is two, then a reduced two digit form is used. For printing, this outputs the rightmost two digits. For parsing, this will parse using the base value of 2000, resulting in a year within the range 2000 to 2099 inclusive. If the count of letters is less than four (but not two), then the sign is only output for negative years as per `SignStyle.NORMAL`. Otherwise, the sign is output if the pad width is exceeded, as per `SignStyle.EXCEEDS_PAD`. 
ZoneId

     This outputs the time-zone ID, such as `Europe/Paris`. If the count of letters is two, then the time-zone ID is output. Any other count of letters throws `IllegalArgumentException`. 
Zone names

     This outputs the display name of the time-zone ID. If the count of letters is one, two or three, then the short name is output. If the count of letters is four, then the full name is output. Five or more letters throws `IllegalArgumentException`. 
Offset X and x

     This formats the offset based on the number of pattern letters. One letter outputs just the hour, such as `+01`, unless the minute is non-zero in which case the minute is also output, such as `+0130`. Two letters outputs the hour and minute, without a colon, such as `+0130`. Three letters outputs the hour and minute, with a colon, such as `+01:30`. Four letters outputs the hour and minute and optional second, without a colon, such as `+013015`. Five letters outputs the hour and minute and optional second, with a colon, such as `+01:30:15`. Six or more letters throws `IllegalArgumentException`. Pattern letter `X` (upper case) will output `Z` when the offset to be output would be zero, whereas pattern letter `x` (lower case) will output `+00`, `+0000`, or `+00:00`. 
Offset O

     This formats the localized offset based on the number of pattern letters. One letter outputs the short form of the localized offset, which is localized offset text, such as `GMT`, with hour without leading zero, optional 2-digit minute and second if non-zero, and colon, for example `GMT+8`. Four letters outputs the full form, which is localized offset text, such as `GMT, with 2-digit hour and minute field, optional second field if non-zero, and colon, for example `GMT+08:00`. Any other count of letters throws `IllegalArgumentException`. 
Offset Z

     This formats the offset based on the number of pattern letters. One, two or three letters outputs the hour and minute, without a colon, such as `+0130`. The output will be `+0000` when the offset is zero. Four letters outputs the full form of localized offset, equivalent to four letters of Offset-O. The output will be the corresponding localized offset text if the offset is zero. Five letters outputs the hour, minute, with optional second if non-zero, with colon. It outputs `Z` if the offset is zero. Six or more letters throws IllegalArgumentException. 
Optional section

     The optional section markers work exactly like calling `DateTimeFormatterBuilder.optionalStart()` and `DateTimeFormatterBuilder.optionalEnd()`. 
Pad modifier

     Modifies the pattern that immediately follows to be padded with spaces. The pad width is determined by the number of pattern letters. This is the same as calling `DateTimeFormatterBuilder.padNext(int)`. 

例如，"ppH"输出在左侧填充的小时，空格宽度为 2。

任何无法识别的字母都是错误。除"["，"]"，"{"，"}"，"#"和单引号以外的任何非字母字符都将直接输出。尽管如此，建议在要直接输出的所有字符两边使用单引号，以确保将来的更改不会破坏应用程序。

### 日期范围聚合中的时区

通过指定"time_zone"参数，可以将日期从另一个时区转换为 UTC。

时区可以指定为 ISO 8601 UTC 偏移量(例如 +01：00 或 -08：00)，也可以指定为 TZ 数据库中的时区 ID 之一。

"time_zone"参数也适用于日期数学表达式中的舍入。例如，要舍入到 CET时区的一天的开始，您可以执行以下操作：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          range: {
            date_range: {
              field: 'date',
              time_zone: 'CET',
              ranges: [
                {
                  to: '2016/02/01'
                },
                {
                  from: '2016/02/01',
                  to: 'now/d'
                },
                {
                  from: 'now/d'
                }
              ]
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
       "aggs": {
           "range": {
               "date_range": {
                   "field": "date",
                   "time_zone": "CET",
                   "ranges": [
                      { "to": "2016/02/01" }, __{ "from": "2016/02/01", "to" : "now/d" }, __{ "from": "now/d" }
                  ]
              }
          }
       }
    }

__

|

此日期将转换为"2016-02-01T00：00：00.000+01：00"。   ---|---    __

|

"now/d"将四舍五入到欧洲中部时间时区的一天的开始。   ### 键控响应编辑

将"keyed"标志设置为"true"会将一个唯一的字符串键与每个存储桶相关联，并将范围作为哈希而不是数组返回：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          range: {
            date_range: {
              field: 'date',
              format: 'MM-yyy',
              ranges: [
                {
                  to: 'now-10M/M'
                },
                {
                  from: 'now-10M/M'
                }
              ],
              keyed: true
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "range": {
          "date_range": {
            "field": "date",
            "format": "MM-yyy",
            "ranges": [
              { "to": "now-10M/M" },
              { "from": "now-10M/M" }
            ],
            "keyed": true
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "range": {
          "buckets": {
            "*-10-2015": {
              "to": 1.4436576E12,
              "to_as_string": "10-2015",
              "doc_count": 7
            },
            "10-2015-*": {
              "from": 1.4436576E12,
              "from_as_string": "10-2015",
              "doc_count": 0
            }
          }
        }
      }
    }

还可以为每个范围自定义键：

    
    
    response = client.search(
      index: 'sales',
      size: 0,
      body: {
        aggregations: {
          range: {
            date_range: {
              field: 'date',
              format: 'MM-yyy',
              ranges: [
                {
                  from: '01-2015',
                  to: '03-2015',
                  key: 'quarter_01'
                },
                {
                  from: '03-2015',
                  to: '06-2015',
                  key: 'quarter_02'
                }
              ],
              keyed: true
            }
          }
        }
      }
    )
    puts response
    
    
    POST /sales/_search?size=0
    {
      "aggs": {
        "range": {
          "date_range": {
            "field": "date",
            "format": "MM-yyy",
            "ranges": [
              { "from": "01-2015", "to": "03-2015", "key": "quarter_01" },
              { "from": "03-2015", "to": "06-2015", "key": "quarter_02" }
            ],
            "keyed": true
          }
        }
      }
    }

Response:

    
    
    {
      ...
      "aggregations": {
        "range": {
          "buckets": {
            "quarter_01": {
              "from": 1.4200704E12,
              "from_as_string": "01-2015",
              "to": 1.425168E12,
              "to_as_string": "03-2015",
              "doc_count": 5
            },
            "quarter_02": {
              "from": 1.425168E12,
              "from_as_string": "03-2015",
              "to": 1.4331168E12,
              "to_as_string": "06-2015",
              "doc_count": 2
            }
          }
        }
      }
    }

[« Date histogram aggregation](search-aggregations-bucket-datehistogram-
aggregation.md) [Diversified sampler aggregation »](search-aggregations-
bucket-diversified-sampler-aggregation.md)
