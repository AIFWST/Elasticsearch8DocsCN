# Elasticsearch 8.9 中文文档翻译项目

欢迎来到我们的GitHub代码仓库！这个项目致力于将Elasticsearch 8.9官方英文文档翻译成中文，以方便非英语母语的开发者和用户阅读和使用。

Elasticsearch是一个开源的分布式搜索和分析引擎，在各种大规模数据处理和搜索场景中得到广泛应用。然而，对于一些非英语母语的开发者和用户来说，阅读英文文档可能会非常困难。

为了解决这个问题，我们使用程序从Elasticsearch官方网站上爬取了所有的英文文档，并调用Edge的翻译接口将它们翻译成中文。

需要注意的是，由于我们使用的是翻译接口进行直接翻译，文档中可能会存在一些描述不准确的地方。因此，这个仓库中的翻译内容仅供参考，[官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/8.9/)仍然是最权威和最准确的资料。

我们计划在公众号【AI财智通】中分享ElasticSearch中文文档学习笔记，与大家一起交流和学习。如果你对Elasticsearch感兴趣，欢迎关注我们的公众号，获取更多有关Elasticsearch的信息和资源。

![wechat.png](./config%2Fwechat.png)

# 程序运行
python main.py


# 阅读目录
[目录](./zh_mds/index.md)

什么是 Elasticsearch？
[What is Elasticsearch?](./zh_mds/elasticsearch-intro.md)

数据来源：文档和索引
[Data in: documents and indices](./zh_mds/documents-indices.md)

信息输出：搜索和分析
[Information out: search and analyze](./zh_mds/search-analyze.md)

可扩展性和弹性
[Scalability and resilience](./zh_mds/scalability.md)

8.9 中的新增功能
[What’s new in 8.9](./zh_mds/release-highlights.md)

设置 Elasticsearch
[Set up Elasticsearch](./zh_mds/setup.md)

安装 Elasticsearch
[Installing Elasticsearch](./zh_mds/install-elasticsearch.md)

在 Linux 或 MacOS 上从存档安装 Elasticsearch
[Install Elasticsearch from archive on Linux or MacOS](./zh_mds/targz.md)

在 Windows 上安装 Elasticsearch with .zip
[Install Elasticsearch with .zip on Windows](./zh_mds/zip-windows.md)

使用 Debian 软件包安装 Elasticsearch
[Install Elasticsearch with Debian Package](./zh_mds/deb.md)

使用 RPM 安装 Elasticsearch
[Install Elasticsearch with RPM](./zh_mds/rpm.md)

使用 Docker 安装 Elasticsearch
[Install Elasticsearch with Docker](./zh_mds/docker.md)

在本地运行 Elasticsearch
[Run Elasticsearch locally](./zh_mds/run-elasticsearch-locally.md)

配置弹性搜索
[Configuring Elasticsearch](./zh_mds/settings.md)

重要 Elasticsearch 配置
[Important Elasticsearch configuration](./zh_mds/important-settings.md)

安全设置
[Secure settings](./zh_mds/secure-settings.md)

审核设置
[Auditing settings](./zh_mds/auditing-settings.md)

断路器设置
[Circuit breaker settings](./zh_mds/circuit-breaker.md)

集群级分片分配和路由设置
[Cluster-level shard allocation and routing settings](./zh_mds/modules-cluster.md)

杂项群集设置
[Miscellaneous cluster settings](./zh_mds/misc-cluster-settings.md)

跨集群复制设置
[Cross-cluster replication settings](./zh_mds/ccr-settings.md)

发现和集群形成设置
[Discovery and cluster formation settings](./zh_mds/modules-discovery-settings.md)

字段数据缓存设置
[Field data cache settings](./zh_mds/modules-fielddata.md)

运行状况诊断设置
[Health Diagnostic settings](./zh_mds/health-diagnostic-settings.md)

索引生命周期管理设置
[Index lifecycle management settings](./zh_mds/ilm-settings.md)

索引管理设置
[Index management settings](./zh_mds/index-management-settings.md)

索引恢复设置
[Index recovery settings](./zh_mds/recovery.md)

索引缓冲区设置
[Indexing buffer settings](./zh_mds/indexing-buffer.md)

许可证设置
[License settings](./zh_mds/license-settings.md)

本地网关设置
[Local gateway settings](./zh_mds/modules-gateway.md)

伐木
[Logging](./zh_mds/logging.md)

机器学习设置
[Machine learning settings](./zh_mds/ml-settings.md)

监视设置
[Monitoring settings](./zh_mds/monitoring-settings.md)

节点
[Node](./zh_mds/modules-node.md)

联网
[Networking](./zh_mds/modules-network.md)

节点查询缓存设置
[Node query cache settings](./zh_mds/query-cache.md)

搜索设置
[Search settings](./zh_mds/search-settings.md)

安全设置
[Security settings](./zh_mds/security-settings.md)

分片请求缓存设置
[Shard request cache settings](./zh_mds/shard-request-cache.md)

快照和还原设置
[Snapshot and restore settings](./zh_mds/snapshot-settings.md)

转换设置
[Transforms settings](./zh_mds/transform-settings.md)

线程池
[Thread pools](./zh_mds/modules-threadpool.md)

观察程序设置
[Watcher settings](./zh_mds/notification-settings.md)

高级配置
[Advanced configuration](./zh_mds/advanced-configuration.md)

重要的系统配置
[Important system configuration](./zh_mds/system-config.md)

配置系统设置
[Configuring system settings](./zh_mds/setting-system-settings.md)

禁用交换
[Disable swapping](./zh_mds/setup-configuration-memory.md)

文件描述符
[File Descriptors](./zh_mds/file-descriptors.md)

虚拟内存
[Virtual memory](./zh_mds/vm-max-map-count.md)

线程数
[Number of threads](./zh_mds/max-number-of-threads.md)

DNS 缓存设置
[DNS cache settings](./zh_mds/networkaddress-cache-ttl.md)

确保 JNA 临时目录允许可执行文件
[Ensure JNA temporary directory permits executables](./zh_mds/executable-jna-tmpdir.md)

TCP 重新传输超时
[TCP retransmission timeout](./zh_mds/system-config-tcpretries.md)

引导程序检查
[Bootstrap Checks](./zh_mds/bootstrap-checks.md)

堆大小检查
[Heap size check](./zh_mds/_heap_size_check.md)

文件描述符检查
[File descriptor check](./zh_mds/_file_descriptor_check.md)

内存锁定检查
[Memory lock check](./zh_mds/_memory_lock_check.md)

最大线程数检查
[Maximum number of threads check](./zh_mds/max-number-threads-check.md)

最大文件大小检查
[Max file size check](./zh_mds/_max_file_size_check.md)

最大大小虚拟内存检查
[Maximum size virtual memory check](./zh_mds/max-size-virtual-memory-check.md)

最大地图计数检查
[Maximum map count check](./zh_mds/_maximum_map_count_check.md)

客户机 JVM 检查
[Client JVM check](./zh_mds/_client_jvm_check.md)

使用串行收集器检查
[Use serial collector check](./zh_mds/_use_serial_collector_check.md)

系统调用过滤器检查
[System call filter check](./zh_mds/_system_call_filter_check.md)

OnError 和 OnOutofMemoryError 检查
[OnError and OnOutOfMemoryError checks](./zh_mds/_onerror_and_onoutofmemoryerror_checks.md)

抢先体验检查
[Early-access check](./zh_mds/_early_access_check.md)

G1GC 检查
[G1GC check](./zh_mds/_g1gc_check.md)

所有权限检查
[All permission check](./zh_mds/_all_permission_check.md)

发现配置检查
[Discovery configuration check](./zh_mds/_discovery_configuration_check.md)

X-Pack 的引导程序检查
[Bootstrap Checks for X-Pack](./zh_mds/bootstrap-checks-xpack.md)

启动弹性搜索
[Starting Elasticsearch](./zh_mds/starting-elasticsearch.md)

停止弹性搜索
[Stopping Elasticsearch](./zh_mds/stopping-elasticsearch.md)

发现和集群形成
[Discovery and cluster formation](./zh_mds/modules-discovery.md)

发现
[Discovery](./zh_mds/discovery-hosts-providers.md)

基于仲裁的决策
[Quorum-based decision making](./zh_mds/modules-discovery-quorums.md)

投票配置
[Voting configurations](./zh_mds/modules-discovery-voting.md)

引导集群
[Bootstrapping a cluster](./zh_mds/modules-discovery-bootstrap-cluster.md)

发布群集状态
[Publishing the cluster state](./zh_mds/cluster-state-publishing.md)

集群故障检测
[Cluster fault detection](./zh_mds/cluster-fault-detection.md)

在群集中添加和删除节点
[Add and remove nodes in your cluster](./zh_mds/add-elasticsearch-nodes.md)

全集群重启和滚动重启
[Full-cluster restart and rolling restart](./zh_mds/restart-cluster.md)

远程群集
[Remote clusters](./zh_mds/remote-clusters.md)

配置具有安全性的远程群集
[Configure remote clusters with security](./zh_mds/remote-clusters-security.md)

连接到远程群集
[Connect to remote clusters](./zh_mds/remote-clusters-connect.md)

为远程群集配置角色和用户
[Configure roles and users for remote clusters](./zh_mds/remote-clusters-privileges.md)

远程群集设置
[Remote cluster settings](./zh_mds/remote-clusters-settings.md)

插件
[Plugins](./zh_mds/modules-plugins.md)

升级弹性搜索
[Upgrade Elasticsearch](./zh_mds/setup-upgrade.md)

存档设置
[Archived settings](./zh_mds/archived-settings.md)

从较旧的 Elasticsearch 版本读取索引
[Reading indices from older Elasticsearch versions](./zh_mds/archive-indices.md)

索引模块
[Index modules](./zh_mds/index-modules.md)

分析
[Analysis](./zh_mds/index-modules-analysis.md)

索引分片分配
[Index Shard Allocation](./zh_mds/index-modules-allocation.md)

索引级分片分配筛选
[Index-level shard allocation filtering](./zh_mds/shard-allocation-filtering.md)

节点离开时延迟分配
[Delaying allocation when a node leaves](./zh_mds/delayed-allocation.md)

索引恢复优先级
[Index recovery prioritization](./zh_mds/recovery-prioritization.md)

每个节点的分片总数
[Total shards per node](./zh_mds/allocation-total-shards.md)

索引级数据层分配筛选
[Index-level data tier allocation filtering](./zh_mds/data-tier-shard-filtering.md)

索引块
[Index blocks](./zh_mds/index-modules-blocks.md)

映射
[Mapper](./zh_mds/index-modules-mapper.md)

合并
[Merge](./zh_mds/index-modules-merge.md)

相似性模块
[Similarity module](./zh_mds/index-modules-similarity.md)

慢日志
[Slow Log](./zh_mds/index-modules-slowlog.md)

商店
[Store](./zh_mds/index-modules-store.md)

将数据预加载到文件系统缓存中
[Preloading data into the file system cache](./zh_mds/preload-data-to-file-system-cache.md)

交易日志
[Translog](./zh_mds/index-modules-translog.md)

历史记录保留
[History retention](./zh_mds/index-modules-history-retention.md)

索引排序
[Index Sorting](./zh_mds/index-modules-index-sorting.md)

使用索引排序加快连词
[Use index sorting to speed up conjunctions](./zh_mds/index-modules-index-sorting-conjunctions.md)

分度压力
[Indexing pressure](./zh_mds/index-modules-indexing-pressure.md)

映射
[Mapping](./zh_mds/mapping.md)

动态映射
[Dynamic mapping](./zh_mds/dynamic-mapping.md)

动态字段映射
[Dynamic field mapping](./zh_mds/dynamic-field-mapping.md)

动态模板
[Dynamic templates](./zh_mds/dynamic-templates.md)

显式映射
[Explicit mapping](./zh_mds/explicit-mapping.md)

运行时字段
[Runtime fields](./zh_mds/runtime.md)

映射运行时字段
[Map a runtime field](./zh_mds/runtime-mapping-fields.md)

在搜索请求中定义运行时字段
[Define runtime fields in a search request](./zh_mds/runtime-search-request.md)

在查询时覆盖字段值
[Override field values at query time](./zh_mds/runtime-override-values.md)

检索运行时字段
[Retrieve a runtime field](./zh_mds/runtime-retrieving-fields.md)

为运行时字段编制索引
[Index a runtime field](./zh_mds/runtime-indexed.md)

使用运行时字段浏览数据
[Explore your data with runtime fields](./zh_mds/runtime-examples.md)

字段数据类型
[Field data types](./zh_mds/mapping-types.md)

聚合指标
[Aggregate metric](./zh_mds/aggregate-metric-double.md)

别名
[Alias](./zh_mds/field-alias.md)

阵 列
[Arrays](./zh_mds/array.md)

二元的
[Binary](./zh_mds/binary.md)

布尔
[Boolean](./zh_mds/boolean.md)

完成
[Completion](./zh_mds/completion.md)

日期
[Date](./zh_mds/date.md)

日期纳秒
[Date nanoseconds](./zh_mds/date_nanos.md)

密集矢量
[Dense vector](./zh_mds/dense-vector.md)

扁平
[Flattened](./zh_mds/flattened.md)

地理点
[Geopoint](./zh_mds/geo-point.md)

地形
[Geoshape](./zh_mds/geo-shape.md)

直方图
[Histogram](./zh_mds/histogram.md)

知识产权
[IP](./zh_mds/ip.md)

加入
[Join](./zh_mds/parent-join.md)

关键词
[Keyword](./zh_mds/keyword.md)

嵌 套
[Nested](./zh_mds/nested.md)

数值的
[Numeric](./zh_mds/number.md)

对象
[Object](./zh_mds/object.md)

渗滤器
[Percolator](./zh_mds/percolator.md)

点
[Point](./zh_mds/point.md)

范围
[Range](./zh_mds/range.md)

排名功能
[Rank feature](./zh_mds/rank-feature.md)

排名功能
[Rank features](./zh_mds/rank-features.md)

键入时搜索
[Search-as-you-type](./zh_mds/search-as-you-type.md)

形状
[Shape](./zh_mds/shape.md)

发短信
[Text](./zh_mds/text.md)

令牌计数
[Token count](./zh_mds/token-count.md)

无符号长
[Unsigned long](./zh_mds/unsigned-long.md)

版本
[Version](./zh_mds/version.md)

元数据字段
[Metadata fields](./zh_mds/mapping-fields.md)

_doc_count字段
[_doc_count field](./zh_mds/mapping-doc-count-field.md)

_field_names字段
[_field_names field](./zh_mds/mapping-field-names-field.md)

_ignored字段
[_ignored field](./zh_mds/mapping-ignored-field.md)

_id字段
[_id field](./zh_mds/mapping-id-field.md)

_index字段
[_index field](./zh_mds/mapping-index-field.md)

_meta字段
[_meta field](./zh_mds/mapping-meta-field.md)

_routing字段
[_routing field](./zh_mds/mapping-routing-field.md)

_source字段
[_source field](./zh_mds/mapping-source-field.md)

_tier字段
[_tier field](./zh_mds/mapping-tier-field.md)

映射参数
[Mapping parameters](./zh_mds/mapping-params.md)

分析器
[analyzer](./zh_mds/analyzer.md)

要挟
[coerce](./zh_mds/coerce.md)

copy_to
[copy_to](./zh_mds/copy-to.md)

doc_values
[doc_values](./zh_mds/doc-values.md)

动态
[dynamic](./zh_mds/dynamic.md)

eager_global_ordinals
[eager_global_ordinals](./zh_mds/eager-global-ordinals.md)

启用
[enabled](./zh_mds/enabled.md)

格式
[format](./zh_mds/mapping-date-format.md)

