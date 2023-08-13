

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« Geoshape query](query-dsl-geo-shape-query.md) [Shape query »](query-dsl-
shape-query.md)

## 形状查询

与"geo_shape"一样，Elasticsearch支持索引任意二维(非地理空间)几何图形的能力，从而可以绘制虚拟世界，体育场馆，主题公园和CAD图表。

Elasticsearch 支持两种类型的笛卡尔数据："点"字段支持 x/y 对，"形状"字段支持点、线、圆、多边形、多多边形等。

此组中的查询包括：

"形状"查询

    

查找具有以下内容的文档：

* 与指定形状相交、包含、位于指定形状内或不相交的"形状" * 与指定形状相交的"点"

[« Geoshape query](query-dsl-geo-shape-query.md) [Shape query »](query-dsl-
shape-query.md)
