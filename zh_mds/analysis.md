

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Removal of mapping types](removal-of-types.md) [Text analysis overview
»](analysis-overview.md)

# 文本分析

Text analysis是将非结构化文本(如电子邮件正文或产品描述)转换为针对搜索进行优化的结构化格式的过程。

### 何时配置文本分析

Elasticsearch在索引或搜索"text"字段时执行文本分析。

如果您的索引不包含"text"字段，则无需进一步设置;您可以跳过本节中的页面。

但是，如果您使用"text"字段或文本搜索未按预期返回结果，则配置文本分析通常会有所帮助。如果您使用 Elasticsearch 来执行以下操作，则还应该查看分析配置：

* 构建搜索引擎 
* 挖掘非结构化数据 
* 微调特定语言的搜索 
* 进行词典编纂或语言研究

### 在本节中

* _概述_ 
* _概念_ 
* _Configure文本analysis_ 
* _Built输入分析器reference_ 
* _Tokenizer reference_ 
* _Token筛选器reference_ 
* _Character筛选器reference_ 
* _规范化器_

[« Removal of mapping types](removal-of-types.md) [Text analysis overview
»](analysis-overview.md)
