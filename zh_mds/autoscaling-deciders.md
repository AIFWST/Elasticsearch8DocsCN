

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Autoscaling](xpack-autoscaling.md)

[« Autoscaling](xpack-autoscaling.md) [Reactive storage decider
»](autoscaling-reactive-storage-decider.md)

## 自动缩放决策程序

反应式存储决策程序

     Estimates required storage capacity of current data set. Available for policies governing data nodes. 
[Proactive storage decider](autoscaling-proactive-storage-decider.html
"Proactive storage decider")

     Estimates required storage capacity based on current ingestion into hot nodes. Available for policies governing hot data nodes. 
[Frozen shards decider](autoscaling-frozen-shards-decider.html "Frozen shards
decider")

     Estimates required memory capacity based on the number of partially mounted shards. Available for policies governing frozen data nodes. 
[Frozen storage decider](autoscaling-frozen-storage-decider.html "Frozen
storage decider")

     Estimates required storage capacity as a percentage of the total data set of partially mounted indices. Available for policies governing frozen data nodes. 
[Frozen existence decider](autoscaling-frozen-existence-decider.html "Frozen
existence decider")

     Estimates a minimum require frozen memory and storage capacity when any index is in the frozen [ILM](index-lifecycle-management.html "ILM: Manage the index lifecycle") phase. 
[Machine learning decider](autoscaling-machine-learning-decider.html "Machine
learning decider")

     Estimates required memory capacity based on machine learning jobs. Available for policies governing machine learning nodes. 
[Fixed decider](autoscaling-fixed-decider.html "Fixed decider")

     Responds with a fixed required capacity. This decider is intended for testing only. 

[« Autoscaling](xpack-autoscaling.md) [Reactive storage decider
»](autoscaling-reactive-storage-decider.md)
