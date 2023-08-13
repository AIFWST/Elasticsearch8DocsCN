

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[SQL](xpack-
sql.md)

[« SQL](xpack-sql.md) [Getting Started with SQL »](sql-getting-started.md)

##Overview

Elasticsearch SQL旨在为Elasticsearch提供一个强大而轻量级的SQL接口。

###Introduction

Elasticsearch SQL是一个X-Pack组件，它允许针对Elasticsearch实时执行类似SQL的查询。无论是使用 REST 接口、命令行还是 JDBC，任何客户端都可以使用 SQL 在 Elasticsearch 中搜索和聚合data_natively_。人们可以将Elasticsearch SQL视为a_translator_，它既能理解SQL又能理解Elasticsearch，并通过利用Elasticsearch功能轻松实时读取和处理数据。

### 为什么选择 Elasticsearch SQL？

原生集成

     Elasticsearch SQL is built from the ground up for Elasticsearch. Each and every query is efficiently executed against the relevant nodes according to the underlying storage. 
No external parts

     No need for additional hardware, processes, runtimes or libraries to query Elasticsearch; Elasticsearch SQL eliminates extra moving parts by running _inside_ the Elasticsearch cluster. 
Lightweight and efficient

     Elasticsearch SQL does not abstract Elasticsearch and its search capabilities - on the contrary, it embraces and exposes SQL to allow proper full-text search, in real-time, in the same declarative, succinct fashion. 

[« SQL](xpack-sql.md) [Getting Started with SQL »](sql-getting-started.md)
