

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Set up
Elasticsearch](setup.md)

[« Set up Elasticsearch](setup.md) [Install Elasticsearch from archive on
Linux or MacOS »](targz.md)

## 安装弹性搜索

### 托管弹性搜索服务

Elastic Cloud 提供 Elasticsearch、Kibana 和 Elastic 的可观测性、企业搜索和 Elastic Security 解决方案的所有功能，作为 AWS、GCP 和 Azure 上提供的托管服务。

要在 Elastic Cloud 中设置 Elasticsearch，请注册免费的 Elastic Cloud试用版。

### 自我管理的弹性搜索选项

如果你想自己安装和管理 Elasticsearch，你可以：

* 在任何 Linux、MacOS 或 Windows 机器上运行 Elasticsearch。  
* 在 Docker 容器中运行 Elasticsearch。  
* 使用 Kubernetes 上的 Elastic Cloud 在 Kubernetes 上设置和管理 Elasticsearch、Kibana、Elastic Agent 和 Elastic Stack 的其余部分。

要在您自己的机器上试用 Elasticsearch，我们建议使用 Docker 并同时运行 Elasticsearch 和 Kibana。

### Elasticsearch install packages

Elasticsearch 以以下包格式提供：

Linux 和 MacOS "tar.gz"存档

| "tar.gz"存档可用于安装在任何Linux发行版和MacOS上。

在 Linux 或 MacOS 上从存档安装 Elasticsearch ---|--- Windows '.zip' 存档

| "zip"存档适合在Windows上安装。

在 Windows 'deb' 上安装 Elasticsearch with '.zip'

| "deb"软件包适用于Debian，Ubuntu和其他基于Debian的系统。Debian 软件包可以从 Elasticsearch 网站或我们的 Debian 仓库下载。

使用 Debian 软件包 'rpm' 安装 Elasticsearch

| "rpm"软件包适合安装在Red Hat，Centos，SLES，OpenSuSE和其他基于RPM的系统上。RPM 可以从 Elasticsearch 网站或我们的 RPM 存储库下载。

使用 RPM 'docker' 安装 Elasticsearch

| 镜像可用于将 Elasticsearch 作为 Docker 容器运行。它们可能是从 Elastic Docker 注册表下载的。

使用 Docker 安装 Elasticsearch ### Java (JVM)Versionedit

Elasticsearch是使用Java构建的，在每个发行版中都包含来自JDK维护者(GPLv2 + CE)的OpenJDK捆绑版本。捆绑的 JVM 是推荐的 JVM。

要使用您自己的 Java 版本，请设置"ES_JAVA_HOME"环境变量。如果必须使用与捆绑的 JVM 不同的 Java 版本，最好使用受支持的 LTS 版本的 Java 的最新版本。Elasticsearch 与某些特定于 OpenJDK 的功能紧密耦合，因此它可能无法与其他 JVM 正常工作。 如果使用已知错误的 Java 版本，Elasticsearch 将拒绝启动。

如果您使用的 JVM 不是捆绑的 JVM，那么您有责任对与其安全问题和错误修复相关的公告做出反应，并且必须自己确定每个更新是否必要。相比之下，捆绑的 JVM 被视为 Elasticsearch 不可或缺的一部分，这意味着 Elastic 负责使其保持最新状态。捆绑的JVM中的安全问题和错误被视为在Elasticsearch本身中。

捆绑的 JVM 位于 Elasticsearchhome 目录的 'jdk' 子目录中。如果使用自己的 JVM，则可以删除此目录。

[« Set up Elasticsearch](setup.md) [Install Elasticsearch from archive on
Linux or MacOS »](targz.md)
