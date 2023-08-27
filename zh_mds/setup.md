

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)

[« What's new in 8.9](release-highlights.md) [Installing Elasticsearch
»](install-elasticsearch.md)

# 设置Elasticsearch

本节包含有关如何设置 Elasticsearch 并使其运行的信息，包括：

* 下载 * 安装 * 开始 * 配置

## 支持的平台

官方支持的操作系统和 JVM 矩阵可在此处获得：支持矩阵。Elasticsearch在列出的平台上进行了测试，但它也可能在其他平台上工作。

## 使用专用主机

在生产环境中，我们建议您在专用主机上或作为主服务运行 Elasticsearch。一些 Elasticsearch 功能，例如自动 JVM 堆大小，会假设ElasticSearch是主机或容器上唯一的资源密集型应用程序。例如，您可以运行 Metricbeat 和 Elasticsearch 来获取集群统计信息，但资源密集型 Logstash 部署应该在其自己的主机上进行。

[« What's new in 8.9](release-highlights.md) [Installing Elasticsearch
»](install-elasticsearch.md)
