

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md)

[« Watching the status of an Elasticsearch cluster](watch-cluster-status.md)
[Command line tools »](commands.md)

## 观察程序限制

### 基于文件的脚本更改时不更新监视

在监视中引用文件脚本时，如果更改文件系统上的脚本，则不会更新监视本身。

目前，在监视中重新加载文件脚本的唯一方法是删除监视并重新创建它。

### 安全集成

启用安全功能后，监视将存储有关存储监视的用户在当时执行的内容的信息。这意味着，如果这些权限随时间而更改，监视仍可使用创建监视时存在的权限执行。

[« Watching the status of an Elasticsearch cluster](watch-cluster-status.md)
[Command line tools »](commands.md)