ignore_above
[ignore_above](./zh_mds/ignore-above.md)

ignore_malformed
[ignore_malformed](./zh_mds/ignore-malformed.md)

指数
[index](./zh_mds/mapping-index.md)

index_options
[index_options](./zh_mds/index-options.md)

index_phrases
[index_phrases](./zh_mds/index-phrases.md)

index_prefixes
[index_prefixes](./zh_mds/index-prefixes.md)

元
[meta](./zh_mds/mapping-field-meta.md)

领域
[fields](./zh_mds/multi-fields.md)

归一化器
[normalizer](./zh_mds/normalizer.md)

规范
[norms](./zh_mds/norms.md)

null_value
[null_value](./zh_mds/null-value.md)

position_increment_gap
[position_increment_gap](./zh_mds/position-increment-gap.md)

性能
[properties](./zh_mds/properties.md)

search_analyzer
[search_analyzer](./zh_mds/search-analyzer.md)

相似
[similarity](./zh_mds/similarity.md)

商店
[store](./zh_mds/mapping-store.md)

子对象
[subobjects](./zh_mds/subobjects.md)

term_vector
[term_vector](./zh_mds/term-vector.md)

映射限制设置
[Mapping limit settings](./zh_mds/mapping-settings-limit.md)

删除映射类型
[Removal of mapping types](./zh_mds/removal-of-types.md)

文本分析
[Text analysis](./zh_mds/analysis.md)

概述
[Overview](./zh_mds/analysis-overview.md)

概念
[Concepts](./zh_mds/analysis-concepts.md)

分析仪剖析
[Anatomy of an analyzer](./zh_mds/analyzer-anatomy.md)

索引和搜索分析
[Index and search analysis](./zh_mds/analysis-index-search-time.md)

堵塞
[Stemming](./zh_mds/stemming.md)

令牌图
[Token graphs](./zh_mds/token-graphs.md)

配置文本分析
[Configure text analysis](./zh_mds/configure-text-analysis.md)

测试分析器
[Test an analyzer](./zh_mds/test-analyzer.md)

配置内置分析器
[Configuring built-in analyzers](./zh_mds/configuring-analyzers.md)

创建自定义分析器
[Create a custom analyzer](./zh_mds/analysis-custom-analyzer.md)

指定分析器
[Specify an analyzer](./zh_mds/specify-analyzer.md)

内置分析器参考
[Built-in analyzer reference](./zh_mds/analysis-analyzers.md)

指纹
[Fingerprint](./zh_mds/analysis-fingerprint-analyzer.md)

关键词
[Keyword](./zh_mds/analysis-keyword-analyzer.md)

语言
[Language](./zh_mds/analysis-lang-analyzer.md)

模式
[Pattern](./zh_mds/analysis-pattern-analyzer.md)

简单
[Simple](./zh_mds/analysis-simple-analyzer.md)

标准
[Standard](./zh_mds/analysis-standard-analyzer.md)

停
[Stop](./zh_mds/analysis-stop-analyzer.md)

空白
[Whitespace](./zh_mds/analysis-whitespace-analyzer.md)

分词器参考
[Tokenizer reference](./zh_mds/analysis-tokenizers.md)

字符组
[Character group](./zh_mds/analysis-chargroup-tokenizer.md)

经典
[Classic](./zh_mds/analysis-classic-tokenizer.md)

边缘 n 元语法
[Edge n-gram](./zh_mds/analysis-edgengram-tokenizer.md)

关键词
[Keyword](./zh_mds/analysis-keyword-tokenizer.md)

信
[Letter](./zh_mds/analysis-letter-tokenizer.md)

小写
[Lowercase](./zh_mds/analysis-lowercase-tokenizer.md)

N-gram
[N-gram](./zh_mds/analysis-ngram-tokenizer.md)

路径层次结构
[Path hierarchy](./zh_mds/analysis-pathhierarchy-tokenizer.md)

模式
[Pattern](./zh_mds/analysis-pattern-tokenizer.md)

简单图案
[Simple pattern](./zh_mds/analysis-simplepattern-tokenizer.md)

简单的图案分割
[Simple pattern split](./zh_mds/analysis-simplepatternsplit-tokenizer.md)

标准
[Standard](./zh_mds/analysis-standard-tokenizer.md)

泰语
[Thai](./zh_mds/analysis-thai-tokenizer.md)

无人机网址电子邮件
[UAX URL email](./zh_mds/analysis-uaxurlemail-tokenizer.md)

空白
[Whitespace](./zh_mds/analysis-whitespace-tokenizer.md)

令牌筛选器引用
[Token filter reference](./zh_mds/analysis-tokenfilters.md)

省略符号
[Apostrophe](./zh_mds/analysis-apostrophe-tokenfilter.md)

ASCII 折叠
[ASCII folding](./zh_mds/analysis-asciifolding-tokenfilter.md)

中日韩双格拉姆
[CJK bigram](./zh_mds/analysis-cjk-bigram-tokenfilter.md)

中日韩宽度
[CJK width](./zh_mds/analysis-cjk-width-tokenfilter.md)

经典
[Classic](./zh_mds/analysis-classic-tokenfilter.md)

普通克
[Common grams](./zh_mds/analysis-common-grams-tokenfilter.md)

有條件的
[Conditional](./zh_mds/analysis-condition-tokenfilter.md)

十进制数字
[Decimal digit](./zh_mds/analysis-decimal-digit-tokenfilter.md)

分隔有效负载
[Delimited payload](./zh_mds/analysis-delimited-payload-tokenfilter.md)

字典解复合剂
[Dictionary decompounder](./zh_mds/analysis-dict-decomp-tokenfilter.md)

边缘 n 元语法
[Edge n-gram](./zh_mds/analysis-edgengram-tokenfilter.md)

元音省略
[Elision](./zh_mds/analysis-elision-tokenfilter.md)

指纹
[Fingerprint](./zh_mds/analysis-fingerprint-tokenfilter.md)

展平图形
[Flatten graph](./zh_mds/analysis-flatten-graph-tokenfilter.md)

亨斯佩尔
[Hunspell](./zh_mds/analysis-hunspell-tokenfilter.md)

连字解复合剂
[Hyphenation decompounder](./zh_mds/analysis-hyp-decomp-tokenfilter.md)

保留类型
[Keep types](./zh_mds/analysis-keep-types-tokenfilter.md)

保留单词
[Keep words](./zh_mds/analysis-keep-words-tokenfilter.md)

关键字标记
[Keyword marker](./zh_mds/analysis-keyword-marker-tokenfilter.md)

关键字重复
[Keyword repeat](./zh_mds/analysis-keyword-repeat-tokenfilter.md)

KStem
[KStem](./zh_mds/analysis-kstem-tokenfilter.md)

长度
[Length](./zh_mds/analysis-length-tokenfilter.md)

限制令牌计数
[Limit token count](./zh_mds/analysis-limit-token-count-tokenfilter.md)

小写
[Lowercase](./zh_mds/analysis-lowercase-tokenfilter.md)

最小哈希
[MinHash](./zh_mds/analysis-minhash-tokenfilter.md)

复 用
[Multiplexer](./zh_mds/analysis-multiplexer-tokenfilter.md)

N-gram
[N-gram](./zh_mds/analysis-ngram-tokenfilter.md)

正常化
[Normalization](./zh_mds/analysis-normalization-tokenfilter.md)

模式捕获
[Pattern capture](./zh_mds/analysis-pattern-capture-tokenfilter.md)

图案替换
[Pattern replace](./zh_mds/analysis-pattern_replace-tokenfilter.md)

语音
[Phonetic](./zh_mds/analysis-phonetic-tokenfilter.md)

波特杆
[Porter stem](./zh_mds/analysis-porterstem-tokenfilter.md)

谓词脚本
[Predicate script](./zh_mds/analysis-predicatefilter-tokenfilter.md)

删除重复项
[Remove duplicates](./zh_mds/analysis-remove-duplicates-tokenfilter.md)

反向
[Reverse](./zh_mds/analysis-reverse-tokenfilter.md)

瓦
[Shingle](./zh_mds/analysis-shingle-tokenfilter.md)

雪球
[Snowball](./zh_mds/analysis-snowball-tokenfilter.md)

干聚体
[Stemmer](./zh_mds/analysis-stemmer-tokenfilter.md)

词干覆盖
[Stemmer override](./zh_mds/analysis-stemmer-override-tokenfilter.md)

停
[Stop](./zh_mds/analysis-stop-tokenfilter.md)

同义词
[Synonym](./zh_mds/analysis-synonym-tokenfilter.md)

同义词图
[Synonym graph](./zh_mds/analysis-synonym-graph-tokenfilter.md)

修剪
[Trim](./zh_mds/analysis-trim-tokenfilter.md)

截断
[Truncate](./zh_mds/analysis-truncate-tokenfilter.md)

独特
[Unique](./zh_mds/analysis-unique-tokenfilter.md)

大写
[Uppercase](./zh_mds/analysis-uppercase-tokenfilter.md)

单词分隔符
[Word delimiter](./zh_mds/analysis-word-delimiter-tokenfilter.md)

单词分隔符图
[Word delimiter graph](./zh_mds/analysis-word-delimiter-graph-tokenfilter.md)

字符筛选器参考
[Character filters reference](./zh_mds/analysis-charfilters.md)

网页条
[HTML strip](./zh_mds/analysis-htmlstrip-charfilter.md)

映射
[Mapping](./zh_mds/analysis-mapping-charfilter.md)

图案替换
[Pattern replace](./zh_mds/analysis-pattern-replace-charfilter.md)

归一化器
[Normalizers](./zh_mds/analysis-normalizers.md)

索引模板
[Index templates](./zh_mds/index-templates.md)

模拟多组件模板
[Simulate multi-component templates](./zh_mds/simulate-multi-component-templates.md)

配置ignore_missing_component_templates
[Config ignore_missing_component_templates](./zh_mds/ignore_missing_component_templates.md)

使用示例
[Usage example](./zh_mds/_usage_example.md)

数据流
[Data streams](./zh_mds/data-streams.md)

设置数据流
[Set up a data stream](./zh_mds/set-up-a-data-stream.md)

使用数据流
[Use a data stream](./zh_mds/use-a-data-stream.md)

修改数据流
[Modify a data stream](./zh_mds/modify-data-streams.md)

时序数据流 （TSDS）
[Time series data stream (TSDS)](./zh_mds/tsds.md)

设置 TSDS
[Set up a TSDS](./zh_mds/set-up-tsds.md)

时序索引设置
[Time series index settings](./zh_mds/tsds-index-settings.md)

对时序数据流进行降采样
[Downsampling a time series data stream](./zh_mds/downsampling.md)

使用 ILM 运行缩减采样
[Run downsampling with ILM](./zh_mds/downsampling-ilm.md)

手动运行缩减采样
[Run downsampling manually](./zh_mds/downsampling-manual.md)

引入管道
[Ingest pipelines](./zh_mds/ingest.md)

示例：分析日志
[Example: Parse logs](./zh_mds/common-log-format-example.md)

丰富您的数据
[Enrich your data](./zh_mds/ingest-enriching-data.md)

设置扩充处理器
[Set up an enrich processor](./zh_mds/enrich-setup.md)

示例：根据地理位置丰富数据
[Example: Enrich your data based on geolocation](./zh_mds/geo-match-enrich-policy-type.md)

示例：根据精确值丰富数据
[Example: Enrich your data based on exact values](./zh_mds/match-enrich-policy-type.md)

示例：通过将值与区域匹配来丰富数据
[Example: Enrich your data by matching a value to a range](./zh_mds/range-enrich-policy-type.md)

处理器参考
[Processor reference](./zh_mds/processors.md)

附加
[Append](./zh_mds/append-processor.md)

附件
[Attachment](./zh_mds/attachment.md)

字节
[Bytes](./zh_mds/bytes-processor.md)

圈
[Circle](./zh_mds/ingest-circle-processor.md)

社区标识
[Community ID](./zh_mds/community-id-processor.md)

转换
[Convert](./zh_mds/convert-processor.md)

.CSV
[CSV](./zh_mds/csv-processor.md)

日期
[Date](./zh_mds/date-processor.md)

日期索引名称
[Date index name](./zh_mds/date-index-name-processor.md)

解剖
[Dissect](./zh_mds/dissect-processor.md)

点扩展器
[Dot expander](./zh_mds/dot-expand-processor.md)

落
[Drop](./zh_mds/drop-processor.md)

丰富
[Enrich](./zh_mds/enrich-processor.md)

失败
[Fail](./zh_mds/fail-processor.md)

指纹
[Fingerprint](./zh_mds/fingerprint-processor.md)

福里奇
[Foreach](./zh_mds/foreach-processor.md)

土工格栅
[Geo-grid](./zh_mds/ingest-geo-grid-processor.md)

地理知识产权
[GeoIP](./zh_mds/geoip-processor.md)

格罗克
[Grok](./zh_mds/grok-processor.md)

格苏比
[Gsub](./zh_mds/gsub-processor.md)

网页条
[HTML strip](./zh_mds/htmlstrip-processor.md)

推理
[Inference](./zh_mds/inference-processor.md)

加入
[Join](./zh_mds/join-processor.md)

杰伦
[JSON](./zh_mds/json-processor.md)

千伏
[KV](./zh_mds/kv-processor.md)

小写
[Lowercase](./zh_mds/lowercase-processor.md)

网络方向
[Network direction](./zh_mds/network-direction-processor.md)

管道
[Pipeline](./zh_mds/pipeline-processor.md)

编辑
[Redact](./zh_mds/redact-processor.md)

注册域名
[Registered domain](./zh_mds/registered-domain-processor.md)

删除
[Remove](./zh_mds/remove-processor.md)

重命名
[Rename](./zh_mds/rename-processor.md)

重新路由
[Reroute](./zh_mds/reroute-processor.md)

脚本
[Script](./zh_mds/script-processor.md)

设置
[Set](./zh_mds/set-processor.md)

设置安全用户
[Set security user](./zh_mds/ingest-node-set-security-user-processor.md)

排序
[Sort](./zh_mds/sort-processor.md)

分裂
[Split](./zh_mds/split-processor.md)

修剪
[Trim](./zh_mds/trim-processor.md)

大写
[Uppercase](./zh_mds/uppercase-processor.md)

网址解码
[URL decode](./zh_mds/urldecode-processor.md)

URI 部件
[URI parts](./zh_mds/uri-parts-processor.md)

用户代理
[User agent](./zh_mds/user-agent-processor.md)

别名
[Aliases](./zh_mds/aliases.md)

搜索您的数据
[Search your data](./zh_mds/search-your-data.md)

折叠搜索结果
[Collapse search results](./zh_mds/collapse-search-results.md)

筛选搜索结果
[Filter search results](./zh_mds/filter-search-results.md)

突出
[Highlighting](./zh_mds/highlighting.md)

长时间运行的搜索
[Long-running searches](./zh_mds/async-search-intro.md)

近乎实时的搜索
[Near real-time search](./zh_mds/near-real-time.md)

对搜索结果进行分页
[Paginate search results](./zh_mds/paginate-search-results.md)

检索内部命中
[Retrieve inner hits](./zh_mds/inner-hits.md)

检索所选字段
[Retrieve selected fields](./zh_mds/search-fields.md)

跨群集搜索
[Search across clusters](./zh_mds/modules-cross-cluster-search.md)

搜索多个数据流和索引
[Search multiple data streams and indices](./zh_mds/search-multiple-indices.md)

搜索分片路由
[Search shard routing](./zh_mds/search-shard-routing.md)

搜索模板
[Search templates](./zh_mds/search-template.md)

使用小胡子搜索模板示例
[Search template examples with Mustache](./zh_mds/search-template-with-mustache-examples.md)

