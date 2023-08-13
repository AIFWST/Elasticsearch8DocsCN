

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Role mapping resources](role-mapping-resources.md) [Migrating to 8.9
»](migrating-8.9.md)

# 迁移指南

本节讨论将应用程序迁移到 8.9.0 时需要注意的更改。有关此版本中新增功能的详细信息，请参阅 8.9_ 中的_What新增功能和发行说明。

随着 Elasticsearch 引入新功能并改进现有功能，这些更改有时会使旧的设置、API 和参数过时。我们通常会弃用过时的功能作为版本的一部分。如果可能，在删除之前，我们支持多个后续版本的弃用功能。这使应用程序能够在您准备从已弃用的功能迁移时继续原封不动地工作。

为了充分利用 Elasticsearch 并促进未来的升级，我们强烈建议尽快放弃使用已弃用的功能。

为了让您深入了解正在使用哪些已弃用的功能，Elasticsearch：

* 每当您提交使用已弃用功能的请求时，都会返回"警告"HTTP 标头。  * 使用已弃用的功能时记录弃用警告。  * 提供弃用信息 API，用于扫描群集的配置和映射以查找已弃用的功能。

有关 8.9 的更多信息，请参阅 8.9_ 中的_What新功能和发行说明。有关如何升级集群的信息，请参阅升级 Elasticsearch。

* 迁移到 8.9 * 迁移到 8.8 * 迁移到 8.7 * 迁移到 8.6 * 迁移到 8.5 * 迁移到 8.4 * 迁移到 8.3 * 迁移到 8.2 * 迁移到 8.1 * 迁移到 8.0

[« Role mapping resources](role-mapping-resources.md) [Migrating to 8.9
»](migrating-8.9.md)
