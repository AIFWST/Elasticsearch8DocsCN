

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Ingest
pipelines](ingest.md)

[« Example: Parse logs in the Common Log Format](common-log-format-
example.md) [Set up an enrich processor »](enrich-setup.md)

## 丰富您的数据

您可以使用扩充处理器在引入期间将现有索引中的数据添加到传入文档。

例如，可以使用扩充处理器执行以下操作：

* 根据已知的 IP 地址识别 Web 服务或供应商 * 根据产品 ID 向零售订单添加产品信息 * 根据电子邮件地址补充联系信息 * 根据用户坐标添加邮政编码

### 扩充处理器的工作原理

大多数处理器都是自包含的，只更改传入文档中的_现有_数据。

！摄取进程

扩充处理器将_new_数据添加到传入的文档，并需要一些特殊组件：

！丰富过程

扩充策略

    

一组配置选项，用于将正确的扩充数据添加到正确的传入文档中。

扩充策略包含：

* 将扩充数据存储为文档的一个或多个_source indices_的列表 * 确定处理器如何将扩充数据与传入文档匹配的_policy type_ * 源索引中用于匹配传入文档的_match field_ * 包含要添加到传入文档的源索引中的扩充数据的_Enrich fields_

在将其与扩充处理器一起使用之前，必须执行扩充策略。执行时，扩充策略使用策略源索引中的扩充数据来创建名为 _enrich index_ 的简化系统索引。处理器使用此索引来匹配和丰富传入的文档。

源索引

     An index which stores enrich data you'd like to add to incoming documents. You can create and manage these indices just like a regular Elasticsearch index. You can use multiple source indices in an enrich policy. You also can use the same source index in multiple enrich policies. 

丰富指数

    

与特定扩充策略相关联的特殊系统索引。

将传入文档直接与源索引中的文档进行匹配可能会很慢且需要大量资源。为了加快速度，扩充处理器使用扩充索引。

扩充索引包含来自源索引的扩充数据，但具有一些特殊属性来帮助简化它们：

* 它们是系统索引，这意味着它们由 Elasticsearch 在内部管理，并且仅用于扩充处理器。  * 它们总是以".enrich-*"开头。  * 它们是只读的，这意味着您无法直接更改它们。  *它们被强制合并以快速检索。

[« Example: Parse logs in the Common Log Format](common-log-format-
example.md) [Set up an enrich processor »](enrich-setup.md)