对搜索结果进行排序
[Sort search results](./zh_mds/sort-search-results.md)

kNN 搜索
[kNN search](./zh_mds/knn-search.md)

语义搜索
[Semantic search](./zh_mds/semantic-search.md)

使用 ELSER 进行语义搜索
[Semantic search with ELSER](./zh_mds/semantic-search-elser.md)

查询 DSL
[Query DSL](./zh_mds/query-dsl.md)

查询和筛选上下文
[Query and filter context](./zh_mds/query-filter-context.md)

复合查询
[Compound queries](./zh_mds/compound-queries.md)

布尔
[Boolean](./zh_mds/query-dsl-bool-query.md)

提高
[Boosting](./zh_mds/query-dsl-boosting-query.md)

常量分数
[Constant score](./zh_mds/query-dsl-constant-score-query.md)

最大析取
[Disjunction max](./zh_mds/query-dsl-dis-max-query.md)

函数得分
[Function score](./zh_mds/query-dsl-function-score-query.md)

全文查询
[Full text queries](./zh_mds/full-text-queries.md)

间隔
[Intervals](./zh_mds/query-dsl-intervals-query.md)

火柴
[Match](./zh_mds/query-dsl-match-query.md)

匹配布尔前缀
[Match boolean prefix](./zh_mds/query-dsl-match-bool-prefix-query.md)

匹配短语
[Match phrase](./zh_mds/query-dsl-match-query-phrase.md)

匹配短语前缀
[Match phrase prefix](./zh_mds/query-dsl-match-query-phrase-prefix.md)

合并字段
[Combined fields](./zh_mds/query-dsl-combined-fields-query.md)

多匹配
[Multi-match](./zh_mds/query-dsl-multi-match-query.md)

查询字符串
[Query string](./zh_mds/query-dsl-query-string-query.md)

简单查询字符串
[Simple query string](./zh_mds/query-dsl-simple-query-string-query.md)

地理查询
[Geo queries](./zh_mds/geo-queries.md)

地理边界框
[Geo-bounding box](./zh_mds/query-dsl-geo-bounding-box-query.md)

地理距离
[Geo-distance](./zh_mds/query-dsl-geo-distance-query.md)

土工格栅
[Geo-grid](./zh_mds/query-dsl-geo-grid-query.md)

地理多边形
[Geo-polygon](./zh_mds/query-dsl-geo-polygon-query.md)

地形
[Geoshape](./zh_mds/query-dsl-geo-shape-query.md)

形状查询
[Shape queries](./zh_mds/shape-queries.md)

形状
[Shape](./zh_mds/query-dsl-shape-query.md)

联接查询
[Joining queries](./zh_mds/joining-queries.md)

嵌 套
[Nested](./zh_mds/query-dsl-nested-query.md)

有孩子
[Has child](./zh_mds/query-dsl-has-child-query.md)

有父级
[Has parent](./zh_mds/query-dsl-has-parent-query.md)

家长编号
[Parent ID](./zh_mds/query-dsl-parent-id-query.md)

全部匹配
[Match all](./zh_mds/query-dsl-match-all-query.md)

跨度查询
[Span queries](./zh_mds/span-queries.md)

跨度包含
[Span containing](./zh_mds/query-dsl-span-containing-query.md)

跨度场掩码
[Span field masking](./zh_mds/query-dsl-span-field-masking-query.md)

跨度优先
[Span first](./zh_mds/query-dsl-span-first-query.md)

跨度多期限
[Span multi-term](./zh_mds/query-dsl-span-multi-term-query.md)

跨度近
[Span near](./zh_mds/query-dsl-span-near-query.md)

跨度不
[Span not](./zh_mds/query-dsl-span-not-query.md)

跨度或
[Span or](./zh_mds/query-dsl-span-or-query.md)

跨度项
[Span term](./zh_mds/query-dsl-span-term-query.md)

跨度在内
[Span within](./zh_mds/query-dsl-span-within-query.md)

专业查询
[Specialized queries](./zh_mds/specialized-queries.md)

距离功能
[Distance feature](./zh_mds/query-dsl-distance-feature-query.md)

更多类似内容
[More like this](./zh_mds/query-dsl-mlt-query.md)

渗 滤液
[Percolate](./zh_mds/query-dsl-percolate-query.md)

排名功能
[Rank feature](./zh_mds/query-dsl-rank-feature-query.md)

脚本
[Script](./zh_mds/query-dsl-script-query.md)

脚本分数
[Script score](./zh_mds/query-dsl-script-score-query.md)

包装纸
[Wrapper](./zh_mds/query-dsl-wrapper-query.md)

固定查询
[Pinned Query](./zh_mds/query-dsl-pinned-query.md)

术语级查询
[Term-level queries](./zh_mds/term-level-queries.md)

存在
[Exists](./zh_mds/query-dsl-exists-query.md)

模糊
[Fuzzy](./zh_mds/query-dsl-fuzzy-query.md)

京东
[IDs](./zh_mds/query-dsl-ids-query.md)

前缀
[Prefix](./zh_mds/query-dsl-prefix-query.md)

范围
[Range](./zh_mds/query-dsl-range-query.md)

正则表达式
[Regexp](./zh_mds/query-dsl-regexp-query.md)

术语
[Term](./zh_mds/query-dsl-term-query.md)

条款
[Terms](./zh_mds/query-dsl-terms-query.md)

术语集
[Terms set](./zh_mds/query-dsl-terms-set-query.md)

通配符
[Wildcard](./zh_mds/query-dsl-wildcard-query.md)

文本扩展
[Text expansion](./zh_mds/query-dsl-text-expansion-query.md)

minimum_should_match参数
[minimum_should_match parameter](./zh_mds/query-dsl-minimum-should-match.md)

重写参数
[rewrite parameter](./zh_mds/query-dsl-multi-term-rewrite.md)

正则表达式语法
[Regular expression syntax](./zh_mds/regexp-syntax.md)

聚合
[Aggregations](./zh_mds/search-aggregations.md)

存储桶聚合
[Bucket aggregations](./zh_mds/search-aggregations-bucket.md)

邻接矩阵
[Adjacency matrix](./zh_mds/search-aggregations-bucket-adjacency-matrix-aggregation.md)

自动间隔日期直方图
[Auto-interval date histogram](./zh_mds/search-aggregations-bucket-autodatehistogram-aggregation.md)

对文本进行分类
[Categorize text](./zh_mds/search-aggregations-bucket-categorize-text-aggregation.md)

孩子
[Children](./zh_mds/search-aggregations-bucket-children-aggregation.md)

复合
[Composite](./zh_mds/search-aggregations-bucket-composite-aggregation.md)

日期直方图
[Date histogram](./zh_mds/search-aggregations-bucket-datehistogram-aggregation.md)

日期范围
[Date range](./zh_mds/search-aggregations-bucket-daterange-aggregation.md)

多样化的采样器
[Diversified sampler](./zh_mds/search-aggregations-bucket-diversified-sampler-aggregation.md)

滤波器
[Filter](./zh_mds/search-aggregations-bucket-filter-aggregation.md)

过滤 器
[Filters](./zh_mds/search-aggregations-bucket-filters-aggregation.md)

常用项目集
[Frequent item sets](./zh_mds/search-aggregations-bucket-frequent-item-sets-aggregation.md)

地理距离
[Geo-distance](./zh_mds/search-aggregations-bucket-geodistance-aggregation.md)

地理哈希网格
[Geohash grid](./zh_mds/search-aggregations-bucket-geohashgrid-aggregation.md)

地理六角网格
[Geohex grid](./zh_mds/search-aggregations-bucket-geohexgrid-aggregation.md)

地瓦格网
[Geotile grid](./zh_mds/search-aggregations-bucket-geotilegrid-aggregation.md)

全球
[Global](./zh_mds/search-aggregations-bucket-global-aggregation.md)

直方图
[Histogram](./zh_mds/search-aggregations-bucket-histogram-aggregation.md)

IP 前缀
[IP prefix](./zh_mds/search-aggregations-bucket-ipprefix-aggregation.md)

IP 范围
[IP range](./zh_mds/search-aggregations-bucket-iprange-aggregation.md)

失踪
[Missing](./zh_mds/search-aggregations-bucket-missing-aggregation.md)

多术语
[Multi Terms](./zh_mds/search-aggregations-bucket-multi-terms-aggregation.md)

嵌 套
[Nested](./zh_mds/search-aggregations-bucket-nested-aggregation.md)

父母
[Parent](./zh_mds/search-aggregations-bucket-parent-aggregation.md)

随机采样器
[Random sampler](./zh_mds/search-aggregations-random-sampler-aggregation.md)

范围
[Range](./zh_mds/search-aggregations-bucket-range-aggregation.md)

稀有术语
[Rare terms](./zh_mds/search-aggregations-bucket-rare-terms-aggregation.md)

反向嵌套
[Reverse nested](./zh_mds/search-aggregations-bucket-reverse-nested-aggregation.md)

采样
[Sampler](./zh_mds/search-aggregations-bucket-sampler-aggregation.md)

重要术语
[Significant terms](./zh_mds/search-aggregations-bucket-significantterms-aggregation.md)

重要文本
[Significant text](./zh_mds/search-aggregations-bucket-significanttext-aggregation.md)

条款
[Terms](./zh_mds/search-aggregations-bucket-terms-aggregation.md)

时间序列
[Time series](./zh_mds/search-aggregations-bucket-time-series-aggregation.md)

可变宽度直方图
[Variable width histogram](./zh_mds/search-aggregations-bucket-variablewidthhistogram-aggregation.md)

分桶范围字段的细微之处
[Subtleties of bucketing range fields](./zh_mds/search-aggregations-bucket-range-field-note.md)

指标聚合
[Metrics aggregations](./zh_mds/search-aggregations-metrics.md)

平均
[Avg](./zh_mds/search-aggregations-metrics-avg-aggregation.md)

箱线图
[Boxplot](./zh_mds/search-aggregations-metrics-boxplot-aggregation.md)

基数
[Cardinality](./zh_mds/search-aggregations-metrics-cardinality-aggregation.md)

扩展统计信息
[Extended stats](./zh_mds/search-aggregations-metrics-extendedstats-aggregation.md)

地理边界
[Geo-bounds](./zh_mds/search-aggregations-metrics-geobounds-aggregation.md)

地心
[Geo-centroid](./zh_mds/search-aggregations-metrics-geocentroid-aggregation.md)

地理线
[Geo-line](./zh_mds/search-aggregations-metrics-geo-line.md)

笛卡尔边界
[Cartesian-bounds](./zh_mds/search-aggregations-metrics-cartesian-bounds-aggregation.md)

笛卡尔质心
[Cartesian-centroid](./zh_mds/search-aggregations-metrics-cartesian-centroid-aggregation.md)

矩阵统计
[Matrix stats](./zh_mds/search-aggregations-matrix-stats-aggregation.md)

麦克斯
[Max](./zh_mds/search-aggregations-metrics-max-aggregation.md)

中位数绝对偏差
[Median absolute deviation](./zh_mds/search-aggregations-metrics-median-absolute-deviation-aggregation.md)

最小值
[Min](./zh_mds/search-aggregations-metrics-min-aggregation.md)

百分位等级
[Percentile ranks](./zh_mds/search-aggregations-metrics-percentile-rank-aggregation.md)

百分位数
[Percentiles](./zh_mds/search-aggregations-metrics-percentile-aggregation.md)

率
[Rate](./zh_mds/search-aggregations-metrics-rate-aggregation.md)

脚本化指标
[Scripted metric](./zh_mds/search-aggregations-metrics-scripted-metric-aggregation.md)

统计
[Stats](./zh_mds/search-aggregations-metrics-stats-aggregation.md)

字符串统计信息
[String stats](./zh_mds/search-aggregations-metrics-string-stats-aggregation.md)

和
[Sum](./zh_mds/search-aggregations-metrics-sum-aggregation.md)

T 检验
[T-test](./zh_mds/search-aggregations-metrics-ttest-aggregation.md)

热门歌曲
[Top hits](./zh_mds/search-aggregations-metrics-top-hits-aggregation.md)

热门指标
[Top metrics](./zh_mds/search-aggregations-metrics-top-metrics.md)

值计数
[Value count](./zh_mds/search-aggregations-metrics-valuecount-aggregation.md)

加权平均
[Weighted avg](./zh_mds/search-aggregations-metrics-weight-avg-aggregation.md)

管道聚合
[Pipeline aggregations](./zh_mds/search-aggregations-pipeline.md)

平均桶数
[Average bucket](./zh_mds/search-aggregations-pipeline-avg-bucket-aggregation.md)

存储桶脚本
[Bucket script](./zh_mds/search-aggregations-pipeline-bucket-script-aggregation.md)

铲斗计数 K-S 测试
[Bucket count K-S test](./zh_mds/search-aggregations-bucket-count-ks-test-aggregation.md)

存储桶关联
[Bucket correlation](./zh_mds/search-aggregations-bucket-correlation-aggregation.md)

存储桶选择器
[Bucket selector](./zh_mds/search-aggregations-pipeline-bucket-selector-aggregation.md)

存储桶排序
[Bucket sort](./zh_mds/search-aggregations-pipeline-bucket-sort-aggregation.md)

更改点
[Change point](./zh_mds/search-aggregations-change-point-aggregation.md)

累积基数
[Cumulative cardinality](./zh_mds/search-aggregations-pipeline-cumulative-cardinality-aggregation.md)

累计总和
[Cumulative sum](./zh_mds/search-aggregations-pipeline-cumulative-sum-aggregation.md)

导数
[Derivative](./zh_mds/search-aggregations-pipeline-derivative-aggregation.md)

扩展统计信息存储桶
[Extended stats bucket](./zh_mds/search-aggregations-pipeline-extended-stats-bucket-aggregation.md)

推理桶
[Inference bucket](./zh_mds/search-aggregations-pipeline-inference-bucket-aggregation.md)

最大铲斗数
[Max bucket](./zh_mds/search-aggregations-pipeline-max-bucket-aggregation.md)

最小铲斗
[Min bucket](./zh_mds/search-aggregations-pipeline-min-bucket-aggregation.md)

移动功能
[Moving function](./zh_mds/search-aggregations-pipeline-movfn-aggregation.md)

移动百分位数
[Moving percentiles](./zh_mds/search-aggregations-pipeline-moving-percentiles-aggregation.md)

正常化
[Normalize](./zh_mds/search-aggregations-pipeline-normalize-aggregation.md)

百分位数桶
[Percentiles bucket](./zh_mds/search-aggregations-pipeline-percentiles-bucket-aggregation.md)

串行差分
[Serial differencing](./zh_mds/search-aggregations-pipeline-serialdiff-aggregation.md)

统计信息存储桶
[Stats bucket](./zh_mds/search-aggregations-pipeline-stats-bucket-aggregation.md)

总和桶
[Sum bucket](./zh_mds/search-aggregations-pipeline-sum-bucket-aggregation.md)

地理空间分析
[Geospatial analysis](./zh_mds/geospatial-analysis.md)

EQL
[EQL](./zh_mds/eql.md)

语法参考
[Syntax reference](./zh_mds/eql-syntax.md)

函数参考
[Function reference](./zh_mds/eql-function-ref.md)

管道参考
[Pipe reference](./zh_mds/eql-pipe-ref.md)

示例：使用 EQL 检测威胁
[Example: Detect threats with EQL](./zh_mds/eql-ex-threat-detection.md)

.SQL
[SQL](./zh_mds/xpack-sql.md)

概述
[Overview](./zh_mds/sql-overview.md)

SQL 入门
[Getting Started with SQL](./zh_mds/sql-getting-started.md)

约定和术语
[Conventions and Terminology](./zh_mds/sql-concepts.md)

