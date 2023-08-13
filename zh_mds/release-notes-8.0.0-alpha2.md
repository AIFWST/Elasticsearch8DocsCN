

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.0.0-beta1](release-notes-8.0.0-beta1.md)
[Elasticsearch version 8.0.0-alpha1 »](release-notes-8.0.0-alpha1.md)

## 弹性搜索版本8.0.0-alpha2

另请参阅 8.0 中的重大更改。

### 重大变更

ILM+SLM

    

* 使 ILM"冻结"操作成为无操作 #77158(问题：#70192)

Infra/Core

    

* 使用自定义数据路径创建索引失败 #76792(问题：#73168) * 系统索引被视为受限索引 #74212(问题：#69298)

License

    

* 为所有许可证设置 'xpack.security.enabled' 为 true #72300

Packaging

    

* 删除 no-jdk 发行版 #76896(问题：#65109)

Security

    

* 删除"kibana_dashboard_only_user"保留角色 #76507

###Enhancements

Authentication

    

* 启动时自动生成并打印弹性密码 #77291 * 使用服务帐户注册 Kibana API #76370 * 添加"重置 kibana-system-user"工具 #77322

ILM+SLM

    

* 允许在分配 ILM 操作 #76794 中设置每个节点的总分片数(问题：#76775)

Infra/Core

    

* 保留对特殊情况的 stdout 引用 #77460

Ingest

    

* 添加对"_meta"字段的支持以引入管道 #76381

机器学习

    

* 添加新的 PUT 训练模型词汇端点 #77387 * 创建新的 PUT 模型定义部件 API #76987

Network

    

* 默认启用 LZ4 传输压缩 #76326(问题：#73497)

Search

    

* REST API 兼容性] 嵌套路径和过滤器排序选项 [#76022(问题：#42809、#51816) * REST API 兼容性] "CommonTermsQuery"和"cutoff_frequency"参数 [#75896(问题：#42654、#51816) * REST API 兼容性] 允许"_msearch"的第一个空行 [#75886(问题：#41011、#51816)

Security

    

* 为注册 API 添加基本的"RestHandler"类 #76564(问题：#76097) * 为弹性用户 #76276 生成和存储密码哈希(问题：#75310) * 设置弹性密码并生成注册令牌 #75816(问题：#75310) * 添加"弹性搜索-注册-节点"工具 #77292 * 在 FIPS 模式下默认哈希器为"PBKDF2_STRETCH" #76274

### 错误修复

ILM+SLM

    

* 确保每个节点的总分片数太低时"收缩操作"不会挂起 #76732(问题：#44070)

Security

    

* 允许访问保留系统角色的受限系统索引 #76845

[« Elasticsearch version 8.0.0-beta1](release-notes-8.0.0-beta1.md)
[Elasticsearch version 8.0.0-alpha1 »](release-notes-8.0.0-alpha1.md)
