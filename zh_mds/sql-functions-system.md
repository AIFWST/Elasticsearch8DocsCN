

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md) ›[Functions and Operators](sql-functions.md)

[« Conditional Functions And Expressions](sql-functions-conditional.md)
[Reserved keywords »](sql-syntax-reserved.md)

## 系统函数

这些函数返回有关所查询系统的元数据类型的信息。

###'数据库'

**Synopsis:**

    
    
    DATABASE()

**输入** ： _无_

**输出**：字符串

**说明**：返回要查询的数据库的名称。在Elasticsearch SQL的情况下，这是Elasticsearch集群的名称。此函数应始终返回非空值。

    
    
    SELECT DATABASE();
    
       DATABASE
    ---------------
    elasticsearch

###'用户'

**Synopsis:**

    
    
    USER()

**输入** ： _无_

**输出**：字符串

**说明**：返回执行查询的经过身份验证的用户的用户名。如果禁用安全性，此函数可以返回"null"。

    
    
    SELECT USER();
    
         USER
    ---------------
    elastic

[« Conditional Functions And Expressions](sql-functions-conditional.md)
[Reserved keywords »](sql-syntax-reserved.md)