跨 SQL 和 Elasticsearch 的映射概念
[Mapping concepts across SQL and Elasticsearch](./zh_mds/_mapping_concepts_across_sql_and_elasticsearch.md)

安全
[Security](./zh_mds/sql-security.md)

SQL REST API
[SQL REST API](./zh_mds/sql-rest.md)

概述
[Overview](./zh_mds/sql-rest-overview.md)

响应数据格式
[Response Data Formats](./zh_mds/sql-rest-format.md)

通过大响应进行分页
[Paginating through a large response](./zh_mds/sql-pagination.md)

使用 Elasticsearch Query DSL 进行过滤
[Filtering using Elasticsearch Query DSL](./zh_mds/sql-rest-filtering.md)

柱状结果
[Columnar results](./zh_mds/sql-rest-columnar.md)

将参数传递给查询
[Passing parameters to a query](./zh_mds/sql-rest-params.md)

使用运行时字段
[Use runtime fields](./zh_mds/sql-runtime-fields.md)

运行异步 SQL 搜索
[Run an async SQL search](./zh_mds/sql-async.md)

SQL 翻译 API
[SQL Translate API](./zh_mds/sql-translate.md)

SQL 命令行界面
[SQL CLI](./zh_mds/sql-cli.md)

SQL JDBC
[SQL JDBC](./zh_mds/sql-jdbc.md)

接口用法
[API usage](./zh_mds/_api_usage.md)

SQL ODBC
[SQL ODBC](./zh_mds/sql-odbc.md)

驱动程序安装
[Driver installation](./zh_mds/sql-odbc-installation.md)

配置
[Configuration](./zh_mds/sql-odbc-setup.md)

SQL 客户端应用程序
[SQL Client Applications](./zh_mds/sql-client-apps.md)

德布弗
[DBeaver](./zh_mds/sql-client-apps-dbeaver.md)

数据库展示台
[DbVisualizer](./zh_mds/sql-client-apps-dbvis.md)

Microsoft Excel
[Microsoft Excel](./zh_mds/sql-client-apps-excel.md)

Microsoft Power BI Desktop
[Microsoft Power BI Desktop](./zh_mds/sql-client-apps-powerbi.md)

Microsoft PowerShell
[Microsoft PowerShell](./zh_mds/sql-client-apps-ps1.md)

微策略桌面
[MicroStrategy Desktop](./zh_mds/sql-client-apps-microstrat.md)

Qlik 感知桌面
[Qlik Sense Desktop](./zh_mds/sql-client-apps-qlik.md)

SQuirreL SQL
[SQuirreL SQL](./zh_mds/sql-client-apps-squirrel.md)

SQL Workbench/J
[SQL Workbench/J](./zh_mds/sql-client-apps-workbench.md)

桌面
[Tableau Desktop](./zh_mds/sql-client-apps-tableau-desktop.md)

Tableau Server
[Tableau Server](./zh_mds/sql-client-apps-tableau-server.md)

SQL 语言
[SQL Language](./zh_mds/sql-spec.md)

词汇结构
[Lexical Structure](./zh_mds/sql-lexical-structure.md)

SQL 命令
[SQL Commands](./zh_mds/sql-commands.md)

描述表
[DESCRIBE TABLE](./zh_mds/sql-syntax-describe-table.md)

选择
[SELECT](./zh_mds/sql-syntax-select.md)

显示目录
[SHOW CATALOGS](./zh_mds/sql-syntax-show-catalogs.md)

显示列
[SHOW COLUMNS](./zh_mds/sql-syntax-show-columns.md)

显示功能
[SHOW FUNCTIONS](./zh_mds/sql-syntax-show-functions.md)

显示表格
[SHOW TABLES](./zh_mds/sql-syntax-show-tables.md)

数据类型
[Data Types](./zh_mds/sql-data-types.md)

索引模式
[Index patterns](./zh_mds/sql-index-patterns.md)

冻结指数
[Frozen Indices](./zh_mds/sql-index-frozen.md)

函数和运算符
[Functions and Operators](./zh_mds/sql-functions.md)

比较运算符
[Comparison Operators](./zh_mds/sql-operators.md)

逻辑运算符
[Logical Operators](./zh_mds/sql-operators-logical.md)

数学运算符
[Math Operators](./zh_mds/sql-operators-math.md)

演员表
[Cast Operators](./zh_mds/sql-operators-cast.md)

喜欢和喜欢运算符
[LIKE and RLIKE Operators](./zh_mds/sql-like-rlike-operators.md)

聚合函数
[Aggregate Functions](./zh_mds/sql-functions-aggs.md)

分组函数
[Grouping Functions](./zh_mds/sql-functions-grouping.md)

日期/时间和间隔函数和运算符
[Date/Time and Interval Functions and Operators](./zh_mds/sql-functions-datetime.md)

全文搜索功能
[Full-Text Search Functions](./zh_mds/sql-functions-search.md)

数学函数
[Mathematical Functions](./zh_mds/sql-functions-math.md)

字符串函数
[String Functions](./zh_mds/sql-functions-string.md)

类型转换函数
[Type Conversion Functions](./zh_mds/sql-functions-type-conversion.md)

地理函数
[Geo Functions](./zh_mds/sql-functions-geo.md)

条件函数和表达式
[Conditional Functions And Expressions](./zh_mds/sql-functions-conditional.md)

系统功能
[System Functions](./zh_mds/sql-functions-system.md)

保留关键字
[Reserved keywords](./zh_mds/sql-syntax-reserved.md)

SQL 限制
[SQL Limitations](./zh_mds/sql-limitations.md)

脚本
[Scripting](./zh_mds/modules-scripting.md)

无痛的脚本语言
[Painless scripting language](./zh_mds/modules-scripting-painless.md)

如何编写脚本
[How to write scripts](./zh_mds/modules-scripting-using.md)

脚本、缓存和搜索速度
[Scripts, caching, and search speed](./zh_mds/scripts-and-search-speed.md)

剖析数据
[Dissecting data](./zh_mds/dissect.md)

格罗克金格罗克
[Grokking grok](./zh_mds/grok.md)

访问文档中的字段
[Access fields in a document](./zh_mds/script-fields-api.md)

常见脚本用例
[Common scripting use cases](./zh_mds/common-script-uses.md)

现场提取
[Field extraction](./zh_mds/scripting-field-extraction.md)

访问文档字段和特殊变量
[Accessing document fields and special variables](./zh_mds/modules-scripting-fields.md)

脚本和安全性
[Scripting and security](./zh_mds/modules-scripting-security.md)

卢塞恩表达式语言
[Lucene expressions language](./zh_mds/modules-scripting-expression.md)

使用脚本引擎的高级脚本
[Advanced scripts using script engines](./zh_mds/modules-scripting-engine.md)

数据管理
[Data management](./zh_mds/data-management.md)

ILM：管理索引生命周期
[ILM: Manage the index lifecycle](./zh_mds/index-lifecycle-management.md)

教程：自定义内置策略
[Tutorial: Customize built-in policies](./zh_mds/example-using-index-lifecycle-policy.md)

教程：自动翻转
[Tutorial: Automate rollover](./zh_mds/getting-started-index-lifecycle-management.md)

Kibana 中的索引管理
[Index management in Kibana](./zh_mds/index-mgmt.md)

概述
[Overview](./zh_mds/overview-index-lifecycle-management.md)

概念
[Concepts](./zh_mds/ilm-concepts.md)

索引生命周期
[Index lifecycle](./zh_mds/ilm-index-lifecycle.md)

过渡
[Rollover](./zh_mds/index-rollover.md)

政策更新
[Policy updates](./zh_mds/update-lifecycle-policy.md)

索引生命周期操作
[Index lifecycle actions](./zh_mds/ilm-actions.md)

分配
[Allocate](./zh_mds/ilm-allocate.md)

删除
[Delete](./zh_mds/ilm-delete.md)

强制合并
[Force merge](./zh_mds/ilm-forcemerge.md)

迁移
[Migrate](./zh_mds/ilm-migrate.md)

只读
[Read only](./zh_mds/ilm-readonly.md)

过渡
[Rollover](./zh_mds/ilm-rollover.md)

下采样
[Downsample](./zh_mds/ilm-downsample.md)

可搜索快照
[Searchable snapshot](./zh_mds/ilm-searchable-snapshot.md)

设置优先级
[Set priority](./zh_mds/ilm-set-priority.md)

收缩
[Shrink](./zh_mds/ilm-shrink.md)

取消关注
[Unfollow](./zh_mds/ilm-unfollow.md)

等待快照
[Wait for snapshot](./zh_mds/ilm-wait-for-snapshot.md)

配置生命周期策略
[Configure a lifecycle policy](./zh_mds/set-up-lifecycle-policy.md)

将索引分配筛选器迁移到节点角色
[Migrate index allocation filters to node roles](./zh_mds/migrate-index-allocation-filters.md)

排查索引生命周期管理错误
[Troubleshooting index lifecycle management errors](./zh_mds/index-lifecycle-error-handling.md)

启动和停止索引生命周期管理
[Start and stop index lifecycle management](./zh_mds/start-stop-ilm.md)

管理现有索引
[Manage existing indices](./zh_mds/ilm-with-existing-indices.md)

跳过翻转
[Skip rollover](./zh_mds/skipping-rollover.md)

还原托管数据流或索引
[Restore a managed data stream or index](./zh_mds/index-lifecycle-and-snapshots.md)

数据层
[Data tiers](./zh_mds/data-tiers.md)

自动缩放
[Autoscaling](./zh_mds/xpack-autoscaling.md)

自动缩放决策程序
[Autoscaling deciders](./zh_mds/autoscaling-deciders.md)

反应式存储决策程序
[Reactive storage decider](./zh_mds/autoscaling-reactive-storage-decider.md)

主动式存储决策程序
[Proactive storage decider](./zh_mds/autoscaling-proactive-storage-decider.md)

冻结分片决策程序
[Frozen shards decider](./zh_mds/autoscaling-frozen-shards-decider.md)

冷冻存储决策程序
[Frozen storage decider](./zh_mds/autoscaling-frozen-storage-decider.md)

冻结存在决定器
[Frozen existence decider](./zh_mds/autoscaling-frozen-existence-decider.md)

机器学习决策程序
[Machine learning decider](./zh_mds/autoscaling-machine-learning-decider.md)

固定决策程序
[Fixed decider](./zh_mds/autoscaling-fixed-decider.md)

监控集群
[Monitor a cluster](./zh_mds/monitor-elasticsearch-cluster.md)

概述
[Overview](./zh_mds/monitoring-overview.md)

工作原理
[How it works](./zh_mds/how-monitoring-works.md)

在生产环境中进行监视
[Monitoring in a production environment](./zh_mds/monitoring-production.md)

使用 Elastic 代理收集监控数据
[Collecting monitoring data with Elastic Agent](./zh_mds/configuring-elastic-agent.md)

使用 Metricbeat 收集监控数据
[Collecting monitoring data with Metricbeat](./zh_mds/configuring-metricbeat.md)

使用 Filebeat 收集日志数据
[Collecting log data with Filebeat](./zh_mds/configuring-filebeat.md)

配置数据流/索引以进行监控
[Configuring data streams/indices for monitoring](./zh_mds/config-monitoring-indices.md)

配置弹性代理创建的数据流
[Configuring data streams created by Elastic Agent](./zh_mds/config-monitoring-data-streams-elastic-agent.md)

配置由 Metricbeat 8 创建的数据流
[Configuring data streams created by Metricbeat 8](./zh_mds/config-monitoring-data-streams-metricbeat-8.md)

配置由 Metricbeat 7 或内部集合创建的索引
[Configuring indices created by Metricbeat 7 or internal collection](./zh_mds/config-monitoring-indices-metricbeat-7-internal-collection.md)

旧版收集方法
[Legacy collection methods](./zh_mds/collecting-monitoring-data.md)

收藏家
[Collectors](./zh_mds/es-monitoring-collectors.md)

出口商
[Exporters](./zh_mds/es-monitoring-exporters.md)

本地出口商
[Local exporters](./zh_mds/local-exporter.md)

HTTP 导出器
[HTTP exporters](./zh_mds/http-exporter.md)

暂停数据收集
[Pausing data collection](./zh_mds/pause-export.md)

汇总或转换数据
[Roll up or transform your data](./zh_mds/data-rollup-transform.md)

汇总历史数据
[Rolling up historical data](./zh_mds/xpack-rollup.md)

概述
[Overview](./zh_mds/rollup-overview.md)

接口快速参考
[API quick reference](./zh_mds/rollup-api-quickref.md)

开始
[Getting started](./zh_mds/rollup-getting-started.md)

了解组
[Understanding groups](./zh_mds/rollup-understanding-groups.md)

汇总聚合限制
[Rollup aggregation limitations](./zh_mds/rollup-agg-limitations.md)

汇总搜索限制
[Rollup search limitations](./zh_mds/rollup-search-limitations.md)

转换数据
[Transforming data](./zh_mds/transforms.md)

概述
[Overview](./zh_mds/transform-overview.md)

设置
[Setup](./zh_mds/transform-setup.md)

何时使用转换
[When to use transforms](./zh_mds/transform-usage.md)

为转换生成警报
[Generating alerts for transforms](./zh_mds/transform-alerts.md)

大规模转型
[Transforms at scale](./zh_mds/transform-scale.md)

检查点的工作原理
[How checkpoints work](./zh_mds/transform-checkpoints.md)

接口快速参考
[API quick reference](./zh_mds/transform-api-quickref.md)

教程：转换电子商务示例数据
[Tutorial: Transforming the eCommerce sample data](./zh_mds/ecommerce-transforms.md)

例子
[Examples](./zh_mds/transform-examples.md)

无痛示例
[Painless examples](./zh_mds/transform-painless-examples.md)

局限性
[Limitations](./zh_mds/transform-limitations.md)

设置群集以实现高可用性
[Set up a cluster for high availability](./zh_mds/high-availability.md)

针对弹性进行设计
[Designing for resilience](./zh_mds/high-availability-cluster-design.md)

小型集群中的弹性
[Resilience in small clusters](./zh_mds/high-availability-cluster-small-clusters.md)

较大集群中的复原能力
[Resilience in larger clusters](./zh_mds/high-availability-cluster-design-large-clusters.md)

跨集群复制
[Cross-cluster replication](./zh_mds/xpack-ccr.md)

设置跨集群复制
[Set up cross-cluster replication](./zh_mds/ccr-getting-started-tutorial.md)

管理跨集群复制
[Manage cross-cluster replication](./zh_mds/ccr-managing.md)

管理自动关注模式
[Manage auto-follow patterns](./zh_mds/ccr-auto-follow.md)

升级集群
[Upgrading clusters](./zh_mds/ccr-upgrading.md)

单向容灾
[Uni-directional disaster recovery](./zh_mds/ccr-disaster-recovery-uni-directional-tutorial.md)

双向灾难恢复
[Bi-directional disaster recovery](./zh_mds/ccr-disaster-recovery-bi-directional-tutorial.md)

快照和还原
[Snapshot and restore](./zh_mds/snapshot-restore.md)

注册存储库
[Register a repository](./zh_mds/snapshots-register-repository.md)

Azure 存储库
[Azure repository](./zh_mds/repository-azure.md)

谷歌云存储存储库
[Google Cloud Storage repository](./zh_mds/repository-gcs.md)

S3 存储库
[S3 repository](./zh_mds/repository-s3.md)

共享文件系统存储库
[Shared file system repository](./zh_mds/snapshots-filesystem-repository.md)

只读网址存储库
[Read-only URL repository](./zh_mds/snapshots-read-only-repository.md)

仅源存储库
[Source-only repository](./zh_mds/snapshots-source-only-repository.md)

创建快照
[Create a snapshot](./zh_mds/snapshots-take-snapshot.md)

