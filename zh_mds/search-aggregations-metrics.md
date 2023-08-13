

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Aggregations](search-aggregations.md)

[« Subtleties of bucketing range fields](search-aggregations-bucket-range-
field-note.md) [Avg aggregation »](search-aggregations-metrics-avg-
aggregation.md)

## 指标聚合

此系列中的聚合基于从正在聚合的文档以一种或另一种方式提取的值来计算指标。这些值通常从文档的字段中提取(使用字段数据)，但也可以使用脚本生成。

数值指标聚合是一种特殊类型的指标聚合，用于输出数值。一些聚合输出单个数值指标(例如"avg")，称为"单值数值指标聚合"，其他聚合生成多个指标(例如"stats")，称为"多值数值计量聚合"。当单值和多值数值指标聚合充当某些存储桶聚合的直接子聚合时，单值和多值数值指标聚合之间的区别会发挥作用(某些存储桶聚合使您能够根据每个存储桶中的数值指标对返回的存储桶进行排序)。

[« Subtleties of bucketing range fields](search-aggregations-bucket-range-
field-note.md) [Avg aggregation »](search-aggregations-metrics-avg-
aggregation.md)
