

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[ILM concepts](ilm-concepts.md)

[« ILM concepts](ilm-concepts.md) [Rollover »](index-rollover.md)

## 索引生命周期

ILM 定义了五个索引生命周期 _阶段_：

* **热门** ： 正在主动更新和查询索引。  * **暖** ：索引不再更新，但仍在查询中。  * **冷**：索引不再更新，并且不经常查询。信息仍然需要可搜索，但如果这些查询速度较慢也没关系。  * **冻结**：索引不再更新，很少被查询。信息仍然需要可搜索，但如果这些查询非常慢也没关系。  * **删除**：不再需要索引，可以安全地删除。

索引的_lifecycle policy_指定哪些阶段适用、每个阶段执行的操作以及索引在阶段之间转换的时间。

您可以在创建索引时手动应用生命周期策略。对于时间序列索引，您需要将生命周期策略与用于在序列中创建新索引的索引模板相关联。当索引滚动更新时，手动应用的策略不会自动应用于新索引。

如果您使用 Elasticsearch 的安全功能，ILM 将以上次更新策略的用户身份执行操作。ILM 仅在上次策略更新时分配给用户的角色。

### 相变

ILM 根据索引的使用期限在生命周期中移动索引。若要控制这些转换的时间，请为每个阶段设置一个_minimum age_。要使 anindex 进入下一阶段，当前阶段中的所有操作都必须完成，并且索引必须早于下一阶段的最低期限。配置的最小年龄必须在后续阶段之间增加，例如，最小年龄为 10 天的"暖"阶段只能是最低年龄未设置或 >= 10 天的"冷"阶段。

最短期限默认为零，这会导致 ILM 在当前阶段中的所有操作完成后立即将索引移动到下一阶段。

如果索引有未分配的分片，且集群健康状态为黄色，则索引仍可以根据其索引生命周期管理策略过渡到下一阶段。但是，由于 Elasticsearch 只能在绿色集群上执行某些清理任务，因此可能会出现意想不到的副作用。

为避免增加磁盘使用率和可靠性问题，请及时解决任何群集运行状况问题。

### 阶段执行

ILM 控制阶段中操作的执行顺序，以及执行what_steps_以对每个操作执行必要的索引操作的顺序。

当索引进入阶段时，ILM 会将阶段定义缓存在索引元数据中。这可确保策略更新不会将索引置于永远无法退出阶段的状态。如果可以安全地应用更改，ILM 将更新缓存的阶段定义。如果不能，阶段执行将继续使用缓存的定义。

ILM 定期运行，检查索引是否符合策略标准，并执行所需的任何步骤。为了避免争用情况，ILM 可能需要运行多次才能执行完成操作所需的所有步骤。例如，如果 ILM 确定某个索引已满足滚动更新条件，它将开始执行完成滚动更新操作所需的步骤。如果达到无法安全前进到下一步的点，则执行将停止。下次 ILM 运行时，ILM 将从中断的位置继续执行。这意味着，即使"indices.lifecycle.poll_interval"设置为 10 分钟并且索引满足滚动更新条件，也可能在滚动更新完成之前 20 分钟。

### 阶段操作

ILM 在每个阶段都支持以下操作。ILM 按列出的顺序执行这些操作。

*热

    * [Set Priority](ilm-set-priority.html "Set priority")
    * [Unfollow](ilm-unfollow.html "Unfollow")
    * [Rollover](ilm-rollover.html "Rollover")
    * [Read-Only](ilm-readonly.html "Read only")
    * [Downsample](ilm-downsample.html "Downsample")
    * [Shrink](ilm-shrink.html "Shrink")
    * [Force Merge](ilm-forcemerge.html "Force merge")
    * [Searchable Snapshot](ilm-searchable-snapshot.html "Searchable snapshot")

*温暖

    * [Set Priority](ilm-set-priority.html "Set priority")
    * [Unfollow](ilm-unfollow.html "Unfollow")
    * [Read-Only](ilm-readonly.html "Read only")
    * [Downsample](ilm-downsample.html "Downsample")
    * [Allocate](ilm-allocate.html "Allocate")
    * [Migrate](ilm-migrate.html "Migrate")
    * [Shrink](ilm-shrink.html "Shrink")
    * [Force Merge](ilm-forcemerge.html "Force merge")

*冷

    * [Set Priority](ilm-set-priority.html "Set priority")
    * [Unfollow](ilm-unfollow.html "Unfollow")
    * [Read-Only](ilm-readonly.html "Read only")
    * [Downsample](ilm-downsample.html "Downsample")
    * [Searchable Snapshot](ilm-searchable-snapshot.html "Searchable snapshot")
    * [Allocate](ilm-allocate.html "Allocate")
    * [Migrate](ilm-migrate.html "Migrate")

*冷冻

    * [Unfollow](ilm-unfollow.html "Unfollow")
    * [Searchable Snapshot](ilm-searchable-snapshot.html "Searchable snapshot")

*删除

    * [Wait For Snapshot](ilm-wait-for-snapshot.html "Wait for snapshot")
    * [Delete](ilm-delete.html "Delete")

[« ILM concepts](ilm-concepts.md) [Rollover »](index-rollover.md)