恢复快照
[Restore a snapshot](./zh_mds/snapshots-restore-snapshot.md)

可搜索的快照
[Searchable snapshots](./zh_mds/searchable-snapshots.md)

保护弹性堆栈
[Secure the Elastic Stack](./zh_mds/secure-cluster.md)

弹性搜索安全原则
[Elasticsearch security principles](./zh_mds/es-security-principles.md)

在自动启用安全性的情况下启动弹性堆栈
[Start the Elastic Stack with security enabled automatically](./zh_mds/configuring-stack-security.md)

手动配置安全性
[Manually configure security](./zh_mds/manually-configure-security.md)

设置最低安全性
[Set up minimal security](./zh_mds/security-minimal-setup.md)

设置基本安全性
[Set up basic security](./zh_mds/security-basic-setup.md)

设置基本安全性以及 HTTPS
[Set up basic security plus HTTPS](./zh_mds/security-basic-setup-https.md)

为本机用户和内置用户设置密码
[Setting passwords for native and built-in users](./zh_mds/change-passwords-native-users.md)

启用密码套件以实现更强的加密
[Enabling cipher suites for stronger encryption](./zh_mds/ciphers.md)

JDK 版本支持的 SSL/TLS 版本
[Supported SSL/TLS versions by JDK version](./zh_mds/jdk-tls-versions.md)

安全文件
[Security files](./zh_mds/security-files.md)

FIPS 140-2
[FIPS 140-2](./zh_mds/fips-140-compliance.md)

更新节点安全证书
[Updating node security certificates](./zh_mds/update-node-certs.md)

使用相同的 CA
[With the same CA](./zh_mds/update-node-certs-same.md)

使用不同的 CA
[With a different CA](./zh_mds/update-node-certs-different.md)

用户身份验证
[User authentication](./zh_mds/setting-up-authentication.md)

内置用户
[Built-in users](./zh_mds/built-in-users.md)

服务帐户
[Service accounts](./zh_mds/service-accounts.md)

内部用户
[Internal users](./zh_mds/internal-users.md)

基于令牌的身份验证服务
[Token-based authentication services](./zh_mds/token-authentication-services.md)

用户配置文件
[User profiles](./zh_mds/user-profile.md)

领域
[Realms](./zh_mds/realms.md)

领域链
[Realm chains](./zh_mds/realm-chains.md)

安全域
[Security domains](./zh_mds/security-domain.md)

活动目录用户身份验证
[Active Directory user authentication](./zh_mds/active-directory-realm.md)

基于文件的用户身份验证
[File-based user authentication](./zh_mds/file-realm.md)

LDAP 用户身份验证
[LDAP user authentication](./zh_mds/ldap-realm.md)

本机用户身份验证
[Native user authentication](./zh_mds/native-realm.md)

OpenID 连接身份验证
[OpenID Connect authentication](./zh_mds/oidc-realm.md)

PKI 用户身份验证
[PKI user authentication](./zh_mds/pki-realm.md)

萨姆勒身份验证
[SAML authentication](./zh_mds/saml-realm.md)

Kerberos 身份验证
[Kerberos authentication](./zh_mds/kerberos-realm.md)

智威汤逊身份验证
[JWT authentication](./zh_mds/jwt-auth-realm.md)

与其他身份验证系统集成
[Integrating with other authentication systems](./zh_mds/custom-realms.md)

启用匿名访问
[Enabling anonymous access](./zh_mds/anonymous-access.md)

在未经身份验证的情况下查找用户
[Looking up users without authentication](./zh_mds/user-lookup.md)

控制用户缓存
[Controlling the user cache](./zh_mds/controlling-user-cache.md)

在弹性堆栈上配置 SAML 单点登录
[Configuring SAML single-sign-on on the Elastic Stack](./zh_mds/saml-guide-stack.md)

使用 OpenID Connect 配置对弹性堆栈的单点登录
[Configuring single sign-on to the Elastic Stack using OpenID Connect](./zh_mds/oidc-guide.md)

用户授权
[User authorization](./zh_mds/authorization.md)

内置角色
[Built-in roles](./zh_mds/built-in-roles.md)

定义角色
[Defining roles](./zh_mds/defining-roles.md)

角色限制
[Role restriction](./zh_mds/role-restriction.md)

安全权限
[Security privileges](./zh_mds/security-privileges.md)

文档级安全性
[Document level security](./zh_mds/document-level-security.md)

字段级安全性
[Field level security](./zh_mds/field-level-security.md)

授予数据流和别名的权限
[Granting privileges for data streams and aliases](./zh_mds/securing-aliases.md)

将用户和组映射到角色
[Mapping users and groups to roles](./zh_mds/mapping-roles.md)

设置字段和文档级别安全性
[Setting up field and document level security](./zh_mds/field-and-document-access-control.md)

代表其他用户提交请求
[Submitting requests on behalf of other users](./zh_mds/run-as-privilege.md)

配置授权委派
[Configuring authorization delegation](./zh_mds/configuring-authorization-delegation.md)

自定义角色和授权
[Customizing roles and authorization](./zh_mds/custom-roles-authorization.md)

启用审核日志记录
[Enable audit logging](./zh_mds/enable-audit-logging.md)

审核事件
[Audit events](./zh_mds/audit-event-types.md)

日志文件审核输出
[Logfile audit output](./zh_mds/audit-log-output.md)

日志文件审核事件忽略策略
[Logfile audit events ignore policies](./zh_mds/audit-log-ignore-policy.md)

审核搜索查询
[Auditing search queries](./zh_mds/auditing-search-queries.md)

使用 IP 过滤限制连接
[Restricting connections with IP filtering](./zh_mds/ip-filtering.md)

保护客户端和集成
[Securing clients and integrations](./zh_mds/security-clients-integrations.md)

HTTP/REST 客户端和安全性
[HTTP/REST clients and security](./zh_mds/http-clients.md)

ES-Hadoop 和安全性
[ES-Hadoop and Security](./zh_mds/hadoop.md)

监控和安全
[Monitoring and security](./zh_mds/secure-monitoring.md)

操作员权限
[Operator privileges](./zh_mds/operator-privileges.md)

配置操作员权限
[Configure operator privileges](./zh_mds/configure-operator-privileges.md)

仅限操作员的功能
[Operator-only functionality](./zh_mds/operator-only-functionality.md)

快照和恢复的操作员权限
[Operator privileges for snapshot and restore](./zh_mds/operator-only-snapshot-and-restore.md)

故障 排除
[Troubleshooting](./zh_mds/security-troubleshooting.md)

某些设置不会通过节点设置 API 返回
[Some settings are not returned via the nodes settings API](./zh_mds/security-trb-settings.md)

授权例外
[Authorization exceptions](./zh_mds/security-trb-roles.md)

用户命令由于额外的参数而失败
[Users command fails due to extra arguments](./zh_mds/security-trb-extraargs.md)

用户经常被锁定在活动目录之外
[Users are frequently locked out of Active Directory](./zh_mds/trouble-shoot-active-directory.md)

Mac 上的 curl 证书验证失败
[Certificate verification fails for curl on Mac](./zh_mds/trb-security-maccurl.md)

SSLHandshakeException导致连接失败
[SSLHandshakeException causes connections to fail](./zh_mds/trb-security-sslhandshake.md)

常见的 SSL/TLS 异常
[Common SSL/TLS exceptions](./zh_mds/trb-security-ssl.md)

常见的 Kerberos 异常
[Common Kerberos exceptions](./zh_mds/trb-security-kerberos.md)

常见的 SAML 问题
[Common SAML issues](./zh_mds/trb-security-saml.md)

Kibana 中的内部服务器错误
[Internal Server Error in Kibana](./zh_mds/trb-security-internalserver.md)

由于连接失败，设置密码命令失败
[Setup-passwords command fails due to connection failure](./zh_mds/trb-security-setup.md)

由于重新定位配置文件而导致的故障
[Failures due to relocation of the configuration files](./zh_mds/trb-security-path.md)

局限性
[Limitations](./zh_mds/security-limitations.md)

观察家
[Watcher](./zh_mds/xpack-alerting.md)

观察者入门
[Getting started with Watcher](./zh_mds/watcher-getting-started.md)

观察程序的工作原理
[How Watcher works](./zh_mds/how-watcher-works.md)

在观察程序中加密敏感数据
[Encrypting sensitive data in Watcher](./zh_mds/encrypting-data.md)

输入
[Inputs](./zh_mds/input.md)

简单输入
[Simple input](./zh_mds/input-simple.md)

搜索输入
[Search input](./zh_mds/input-search.md)

HTTP输入
[HTTP input](./zh_mds/input-http.md)

链输入
[Chain input](./zh_mds/input-chain.md)

触发器
[Triggers](./zh_mds/trigger.md)

计划触发器
[Schedule trigger](./zh_mds/trigger-schedule.md)

条件
[Conditions](./zh_mds/condition.md)

始终状态
[Always condition](./zh_mds/condition-always.md)

从不条件
[Never condition](./zh_mds/condition-never.md)

比较条件
[Compare condition](./zh_mds/condition-compare.md)

数组比较条件
[Array compare condition](./zh_mds/condition-array-compare.md)

脚本条件
[Script condition](./zh_mds/condition-script.md)

行动
[Actions](./zh_mds/actions.md)

为数组中的每个元素运行操作
[Running an action for each element in an array](./zh_mds/action-foreach.md)

向操作添加条件
[Adding conditions to actions](./zh_mds/action-conditions.md)

电子邮件操作
[Email action](./zh_mds/actions-email.md)

网络钩子操作
[Webhook action](./zh_mds/actions-webhook.md)

索引操作
[Index action](./zh_mds/actions-index.md)

日志记录操作
[Logging action](./zh_mds/actions-logging.md)

松弛动作
[Slack action](./zh_mds/actions-slack.md)

寻呼机值班操作
[PagerDuty action](./zh_mds/actions-pagerduty.md)

吉拉行动
[Jira action](./zh_mds/actions-jira.md)

变换
[Transforms](./zh_mds/transform.md)

搜索有效负载转换
[Search payload transform](./zh_mds/transform-search.md)

脚本有效负载转换
[Script payload transform](./zh_mds/transform-script.md)

链有效载荷变换
[Chain payload transform](./zh_mds/transform-chain.md)

管理监视
[Managing watches](./zh_mds/managing-watches.md)

示例手表
[Example watches](./zh_mds/example-watches.md)

观察 Elasticsearch 集群的状态
[Watching the status of an Elasticsearch cluster](./zh_mds/watch-cluster-status.md)

局限性
[Limitations](./zh_mds/watcher-limitations.md)

命令行工具
[Command line tools](./zh_mds/commands.md)

elasticsearch-certgen
[elasticsearch-certgen](./zh_mds/certgen.md)

elasticsearch-certutil
[elasticsearch-certutil](./zh_mds/certutil.md)

弹性搜索-创建-注册-令牌
[elasticsearch-create-enrollment-token](./zh_mds/create-enrollment-token.md)

Elasticsearch-croneval
[elasticsearch-croneval](./zh_mds/elasticsearch-croneval.md)

弹性搜索密钥库
[elasticsearch-keystore](./zh_mds/elasticsearch-keystore.md)

弹性搜索节点
[elasticsearch-node](./zh_mds/node-tool.md)

Elasticsearch-reconfigure-node
[elasticsearch-reconfigure-node](./zh_mds/reconfigure-node.md)

弹性搜索-重置-密码
[elasticsearch-reset-password](./zh_mds/reset-password.md)

elasticsearch-saml-metadata
[elasticsearch-saml-metadata](./zh_mds/saml-metadata.md)

elasticsearch-service-tokens
[elasticsearch-service-tokens](./zh_mds/service-tokens-command.md)

弹性搜索设置密码
[elasticsearch-setup-passwords](./zh_mds/setup-passwords.md)

Elasticsearch-shard
[elasticsearch-shard](./zh_mds/shard-tool.md)

Elasticsearch-syskeygen
[elasticsearch-syskeygen](./zh_mds/syskeygen.md)

弹性搜索用户
[elasticsearch-users](./zh_mds/users-command.md)

如何
[How to](./zh_mds/how-to.md)

一般性建议
[General recommendations](./zh_mds/general-recommendations.md)

食谱
[Recipes](./zh_mds/recipes.md)

将精确搜索与词干提取混合在一起
[Mixing exact search with stemming](./zh_mds/mixing-exact-search-with-stemming.md)

获得一致的评分
[Getting consistent scoring](./zh_mds/consistent-scoring.md)

将静态相关性信号合并到分数中
[Incorporating static relevance signals into the score](./zh_mds/static-scoring-signals.md)

调整索引速度
[Tune for indexing speed](./zh_mds/tune-for-indexing-speed.md)

调整搜索速度
[Tune for search speed](./zh_mds/tune-for-search-speed.md)

调整近似 kNN 搜索
[Tune approximate kNN search](./zh_mds/tune-knn-search.md)

针对磁盘使用情况进行调整
[Tune for disk usage](./zh_mds/tune-for-disk-usage.md)

调整分片大小
[Size your shards](./zh_mds/size-your-shards.md)

使用 Elasticsearch 获取时间序列数据
[Use Elasticsearch for time series data](./zh_mds/use-elasticsearch-for-time-series-data.md)

故障 排除
[Troubleshooting](./zh_mds/troubleshooting.md)

修复常见的集群问题
[Fix common cluster issues](./zh_mds/fix-common-cluster-issues.md)

水印错误
[Watermark errors](./zh_mds/fix-watermark-errors.md)

断路器错误
[Circuit breaker errors](./zh_mds/circuit-breaker-errors.md)

高 CPU 使用率
[High CPU usage](./zh_mds/high-cpu-usage.md)

高 JVM 内存压力
[High JVM memory pressure](./zh_mds/high-jvm-memory-pressure.md)

红色或黄色集群状态
[Red or yellow cluster status](./zh_mds/red-yellow-cluster-status.md)

拒绝的请求
[Rejected requests](./zh_mds/rejected-requests.md)

任务队列积压工作
[Task queue backlog](./zh_mds/task-queue-backlog.md)

映射爆炸
[Mapping explosion](./zh_mds/mapping-explosion.md)

热点
[Hot spotting](./zh_mds/hotspotting.md)

诊断未分配的分片
[Diagnose unassigned shards](./zh_mds/diagnose-unassigned-shards.md)

向系统添加缺少的层
[Add a missing tier to the system](./zh_mds/add-tier.md)

允许 Elasticsearch 分配系统中的数据
[Allow Elasticsearch to allocate the data in the system](./zh_mds/allow-all-cluster-allocation.md)

允许 Elasticsearch 分配索引
[Allow Elasticsearch to allocate the index](./zh_mds/allow-all-index-allocation.md)

索引将索引分配筛选器与数据层节点角色混合在一起，以在数据层中移动
[Indices mix index allocation filters with data tiers node roles to move through data tiers](./zh_mds/troubleshoot-migrate-to-tiers.md)

没有足够的节点来分配所有分片副本
[Not enough nodes to allocate all shard replicas](./zh_mds/increase-tier-capacity.md)

超出单个节点上索引的分片总数
[Total number of shards for an index on a single node exceeded](./zh_mds/increase-shard-limit.md)

已达到每个节点的分片总数
[Total number of shards per node has been reached](./zh_mds/increase-cluster-shard-limit.md)

解决损坏问题
[Troubleshooting corruption](./zh_mds/corruption-troubleshooting.md)

修复磁盘外的数据节点
[Fix data nodes out of disk](./zh_mds/fix-data-node-out-of-disk.md)

增加数据节点的磁盘容量
[Increase the disk capacity of data nodes](./zh_mds/increase-capacity-data-node.md)

