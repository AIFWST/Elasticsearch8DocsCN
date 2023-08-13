

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Troubleshooting](troubleshooting.md) [Fix watermark errors »](fix-
watermark-errors.md)

## 修复常见集群问题

本指南介绍如何修复 Elasticsearchcluster 的常见错误和问题。

水印错误

     Fix watermark errors that occur when a data node is critically low on disk space and has reached the flood-stage disk usage watermark. 
[Circuit breaker errors](circuit-breaker-errors.html "Circuit breaker errors")

     Elasticsearch uses circuit breakers to prevent nodes from running out of JVM heap memory. If Elasticsearch estimates an operation would exceed a circuit breaker, it stops the operation and returns an error. 
[High CPU usage](high-cpu-usage.html "High CPU usage")

     The most common causes of high CPU usage and their solutions. 
[High JVM memory pressure](high-jvm-memory-pressure.html "High JVM memory
pressure")

     High JVM memory usage can degrade cluster performance and trigger circuit breaker errors. 
[Red or yellow cluster status](red-yellow-cluster-status.html "Red or yellow
cluster status")

     A red or yellow cluster status indicates one or more shards are missing or unallocated. These unassigned shards increase your risk of data loss and can degrade cluster performance. 
[Rejected requests](rejected-requests.html "Rejected requests")

     When Elasticsearch rejects a request, it stops the operation and returns an error with a `429` response code. 
[Task queue backlog](task-queue-backlog.html "Task queue backlog")

     A backlogged task queue can prevent tasks from completing and put the cluster into an unhealthy state. 
[Diagnose unassigned shards](diagnose-unassigned-shards.html "Diagnose
unassigned shards")

     There are multiple reasons why shards might get unassigned, ranging from misconfigured allocation settings to lack of disk space. 
[Troubleshooting an unstable cluster](cluster-fault-detection.html#cluster-
fault-detection-troubleshooting "Troubleshooting an unstable cluster")

     A cluster in which nodes leave unexpectedly is unstable and can create several issues. 
[Mapping explosion](mapping-explosion.html "Mapping explosion")

     A cluster in which an index or index pattern as exploded with a high count of mapping fields which causes performance look-up issues for Elasticsearch and Kibana. 
[Hot spotting](hotspotting.html "Hot spotting")

     Hot spotting may occur in Elasticsearch when resource utilizations are unevenly distributed across nodes. 

[« Troubleshooting](troubleshooting.md) [Fix watermark errors »](fix-
watermark-errors.md)
