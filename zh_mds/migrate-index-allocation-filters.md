

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md)

[« Configure a lifecycle policy](set-up-lifecycle-policy.md)
[Troubleshooting index lifecycle management errors »](index-lifecycle-error-
handling.md)

## 将索引分配筛选器迁移到节点角色

如果您当前使用自定义节点属性和基于属性的分配筛选器在热温冷架构中的数据层之间移动索引，我们建议您切换到使用内置节点角色和自动数据层分配。使用 noderoles 使 ILM 能够在数据层之间自动移动索引。

虽然我们建议依靠自动数据层分配来管理热温冷体系结构中的数据，但仍可以使用基于属性的分配筛选器来控制分片分配以用于其他目的。

Elasticsearch Service 和 Elastic Cloud Enterprise 可以自动执行迁移。对于自我管理部署，您需要手动更新配置、ILM 策略和索引以切换到节点角色。

### 自动迁移到 Elasticsearch Service 或 ElasticCloudEnterprise 上的节点角色

如果您在 Elasticsearch Service 或 Elastic Cloud Enterprise 中使用默认部署模板中的节点属性，则在执行以下操作时，系统会提示您切换到节点角色：

* 升级到 Elasticsearch 7.10 或更高版本 * 部署暖、冷或冻结数据层 * 启用自动缩放

这些操作会自动更新您的群集配置和 ILM 策略以使用节点角色。此外，升级到版本 7.14 或更高版本会在将任何配置更改应用于您的部署时自动更新 ILM 策略。

如果使用自定义索引模板，请在自动迁移完成后检查它们，并删除所有基于属性的分配筛选器。

自动迁移后，您无需执行任何进一步操作。仅当您不允许自动迁移或具有自我管理部署时，才需要执行以下手动步骤。

### 迁移到自我管理部署上的节点角色

要切换到使用节点角色，请执行以下操作：

1. 将数据节点分配到相应的数据层。  2. 从索引生命周期管理策略中删除基于属性的分配设置。  3. 停止在新索引上设置自定义热属性。  4. 更新现有索引以设置层首选项。

#### 将数据节点分配给数据层

为每个数据节点配置适当的角色，以将其分配给一个或多个数据层："data_hot"、"data_content"、"data_warm"、"data_cold"或"data_frozen"。节点还可以具有其他角色。默认情况下，新节点配置了所有角色。

当您将数据层添加到 Elasticsearch Service 部署时，一个或多个节点会自动配置相应的角色。要显式更改节点在 Elasticsearch Service 部署中的角色，请使用更新部署 API。将节点的"node_type"配置替换为相应的"node_roles"。例如，以下配置将节点添加到热层和内容层，并使其能够充当引入节点、远程和转换节点。

    
    
    "node_roles": [
      "data_hot",
      "data_content",
      "ingest",
      "remote_cluster_client",
      "transform"
    ],

如果您直接管理自己的集群，请在"elasticsearch.yml"中为每个节点配置适当的角色。例如，以下设置将节点配置为热层和内容层中的仅数据节点。

    
    
    node.roles [ data_hot, data_content ]

#### 从现有 ILM 策略中删除自定义分配设置

更新每个生命周期阶段的分配操作以删除基于属性的分配设置。ILM 将在每个阶段注入迁移操作，以通过数据层自动转换索引。

如果分配操作未设置副本数，请完全删除分配操作。(空分配操作无效。

策略必须为体系结构中的每个数据层指定相应的阶段。每个阶段都必须存在，以便 ILM 可以注入迁移操作以在数据层之间移动索引。如果不需要执行任何其他操作，则阶段可以为空。例如，如果为部署启用暖数据和冷数据层，则策略必须包括热阶段、温阶段和冷阶段。

#### 停止在新索引上设置自定义热属性

创建数据流时，其第一个后备索引现在会自动分配给"data_hot"节点。同样，当您直接创建索引时，它会自动分配给"data_content"节点。

在 Elasticsearch Service 部署中，删除在所有索引上设置热分片分配属性的"云-热-暖-分配-0"索引模板。

    
    
    response = client.indices.delete_template(
      name: '.cloud-hot-warm-allocation-0'
    )
    puts response
    
    
    DELETE _template/.cloud-hot-warm-allocation-0

如果您使用的是自定义索引模板，请对其进行更新以删除用于将新索引分配到热层的基于属性的分配筛选器。

为了完全避免混合层首选项和自定义属性路由设置时出现的问题，我们还建议更新所有旧版、可组合模板和组件模板，以从其配置的设置中删除基于属性的分配筛选器。

#### 为现有索引设置层首选项

ILM 通过自动将迁移操作注入到每个阶段，自动通过可用的数据层转换托管索引。

若要使 ILM 能够通过数据层移动_现有_托管索引，请将索引设置更新为：

1. 通过将自定义分配筛选器设置为"null"来删除它。  2. 设置层首选项。

例如，如果您的旧模板将"data"属性设置为"hot"以将分片分配到热层，请将"data"属性设置为"null"并将"_tier_preference"设置为"data_hot"。

    
    
    response = client.indices.put_settings(
      index: 'my-index',
      body: {
        "index.routing.allocation.require.data": nil,
        "index.routing.allocation.include._tier_preference": 'data_hot'
      }
    )
    puts response
    
    
    PUT my-index/_settings
    {
      "index.routing.allocation.require.data": null,
      "index.routing.allocation.include._tier_preference": "data_hot"
    }

对于已从热阶段转换出来的索引，层首选项应包括适当的回退层，以确保在首选层不可用时可以分配索引分片。例如，将热层指定为已处于暖阶段的索引的回退。

    
    
    response = client.indices.put_settings(
      index: 'my-index',
      body: {
        "index.routing.allocation.require.data": nil,
        "index.routing.allocation.include._tier_preference": 'data_warm,data_hot'
      }
    )
    puts response
    
    
    PUT my-index/_settings
    {
      "index.routing.allocation.require.data": null,
      "index.routing.allocation.include._tier_preference": "data_warm,data_hot"
    }

如果索引已处于冷阶段，请包括冷、暖和热。

对于同时配置了"_tier_preference"和"require.data"但"_tier_preference"已过时的索引(即节点属性配置比配置的"_tier_preference""冷")，迁移需要删除"require.data"属性并更新"_tier_preference"以反映正确的分层。

例如。对于具有以下路由配置的索引：

    
    
    {
      "index.routing.allocation.require.data": "warm",
      "index.routing.allocation.include._tier_preference": "data_hot"
    }

路由配置应按如下方式修复：

    
    
    response = client.indices.put_settings(
      index: 'my-index',
      body: {
        "index.routing.allocation.require.data": nil,
        "index.routing.allocation.include._tier_preference": 'data_warm,data_hot'
      }
    )
    puts response
    
    
    PUT my-index/_settings
    {
      "index.routing.allocation.require.data": null,
      "index.routing.allocation.include._tier_preference": "data_warm,data_hot"
    }

这种情况可能发生在默认为数据层的系统中，例如，当使用节点属性的 ILM 策略恢复并将托管索引从热阶段转换为暖阶段时。在这种情况下，节点属性配置指示应在其中分配索引的正确层。

[« Configure a lifecycle policy](set-up-lifecycle-policy.md)
[Troubleshooting index lifecycle management errors »](index-lifecycle-error-
handling.md)