降低数据节点的磁盘使用率
[Decrease the disk usage of data nodes](./zh_mds/decrease-disk-usage-data-node.md)

修复主节点磁盘外的问题
[Fix master nodes out of disk](./zh_mds/fix-master-node-out-of-disk.md)

修复磁盘外的其他角色节点
[Fix other role nodes out of disk](./zh_mds/fix-other-node-out-of-disk.md)

启动索引生命周期管理
[Start index lifecycle management](./zh_mds/start-ilm.md)

启动快照生命周期管理
[Start Snapshot Lifecycle Management](./zh_mds/start-slm.md)

从快照还原
[Restore from snapshot](./zh_mds/restore-from-snapshot.md)

写入同一快照存储库的多个部署
[Multiple deployments writing to the same snapshot repository](./zh_mds/add-repository.md)

解决重复的快照策略故障
[Addressing repeated snapshot policy failures](./zh_mds/repeated-snapshot-failures.md)

发现疑难解答
[Troubleshooting discovery](./zh_mds/discovery-troubleshooting.md)

监控疑难解答
[Troubleshooting monitoring](./zh_mds/monitoring-troubleshooting.md)

转换疑难解答
[Troubleshooting transforms](./zh_mds/transform-troubleshooting.md)

观察程序疑难解答
[Troubleshooting Watcher](./zh_mds/watcher-troubleshooting.md)

搜索疑难解答
[Troubleshooting searches](./zh_mds/troubleshooting-searches.md)

排查分片容量运行状况问题
[Troubleshooting shards capacity health issues](./zh_mds/troubleshooting-shards-capacity-issues.md)

休息接口
[REST APIs](./zh_mds/rest-apis.md)

接口约定
[API conventions](./zh_mds/api-conventions.md)

常用选项
[Common options](./zh_mds/common-options.md)

REST API 兼容性
[REST API compatibility](./zh_mds/rest-api-compatibility.md)

自动缩放 API
[Autoscaling APIs](./zh_mds/autoscaling-apis.md)

创建或更新自动缩放策略
[Create or update autoscaling policy](./zh_mds/autoscaling-put-autoscaling-policy.md)

获取自动缩放容量
[Get autoscaling capacity](./zh_mds/autoscaling-get-autoscaling-capacity.md)

删除自动缩放策略
[Delete autoscaling policy](./zh_mds/autoscaling-delete-autoscaling-policy.md)

获取自动缩放策略
[Get autoscaling policy](./zh_mds/autoscaling-get-autoscaling-policy.md)

行为分析接口
[Behavioral Analytics APIs](./zh_mds/behavioral-analytics-apis.md)

放置分析集合
[Put Analytics Collection](./zh_mds/put-analytics-collection.md)

删除分析集合
[Delete Analytics Collection](./zh_mds/delete-analytics-collection.md)

列出分析集合
[List Analytics Collections](./zh_mds/list-analytics-collection.md)

分析后收集事件
[Post Analytics Collection Event](./zh_mds/post-analytics-collection-event.md)

压缩和对齐文本 （CAT） API
[Compact and aligned text (CAT) APIs](./zh_mds/cat.md)

猫别名
[cat aliases](./zh_mds/cat-alias.md)

猫分配
[cat allocation](./zh_mds/cat-allocation.md)

猫异常检测器
[cat anomaly detectors](./zh_mds/cat-anomaly-detectors.md)

猫组件模板
[cat component templates](./zh_mds/cat-component-templates.md)

猫数量
[cat count](./zh_mds/cat-count.md)

猫数据帧分析
[cat data frame analytics](./zh_mds/cat-dfanalytics.md)

猫数据馈送
[cat datafeeds](./zh_mds/cat-datafeeds.md)

猫场数据
[cat fielddata](./zh_mds/cat-fielddata.md)

猫咪健康
[cat health](./zh_mds/cat-health.md)

猫指数
[cat indices](./zh_mds/cat-indices.md)

猫大师
[cat master](./zh_mds/cat-master.md)

猫节点
[cat nodeattrs](./zh_mds/cat-nodeattrs.md)

猫节点
[cat nodes](./zh_mds/cat-nodes.md)

猫待处理任务
[cat pending tasks](./zh_mds/cat-pending-tasks.md)

猫插件
[cat plugins](./zh_mds/cat-plugins.md)

猫恢复
[cat recovery](./zh_mds/cat-recovery.md)

猫存储库
[cat repositories](./zh_mds/cat-repositories.md)

猫段
[cat segments](./zh_mds/cat-segments.md)

猫碎片
[cat shards](./zh_mds/cat-shards.md)

猫快照
[cat snapshots](./zh_mds/cat-snapshots.md)

猫任务管理
[cat task management](./zh_mds/cat-tasks.md)

猫模板
[cat templates](./zh_mds/cat-templates.md)

猫线程池
[cat thread pool](./zh_mds/cat-thread-pool.md)

猫训练模型
[cat trained model](./zh_mds/cat-trained-model.md)

猫变身
[cat transforms](./zh_mds/cat-transforms.md)

集群接口
[Cluster APIs](./zh_mds/cluster.md)

群集分配说明
[Cluster allocation explain](./zh_mds/cluster-allocation-explain.md)

群集获取设置
[Cluster get settings](./zh_mds/cluster-get-settings.md)

群集运行状况
[Cluster health](./zh_mds/cluster-health.md)

健康
[Health](./zh_mds/health-api.md)

群集重新路由
[Cluster reroute](./zh_mds/cluster-reroute.md)

群集状态
[Cluster state](./zh_mds/cluster-state.md)

集群统计信息
[Cluster stats](./zh_mds/cluster-stats.md)

群集更新设置
[Cluster update settings](./zh_mds/cluster-update-settings.md)

节点功能使用情况
[Nodes feature usage](./zh_mds/cluster-nodes-usage.md)

节点热线程
[Nodes hot threads](./zh_mds/cluster-nodes-hot-threads.md)

节点信息
[Nodes info](./zh_mds/cluster-nodes-info.md)

预验证节点删除
[Prevalidate node removal](./zh_mds/prevalidate-node-removal-api.md)

节点重新加载安全设置
[Nodes reload secure settings](./zh_mds/cluster-nodes-reload-secure-settings.md)

节点统计信息
[Nodes stats](./zh_mds/cluster-nodes-stats.md)

集群信息
[Cluster Info](./zh_mds/cluster-info.md)

挂起的群集任务
[Pending cluster tasks](./zh_mds/cluster-pending.md)

远程群集信息
[Remote cluster info](./zh_mds/cluster-remote-info.md)

任务管理
[Task management](./zh_mds/tasks.md)

投票配置排除项
[Voting configuration exclusions](./zh_mds/voting-config-exclusions.md)

创建或更新所需节点
[Create or update desired nodes](./zh_mds/update-desired-nodes.md)

获取所需的节点
[Get desired nodes](./zh_mds/get-desired-nodes.md)

删除所需的节点
[Delete desired nodes](./zh_mds/delete-desired-nodes.md)

获得所需的平衡
[Get desired balance](./zh_mds/get-desired-balance.md)

删除/重置所需余额
[Delete/reset desired balance](./zh_mds/delete-desired-balance.md)

跨集群复制接口
[Cross-cluster replication APIs](./zh_mds/ccr-apis.md)

获取 CCR 统计信息
[Get CCR stats](./zh_mds/ccr-get-stats.md)

创建关注者
[Create follower](./zh_mds/ccr-put-follow.md)

暂停关注者
[Pause follower](./zh_mds/ccr-post-pause-follow.md)

简历关注者
[Resume follower](./zh_mds/ccr-post-resume-follow.md)

取消关注
[Unfollow](./zh_mds/ccr-post-unfollow.md)

忘记追随者
[Forget follower](./zh_mds/ccr-post-forget-follower.md)

获取关注者统计信息
[Get follower stats](./zh_mds/ccr-get-follow-stats.md)

获取关注者信息
[Get follower info](./zh_mds/ccr-get-follow-info.md)

创建自动关注模式
[Create auto-follow pattern](./zh_mds/ccr-put-auto-follow-pattern.md)

删除自动关注模式
[Delete auto-follow pattern](./zh_mds/ccr-delete-auto-follow-pattern.md)

获取自动关注模式
[Get auto-follow pattern](./zh_mds/ccr-get-auto-follow-pattern.md)

暂停自动关注模式
[Pause auto-follow pattern](./zh_mds/ccr-pause-auto-follow-pattern.md)

恢复自动关注模式
[Resume auto-follow pattern](./zh_mds/ccr-resume-auto-follow-pattern.md)

数据流接口
[Data stream APIs](./zh_mds/data-stream-apis.md)

创建数据流
[Create data stream](./zh_mds/indices-create-data-stream.md)

删除数据流
[Delete data stream](./zh_mds/indices-delete-data-stream.md)

获取数据流
[Get data stream](./zh_mds/indices-get-data-stream.md)

迁移到数据流
[Migrate to data stream](./zh_mds/indices-migrate-to-data-stream.md)

数据流统计信息
[Data stream stats](./zh_mds/data-stream-stats-api.md)

提升数据流
[Promote data stream](./zh_mds/promote-data-stream-api.md)

修改数据流
[Modify data streams](./zh_mds/modify-data-streams-api.md)

下采样
[Downsample](./zh_mds/indices-downsample-data-stream.md)

文档接口
[Document APIs](./zh_mds/docs.md)

阅读和写入文档
[Reading and Writing documents](./zh_mds/docs-replication.md)

指数
[Index](./zh_mds/docs-index_.md)

获取
[Get](./zh_mds/docs-get.md)

删除
[Delete](./zh_mds/docs-delete.md)

按查询删除
[Delete by query](./zh_mds/docs-delete-by-query.md)

更新
[Update](./zh_mds/docs-update.md)

按查询更新
[Update by query](./zh_mds/docs-update-by-query.md)

多重获取
[Multi get](./zh_mds/docs-multi-get.md)

散装
[Bulk](./zh_mds/docs-bulk.md)

重新索引
[Reindex](./zh_mds/docs-reindex.md)

术语向量
[Term vectors](./zh_mds/docs-termvectors.md)

多项向量
[Multi term vectors](./zh_mds/docs-multi-termvectors.md)

？刷新
[?refresh](./zh_mds/docs-refresh.md)

乐观并发控制
[Optimistic concurrency control](./zh_mds/optimistic-concurrency-control.md)

丰富接口
[Enrich APIs](./zh_mds/enrich-apis.md)

创建扩充策略
[Create enrich policy](./zh_mds/put-enrich-policy-api.md)

删除扩充策略
[Delete enrich policy](./zh_mds/delete-enrich-policy-api.md)

获取扩充策略
[Get enrich policy](./zh_mds/get-enrich-policy-api.md)

执行扩充策略
[Execute enrich policy](./zh_mds/execute-enrich-policy-api.md)

丰富统计数据
[Enrich stats](./zh_mds/enrich-stats-api.md)

均衡器接口
[EQL APIs](./zh_mds/eql-apis.md)

删除异步 EQL 搜索
[Delete async EQL search](./zh_mds/delete-async-eql-search-api.md)

EQL 搜索
[EQL search](./zh_mds/eql-search-api.md)

获取异步 EQL 搜索
[Get async EQL search](./zh_mds/get-async-eql-search-api.md)

获取异步 EQL 搜索状态
[Get async EQL search status](./zh_mds/get-async-eql-status-api.md)

功能接口
[Features APIs](./zh_mds/features-apis.md)

获取功能
[Get features](./zh_mds/get-features-api.md)

重置功能
[Reset features](./zh_mds/reset-features-api.md)

队列接口
[Fleet APIs](./zh_mds/fleet-apis.md)

获取全局检查点
[Get global checkpoints](./zh_mds/get-global-checkpoints.md)

机队搜索
[Fleet search](./zh_mds/fleet-search.md)

机队搜索
[Fleet search](./zh_mds/fleet-multi-search.md)

查找结构接口
[Find structure API](./zh_mds/find-structure.md)

图形探索 API
[Graph explore API](./zh_mds/graph-explore-api.md)

索引接口
[Index APIs](./zh_mds/indices.md)

存在别名
[Alias exists](./zh_mds/indices-alias-exists.md)

别名
[Aliases](./zh_mds/indices-aliases.md)

分析
[Analyze](./zh_mds/indices-analyze.md)

分析索引磁盘使用情况
[Analyze index disk usage](./zh_mds/indices-disk-usage.md)

清除缓存
[Clear cache](./zh_mds/indices-clearcache.md)

克隆索引
[Clone index](./zh_mds/indices-clone-index.md)

收盘指数
[Close index](./zh_mds/indices-close.md)

创建索引
[Create index](./zh_mds/indices-create-index.md)

创建或更新别名
[Create or update alias](./zh_mds/indices-add-alias.md)

创建或更新组件模板
[Create or update component template](./zh_mds/indices-component-template.md)

创建或更新索引模板
[Create or update index template](./zh_mds/indices-put-template.md)

创建或更新索引模板（旧版）
[Create or update index template (legacy)](./zh_mds/indices-templates-v1.md)

删除组件模板
[Delete component template](./zh_mds/indices-delete-component-template.md)

删除悬空索引
[Delete dangling index](./zh_mds/dangling-index-delete.md)

删除别名
[Delete alias](./zh_mds/indices-delete-alias.md)

删除索引
[Delete index](./zh_mds/indices-delete-index.md)

删除索引模板
[Delete index template](./zh_mds/indices-delete-template.md)

删除索引模板（旧版）
[Delete index template (legacy)](./zh_mds/indices-delete-template-v1.md)

存在
[Exists](./zh_mds/indices-exists.md)

字段使用情况统计信息
[Field usage stats](./zh_mds/field-usage-stats.md)

冲洗
[Flush](./zh_mds/indices-flush.md)

强制合并
[Force merge](./zh_mds/indices-forcemerge.md)

获取别名
[Get alias](./zh_mds/indices-get-alias.md)

获取组件模板
[Get component template](./zh_mds/getting-component-templates.md)

获取字段映射
[Get field mapping](./zh_mds/indices-get-field-mapping.md)

获取索引
[Get index](./zh_mds/indices-get-index.md)

获取索引设置
[Get index settings](./zh_mds/indices-get-settings.md)

获取索引模板
[Get index template](./zh_mds/indices-get-template.md)

获取索引模板（旧版）
[Get index template (legacy)](./zh_mds/indices-get-template-v1.md)

获取映射
[Get mapping](./zh_mds/indices-get-mapping.md)

进口悬空指数
[Import dangling index](./zh_mds/dangling-index-import.md)

索引恢复
[Index recovery](./zh_mds/indices-recovery.md)

索引段
[Index segments](./zh_mds/indices-segments.md)

索引分片存储
[Index shard stores](./zh_mds/indices-shards-stores.md)

指数统计
[Index stats](./zh_mds/indices-stats.md)

索引模板存在（旧版）
[Index template exists (legacy)](./zh_mds/indices-template-exists-v1.md)

列出悬空索引
[List dangling indices](./zh_mds/dangling-indices-list.md)

打开索引
[Open index](./zh_mds/indices-open-close.md)

刷新
[Refresh](./zh_mds/indices-refresh.md)

解析索引
[Resolve index](./zh_mds/indices-resolve-index-api.md)

过渡
[Rollover](./zh_mds/indices-rollover-index.md)

收缩指数
[Shrink index](./zh_mds/indices-shrink-index.md)

模拟索引
[Simulate index](./zh_mds/indices-simulate-index.md)

模拟模板
[Simulate template](./zh_mds/indices-simulate-template.md)

拆分索引
[Split index](./zh_mds/indices-split-index.md)

解冻索引
[Unfreeze index](./zh_mds/unfreeze-index-api.md)

更新索引设置
[Update index settings](./zh_mds/indices-update-settings.md)

