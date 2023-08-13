

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Cluster APIs](cluster.md)

[« Cluster APIs](cluster.md) [Cluster get settings API »](cluster-get-
settings.md)

## 集群分配说明API

提供分片当前分配的说明。

    
    
    response = client.cluster.allocation_explain(
      body: {
        index: 'my-index-000001',
        shard: 0,
        primary: false,
        current_node: 'my-node'
      }
    )
    puts response
    
    
    GET _cluster/allocation/explain
    {
      "index": "my-index-000001",
      "shard": 0,
      "primary": false,
      "current_node": "my-node"
    }

###Request

"获取_cluster/分配/解释"

"发布_cluster/分配/解释"

###Prerequisites

* 如果启用了 Elasticsearch 安全功能，您必须具有"监控"或"管理"集群权限才能使用此 API。

###Description

集群分配说明 API 的目的是为集群中的分片分配提供说明。对于未分配的分片，说明 API 提供了未分配分片原因的说明。对于分配的分片，explain API 解释了为什么分片保留在其当前节点上，并且没有移动或重新平衡到另一个节点。在尝试诊断分片未分配的原因或为什么 ashard 继续保留在其当前节点上时，此 API 非常有用，而您可能期望并非如此。

### 查询参数

`include_disk_info`

     (Optional, Boolean) If `true`, returns information about disk usage and shard sizes. Defaults to `false`. 
`include_yes_decisions`

     (Optional, Boolean) If `true`, returns _YES_ decisions in explanation. Defaults to `false`. 

### 请求正文

`current_node`

     (Optional, string) Specifies the node ID or the name of the node currently holding the shard to explain. To explain an unassigned shard, omit this parameter. 
`index`

     (Optional, string) Specifies the name of the index that you would like an explanation for. 
`primary`

     (Optional, Boolean) If `true`, returns explanation for the primary shard for the given shard ID. 
`shard`

     (Optional, integer) Specifies the ID of the shard that you would like an explanation for. 

###Examples

#### 未分配的主分片

以下请求获取未分配的主分片的分配说明。

    
    
    response = client.cluster.allocation_explain(
      body: {
        index: 'my-index-000001',
        shard: 0,
        primary: true
      }
    )
    puts response
    
    
    GET _cluster/allocation/explain
    {
      "index": "my-index-000001",
      "shard": 0,
      "primary": true
    }

API 响应指示分片只能分配给不存在的节点。

    
    
    {
      "index" : "my-index-000001",
      "shard" : 0,
      "primary" : true,
      "current_state" : "unassigned",                 __"unassigned_info" : {
        "reason" : "INDEX_CREATED", __"at" : "2017-01-04T18:08:16.600Z",
        "last_allocation_status" : "no"
      },
      "can_allocate" : "no", __"allocate_explanation" : "Elasticsearch isn't allowed to allocate this shard to any of the nodes in the cluster. Choose a node to which you expect this shard to be allocated, find this node in the node-by-node explanation, and address the reasons which prevent Elasticsearch from allocating this shard there.",
      "node_allocation_decisions" : [
        {
          "node_id" : "8qt2rY-pT6KNZB3-hGfLnw",
          "node_name" : "node-0",
          "transport_address" : "127.0.0.1:9401",
          "node_attributes" : {},
          "node_decision" : "no", __"weight_ranking" : 1,
          "deciders" : [
            {
              "decider" : "filter", __"decision" : "NO",
              "explanation" : "node does not match index setting [index.routing.allocation.include] filters [_name:\"nonexistent_node\"]" __}
          ]
        }
      ]
    }

__

|

分片的当前状态。   ---|---    __

|

分片最初变得未分配的原因。   __

|

是否分配分片。   __

|

是否将分片分配给特定节点。   __

|

导致节点做出"否"决策的决策程序。   __

|

解释为什么决策程序返回"否"决策，并附有指向导致决策的设置的有用提示。   以下响应包含之前分配的未分配主分片的分配说明。

    
    
    {
      "index" : "my-index-000001",
      "shard" : 0,
      "primary" : true,
      "current_state" : "unassigned",
      "unassigned_info" : {
        "reason" : "NODE_LEFT",
        "at" : "2017-01-04T18:03:28.464Z",
        "details" : "node_left[OIWe8UhhThCK0V5XfmdrmQ]",
        "last_allocation_status" : "no_valid_shard_copy"
      },
      "can_allocate" : "no_valid_shard_copy",
      "allocate_explanation" : "Elasticsearch can't allocate this shard because there are no copies of its data in the cluster. Elasticsearch will allocate this shard when a node holding a good copy of its data joins the cluster. If no such node is available, restore this index from a recent snapshot."
    }

#### 未分配的副本分片

