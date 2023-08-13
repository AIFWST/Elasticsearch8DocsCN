

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« Type Conversion Functions](sql-functions-type-conversion.md) [Conditional
Functions And Expressions »](sql-functions-conditional.md)

## 地理函数

此功能处于测试阶段，可能会发生变化。设计和代码不如官方 GA 功能成熟，并且按原样提供，不提供任何保证。测试版功能不受官方 GA 功能的支持 SLA 的约束。

地理函数适用于存储在"geo_point"、"geo_shape"和"形状"字段中的几何图形，或由其他地理函数返回的几何图形。

###Limitations

"geo_point"、"geo_shape"和"形状"和类型在 SQL 中表示为几何图形，可以互换使用，但以下情况除外：

* "geo_shape"和"shape"字段没有文档值，因此这些字段不能用于过滤、分组或排序。  * 默认情况下，"geo_points"字段已编制索引并具有文档值，但仅存储和索引纬度和经度，与原始值相比精度有所下降(纬度为 4.190951585769653E-8，经度为 8.381903171539307E-8)。高度分量被接受，但不存储在文档值中，也不编制索引。因此，在过滤、分组或排序中调用"ST_Z"函数将返回"null"。

### 几何转换

####'ST_AsWKT'

**Synopsis:**

    
    
    ST_AsWKT(
        geometry __)

**输入**：

__

|

几何学。如果为"null"，则函数返回"null"。   ---|--- 输出**：字符串

**说明**：返回"几何图形"的 WKT 表示形式。

    
    
    SELECT city, ST_AsWKT(location) location FROM "geo" WHERE city = 'Amsterdam';
    
         city:s    |     location:s
    Amsterdam      |POINT (4.850312 52.347557)

####'ST_WKTToSQL'

**Synopsis:**

    
    
    ST_WKTToSQL(
        string __)

**输入**：

__

|

几何的字符串 WKT 表示。如果为"null"，则函数返回"null"。   ---|--- **输出**：几何

**说明**：返回 WKT 表示中的几何图形。

    
    
    SELECT CAST(ST_WKTToSQL('POINT (10 20)') AS STRING) location;
    
       location:s
    POINT (10.0 20.0)

### 几何属性

####'ST_GeometryType'

**Synopsis:**

    
    
    ST_GeometryType(
        geometry __)

**输入**：

__

|

几何学。如果为"null"，则函数返回"null"。   ---|--- 输出**：字符串

**描述**：返回"几何"的类型，例如点，多点，线串，多线串，多边形，多多边形，几何集合，包络或圆。

    
    
    SELECT ST_GeometryType(ST_WKTToSQL('POINT (10 20)')) type;
    
          type:s
    POINT

####'ST_X'

**Synopsis:**

    
    
    ST_X(
        geometry __)

**输入**：

__

|

几何学。如果为"null"，则函数返回"null"。   ---|--- **输出**：双倍

**说明** ：返回几何图形中第一个点的经度。

    
    
    SELECT ST_X(ST_WKTToSQL('POINT (10 20)')) x;
    
          x:d
    10.0

####'ST_Y'

**Synopsis:**

    
    
    ST_Y(
        geometry __)

**输入**：

__

|

几何学。如果为"null"，则函数返回"null"。   ---|--- **输出**：双倍

**说明**：返回几何图形中第一个点的纬度。

    
    
    SELECT ST_Y(ST_WKTToSQL('POINT (10 20)')) y;
    
          y:d
    20.0

####'ST_Z'

**Synopsis:**

    
    
    ST_Z(
        geometry __)

**输入**：

__

|

几何学。如果为"null"，则函数返回"null"。   ---|--- **输出**：双倍

**说明**：返回几何图形中第一个点的高度。

    
    
    SELECT ST_Z(ST_WKTToSQL('POINT (10 20 30)')) z;
    
          z:d
    30.0

####'ST_Distance'

**Synopsis:**

    
    
    ST_Distance(
        geometry, __geometry __)

**输入**：

__

|

源几何图形。如果为"null"，则函数返回"null"。   ---|---    __

|

目标几何图形。如果为"null"，则函数返回"null"。   **输出**：双倍

**说明** ：返回几何图形之间的距离(以米为单位)。两个几何形状都必须是点。

    
    
    SELECT ST_Distance(ST_WKTToSQL('POINT (10 20)'), ST_WKTToSQL('POINT (20 30)')) distance;
    
       distance:d
    1499101.2889383635

[« Type Conversion Functions](sql-functions-type-conversion.md) [Conditional
Functions And Expressions »](sql-functions-conditional.md)