更新映射
[Update mapping](./zh_mds/indices-put-mapping.md)

索引生命周期管理 API
[Index lifecycle management APIs](./zh_mds/index-lifecycle-management-api.md)

创建或更新生命周期策略
[Create or update lifecycle policy](./zh_mds/ilm-put-lifecycle.md)

获取策略
[Get policy](./zh_mds/ilm-get-lifecycle.md)

删除策略
[Delete policy](./zh_mds/ilm-delete-lifecycle.md)

移至步骤
[Move to step](./zh_mds/ilm-move-to-step.md)

删除策略
[Remove policy](./zh_mds/ilm-remove-policy.md)

重试策略
[Retry policy](./zh_mds/ilm-retry-policy.md)

获取索引生命周期管理状态
[Get index lifecycle management status](./zh_mds/ilm-get-status.md)

解释生命周期
[Explain lifecycle](./zh_mds/ilm-explain-lifecycle.md)

启动索引生命周期管理
[Start index lifecycle management](./zh_mds/ilm-start.md)

停止索引生命周期管理
[Stop index lifecycle management](./zh_mds/ilm-stop.md)

将索引、ILM 策略以及旧版、可组合模板和组件模板迁移到数据层路由
[Migrate indices, ILM policies, and legacy, composable and component templates to data tiers routing](./zh_mds/ilm-migrate-to-data-tiers.md)

摄取 API
[Ingest APIs](./zh_mds/ingest-apis.md)

创建或更新管道
[Create or update pipeline](./zh_mds/put-pipeline-api.md)

删除管道
[Delete pipeline](./zh_mds/delete-pipeline-api.md)

地理IP统计
[GeoIP stats](./zh_mds/geoip-stats-api.md)

获取管道
[Get pipeline](./zh_mds/get-pipeline-api.md)

模拟管道
[Simulate pipeline](./zh_mds/simulate-pipeline-api.md)

信息接口
[Info API](./zh_mds/info-api.md)

许可接口
[Licensing APIs](./zh_mds/licensing-apis.md)

删除许可证
[Delete license](./zh_mds/delete-license.md)

获取许可证
[Get license](./zh_mds/get-license.md)

获取试用状态
[Get trial status](./zh_mds/get-trial-status.md)

开始试用
[Start trial](./zh_mds/start-trial.md)

获取基本状态
[Get basic status](./zh_mds/get-basic-status.md)

从基本开始
[Start basic](./zh_mds/start-basic.md)

更新许可证
[Update license](./zh_mds/update-license.md)

日志存储 API
[Logstash APIs](./zh_mds/logstash-apis.md)

创建或更新日志存储管道
[Create or update Logstash pipeline](./zh_mds/logstash-api-put-pipeline.md)

删除日志存储管道
[Delete Logstash pipeline](./zh_mds/logstash-api-delete-pipeline.md)

获取日志存储管道
[Get Logstash pipeline](./zh_mds/logstash-api-get-pipeline.md)

机器学习接口
[Machine learning APIs](./zh_mds/ml-apis.md)

获取机器学习信息
[Get machine learning info](./zh_mds/get-ml-info.md)

获取机器学习内存统计信息
[Get machine learning memory stats](./zh_mds/get-ml-memory.md)

设置升级模式
[Set upgrade mode](./zh_mds/ml-set-upgrade-mode.md)

机器学习异常检测 API
[Machine learning anomaly detection APIs](./zh_mds/ml-ad-apis.md)

将事件添加到日历
[Add events to calendar](./zh_mds/ml-post-calendar-event.md)

将作业添加到日历
[Add jobs to calendar](./zh_mds/ml-put-calendar-job.md)

关闭作业
[Close jobs](./zh_mds/ml-close-job.md)

创造就业机会
[Create jobs](./zh_mds/ml-put-job.md)

创建日历
[Create calendars](./zh_mds/ml-put-calendar.md)

创建数据馈送
[Create datafeeds](./zh_mds/ml-put-datafeed.md)

创建筛选器
[Create filters](./zh_mds/ml-put-filter.md)

删除日历
[Delete calendars](./zh_mds/ml-delete-calendar.md)

删除数据馈送
[Delete datafeeds](./zh_mds/ml-delete-datafeed.md)

从日历中删除事件
[Delete events from calendar](./zh_mds/ml-delete-calendar-event.md)

删除筛选器
[Delete filters](./zh_mds/ml-delete-filter.md)

删除预测
[Delete forecasts](./zh_mds/ml-delete-forecast.md)

删除作业
[Delete jobs](./zh_mds/ml-delete-job.md)

从日历中删除作业
[Delete jobs from calendar](./zh_mds/ml-delete-calendar-job.md)

删除模型快照
[Delete model snapshots](./zh_mds/ml-delete-snapshot.md)

删除过期数据
[Delete expired data](./zh_mds/ml-delete-expired-data.md)

估计模型内存
[Estimate model memory](./zh_mds/ml-estimate-model-memory.md)

冲洗作业
[Flush jobs](./zh_mds/ml-flush-job.md)

预测作业
[Forecast jobs](./zh_mds/ml-forecast.md)

获取存储桶
[Get buckets](./zh_mds/ml-get-bucket.md)

获取日历
[Get calendars](./zh_mds/ml-get-calendar.md)

获取类别
[Get categories](./zh_mds/ml-get-category.md)

获取数据馈送
[Get datafeeds](./zh_mds/ml-get-datafeed.md)

获取数据馈送统计信息
[Get datafeed statistics](./zh_mds/ml-get-datafeed-stats.md)

获取网红
[Get influencers](./zh_mds/ml-get-influencer.md)

获取工作
[Get jobs](./zh_mds/ml-get-job.md)

获取作业统计信息
[Get job statistics](./zh_mds/ml-get-job-stats.md)

获取模型快照
[Get model snapshots](./zh_mds/ml-get-snapshot.md)

获取模型快照升级统计信息
[Get model snapshot upgrade statistics](./zh_mds/ml-get-job-model-snapshot-upgrade-stats.md)

获取整体存储桶
[Get overall buckets](./zh_mds/ml-get-overall-buckets.md)

获取计划事件
[Get scheduled events](./zh_mds/ml-get-calendar-event.md)

获取筛选器
[Get filters](./zh_mds/ml-get-filter.md)

获取记录
[Get records](./zh_mds/ml-get-record.md)

空缺职位
[Open jobs](./zh_mds/ml-open-job.md)

将数据发布到作业
[Post data to jobs](./zh_mds/ml-post-data.md)

预览数据馈送
[Preview datafeeds](./zh_mds/ml-preview-datafeed.md)

重置作业
[Reset jobs](./zh_mds/ml-reset-job.md)

还原模型快照
[Revert model snapshots](./zh_mds/ml-revert-snapshot.md)

启动数据馈送
[Start datafeeds](./zh_mds/ml-start-datafeed.md)

停止数据馈送
[Stop datafeeds](./zh_mds/ml-stop-datafeed.md)

更新数据馈送
[Update datafeeds](./zh_mds/ml-update-datafeed.md)

更新筛选器
[Update filters](./zh_mds/ml-update-filter.md)

更新作业
[Update jobs](./zh_mds/ml-update-job.md)

更新模型快照
[Update model snapshots](./zh_mds/ml-update-snapshot.md)

升级模型快照
[Upgrade model snapshots](./zh_mds/ml-upgrade-job-model-snapshot.md)

机器学习数据帧分析 API
[Machine learning data frame analytics APIs](./zh_mds/ml-df-analytics-apis.md)

创建数据框分析作业
[Create data frame analytics jobs](./zh_mds/put-dfanalytics.md)

删除数据框分析作业
[Delete data frame analytics jobs](./zh_mds/delete-dfanalytics.md)

评估数据框分析
[Evaluate data frame analytics](./zh_mds/evaluate-dfanalytics.md)

解释数据框分析
[Explain data frame analytics](./zh_mds/explain-dfanalytics.md)

获取数据框分析作业
[Get data frame analytics jobs](./zh_mds/get-dfanalytics.md)

获取数据框分析作业统计信息
[Get data frame analytics jobs stats](./zh_mds/get-dfanalytics-stats.md)

预览数据框分析
[Preview data frame analytics](./zh_mds/preview-dfanalytics.md)

启动数据框分析作业
[Start data frame analytics jobs](./zh_mds/start-dfanalytics.md)

停止数据帧分析作业
[Stop data frame analytics jobs](./zh_mds/stop-dfanalytics.md)

更新数据框分析作业
[Update data frame analytics jobs](./zh_mds/update-dfanalytics.md)

机器学习训练模型 API
[Machine learning trained model APIs](./zh_mds/ml-df-trained-models-apis.md)

清除经过训练的模型部署缓存
[Clear trained model deployment cache](./zh_mds/clear-trained-model-deployment-cache.md)

创建或更新经过训练的模型别名
[Create or update trained model aliases](./zh_mds/put-trained-models-aliases.md)

创建已训练模型的一部分
[Create part of a trained model](./zh_mds/put-trained-model-definition-part.md)

创建经过训练的模型
[Create trained models](./zh_mds/put-trained-models.md)

创建经过训练的模型词汇
[Create trained model vocabulary](./zh_mds/put-trained-model-vocabulary.md)

删除经过训练的模型别名
[Delete trained model aliases](./zh_mds/delete-trained-models-aliases.md)

删除已训练的模型
[Delete trained models](./zh_mds/delete-trained-models.md)

获取经过训练的模型
[Get trained models](./zh_mds/get-trained-models.md)

获取经过训练的模型统计信息
[Get trained models stats](./zh_mds/get-trained-models-stats.md)

推断训练模型
[Infer trained model](./zh_mds/infer-trained-model.md)

开始训练模型部署
[Start trained model deployment](./zh_mds/start-trained-model-deployment.md)

停止经过训练的模型部署
[Stop trained model deployment](./zh_mds/stop-trained-model-deployment.md)

更新经过训练的模型部署
[Update trained model deployment](./zh_mds/update-trained-model-deployment.md)

迁移接口
[Migration APIs](./zh_mds/migration-api.md)

弃用信息
[Deprecation info](./zh_mds/migration-api-deprecation.md)

功能迁移
[Feature migration](./zh_mds/feature-migration-api.md)

节点生命周期接口
[Node lifecycle APIs](./zh_mds/node-lifecycle-api.md)

放关机接口
[Put shutdown API](./zh_mds/put-shutdown.md)

获取关机接口
[Get shutdown API](./zh_mds/get-shutdown.md)

删除关机接口
[Delete shutdown API](./zh_mds/delete-shutdown.md)

重新加载搜索分析器 API
[Reload search analyzers API](./zh_mds/indices-reload-analyzers.md)

存储库计量 API
[Repositories metering APIs](./zh_mds/repositories-metering-apis.md)

获取存储库计量信息
[Get repositories metering information](./zh_mds/get-repositories-metering-api.md)

清除存储库计量存档
[Clear repositories metering archive](./zh_mds/clear-repositories-metering-archive-api.md)

汇总 API
[Rollup APIs](./zh_mds/rollup-apis.md)

创建汇总作业
[Create rollup jobs](./zh_mds/rollup-put-job.md)

删除汇总作业
[Delete rollup jobs](./zh_mds/rollup-delete-job.md)

获取工作
[Get job](./zh_mds/rollup-get-job.md)

获取汇总上限
[Get rollup caps](./zh_mds/rollup-get-rollup-caps.md)

获取汇总索引上限
[Get rollup index caps](./zh_mds/rollup-get-rollup-index-caps.md)

汇总搜索
[Rollup search](./zh_mds/rollup-search.md)

启动汇总作业
[Start rollup jobs](./zh_mds/rollup-start-job.md)

停止汇总作业
[Stop rollup jobs](./zh_mds/rollup-stop-job.md)

脚本接口
[Script APIs](./zh_mds/script-apis.md)

创建或更新存储的脚本
[Create or update stored script](./zh_mds/create-stored-script-api.md)

删除存储的脚本
[Delete stored script](./zh_mds/delete-stored-script-api.md)

获取脚本上下文
[Get script contexts](./zh_mds/get-script-contexts-api.md)

获取脚本语言
[Get script languages](./zh_mds/get-script-languages-api.md)

获取存储的脚本
[Get stored script](./zh_mds/get-stored-script-api.md)

搜索接口
[Search APIs](./zh_mds/search.md)

搜索
[Search](./zh_mds/search-search.md)

异步搜索
[Async search](./zh_mds/async-search.md)

时间点
[Point in time](./zh_mds/point-in-time-api.md)

kNN 搜索
[kNN search](./zh_mds/knn-search-api.md)

倒数等级融合
[Reciprocal rank fusion](./zh_mds/rrf.md)

滚动
[Scroll](./zh_mds/scroll-api.md)

清除滚动
[Clear scroll](./zh_mds/clear-scroll-api.md)

搜索模板
[Search template](./zh_mds/search-template-api.md)

多搜索模板
[Multi search template](./zh_mds/multi-search-template.md)

呈现搜索模板
[Render search template](./zh_mds/render-search-template-api.md)

搜索分片
[Search shards](./zh_mds/search-shards.md)

建议器
[Suggesters](./zh_mds/search-suggesters.md)

多重搜索
[Multi search](./zh_mds/search-multi-search.md)

计数
[Count](./zh_mds/search-count.md)

驗證
[Validate](./zh_mds/search-validate.md)

术语枚举
[Terms enum](./zh_mds/search-terms-enum.md)

解释
[Explain](./zh_mds/search-explain.md)

轮廓
[Profile](./zh_mds/search-profile.md)

现场能力
[Field capabilities](./zh_mds/search-field-caps.md)

排名评估
[Ranking evaluation](./zh_mds/search-rank-eval.md)

矢量图块搜索
[Vector tile search](./zh_mds/search-vector-tile-api.md)

搜索应用程序接口
[Search Application APIs](./zh_mds/search-application-apis.md)

放置搜索应用程序
[Put Search Application](./zh_mds/put-search-application.md)

获取搜索应用程序
[Get Search Application](./zh_mds/get-search-application.md)

列出搜索应用程序
[List Search Applications](./zh_mds/list-search-applications.md)

删除搜索应用程序
[Delete Search Application](./zh_mds/delete-search-application.md)

搜索应用程序搜索
[Search Application Search](./zh_mds/search-application-search.md)

呈现搜索应用程序查询
[Render Search Application Query](./zh_mds/search-application-render-query.md)

可搜索快照 API
[Searchable snapshots APIs](./zh_mds/searchable-snapshots-apis.md)

装载快照
[Mount snapshot](./zh_mds/searchable-snapshots-api-mount-snapshot.md)

缓存统计信息
[Cache stats](./zh_mds/searchable-snapshots-api-cache-stats.md)

可搜索的快照统计信息
[Searchable snapshot statistics](./zh_mds/searchable-snapshots-api-stats.md)

清除缓存
[Clear cache](./zh_mds/searchable-snapshots-api-clear-cache.md)

安全接口
[Security APIs](./zh_mds/security-api.md)

证实
[Authenticate](./zh_mds/security-api-authenticate.md)

更改密码
[Change passwords](./zh_mds/security-api-change-password.md)

清除缓存
[Clear cache](./zh_mds/security-api-clear-cache.md)

清除角色缓存
[Clear roles cache](./zh_mds/security-api-clear-role-cache.md)

清除权限缓存
[Clear privileges cache](./zh_mds/security-api-clear-privilege-cache.md)

清除 API 密钥缓存
[Clear API key cache](./zh_mds/security-api-clear-api-key-cache.md)

清除服务帐户令牌缓存
[Clear service account token caches](./zh_mds/security-api-clear-service-token-caches.md)

创建接口密钥
[Create API keys](./zh_mds/security-api-create-api-key.md)

