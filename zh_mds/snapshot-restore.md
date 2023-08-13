

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« Tutorial: Disaster recovery based on bi-directional cross-cluster
replication](ccr-disaster-recovery-bi-directional-tutorial.md) [Register a
snapshot repository »](snapshots-register-repository.md)

# 快照和恢复

快照是正在运行的 Elasticsearch 集群的备份。您可以使用快照执行以下操作：

* 定期备份集群，无需停机 * 删除或硬件故障后恢复数据 * 在集群之间传输数据 * 通过在冷数据和冻结数据层中使用可搜索快照来降低存储成本

## 快照工作流

Elasticsearch 将快照存储在称为快照存储库的集群外存储位置。在拍摄或还原快照之前，必须在集群上注册快照存储库。Elasticsearch 支持多种存储库类型以及云存储选项，包括：

* AWS S3 * Google Cloud Storage (GCS) * Microsoft Azure

注册快照存储库后，您可以使用快照生命周期管理 (SLM) 自动拍摄和管理快照。然后，您可以还原快照以恢复或传输其数据。

## 快照内容

默认情况下，集群的快照包含集群状态、所有常规数据流和所有常规索引。群集状态包括：

* 持久群集设置 * 索引模板 * 旧索引模板 * 引入管道 * ILM 策略 * 对于 7.12.0 之后拍摄的快照，功能状态

您还可以仅拍摄集群中特定数据流或索引的快照。包含数据流或索引的快照会自动包含其别名。还原快照时，可以选择是否还原这些别名。

快照不包含或备份：

* 瞬态群集设置 * 已注册的快照存储库 * 节点配置文件 * 安全配置文件

### 功能状态

功能状态包含用于存储 Elastic 功能(如 Elasticsearch 安全性或 Kibana)的配置、历史记录和其他数据的索引和数据流。

若要检索功能状态列表，请使用功能 API。

功能状态通常包括一个或多个系统索引或系统数据流。它还可能包括功能使用的常规索引和数据流。例如，特征状态可能包括包含特征执行历史记录的常规索引。将此历史记录存储在常规索引中可以更轻松地搜索它。

在 Elasticsearch 8.0 及更高版本中，功能状态是备份和恢复系统索引和系统数据流的唯一方法。

## 快照的工作原理

快照会自动重复数据删除，以节省存储空间并降低网络传输成本。要备份索引，快照会复制索引的段并将其存储在快照存储库中。由于段是不可变的，因此快照只需复制自存储库上次快照以来创建的任何新段。

每个快照在逻辑上也是独立的。删除快照时，Elasticsearch 只会删除该快照独占使用的分段。Elasticsearch 不会删除存储库中其他快照使用的区段。

### 快照和分片分配

快照从索引的主分片复制段。当您启动快照时，Elasticsearch 会立即开始复制任何可用主分片的段。如果分片正在启动或重新定位，Elasticsearch 将等待这些进程完成，然后再复制分片的段。如果一个或多个主分片不可用，快照尝试将失败。

一旦快照开始复制分片的段，Elasticsearch 就不会将分片移动到另一个节点，即使重新平衡或分片分配设置通常会触发重新分配。Elasticsearch 只会在快照完成复制分片数据后移动分片。

### 快照启动和停止时间

快照不代表精确时间点的集群。相反，每个快照都包含开始和结束时间。快照表示在这两个时间之间的某个时间点的每个分片数据的视图。

## 快照兼容性

要将快照还原到集群，快照、集群和任何还原索引的版本必须兼容。

### 快照版本兼容性

您无法将快照恢复到早期版本的 Elasticsearch。例如，您无法将 7.6.0 中拍摄的快照还原到运行 7.5.0 的集群。

### 索引兼容性

从快照还原的任何索引也必须与当前群集的版本兼容。如果尝试还原在不兼容版本中创建的索引，则还原尝试将失败。

|

集群版本** ---|--- 索引创建版本**

|

6.8

|

7.0–7.1

|

7.2–7.17

|

8.0–8.2

|

8.3-8.9    5.0–5.6

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!是[1] 6.0–6.7

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!是[1] 6.8

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

!是[1] 7.0–7.1

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 7.2–7.17

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 8.0–8.9

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![No](https://doc-icons.s3.us-east-2.amazonaws.com/icon-no.png)

|

![Yes](https://doc-icons.s3.us-east-2.amazonaws.com/icon-yes.png)

|

!是 1\。支持存档索引。

您无法将索引恢复到早期版本的 Elasticsearch。例如，无法将 7.6.0 中创建的索引还原到运行 7.5.0 的集群。

兼容快照可以包含在较旧的不兼容版本中创建的索引。例如，7.17 集群的快照可以包含 6.8 中创建的索引。将 6.8 索引还原到 8.9 集群将失败，除非您可以使用存档功能。如果在升级集群之前拍摄快照，请记住这一点。

作为一种解决方法，您可以先将索引还原到运行最新版本 Elasticsearch 的另一个集群，该集群与索引和当前集群兼容。然后，您可以使用远程重新索引在当前集群上重建索引。仅当启用了索引的"_source"时，才能从远程重新索引。

从远程重新索引可能比还原快照花费更长的时间。在开始之前，请使用数据子集测试远程进程的重新索引，以估计您的时间要求。

##Warnings

### 其他备份方法

**拍摄快照是备份集群的唯一可靠且受支持的方法。 您无法通过复制 Elasticsearch 集群节点的数据目录来备份集群。没有支持的方法可以从文件系统级备份恢复任何数据。如果尝试从此类备份还原群集，则群集可能会失败，并报告损坏或丢失文件或其他数据不一致，或者看起来已成功丢失某些数据。

群集节点的数据目录的副本不能用作备份，因为它不是其内容在单个时间点的一致表示形式。您无法通过在创建副本时关闭节点或拍摄原子文件系统级快照来解决此问题，因为 Elasticsearch 具有跨越整个集群的一致性要求。必须对群集备份使用内置快照功能。

### 存储库内容

**不要修改存储库中的任何内容或运行可能干扰其内容的进程。 如果 Elasticsearch 以外的内容修改了存储库的内容，那么将来的快照或还原操作可能会失败，报告损坏或其他数据不一致，或者可能会在静默丢失某些数据后看起来成功。

但是，您可以安全地从备份还原存储库只要

1. 当您恢复存储库的内容时，存储库未在 Elasticsearch 中注册。  2. 恢复完存储库后，其内容与备份时完全相同。

如果您不再需要存储库中的任何快照，请先从 Elasticsearch 注销该快照，然后再从底层存储中删除其内容。

此外，快照可能包含安全敏感信息，您可能希望将其存储在专用存储库中。

[« Tutorial: Disaster recovery based on bi-directional cross-cluster
replication](ccr-disaster-recovery-bi-directional-tutorial.md) [Register a
snapshot repository »](snapshots-register-repository.md)
