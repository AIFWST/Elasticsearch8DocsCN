

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Restore from snapshot](restore-from-snapshot.md) [Addressing repeated
snapshot policy failures »](repeated-snapshot-failures.md)

## 多个部署到同一快照存储库

多个 Elasticsearch 部署正在写入同一个快照存储库。Elasticsearch 不支持此配置，只允许一个集群写入同一个仓库。请参阅存储库内容，了解存储库内容损坏的潜在副作用，以下指南可能无法解决这些副作用。要纠正这种情况，请将存储库标记为只读或将其从所有其他部署中删除，然后在当前部署中重新添加(重新创建)存储库：

弹性搜索服务 自我管理

修复损坏的存储库将需要在写入同一快照存储库的多个部署中进行更改。只有一个部署必须写入存储库。将继续写入存储库的部署将称为"主"部署(当前集群)，而我们将存储库标记为只读的其他部署称为"辅助"部署。

首先在辅助部署上将存储库标记为只读：

**使用 Kibana**

1. 登录弹性云控制台。  2. 在"弹性搜索服务"面板上，单击部署的名称。

如果您的部署名称被禁用，您的 Kibana 实例可能运行状况不佳，在这种情况下，请联系 ElasticSupport。如果您的部署不包含 Kibana，您需要做的就是先启用它。

3. 打开部署的侧面导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **堆栈管理>快照和还原>存储库**。

!木花控制台

4. 存储库表现在应该可见。单击存储库右侧的铅笔图标以标记为只读。在打开的"编辑"页面上，向下滚动并选中"只读存储库"。点击"保存"。或者，如果最好完全删除存储库，请选中存储库表中存储库名称左侧的复选框，然后单击表左上角的"删除存储库"红色按钮。

此时，只有将存储库标记为可写的主(当前)部署。Elasticsearch认为它是损坏的，所以需要删除并重新添加存储库，以便Elasticsearch可以恢复使用它：

请注意，我们现在正在配置主(当前)部署。

1. 打开主部署的侧面导航菜单(位于左上角的 Elastic 徽标下方)，然后转到 **堆栈管理>快照和还原>存储库**。

!木花控制台

2. 单击存储库右侧的铅笔图标。在打开的"编辑"页面上，向下滚动并单击"保存"，而不对现有设置进行任何更改。

修复损坏的存储库需要在写入同一快照存储库的多个群集中进行更改。只有一个集群必须写入存储库。让我们将要继续写入存储库的集群称为"主"集群(当前集群)，而将存储库标记为只读的其他集群称为"辅助"集群。

让我们首先处理辅助集群：

1. 获取存储库的配置：响应 = client.snapshot.get_repository(存储库："我的存储库")将响应 GET _snapshot/my-repo

响应将如下所示：

    
        {
      "my-repo": { __"type": "s3",
        "settings": {
          "bucket": "repo-bucket",
          "client": "elastic-internal-71bcd3",
          "base_path": "myrepo"
        }
      }
    }

__

|

表示存储库的当前配置。   ---|--- 2.使用上面检索到的设置，添加"只读：true"选项以将其标记为只读： PUT _snapshot/my-repo { "type"： "s3"， "settings"： { "bucket"： "repo-bucket"， "client"： "elastic-internal-71bcd3"， "base_path"： "myrepo"， "readonly"： true __} }

__

|

将存储库标记为只读。   ---|--- 3.或者，删除存储库是一个选项，使用：响应 = client.snapshot.delete_repository(存储库："my-repo")放置响应删除_snapshot/my-repo

响应将如下所示：

    
        {
      "acknowledged": true
    }

此时，只有主(当前)集群将存储库标记为可写。Elasticsearch认为它是损坏的，所以让我们重新创建它，以便Elasticsearch可以恢复使用它。请注意，现在我们正在配置主(当前)集群：

1. 获取存储库的配置并保存其配置，因为我们将使用它来重新创建存储库： 响应 = client.snapshot.get_repository( 存储库："my-repo" ) 放置响应 获取_snapshot/my-repo

2. 使用我们上面获得的配置，让我们重新创建存储库： PUT _snapshot/my-repo { "type"： "s3"， "settings"： { "bucket"： "repo-bucket"， "client"： "elastic-internal-71bcd3"， "base_path"： "myrepo" } }

响应将如下所示：

    
        {
      "acknowledged": true
    }

[« Restore from snapshot](restore-from-snapshot.md) [Addressing repeated
snapshot policy failures »](repeated-snapshot-failures.md)