创建或更新应用程序权限
[Create or update application privileges](./zh_mds/security-api-put-privileges.md)

创建或更新角色映射
[Create or update role mappings](./zh_mds/security-api-put-role-mapping.md)

创建或更新角色
[Create or update roles](./zh_mds/security-api-put-role.md)

创建或更新用户
[Create or update users](./zh_mds/security-api-put-user.md)

创建服务帐户令牌
[Create service account tokens](./zh_mds/security-api-create-service-token.md)

委托 PKI 身份验证
[Delegate PKI authentication](./zh_mds/security-api-delegate-pki-authentication.md)

删除应用程序权限
[Delete application privileges](./zh_mds/security-api-delete-privilege.md)

删除角色映射
[Delete role mappings](./zh_mds/security-api-delete-role-mapping.md)

删除角色
[Delete roles](./zh_mds/security-api-delete-role.md)

删除服务帐户令牌
[Delete service account token](./zh_mds/security-api-delete-service-token.md)

删除用户
[Delete users](./zh_mds/security-api-delete-user.md)

禁用用户
[Disable users](./zh_mds/security-api-disable-user.md)

启用用户
[Enable users](./zh_mds/security-api-enable-user.md)

注册木花
[Enroll Kibana](./zh_mds/security-api-kibana-enrollment.md)

注册节点
[Enroll node](./zh_mds/security-api-node-enrollment.md)

获取接口密钥信息
[Get API key information](./zh_mds/security-api-get-api-key.md)

获取应用程序权限
[Get application privileges](./zh_mds/security-api-get-privileges.md)

获取内置权限
[Get builtin privileges](./zh_mds/security-api-get-builtin-privileges.md)

获取角色映射
[Get role mappings](./zh_mds/security-api-get-role-mapping.md)

获取角色
[Get roles](./zh_mds/security-api-get-role.md)

获取服务帐户
[Get service accounts](./zh_mds/security-api-get-service-accounts.md)

获取服务帐户凭据
[Get service account credentials](./zh_mds/security-api-get-service-credentials.md)

获取令牌
[Get token](./zh_mds/security-api-get-token.md)

获取用户权限
[Get user privileges](./zh_mds/security-api-get-user-privileges.md)

获取用户
[Get users](./zh_mds/security-api-get-user.md)

授予 API 密钥
[Grant API keys](./zh_mds/security-api-grant-api-key.md)

拥有特权
[Has privileges](./zh_mds/security-api-has-privileges.md)

使 API 密钥失效
[Invalidate API key](./zh_mds/security-api-invalidate-api-key.md)

使令牌无效
[Invalidate token](./zh_mds/security-api-invalidate-token.md)

OpenID Connect 准备身份验证
[OpenID Connect prepare authentication](./zh_mds/security-api-oidc-prepare-authentication.md)

OpenID Connect 身份验证
[OpenID Connect authenticate](./zh_mds/security-api-oidc-authenticate.md)

开放ID连接注销
[OpenID Connect logout](./zh_mds/security-api-oidc-logout.md)

查询接口密钥信息
[Query API key information](./zh_mds/security-api-query-api-key.md)

更新 API 密钥
[Update API key](./zh_mds/security-api-update-api-key.md)

批量更新 API 密钥
[Bulk update API keys](./zh_mds/security-api-bulk-update-api-keys.md)

SAML 准备身份验证
[SAML prepare authentication](./zh_mds/security-api-saml-prepare-authentication.md)

SAML 身份验证
[SAML authenticate](./zh_mds/security-api-saml-authenticate.md)

萨姆勒注销
[SAML logout](./zh_mds/security-api-saml-logout.md)

存储层无效
[SAML invalidate](./zh_mds/security-api-saml-invalidate.md)

SAML 完成注销
[SAML complete logout](./zh_mds/security-api-saml-complete-logout.md)

SAML 服务提供商元数据
[SAML service provider metadata](./zh_mds/security-api-saml-sp-metadata.md)

SSL 证书
[SSL certificate](./zh_mds/security-api-ssl.md)

激活用户配置文件
[Activate user profile](./zh_mds/security-api-activate-user-profile.md)

禁用用户配置文件
[Disable user profile](./zh_mds/security-api-disable-user-profile.md)

启用用户配置文件
[Enable user profile](./zh_mds/security-api-enable-user-profile.md)

获取用户配置文件
[Get user profiles](./zh_mds/security-api-get-user-profile.md)

建议用户配置文件
[Suggest user profile](./zh_mds/security-api-suggest-user-profile.md)

更新用户配置文件数据
[Update user profile data](./zh_mds/security-api-update-user-profile-data.md)

具有权限用户配置文件
[Has privileges user profile](./zh_mds/security-api-has-privileges-user-profile.md)

快照和还原 API
[Snapshot and restore APIs](./zh_mds/snapshot-restore-apis.md)

创建或更新快照存储库
[Create or update snapshot repository](./zh_mds/put-snapshot-repo-api.md)

验证快照存储库
[Verify snapshot repository](./zh_mds/verify-snapshot-repo-api.md)

存储库分析
[Repository analysis](./zh_mds/repo-analysis-api.md)

获取快照存储库
[Get snapshot repository](./zh_mds/get-snapshot-repo-api.md)

删除快照存储库
[Delete snapshot repository](./zh_mds/delete-snapshot-repo-api.md)

清理快照存储库
[Clean up snapshot repository](./zh_mds/clean-up-snapshot-repo-api.md)

克隆快照
[Clone snapshot](./zh_mds/clone-snapshot-api.md)

创建快照
[Create snapshot](./zh_mds/create-snapshot-api.md)

获取快照
[Get snapshot](./zh_mds/get-snapshot-api.md)

获取快照状态
[Get snapshot status](./zh_mds/get-snapshot-status-api.md)

恢复快照
[Restore snapshot](./zh_mds/restore-snapshot-api.md)

删除快照
[Delete snapshot](./zh_mds/delete-snapshot-api.md)

快照生命周期管理 API
[Snapshot lifecycle management APIs](./zh_mds/snapshot-lifecycle-management-api.md)

创建或更新策略
[Create or update policy](./zh_mds/slm-api-put-policy.md)

获取策略
[Get policy](./zh_mds/slm-api-get-policy.md)

删除策略
[Delete policy](./zh_mds/slm-api-delete-policy.md)

执行快照生命周期策略
[Execute snapshot lifecycle policy](./zh_mds/slm-api-execute-lifecycle.md)

执行快照保留策略
[Execute snapshot retention policy](./zh_mds/slm-api-execute-retention.md)

获取快照生命周期管理状态
[Get snapshot lifecycle management status](./zh_mds/slm-api-get-status.md)

获取快照生命周期统计信息
[Get snapshot lifecycle stats](./zh_mds/slm-api-get-stats.md)

启动快照生命周期管理
[Start snapshot lifecycle management](./zh_mds/slm-api-start.md)

停止快照生命周期管理
[Stop snapshot lifecycle management](./zh_mds/slm-api-stop.md)

应用程序接口
[SQL APIs](./zh_mds/sql-apis.md)

清除 SQL 游标
[Clear SQL cursor](./zh_mds/clear-sql-cursor-api.md)

删除异步 SQL 搜索
[Delete async SQL search](./zh_mds/delete-async-sql-search-api.md)

获取异步 SQL 搜索
[Get async SQL search](./zh_mds/get-async-sql-search-api.md)

获取异步 SQL 搜索状态
[Get async SQL search status](./zh_mds/get-async-sql-search-status-api.md)

数据库搜索
[SQL search](./zh_mds/sql-search-api.md)

SQL 翻译
[SQL translate](./zh_mds/sql-translate-api.md)

转换接口
[Transform APIs](./zh_mds/transform-apis.md)

创建转换
[Create transform](./zh_mds/put-transform.md)

删除转换
[Delete transform](./zh_mds/delete-transform.md)

获取转换
[Get transforms](./zh_mds/get-transform.md)

获取转换统计信息
[Get transform statistics](./zh_mds/get-transform-stats.md)

预览转换
[Preview transform](./zh_mds/preview-transform.md)

重置转换
[Reset transform](./zh_mds/reset-transform.md)

“立即计划”转换
[Schedule now transform](./zh_mds/schedule-now-transform.md)

开始转换
[Start transform](./zh_mds/start-transform.md)

停止转换
[Stop transforms](./zh_mds/stop-transform.md)

更新转换
[Update transform](./zh_mds/update-transform.md)

升级转换
[Upgrade transforms](./zh_mds/upgrade-transforms.md)

使用接口
[Usage API](./zh_mds/usage-api.md)

观察程序接口
[Watcher APIs](./zh_mds/watcher-api.md)

阿克手表
[Ack watch](./zh_mds/watcher-api-ack-watch.md)

激活手表
[Activate watch](./zh_mds/watcher-api-activate-watch.md)

停用手表
[Deactivate watch](./zh_mds/watcher-api-deactivate-watch.md)

删除监视
[Delete watch](./zh_mds/watcher-api-delete-watch.md)

执行监视
[Execute watch](./zh_mds/watcher-api-execute-watch.md)

获取手表
[Get watch](./zh_mds/watcher-api-get-watch.md)

获取观察者统计信息
[Get Watcher stats](./zh_mds/watcher-api-stats.md)

查询监视
[Query watches](./zh_mds/watcher-api-query-watches.md)

创建或更新监视
[Create or update watch](./zh_mds/watcher-api-put-watch.md)

更新观察程序设置
[Update Watcher settings](./zh_mds/watcher-api-update-settings.md)

获取观察程序设置
[Get Watcher settings](./zh_mds/watcher-api-get-settings.md)

启动监视服务
[Start watch service](./zh_mds/watcher-api-start.md)

秒表服务
[Stop watch service](./zh_mds/watcher-api-stop.md)

定义
[Definitions](./zh_mds/api-definitions.md)

角色映射资源
[Role mapping resources](./zh_mds/role-mapping-resources.md)

迁移指南
[Migration guide](./zh_mds/breaking-changes.md)

8.9
[8.9](./zh_mds/migrating-8.9.md)

8.8
[8.8](./zh_mds/migrating-8.8.md)

8.7
[8.7](./zh_mds/migrating-8.7.md)

8.6
[8.6](./zh_mds/migrating-8.6.md)

8.5
[8.5](./zh_mds/migrating-8.5.md)

8.4
[8.4](./zh_mds/migrating-8.4.md)

8.3
[8.3](./zh_mds/migrating-8.3.md)

8.2
[8.2](./zh_mds/migrating-8.2.md)

8.1
[8.1](./zh_mds/migrating-8.1.md)

8.0
[8.0](./zh_mds/migrating-8.0.md)

Java 时间迁移指南
[Java time migration guide](./zh_mds/migrate-to-java-time.md)

瞬态设置迁移指南
[Transient settings migration guide](./zh_mds/transient-settings-migration-guide.md)

发行说明
[Release notes](./zh_mds/es-release-notes.md)

弹性搜索版本 8.9.0
[Elasticsearch version 8.9.0](./zh_mds/release-notes-8.9.0.md)

弹性搜索版本 8.8.2
[Elasticsearch version 8.8.2](./zh_mds/release-notes-8.8.2.md)

弹性搜索版本 8.8.1
[Elasticsearch version 8.8.1](./zh_mds/release-notes-8.8.1.md)

弹性搜索版本 8.8.0
[Elasticsearch version 8.8.0](./zh_mds/release-notes-8.8.0.md)

弹性搜索版本 8.7.1
[Elasticsearch version 8.7.1](./zh_mds/release-notes-8.7.1.md)

弹性搜索版本 8.7.0
[Elasticsearch version 8.7.0](./zh_mds/release-notes-8.7.0.md)

弹性搜索版本 8.6.2
[Elasticsearch version 8.6.2](./zh_mds/release-notes-8.6.2.md)

弹性搜索版本 8.6.1
[Elasticsearch version 8.6.1](./zh_mds/release-notes-8.6.1.md)

弹性搜索版本 8.6.0
[Elasticsearch version 8.6.0](./zh_mds/release-notes-8.6.0.md)

弹性搜索版本 8.5.3
[Elasticsearch version 8.5.3](./zh_mds/release-notes-8.5.3.md)

弹性搜索版本 8.5.2
[Elasticsearch version 8.5.2](./zh_mds/release-notes-8.5.2.md)

弹性搜索版本 8.5.1
[Elasticsearch version 8.5.1](./zh_mds/release-notes-8.5.1.md)

弹性搜索版本 8.5.0
[Elasticsearch version 8.5.0](./zh_mds/release-notes-8.5.0.md)

Elasticsearch 版本 8.4.3
[Elasticsearch version 8.4.3](./zh_mds/release-notes-8.4.3.md)

弹性搜索版本 8.4.2
[Elasticsearch version 8.4.2](./zh_mds/release-notes-8.4.2.md)

弹性搜索版本 8.4.1
[Elasticsearch version 8.4.1](./zh_mds/release-notes-8.4.1.md)

弹性搜索版本 8.4.0
[Elasticsearch version 8.4.0](./zh_mds/release-notes-8.4.0.md)

弹性搜索版本 8.3.3
[Elasticsearch version 8.3.3](./zh_mds/release-notes-8.3.3.md)

弹性搜索版本 8.3.2
[Elasticsearch version 8.3.2](./zh_mds/release-notes-8.3.2.md)

弹性搜索版本 8.3.1
[Elasticsearch version 8.3.1](./zh_mds/release-notes-8.3.1.md)

弹性搜索版本 8.3.0
[Elasticsearch version 8.3.0](./zh_mds/release-notes-8.3.0.md)

弹性搜索版本 8.2.3
[Elasticsearch version 8.2.3](./zh_mds/release-notes-8.2.3.md)

弹性搜索版本 8.2.2
[Elasticsearch version 8.2.2](./zh_mds/release-notes-8.2.2.md)

弹性搜索版本 8.2.1
[Elasticsearch version 8.2.1](./zh_mds/release-notes-8.2.1.md)

弹性搜索版本 8.2.0
[Elasticsearch version 8.2.0](./zh_mds/release-notes-8.2.0.md)

弹性搜索版本 8.1.3
[Elasticsearch version 8.1.3](./zh_mds/release-notes-8.1.3.md)

Elasticsearch 版本 8.1.2
[Elasticsearch version 8.1.2](./zh_mds/release-notes-8.1.2.md)

Elasticsearch 版本 8.1.1
[Elasticsearch version 8.1.1](./zh_mds/release-notes-8.1.1.md)

弹性搜索版本 8.1.0
[Elasticsearch version 8.1.0](./zh_mds/release-notes-8.1.0.md)

弹性搜索版本 8.0.1
[Elasticsearch version 8.0.1](./zh_mds/release-notes-8.0.1.md)

弹性搜索版本 8.0.0
[Elasticsearch version 8.0.0](./zh_mds/release-notes-8.0.0.md)

Elasticsearch 版本 8.0.0-rc2
[Elasticsearch version 8.0.0-rc2](./zh_mds/release-notes-8.0.0-rc2.md)

Elasticsearch 版本 8.0.0-rc1
[Elasticsearch version 8.0.0-rc1](./zh_mds/release-notes-8.0.0-rc1.md)

Elasticsearch 版本 8.0.0-beta1
[Elasticsearch version 8.0.0-beta1](./zh_mds/release-notes-8.0.0-beta1.md)

Elasticsearch 版本 8.0.0-alpha2
[Elasticsearch version 8.0.0-alpha2](./zh_mds/release-notes-8.0.0-alpha2.md)

Elasticsearch 版本 8.0.0-alpha1
[Elasticsearch version 8.0.0-alpha1](./zh_mds/release-notes-8.0.0-alpha1.md)

依赖项和版本
[Dependencies and versions](./zh_mds/dependencies-versions.md)