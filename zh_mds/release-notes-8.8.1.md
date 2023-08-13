

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.8.2](release-notes-8.8.2.md) [Elasticsearch
version 8.8.0 »](release-notes-8.8.0.md)

## 弹性搜索版本8.8.1

另请参阅 8.8 中的重大更改。

### 错误修正

数据流

    

* 如果还有其他模板与相关数据流匹配，则允许删除正在使用的模板 #96286

Geo

    

* "geo_bounding_box"查询 #96317 中类型参数的 API 其余兼容性

Rollup

    

* 请勿复制"index.default_pipeline"和"index.final_pipeline"#96494(问题：#96478)

TSDB

    

* 在需要时在协调器重写期间将开始和结束时间扩展到纳秒 #96035(问题：#96030) * 修复了索引刚刚在 tsdb 索引中删除的文档时的 NPE 问题 #96461

Transform

    

* 改进了转换"_update"冲突的错误消息 #96432 * 报告并发更新的版本冲突 #96293(问题：#96311)

###Enhancements

查询语言

    

* 减少相同布尔查询的嵌套 #96265(问题：#96236)

[« Elasticsearch version 8.8.2](release-notes-8.8.2.md) [Elasticsearch
version 8.8.0 »](release-notes-8.8.0.md)
