

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md) ›[Configuring Elasticsearch](settings.md)

[« Auditing security settings](auditing-settings.md) [Cluster-level shard
allocation and routing settings »](modules-cluster.md)

## 断路器设置

Elasticsearch 包含多个断路器，用于防止操作导致内存不足错误。每个断路器指定它可以使用的内存量限制。此外，还有一个父级断路器，用于指定可在所有断路器中使用的内存总量。

除非另有说明，否则可以使用群集更新设置 API 在活动群集上动态更新这些设置。

有关断路器错误的信息，请参阅断路器错误。

#### 父断路器

可以使用以下设置配置父级断路器：

`indices.breaker.total.use_real_memory`

     ([Static](settings.html#static-cluster-setting)) Determines whether the parent breaker should take real memory usage into account (`true`) or only consider the amount that is reserved by child circuit breakers (`false`). Defaults to `true`. 

"索引.破坏者.总限制" ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Dynamic](settings.html#dynamic-cluster-setting)) Starting limit for overall parent breaker. Defaults to 70% of JVM heap if `indices.breaker.total.use_real_memory` is `false`. If `indices.breaker.total.use_real_memory` is `true`, defaults to 95% of the JVM heap. 

#### 现场数据断路器

现场数据断路器估计将字段加载到现场数据缓存所需的堆内存。如果加载字段会导致缓存超过预定义的内存限制，则断路器将停止操作并返回错误。

'index.breaker.fielddata.limit' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Dynamic](settings.html#dynamic-cluster-setting)) Limit for fielddata breaker. Defaults to 40% of JVM heap. 

"索引.破坏者.字段数据.开销" ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Dynamic](settings.html#dynamic-cluster-setting)) A constant that all field data estimations are multiplied with to determine a final estimation. Defaults to `1.03`. 

#### 请求断路器

请求断路器允许 Elasticsearch 防止每个请求的数据结构(例如，用于在请求期间计算聚合的内存)超过一定量的内存。

'index.breaker.request.limit' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Dynamic](settings.html#dynamic-cluster-setting)) Limit for request breaker, defaults to 60% of JVM heap. 

'index.breaker.request.overhead' ！[标志云](https://www.elastic.co/cloud/elasticsearch-service/signup?baymax=docs-body&elektra=docs)

     ([Dynamic](settings.html#dynamic-cluster-setting)) A constant that all request estimations are multiplied with to determine a final estimation. Defaults to `1`. 

#### 飞行中请求断路器

传输中请求断路器允许 Elasticsearch 限制传输或 HTTPlevel 上所有当前活动的传入请求的内存使用量，使其不超过节点上的一定内存量。内存使用量基于请求本身的内容长度。此断路器还认为，内存不仅需要用于表示原始请求，还需要作为默认开销反映的结构化对象。

`network.breaker.inflight_requests.limit`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Limit for in flight requests breaker, defaults to 100% of JVM heap. This means that it is bound by the limit configured for the parent circuit breaker. 
`network.breaker.inflight_requests.overhead`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A constant that all in flight requests estimations are multiplied with to determine a final estimation. Defaults to 2. 

#### 记帐请求断路器

记帐断路器允许 Elasticsearch 限制内存中保存的事物的内存使用量，这些内容在请求完成时不会释放。这包括Lucene段存储器之类的东西。

`indices.breaker.accounting.limit`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Limit for accounting breaker, defaults to 100% of JVM heap. This means that it is bound by the limit configured for the parent circuit breaker. 
`indices.breaker.accounting.overhead`

     ([Dynamic](settings.html#dynamic-cluster-setting)) A constant that all accounting estimations are multiplied with to determine a final estimation. Defaults to 1 

#### 脚本编译断路器

与以前的基于内存的断路器略有不同，脚本编译断路器限制一段时间内内联脚本编译的数量。

有关详细信息，请参阅脚本文档的"首选参数"部分。

`script.max_compilations_rate`

     ([Dynamic](settings.html#dynamic-cluster-setting)) Limit for the number of unique dynamic scripts within a certain interval that are allowed to be compiled. Defaults to `150/5m`, meaning 150 every 5 minutes. 

如果集群经常遇到给定的"max_compilation_rate"，则脚本缓存可能大小不足，请使用节点统计信息检查最近的缓存逐出次数，"script.cache_evictions_history"和编译"script.compilations_history"。如果有大量最近的缓存逐出或编译，则脚本缓存的大小可能会不足，请考虑通过设置"script.cache.max_size"将脚本缓存的大小加倍。

#### 正则表达式断路器

编写不当的正则表达式会降低集群稳定性和性能。正则表达式断路器限制了正则表达式无痛脚本的使用和复杂性。

`script.painless.regex.enabled`

    

(静态)在无痛脚本中启用正则表达式。接受：

"有限"(默认)

     Enables regex but limits complexity using the [`script.painless.regex.limit-factor`](circuit-breaker.html#script-painless-regex-limit-factor) cluster setting. 
`true`

     Enables regex with no complexity limits. Disables the regex circuit breaker. 
`false`

     Disables regex. Any Painless script containing a regular expression returns an error. 

`script.painless.regex.limit-factor`

    

(静态)限制无痛脚本中的正则表达式可以考虑的字符数。Elasticsearch 通过将设置值乘以脚本输入的字符长度来计算此限制。

例如，输入"foobarbaz"的字符长度为"9"。如果 'script.painless.regex.limit-factor' 是 '6'，则 'foobarbaz' 上的正则表达式最多可以考虑 54 (9 * 6) 个字符。如果表达式超过此限制，它将触发正则表达式断路器并返回错误。

Elasticsearch 仅在 'script.painless.regex.enabled' 为 "limited" 时才应用此限制。

### EQL 断路器

当执行序列查询时，处理查询的节点需要在内存中保留一些结构，这是实现序列匹配的算法所需要的。当需要处理大量数据和/或用户请求大量匹配序列时(通过设置大小查询参数)，这些结构占用的内存可能会超过JVM的可用内存。这将导致"内存不足"异常，从而导致节点关闭。

为了防止这种情况发生，使用了特殊的断路器，该断路器在执行序列查询期间限制内存分配。当断路器被触发时，将抛出'org.elasticsearch.common.breaker.CircuitBreakingException'，并向用户返回描述性错误消息。

可以使用以下设置配置此断路器：

`breaker.eql_sequence.limit`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The limit for circuit breaker used to restrict the memory utilisation during the execution of an EQL sequence query. This value is defined as a percentage of the JVM heap. Defaults to `50%`. If the [parent circuit breaker](circuit-breaker.html#parent-circuit-breaker "Parent circuit breaker") is set to a value less than `50%`, this setting uses that value as its default instead. 
`breaker.eql_sequence.overhead`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) A constant that sequence query memory estimates are multiplied by to determine a final estimate. Defaults to `1`. 
`breaker.eql_sequence.type`

    

(静态)断路器类型。有效值为：

"内存"(默认)

     The breaker limits memory usage for EQL sequence queries. 
`noop`

     Disables the breaker. 

#### 机器学习断路器

`breaker.model_inference.limit`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) The limit for the trained model circuit breaker. This value is defined as a percentage of the JVM heap. Defaults to `50%`. If the [parent circuit breaker](circuit-breaker.html#parent-circuit-breaker "Parent circuit breaker") is set to a value less than `50%`, this setting uses that value as its default instead. 
`breaker.model_inference.overhead`

     ([Dynamic](cluster-update-settings.html "Cluster update settings API")) A constant that all trained model estimations are multiplied by to determine a final estimation. See [Circuit breaker settings](circuit-breaker.html "Circuit breaker settings"). Defaults to `1`. 
`breaker.model_inference.type`

     ([Static](settings.html#static-cluster-setting)) The underlying type of the circuit breaker. There are two valid options: `noop` and `memory`. `noop` means the circuit breaker does nothing to prevent too much memory usage. `memory` means the circuit breaker tracks the memory used by trained models and can potentially break and prevent `OutOfMemory` errors. The default value is `memory`. 

[« Auditing security settings](auditing-settings.md) [Cluster-level shard
allocation and routing settings »](modules-cluster.md)
