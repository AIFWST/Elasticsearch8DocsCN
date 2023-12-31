

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Release
notes](es-release-notes.md)

[« Elasticsearch version 8.0.1](release-notes-8.0.1.md) [Elasticsearch
version 8.0.0-rc2 »](release-notes-8.0.0-rc2.md)

## 弹性搜索版本8.0.0

以下列表是 8.0.0 与 7.17.0 相比的变化，并合并了 8.0.0-alpha1、-alpha2、-beta1、-rc1 和 -rc2 版本的发行说明。

另请参阅 8.0 中的重大更改。

### 已知问题

* 如果您在 aarch64 平台(如 Linux ARM 或 macOS M1)上的存档中安装了 Elasticsearch，则在首次启动节点时不会自动生成"弹性"用户密码和 Kibana 注册令牌。

节点启动后，使用"bin/elasticsearch-reset-password"工具生成"弹性"密码：

    
        bin/elasticsearch-reset-password -u elastic

然后，使用 'bin/elasticsearch-create-enrollment-token' 工具为 Kibana 创建一个注册令牌：

    
        bin/elasticsearch-create-enrollment-token -s kibana

* 当数组中的最后一个元素被过滤掉(例如使用"_source_includes")时解析请求失败。这是由于杰克逊解析器中的一个错误。在 Elasticsearch 8.6.1 中修复 (#91456)

### 重大变更

Aggregations

    

* 百分位数聚合：不允许指定相同的百分位数值两次 #52257(问题：#51871) * 删除邻接矩阵设置 #46327(问题：#46257、#46324) * 删除"移动平均值"管道聚合 #39328 * 删除已弃用的"_time"和"_term"排序顺序 #39450 * 删除已弃用的日期历史间隔 #75000

Allocation

    

* 要求单个数据节点遵守磁盘水印 #73737(问题：#55805、#73733) * 删除"include_relocations"设置#47717(问题：#46079、#47443)

Analysis

    

* 清理分析中的版本化弃用 #41560(问题：#41164)* 删除预配置的"delimited_payload_filter"#43686(问题：#41560、#43684)

Authentication

    

* 始终添加文件和本机领域，除非明确禁用 #69096(问题：#50892) * 默认情况下不要在策略中设置 NameID 格式 #44090(问题：#40353) * 强制设置 Realm 配置 #51195 的订单设置(问题：#37614)

CCR

    

* 避免在 CCR #72815 中自动跟随前导系统索引(问题：#67686)

集群协调

    

* 删除加入超时 #60873(问题：#60872) * 删除投票配置排除项的节点过滤器 #55673(问题：#47990、#50836) * 删除对延迟状态恢复的支持 等待主服务器 #53845(问题：#51806)

Distributed

    

* 删除同步刷新 #50882(问题：#50776、#50835) * 删除"cluster.remote.connect"设置 #54175(问题：#53924)

Engine

    

* 强制合并应拒绝设置了"only_expunge_deletes"和"max_num_segments"的请求 #44761(问题：#43102) * 删除按类型索引统计信息 #47203(问题：#41059) * 删除 translog 保留设置 #51697(问题：#50775)

功能/CAT API

    

* 删除"_cat/索引"#64868 的已弃用的"local"参数(问题：#62198) * 删除"_cat/分片"#64867 的已弃用的"local"参数(问题：#62197)

Features/Features

    

* 删除已弃用的"._tier"分配筛选设置 #73074(问题：#72835)

Features/ILM+SLM

    

* 在"poll_interval"上添加下限 #39593(问题：#39163) * 使 ILM"冻结"操作成为无操作 #77158(问题：#70192) * 始终强制实施默认层首选项 #79751(问题：#76147) * 验证 ILM 策略在创建/更新时是否存在快照存储库 #78468(问题：#72957、#77657) * 默认"cluster.routing.allocation.enforce_default_tier_preference"为"true" #79275(问题：#76147、#79210)

功能/索引 API

    

* 将"prefer_v2_templates"参数更改为默认值 true #55489(问题：#53101、#55411) * 删除已弃用的"_upgrade"API #64732(问题：#21337) * 删除获取字段映射请求 #55100 的本地参数(问题：#55099) * 从 REST 层中删除"include_type_name"参数 #48632(问题：#41059) * 删除索引模板 #49460 中的"模板"字段(问题：#21009) * 删除冻结索引的端点 #78918(问题： #70192, #77273)

Features/Watcher

    

* 将观察程序历史记录移动到数据流 #64252

Geo

    

* 禁止使用已弃用的参数创建"geo_shape"映射 #70850(问题：#32039) * 删除边界框查询"类型"参数 #74536

基础设施/断路器

    

* 修复了与内部变量 #40878 同步机上断路器的问题

Infra/Core

    

* 按可用处理器限制处理器 #44894(问题：#44889) * 从数据路径中删除"nodes/0"文件夹前缀 #42489 * 删除"bootstrap.system_call_filter"设置 #72848 * 删除"fixed_auto_queue_size"线程池类型 #52280 * 删除"node.max_local_storage_nodes" #42428(问题：#42426) * 删除名为日期/时间格式的驼峰大小写 #60044 * 删除旧角色设置 #71163(问题：#54998、#66409、#71143) * 删除"处理器"设置 #45905(问题： #45855) * 删除"/_cat/节点"的"local"参数 #50594(问题：#50088、#50499) * 删除侦听器线程池 #53314(问题：#53049) * 删除节点本地存储设置 #54381(问题：#54374) * 删除"pidfile"设置 #45940(问题：#45938) * 删除"week_year"日期格式 #63384(问题：#60707) * 系统索引被视为受限索引 #74212(问题：#69298) * 删除 Joda 依赖项 #79007 * 从日期格式化程序中删除 Joda 支持 #78990 * 所有系统索引是隐藏索引 #79512

Infra/Logging

    

* 删除慢日志级别 #57591(问题：#56171)

Infra/Plugins

    

* 删除已弃用的基本许可证功能启用设置 #56211(问题：#54745)

基础设施/休息接口

    

* 删除内容类型所需的设置 #61043 * 删除包含"_xpack"的已弃用终结点 #48170(问题：#35958) * 删除热线程 API #55109 的已弃用终结点(问题：#52640) * 允许解析版本 #61427 的内容类型和接受标头

Infra/Resiliency

    

* 包含古代封闭索引 #44264 的失败节点(问题：#21830、#41731、#44230)

Infra/Scripting

    

* 从对象 #59507 合并脚本解析(问题：#59391) * 将"script_cache"移动到_nodes/统计信息 #59265(问题：#50152、#59262) * 删除常规缓存设置 #59262(问题：#50152)

Infra/Settings

    

* 将默认值"action.destructive_requires_name"更改为"true" #66908(问题：#61074) * 禁止没有命名空间的设置 #45947(问题：#45905、#45940)

Ingest

    

* 从发行版中删除默认的 maxmind GeoIP 数据库 #78362(问题：#68920)

License

    

* 为所有许可证设置 'xpack.security.enabled' 为 true #72300 * 强制许可证过期 #79671

机器学习

    

* 删除已弃用的"_xpack"端点 #59870(问题：#35958、#48170) * 删除更新数据馈送的"job_id"的功能 #44752(问题：#44616) * 从 API 中删除"allow_no_datafeeds"和"allow_no_jobs"参数 #80048(问题：#60732)

Mapping

    

* 删除"boost"映射参数 #62639(问题：#62623) * 删除对链式多字段的支持 #42333(问题：#41267、#41926) * 删除对"unmapped_type"中的字符串的支持 #45675 * 从映射 API 中删除类型化的 URL #41676

Network

    

* 删除客户端功能跟踪 #44929(问题：#31020、#42538、#44667) * 删除允许不兼容构建的逃生舱口 #65753(问题：#65249、#65601)

Packaging

    

* 删除 SysV 初始化支持 #51716(问题：#51480) * 删除对"JAVA_HOME"的支持 #69149(问题：#55820) * 删除 no-jdk 发行版 #76896(问题：#65109) * 需要 Java 17 才能运行 Elasticsearch #79873

Recovery

    

* 删除悬空索引自动导入功能 #59698(问题：#48366)

Reindex

    

* 从远程编码重新索引 #41007(问题：#40303) * 重新索引删除外部级别大小 #43373(问题：#24344、#41894)

Rollup

    

* 如果作业已启动，"RollupStart"终结点应返回"正常"#41502(问题：#35928、#39845)

Search

    

* 将分片分配感知与搜索和获取请求分离 #45735(问题：#43453) * 修复了对数字输入的日期字段的范围查询 #63692(问题：#63680) * 使模糊更早地拒绝非法值 #33511 * 使远程群集分辨率更严格 #40419(问题：#37863) * 将 msearch 请求正文中的第一行空解析为操作元数据 #41011(问题：#39841) * 删除"CommonTermsQuery"和"cutoff_frequency"参数 #42654(问题： #37096) * 删除"类型"查询 #47207(问题：#41059) * 删除文档值字段的"use_field_mapping"格式选项 #55622 * 删除已弃用的"SimpleQueryStringBuilder"参数 #57200 * 删除已弃用的"search.remote"设置 #42381(问题：#33413、#38556) * 删除已弃用的排序选项："nested_path"和"nested_filter" #42809(问题：#27098) * 删除已弃用的向量函数 #48725(问题：#48604) * 删除搜索中对"_type"的支持 #68564(问题： #41059， #68311) * 删除对稀疏向量 #48781 的支持(问题： #48368) * 删除"indices_boost"的对象格式 #55078 * 从"术语向量"API 中删除类型 #42198(问题：#41059) * 从搜索和相关 API 中删除类型化终结点 #41640 * 设置存储的异步响应的最大允许大小 #74455 (问题： #67594) * 'index.query.bool.max_clause_count' 现在限制所有查询子句 #75297

Security

    

* 删除过时的安全设置 #40496 * 删除在生成证书时动态创建 CA 的支持 #65590(问题：#61884) * 从"无效ApiKey"API 中删除"id"字段 #66671(问题：#66317) * 删除迁移工具 #42174 * 压缩审核日志 #64472(问题：#63843) * 删除不安全的设置 #46147(问题：#45947) * 删除"kibana_dashboard_only_user"保留角色 #76507

Snapshot/Restore

    

* Blob 存储压缩默认为"true" #40033 * 获取对多个存储库的快照支持 #42090(问题：#41210) * 删除存储库统计信息 API #62309(问题：#62297) * 删除冻结缓存设置宽大处理 #71013(问题：#70341) * 调整快照索引解析行为以使其更直观 #79670(问题：#78320)

TLS

    

* 拒绝配置错误/不明确的 SSL 服务器配置 #45892 * 删除对可配置 PKCS#11 密钥库的支持 #75404 * 删除客户端传输配置文件筛选器 #43236

### 中断 JavaChanges

Authentication

    

* 强制安装 x-pack REST 处理程序 #71061(问题：#70523)

CCR

    

* 删除"Ccr客户端" #42816

CRUD

    

* 从"批量请求"中删除类型 #46983 (问题： #41059) * 删除 'Client.prepareIndex(index， type， id)' 方法 #48443

Client

    

* 从 x-pack #42471 中删除"安全客户端"

Features/ILM+SLM

    

* 删除"ILMClient" #42817

Features/Monitoring

    

* 从 x-pack #42770 中删除"监控客户端"

Features/Watcher

    

* 从 x-pack #42815 中删除"观察者客户端"

Infra/Core

    

* 从 x-pack 中删除"XPackClient" #42729 * 删除传输客户端 #42538 * 从 x-pack 中删除传输客户端 #42202

基础设施/休息接口

    

* 将 HTTP 标头严格复制到"线程上下文"#45945

机器学习

    

* 删除"机器学习客户端"#43108

Mapping

    

* 从"GetMappings"API 中删除类型过滤器 #47364(问题：#41059) * 从"PutMappingRequest.buildFromSimplifiedDef()"中删除"类型"参数 #50844(问题：#41059) * 从"元数据字段映射器.类型解析器#getDefault()"中删除未使用的参数 #51219 * 从"CIR.mapping(type，object...)"中删除"类型"参数' #50739(问题：#41059)

Search

    

* 从"搜索请求"和"查询分片上下文"中删除类型 #42112

Snapshot/Restore

    

* 删除已弃用的存储库方法 #42359(问题：#42213)

###Deprecations

Authentication

    

* 弃用设置密码工具 #76902

CRUD

    

* 删除"indices_segments"_verbose_ 参数 #78451(问题：#75955)

Engine

    

* 弃用设置"max_merge_at_once_explicit"#80574

机器学习

    

* 弃用"estimated_heap_memory_usage_bytes"并替换为"model_size_bytes" #80554

Monitoring

    

* 为已弃用的监视设置添加弃用信息 API 条目 #78799 * 在插件初始化时自动安装监视模板 #78350 * 删除监视引入管道 #77459(问题：#50770)

Search

    

* 根据节点特征配置 'IndexSearcher.maxClauseCount()' #81525 (问题： #46433)

Transform

    

* 改进转换弃用消息 #81847(问题：#81521、#81523)

### 新功能

Security

    

* 为新群集的新节点自动配置 TLS #77231(问题：#75144、#75704)

Snapshot/Restore

    

* 支持 Kubernetes 服务账户的 IAM 角色 #81255(问题：#52625)

Watcher

    

* 对观察程序历史记录模板名称使用"startsWith"而不是完全匹配 #82396

###Enhancements

Analysis

    

* 将"reload_analyzers"端点移动到 x-pack #43559

Authentication

    

* 重置弹性密码 CLI 工具 #74892(问题：#70113、#74890) * 启动时自动生成并打印弹性密码 #77291 * 注册 Kibana API 使用服务帐户 #76370 * 添加"重置 kibana-system-user"工具 #77322 * 新的 CLI 工具，用于重置内置用户的密码 #79709 * 自动配置"弹性"用户密码 #78306

Authorization

    

* 授予"kibana_system"保留角色对".internal.preview.alerts*"索引 #80889 的"所有"权限的访问权限(问题：#76624、#80746、#116374) * 授予"kibana_system"保留角色对 .preview.alerts* 索引的"所有"权限的访问权限 #80746 * 授予编辑者和查看者角色对警报即数据索引的访问权限 #81285

集群协调

    

* 防止从 8.x 降级到 7.x #78586(问题：#42489、#52414) * 防止从 8.x 降级到 7.x #78638(问题：#42489、#52414) * 减少"任务批处理器"的锁重 #82227(问题：#77466)

数据流

    

* 数据流支持使用自定义路由和分区大小进行读写 #74394(问题：#74390)

EQL

    

* 添加从流尾返回结果的选项 #64869 (问题： #58646) * 引入不区分大小写的变体 'in~' #68176 (问题： #68172) * 优化冗余的 'toString' #71070 (问题： #70681)

Engine

    

* 始终在"内部引擎"中使用软删除 #50415 * 删除事务日志保留策略 #51417(问题：#50775)

功能/CAT API

    

* 删除"大小"并将"时间"参数添加到"_cat/线程池"#55736(问题：#54478)

Features/ILM+SLM

    

* 允许在分配 ILM 操作 #76794 中设置每个节点的总分片数(问题：#76775) * 注入迁移操作，而不考虑分配操作 #79090(问题：#76147) * 将未更改的 ILM 策略更新转换为 noop #82240(问题：#82065) * 避免不必要的"生命周期执行状态"重新计算 #81558(问题：#77466、#79692)

功能/索引 API

    

* 批量滚动更新群集状态更新 #79945(问题：#77466、#79782)* 在元数据类 #80348 中重用"映射元数据"实例(问题：#69772、#77466)

Features/Stats

    

* 添加批量统计信息跟踪每个分片的批量 #52208(问题：#47345、#50536)

Features/Watcher

    

* 从监控中删除观察程序历史记录清理 #67154

Infra/Core

    

* 删除别名存在操作 #43430 * 删除索引存在操作 #43164 * 删除类型存在操作 #43344 * 保留对标准输出的引用以应对特殊情况 #77460 * 检查标准输出是否是真正的控制台 #79882 * 共享整数、长整型、浮点数、双精度和字节页 #75053 * 恢复"弃用日期字段上的分辨率损失 (#78921)" #79914(问题：#78921) * 在弃用信息 API #80290 中添加两个缺少的条目(问题： #80233) * 阻止升级到 8.0，而无需先升级到最后一个 7.x 版本 #82321(问题：#81865)

Infra/Logging

    

* 使 Elasticsearch JSON 日志符合 ECS 标准 #47105(问题：#46119)

基础设施/休息接口

    

* 允许为将来的兼容版本进行字段声明 #69774 (问题： #51816) * 在 REST API 规范中引入稳定性描述 #38413 * 解析：验证字段是否未注册两次 #70243 * 支持版本化媒体类型 #65500 的响应内容类型(问题：#51816) * REST API 兼容性] 索引和获取 API 的类型化终结点 [#69131(问题：#54160) * REST API 兼容性] 用于放置和获取映射以及获取字段映射的类型化终结点 [#71721(问题：#51816、#54160) * REST API 兼容性] 允许"copy_settings"标志进行调整大小操作 [#75184(问题：#38514、#51816)* REST API 兼容性] 允许在地理形状查询中键入 [#74553(问题：#51816、#54160)* REST API 兼容性] 始终返回"adjust_pure_negative"值 [#75182(问题：#49543、#51816)* REST API 兼容性] 清理 X-Pack/插件 REST 兼容测试 [#74701(问题： #51816) * REST API 兼容性] 对于模板中的空映射，不要返回"_doc" [#75448 (问题： #51816， #54160， #70966， #74544) * REST API 兼容性] "索引.升级"API 的虚拟 REST 操作 [#75136 (问题： #51816) * REST API 兼容性] REST 术语矢量类型响应 [#73117 * REST API 兼容性] 重命名"批量项目响应.失败"类型字段 [#74937(问题：#51816)* REST API 兼容性] 模拟请求中使用的文档的类型元数据 [#74222(问题： #51816， #54160) * REST API 兼容性] 键入的"术语查找" [#74544 (问题： #46943， #51816， #54160) * REST API 兼容性] 类型和 x 包图探索 API [#74185(问题： #46935、#51816、#54160) * REST API 兼容性] 批量 API 的类型化终结点 [#73571(问题： #51816) * REST API 兼容性] 多获取 API 的类型化终结点 [#73878(问题： #51816) * REST API 兼容性] "RestUpdateAction"和"RestDeleteAction"的类型化终结点 [#73115(问题： #51816， #54160) * REST API 兼容性] "get_source"API 的类型化终结点 [#73957 (问题： #46587、#46931、#51816) * REST API 兼容性] 解释 API 的类型化终结点 [#73901(问题： #51816) * REST API 兼容性] 用于搜索"_count"API 的类型化终结点 [#73958(问题：#42112、#51816)* REST API 兼容性] 类型化索引统计信息 [#74181(问题：#47203、#51816、#54160)* REST API 兼容性] 渗透查询 API 的类型 [#74698(问题： #46985， #51816， #54160， #74689) * REST API 兼容性] 验证查询类型 API [#74171(问题： #46927、#51816、#54160) * REST API 兼容性] 投票配置排除异常消息 [#75406(问题：#51816、#55291)* REST API 兼容性] 类型为 [#75123 (问题： #42198、#51816、#54160) * REST API 兼容性] 通过使用大小字段的查询进行更新和删除 [#69606 * REST API 兼容性] 对象格式的指示符提升 [#74422(问题： #51816， #55078) * REST API 兼容性] 搜索和相关终结点的类型化终结点 [#72155(问题：#51816、#54160) * REST API 兼容性] 允许使用大小"-1" [#75342(问题：#51816、#69548、#70209) * REST API 兼容性] 忽略文档值的"use_field_mapping"选项 [#74435(问题：#55622) * REST API 兼容性] "_time"和"_term"排序顺序 [#74919(问题：#39450、#51816) * REST API 兼容性] PUT 索引模板上的"模板"参数和字段 [#71238(问题：#49460、#51816、#68905) * REST API 兼容性] 使查询注册更容易 [#75722(问题：#51816)* REST API 兼容性] 类型化查询 [#75453(问题：#47207、#51816、#54160)* REST API 兼容性] 弃用同步刷新 [#75372(问题：#50882、#51816)* REST API 兼容性] 许可证"accept_enterprise"和响应更改 [#75479(问题：#50067、#50735、#51816、#58217)

Infra/Scripting

    

* 将"弃用映射"更新为"动态映射" #56149(问题：#52103) * 将 nio 缓冲区添加到无痛 #79870(问题：#79867) * 恢复脚本常规缓存 #79453(问题：#62899)

Infra/Settings

    

* 修复了不一致的"Setting.exist()"#46603(问题：#41830) * 删除"index.optimize_auto_generated_id"设置 (#27583) #27600(问题：#27583) * 通过字符串实习实施设置重复数据删除 #80493(问题：#77466、#78892)

Ingest

    

* 添加对"_meta"字段的支持以引入管道 #76381 * 附件处理器执行后删除二进制字段 #79172 * 改进缓存查找以减少重新计算/搜索 #77259 * 从二进制文件中提取更多标准元数据 #78754(问题：#22339)

License

    

* 将已弃用的"accept_enterprise"参数添加到"/_xpack"#58220(问题：#58217) * 在获取许可证 API #50067 中支持"accept_enterprise"参数(问题：#49474) * 对所有许可证强制执行传输 TLS 检查 #79602(问题：#75292)

机器学习

    

* 用于机器学习C++代码的 Windows 构建平台现在使用 Visual Studio 2019 #1352 * 用于机器学习C++代码的 macOS 构建平台现在运行 Xcode 11.3.1 的 Mojave 或运行 clang 8 的 Ubuntu 20.04 进行交叉编译 #1429 * 添加一个用于评估 PyTorch 模型的新应用程序。该应用程序依赖于 LibTorch(PyTorch 的C++前端)，并对以 TorchScript 格式存储的模型执行推理 #1902 * 添加新的 PUT 训练模型词汇端点 #77387 * 创建新的 PUT 模型定义部件 API #76987 * 添加推理时间配置覆盖 #78441(问题：#77799) * 优化"categorize_text"聚合的源提取 #79099 * 机器学习C++代码的 Linux 构建平台现在是运行 gcc 10.3 的 CentOS 7。#2028 * 当节点成为主节点时隐藏 ML 索引 #77416(问题：#53674) * 将"deployment_stats"添加到训练模型统计信息 #80531 * 设置"use_auto_machine_memory_percent"现在默认为"max_model_memory_limit" #80532(问题：#80415)

Mapping

    

* 稀疏向量始终抛出异常 #62646 * 添加对配置 HNSW 参数的支持 #79193(问题：#78473) * 扩展"dense_vector"以支持索引向量 #78491(问题：#78473)

Monitoring

    

* 将之前删除的监控设置重新添加到 8.0 #78784 中 * 将监控插件群集警报更改为默认不安装 #79657 * 为 Metricbeat ECS 数据添加默认模板 #81744

Network

    

* 默认启用 LZ4 传输压缩 #76326 (问题： #73497) * 改进慢速入站处理以包含响应类型 #80425

Packaging

    

* 使 Docker 构建在云中更可重用 #50277 (问题： #46166， #49926) * 更新 docker-compose.yml 以修复引导程序检查错误 #47650 * 允许覆盖总内存 #78750 (问题： #65905) * 将存储库插件转换为模块 #81870(问题： #81652)

Recovery

    

* 在对等恢复和重新同步中使用 Lucene 索引 #51189(问题：#50775) * 修复了"挂起复制操作"将大量"NOOP"任务提交到"通用"#82092(问题：#77466、#79837)

Reindex

    

* 使重新索引由持久任务管理#43382(问题：#42612) * 从检查点 #46055 重新索引重新启动(问题：#42612) * 重新索引搜索弹性 #45497(问题：#42612、#43187) * 重新索引 v2 限制切片修复 #46967(问题：#42612、#46763) * 如果最大文档小于滚动大小，则不要滚动(通过查询更新/删除) #81654(问题：#54270)

Rollup

    

* 在汇总指标和"日期直方图"配置中添加对"date_nanos"的支持 #59349(问题：#44505)

SQL

    

* 添加对多值的文本格式支持 #68606 * 添加 xDBC 和 CLI 支持。QA CSV 规格 #68966 * 通过结果集导出数组值 #69512 * 改进子查询中的别名解析 #67216(问题：#56713) * 改进空条件的优化 #71192 * 在子查询中推送"WHERE"子句 #71362 * 对"LTRIM/RTRIM"使用 Java "字符串"方法 #57594 * QL：使规范形式考虑到子项 #71266 * QL： 波兰语优化器表达式规则声明 #71396 * QL： 跨连词传播可为空性约束 #71187(问题：#70683)

Search

    

* 完全禁止在搜索中设置负大小 #70209 (问题： #69548) * 将"0"作为"has_child"查询中"min_children"的无效值 #41347 * 本地解析远程索引时返回错误 #74556(问题：#26247) * REST API 兼容性] 嵌套路径和过滤器排序选项 [#76022(问题：#42809、#51816)* REST API 兼容性] "CommonTermsQuery"和"cutoff_frequency"参数 [#75896(问题： #42654， #51816) * REST API 兼容性] 允许"_msearch"的第一个空行 [#75886(问题：#41011、#51816)* 节点级别可以匹配操作 #78765 * TSDB：将时间序列信息添加到字段上限 #78790(问题：#74660) * 添加新的 kNN 搜索端点 #79013(问题：#78473) * 禁止对嵌套向量字段 #79403 进行 kNN 搜索(问题：#78473) * 确保 kNN 搜索遵循授权 #79693(问题： #78473) * 使用 mmapfs 加载 kNN 向量格式 #78724 (问题： #78473) * 支持 kNN 搜索中的余弦相似性 #79500 * 节点级别可以匹配操作 #78765 * 在 kNN 搜索 #80516 中检查前面的嵌套字段 #80516(问题：#78473)

Security

    

* 添加用于创建注册令牌的工具 #74890 * 添加注册 Kibana API #72207 * 更改 FIPS 140 的默认哈希算法 #55544 * 创建注册令牌 #73573(问题：#71438、#72129) * 注册节点 API #72129 * 配置初始节点 CLI 的安全性 #74868 * 为弹性用户 #76276 生成和存储密码哈希(问题：#75310) * 设置弹性密码并生成注册令牌 #75816(问题： #75310) * 添加"弹性搜索-注册-节点"工具 #77292 * FIPS 模式下的默认哈希器为"PBKDF2_STRETCH" #76274 * 添加 v7 "restCompat"，用于使 id 字段 #78664 的 API 密钥失效(问题：#66671) * 启动时打印注册令牌 #78293 * 安全隐式行为更改的启动检查 #76879 * 用于重新配置节点以注册的 CLI 工具 #79690(问题：#7718) * 打包安装的安全自动配置 #75144(问题： #78306)

Snapshot/Restore

    

* 引入可搜索快照索引设置，用于级联删除快照 #74977 * 统一 blob 存储压缩设置 #39346(问题：#39073) * 为可搜索快照添加恢复状态跟踪 #60505 * 允许列出较旧的存储库 #78244 * 优化 SLM 策略查询 #79341(问题：#79321)

TLS

    

* 在 Java 12+ 上添加"ChaCha20"TLS 密码 #42155 * 将"密钥库"过滤器的支持添加到"ssl-config" #75407 * 更新 JDK 11 的 TLS 密码和协议 #41808(问题：#38646、#41385)

Transform

    

* 防止旧的测试版转换开始 #79712

TSDB

    

* 自动添加时间戳映射器 #79136 * 为 tsdb 创建协调节点级读取器 #79197 * 修复多版本集群中的 TSDB 收缩测试 #79940(问题：#79936) * 不允许阴影指标或维度 #79757

### 错误修正

Aggregations

    

* 修复"x_pack/用法"#55181 的 BWC 问题(问题：#54847) * 修复"双边界"空序列化 #59475 * 修复"TopHitsAggregationBuilder"添加重复的"_score"排序子句 #42179(问题：#42154) * 修复"t_test"使用情况统计信息 #54753(问题：#54744) * 如果无法在"日期间隔包装器"中解析旧间隔，则引发异常 #41972(问题：#41970)

Autoscaling

    

* 自动缩放使用调整后的总内存 #80528(问题：#78750)

CCR

    

* 修复"自动关注"版本检查 #73776(问题：#72935)

集群协调

    

* 在系统上下文中应用群集状态 #53785(问题：#53751)

数据流

    

* 禁止还原具有冲突写入数据流的数据流别名 #81217(问题：#80976)

Distributed

    

* 引入"？wait_for_active_shards=索引设置" #67158(问题：#66419) * 修复任务结果索引映射 #50359(问题：#50248)

功能/CAT API

    

* 修复字节字段的 cat 恢复显示 #40379(问题：#40335)

Features/ILM+SLM

    

* 确保每个节点的总分片数太低时"收缩操作"不会挂起 #76732(问题：#44070) * SLM 元数据中快照失败的详细序列化较少 #80942(问题：#77466)

功能/索引 API

    

* 修复"可组合索引模板"等于"composed_of"为空时 #80864

功能/Java 高级 REST 客户端

    

* Java High Level Rest Client (HLRC) 已被移除，取而代之的是新的 Elasticsearch Java 客户端。有关迁移步骤，请参阅从高级 Rest 客户端迁移。

Geo

    

* 在处理多边形环以进行分解之前对其进行预处理 #59501(问题：#54441、#59386)

Infra/Core

    

* 将可搜索的快照缓存文件夹添加到"节点环境" #66297 (问题： #65725) * CLI 工具：将错误写入 stderr 而不是 stdout #45586(问题： #43260) * 为 XContentType #67409 预计算"解析媒体类型" * 防止舍入时堆栈溢出 #80450

Infra/Logging

    

* 修复了在 JSON 中记录空值时的 NPE #53715(问题：#46702) * 修复慢日志中的统计信息为转义的 JSON #44642 * 未提供"xOpaqueId"时填充数据流字段 #62156

基础设施/休息接口

    

* 不允许在"MediaType"参数中留有空格 #64650(问题：#51816) * 处理不正确的标头值 #64708(问题：#51816、#64689) * 解析 #64721 时忽略媒体范围(问题：#51816、#64689) * "RestController"不应使用请求内容 #44902(问题：#37504) * 处理从"RestCompatibleVersionHelper"#80253 (问题： #78214、#79060) 引发的异常

Infra/Scripting

    

* 更改复合赋值结构以支持字符串连接 #61825 * 修复了常量折叠中的强制转换 #61508 * 几个小的无痛修复 #61594 * 修复脚本引擎创建时重复的允许列表 #82820(问题：#82778)

Infra/Settings

    

* 在 REST 层上更严格的"更新设置请求"解析 #79227(问题：#29268) * 设置弃用日志数据流的自动扩展副本 #79226(问题：#78991)

Ingest

    

* 将默认 geoip 日志记录调整为不那么详细 #81404(问题：#81356)

机器学习

    

* 添加删除训练模型的超时参数 API #79739(问题：#77070) * 调低 ML 未分配作业通知 #79578(问题：#79270) * 将来使用新的批注索引 #79006(问题：#78439) * 将模型状态兼容版本设置为 8.0.0 #2139 * 在开始部署之前检查"total_definition_length"是否一致 #80553 * 在某些错误类型上更一致地使推理处理器失败 #81475 * 优化作业统计调用以减少搜索#82362(问题：#82255)

Mapping

    

* 删除映射具有一个顶级键的断言 #58779(问题：#58521)

Packaging

    

* 禁止插件安装中的非法访问 #41620 (问题： #41478)

Recovery

    

* 使分片启动的响应处理仅在群集状态更新完成后返回 #82790(问题：#81628)

SQL

    

* 为"HAVING"声明引入专用节点 #71279 (问题： #69758) * 使"RestSqlQueryAction"线程安全 #69901

Search

    

* 检查搜索请求正文 #54953 中的负"from"值(问题：#54897) * 修复 BWC 模式 #55399 中的"矢量功能集用法"序列化(问题：#55378) * 处理等于"track_total_hits"的总命中数 #37907(问题：#37897) * 改进了没有远程群集角色的节点上 CCS 请求的错误消息 #60351(问题：#59683) * 删除通配符字段中不安全的断言 #78966

Security

    

* 允许访问保留系统角色的受限系统索引 #76845

Snapshot/Restore

    

* 修复"GET /_snapshot/_all/_all"如果没有存储库 #43558(问题：#43547) * 不要填充"快照分片失败"中的堆栈跟踪 #80009(问题：#79718) * 如果没有要还原的内容，请删除自定义元数据 #81373(问题：#81247、#82019)

###Regressions

Search

    

* 有条件地禁用数字排序优化 #78103

###Upgrades

Authentication

    

* 升级到未绑定 ID LDAP SDK v6.0.2 #79332

Infra/Logging

    

* 升级 ECS 日志记录布局至最新版本 #80500

Search

    

* 升级到 Lucene 9 #81426

Security

    

* 更新至 OpenSAML 4 #77012(问题：#71983)

Snapshot/Restore

    

* 将存储库-hdfs 插件升级到 Hadoop 3 #76897

[« Elasticsearch version 8.0.1](release-notes-8.0.1.md) [Elasticsearch
version 8.0.0-rc2 »](release-notes-8.0.0-rc2.md)
