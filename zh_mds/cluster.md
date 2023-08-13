

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md)

[« cat transforms API](cat-transforms.md) [Cluster allocation explain API
»](cluster-allocation-explain.md)

## 集群接口

### 节点规范

某些集群级 API 可能会在可以使用_node filters_指定的节点子集上运行。例如，任务管理、节点统计信息和节点信息 API 都可以报告来自一组筛选节点而不是所有节点的结果。

_Node filters_以逗号分隔的单个筛选器列表的形式编写，每个筛选器都在所选子集中添加或删除节点。每个筛选器可以是以下筛选器之一：

* "_all"，将所有节点添加到子集。  * "_local"，将本地节点添加到子集中。  * "_master"，将当前选择的主节点添加到子集中。  * 节点 ID 或名称，用于将此节点添加到子集。  * IP 地址或主机名，用于将所有匹配的节点添加到子集。  * 一种模式，使用"*"通配符，将所有节点添加到名称、地址或主机名与模式匹配的子集中。  * "master：true"、"data：true"、"ingest：true"、"voting_only：true"、"ml：true"或"coordinating_only：true"，它们分别将所有符合主节点条件的节点、所有数据节点、所有摄取节点、所有仅投票节点、所有机器学习节点和所有仅协调节点添加到子集中。  * "master：false"、"data：false"、"ingest：false"、"voting_only：true"、"ml：false"或"coordinating_only：false"，分别从子集中删除所有符合主节点条件的节点、所有数据节点、所有摄取节点、所有仅投票节点、所有机器学习节点和所有仅协调节点。  * 一对模式，使用"*"通配符，格式为"attrname：attrvalue"，它将具有自定义节点属性的所有节点添加到子集中，该节点属性的名称和值与相应的模式匹配。自定义节点属性是通过在配置文件中设置属性来配置的，格式为"node.attr.attrname： attrvalue"。

节点筛选器按给定顺序运行，如果使用从集合中删除节点的筛选器，这一点很重要。例如，"_all，master：false"表示除符合主节点条件的节点之外的所有节点，但"master：false，_all"表示与"_all"相同，因为"_all"过滤器在"master：false"过滤器之后运行。

如果未给出筛选器，则默认为选择所有节点。但是，如果给出了任何过滤器，则它们从空的选定子集开始运行。这意味着从所选子集中删除节点的过滤器(如 'master：false' )只有在它们出现在其他过滤器之后时才有用。当在其播种上使用时，"master：false"不选择任何节点。

以下是将节点筛选器与 NodesInfo API 结合使用的一些示例。

    
    
    response = client.nodes.info
    puts response
    
    response = client.nodes.info(
      node_id: '_all'
    )
    puts response
    
    response = client.nodes.info(
      node_id: '_local'
    )
    puts response
    
    response = client.nodes.info(
      node_id: '_master'
    )
    puts response
    
    response = client.nodes.info(
      node_id: 'node_name_goes_here'
    )
    puts response
    
    response = client.nodes.info(
      node_id: 'node_name_goes_*'
    )
    puts response
    
    response = client.nodes.info(
      node_id: '10.0.0.3,10.0.0.4'
    )
    puts response
    
    response = client.nodes.info(
      node_id: '10.0.0.*'
    )
    puts response
    
    response = client.nodes.info(
      node_id: '_all,master:false'
    )
    puts response
    
    response = client.nodes.info(
      node_id: 'data:true,ingest:true'
    )
    puts response
    
    response = client.nodes.info(
      node_id: 'coordinating_only:true'
    )
    puts response
    
    response = client.nodes.info(
      node_id: 'master:true,voting_only:false'
    )
    puts response
    
    response = client.nodes.info(
      node_id: 'rack:2'
    )
    puts response
    
    response = client.nodes.info(
      node_id: 'ra*:2'
    )
    puts response
    
    response = client.nodes.info(
      node_id: 'ra*:2*'
    )
    puts response
    
    
    # If no filters are given, the default is to select all nodes
    GET /_nodes
    # Explicitly select all nodes
    GET /_nodes/_all
    # Select just the local node
    GET /_nodes/_local
    # Select the elected master node
    GET /_nodes/_master
    # Select nodes by name, which can include wildcards
    GET /_nodes/node_name_goes_here
    GET /_nodes/node_name_goes_*
    # Select nodes by address, which can include wildcards
    GET /_nodes/10.0.0.3,10.0.0.4
    GET /_nodes/10.0.0.*
    # Select nodes by role
    GET /_nodes/_all,master:false
    GET /_nodes/data:true,ingest:true
    GET /_nodes/coordinating_only:true
    GET /_nodes/master:true,voting_only:false
    # Select nodes by custom attribute (e.g. with something like `node.attr.rack: 2` in the configuration file)
    GET /_nodes/rack:2
    GET /_nodes/ra*:2
    GET /_nodes/ra*:2*

[« cat transforms API](cat-transforms.md) [Cluster allocation explain API
»](cluster-allocation-explain.md)
