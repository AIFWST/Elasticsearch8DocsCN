

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« SQL Limitations](sql-limitations.md) [Painless scripting language
»](modules-scripting-painless.md)

#Scripting

通过脚本编写，您可以在 Elasticsearch 中评估自定义表达式。例如，可以使用脚本将计算值作为字段返回，或评估查询的自定义分数。

默认脚本语言为无痛。额外的"lang"插件可用于运行用其他语言编写的脚本。您可以在脚本运行的任何位置指定脚本的语言。

## 可用的脚本语言

Painless 专为 Elasticsearch 而构建，可用于脚本 API 中的任何目的，并提供最大的灵活性。其他语言不太灵活，但可用于特定目的。

语言 |沙盒 |必需插件 |目的 ---|---|---|--- "无痛"

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

Built-in

|

专为 Elasticsearch "表达式"而打造

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

Built-in

|

快速自定义排名和排序"胡须"

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

Built-in

|

模板"java"

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

你写！

|

专家 API « SQL 限制 无痛脚本语言»