

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Query
DSL](query-dsl.md)

[« Simple query string query](query-dsl-simple-query-string-query.md) [Geo-
bounding box query »](query-dsl-geo-bounding-box-query.md)

## 地理查询

Elasticsearch 支持两种类型的地理数据："geo_point"字段支持纬度/纬度对，以及"geo_shape"字段，支持点、线、圆、多边形、多多边形等。

此组中的查询包括：

"geo_bounding_box"查询

     Finds documents with geoshapes or geopoints which intersect the specified rectangle. 
[`geo_distance`](query-dsl-geo-distance-query.html "Geo-distance query") query

     Finds documents with geoshapes or geopoints within the specified distance of a central point. 
[`geo_grid`](query-dsl-geo-grid-query.html "Geo-grid query") query

    

查找具有以下内容的文档：

* 与指定地理哈希相交的地理形状或地理点 * 与指定地图图块相交的地理形状或地理点 * 与指定 H3 箱相交的地理点

"geo_polygon"查询

     Find documents with geoshapes or geopoints which intersect the specified polygon. 
[`geo_shape`](query-dsl-geo-shape-query.html "Geoshape query") query

     Finds documents with geoshapes or geopoints which are related to the specified geoshape. Possible spatial relationships to specify are: intersects, contained, within and disjoint. 

[« Simple query string query](query-dsl-simple-query-string-query.md) [Geo-
bounding box query »](query-dsl-geo-bounding-box-query.md)