以下响应包含由于分配延迟而日照分配的副本的分配说明。

    
    
    {
      "index" : "my-index-000001",
      "shard" : 0,
      "primary" : false,
      "current_state" : "unassigned",
      "unassigned_info" : {
        "reason" : "NODE_LEFT",
        "at" : "2017-01-04T18:53:59.498Z",
        "details" : "node_left[G92ZwuuaRY-9n8_tc-IzEg]",
        "last_allocation_status" : "no_attempt"
      },
      "can_allocate" : "allocation_delayed",
      "allocate_explanation" : "The node containing this shard copy recently left the cluster. Elasticsearch is waiting for it to return. If the node does not return within [%s] then Elasticsearch will allocate this shard to another node. Please wait.",
      "configured_delay" : "1m",                      __"configured_delay_in_millis" : 60000,
      "remaining_delay" : "59.8s", __"remaining_delay_in_millis" : 59824,
      "node_allocation_decisions" : [
        {
          "node_id" : "pmnHu_ooQWCPEFobZGbpWw",
          "node_name" : "node_t2",
          "transport_address" : "127.0.0.1:9402",
          "node_decision" : "yes"
        },
        {
          "node_id" : "3sULLVJrRneSg0EfBB-2Ew",
          "node_name" : "node_t0",
          "transport_address" : "127.0.0.1:9400",
          "node_decision" : "no",
          "store" : { __"matching_size" : "4.2kb",
            "matching_size_in_bytes" : 4325
          },
          "deciders" : [
            {
              "decider" : "same_shard",
              "decision" : "NO",
              "explanation" : "a copy of this shard is already allocated to this node [[my-index-000001][0], node[3sULLVJrRneSg0EfBB-2Ew], [P], s[STARTED], a[id=eV9P8BN1QPqRc3B4PLx6cg]]"
            }
          ]
        }
      ]
    }

__

|

分配副本分片之前配置的延迟，该副本分片由于持有副本分片的节点离开集群而不存在。   ---|---    __

|

分配副本分片之前的剩余延迟。   __

|

有关在节点上找到的分片数据的信息。   #### 已分配分片编辑

以下响应包含已分配分片的分配说明。响应指示不允许分片保留在其当前节点上，必须重新分配。

    
    
    {
      "index" : "my-index-000001",
      "shard" : 0,
      "primary" : true,
      "current_state" : "started",
      "current_node" : {
        "id" : "8lWJeJ7tSoui0bxrwuNhTA",
        "name" : "node_t1",
        "transport_address" : "127.0.0.1:9401"
      },
      "can_remain_on_current_node" : "no",            __"can_remain_decisions" : [ __{
          "decider" : "filter",
          "decision" : "NO",
          "explanation" : "node does not match index setting [index.routing.allocation.include] filters [_name:\"nonexistent_node\"]"
        }
      ],
      "can_move_to_other_node" : "no", __"move_explanation" : "This shard may not remain on its current node, but Elasticsearch isn't allowed to move it to another node. Choose a node to which you expect this shard to be allocated, find this node in the node-by-node explanation, and address the reasons which prevent Elasticsearch from allocating this shard there.",
      "node_allocation_decisions" : [
        {
          "node_id" : "_P8olZS8Twax9u6ioN-GGA",
          "node_name" : "node_t0",
          "transport_address" : "127.0.0.1:9400",
          "node_decision" : "no",
          "weight_ranking" : 1,
          "deciders" : [
            {
              "decider" : "filter",
              "decision" : "NO",
              "explanation" : "node does not match index setting [index.routing.allocation.include] filters [_name:\"nonexistent_node\"]"
            }
          ]
        }
      ]
    }

__

|

是否允许分片保留在其当前节点上。   ---|---    __

|

决定为什么不允许分片保留在其当前节点上的决策因素。   __

|

是否允许将分片分配给另一个节点。   以下响应包含必须保留在其当前节点上的分片的分配说明。将分片移动到另一个节点不会改善集群平衡。

    
    
    {
      "index" : "my-index-000001",
      "shard" : 0,
      "primary" : true,
      "current_state" : "started",
      "current_node" : {
        "id" : "wLzJm4N4RymDkBYxwWoJsg",
        "name" : "node_t0",
        "transport_address" : "127.0.0.1:9400",
        "weight_ranking" : 1
      },
      "can_remain_on_current_node" : "yes",
      "can_rebalance_cluster" : "yes",                __"can_rebalance_to_other_node" : "no", __"rebalance_explanation" : "Elasticsearch cannot rebalance this shard to another node since there is no node to which allocation is permitted which would improve the cluster balance. If you expect this shard to be rebalanced to another node, find this node in the node-by-node explanation and address the reasons which prevent Elasticsearch from rebalancing this shard there.",
      "node_allocation_decisions" : [
        {
          "node_id" : "oE3EGFc8QN-Tdi5FFEprIA",
          "node_name" : "node_t1",
          "transport_address" : "127.0.0.1:9401",
          "node_decision" : "worse_balance", __"weight_ranking" : 1
        }
      ]
    }

__

|

是否允许在群集上重新平衡。   ---|---    __

|

分片是否可以重新平衡到另一个节点。   __

|

分片无法重新平衡到节点的原因，在这种情况下表明它没有提供比当前节点更好的平衡。   #### 无参数编辑

如果您调用不带参数的 API，Elasticsearch 将检索任意未分配的主分片或副本分片的分配说明。

    
    
    response = client.cluster.allocation_explain
    puts response
    
    
    GET _cluster/allocation/explain

如果集群不包含未分配的分片，API 将返回"400"错误。

[« Cluster APIs](cluster.md) [Cluster get settings API »](cluster-get-
settings.md)
