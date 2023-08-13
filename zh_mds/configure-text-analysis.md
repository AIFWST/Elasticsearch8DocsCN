

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md)

[« Token graphs](token-graphs.md) [Test an analyzer »](test-analyzer.md)

## 配置文本分析

默认情况下，Elasticsearch 使用"标准"分析器进行所有文本分析。"标准"分析器为您提供对大多数自然语言和用例的开箱即用支持。如果选择按原样使用"标准"分析器，则无需进一步配置。

如果标准分析器不符合您的需求，请查看并测试Elasticsearch的其他内置分析器。内置分析器不需要配置，但需要一些可用于调整其行为的支持选项。例如，您可以使用要删除的自定义停用词列表配置"标准"分析器。

如果没有内置分析器满足您的需求，则可以测试并创建自定义分析器。定制分析仪涉及选择和组合不同的分析仪组件，使您能够更好地控制过程。

* 测试分析器 * 配置内置分析器 * 创建自定义分析器 * 指定分析器

[« Token graphs](token-graphs.md) [Test an analyzer »](test-analyzer.md)
