

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md)

[« Skip rollover](skipping-rollover.md) [Data tiers »](data-tiers.md)

## 还原托管数据流或索引

要还原托管索引，请确保索引引用的 ILM 策略存在。如有必要，您可以通过将"include_global_state"设置为"true"来恢复 ILM 策略。

当您使用托管后备索引还原托管索引或数据流时，ILM 会自动恢复执行还原的索引的策略。还原索引的"min_age"相对于最初创建或滚动更新的时间，而不是其还原时间。无论索引是否已从快照还原，策略操作都按相同的计划执行。如果还原在其长达一个月的生命周期中途意外删除的索引，它将在其生命周期的最后两周正常进行。

在某些情况下，您可能希望阻止 ILM 立即对还原的索引执行其策略。例如，如果要恢复较旧的快照，则可能希望防止它在其所有生命周期阶段快速发展。您可能希望在文档标记为只读或收缩之前添加或更新文档，或者防止立即删除索引。

要防止 ILM 执行还原的索引的策略，请执行以下操作：

1. 暂时停止 ILM。这将暂停 _all_ ILM 策略的执行。  2. 恢复快照。  3. 在 ILM 恢复策略执行之前，从索引中删除策略或执行所需的任何操作。  4. 重新启动 ILM 以恢复策略执行。

[« Skip rollover](skipping-rollover.md) [Data tiers »](data-tiers.md)
