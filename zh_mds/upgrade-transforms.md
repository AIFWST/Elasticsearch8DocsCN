

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[REST
APIs](rest-apis.md) ›[Transform APIs](transform-apis.md)

[« Update transform API](update-transform.md) [Usage API »](usage-api.md)

## 升级转换接口

升级所有转换。

###Request

"发布_transform/_upgrade"

###Prerequisites

需要以下权限：

* 群集："manage_transform"("transform_admin"内置角色授予此权限)

###Description

转换在次要版本之间以及支持的主要版本之间兼容。但是，随着时间的推移，转换配置信息的格式可能会更改。此 API 识别具有旧版配置格式的转换，并将其升级到最新版本;包括清理存储转换状态和检查点的内部数据结构。转换升级不会影响源索引和目标索引。

如果转换升级步骤失败，升级将停止，并返回有关基础问题的错误。解决问题，然后再次重新运行该过程。升级完成后将返回摘要。

为了确保连续转换在群集的主要版本升级期间(例如，从 7.16 升级到 8.0)保持运行，建议在升级群集之前升级转换。您可能需要在升级之前执行最近的群集备份。

* 启用 Elasticsearch 安全功能后，您的转换会记住上次创建或更新它的用户的角色。与更新转换相反，转换升级不会更改存储的角色，因此用于读取源数据和写入目标索引的角色保持不变。

### 查询参数

`dry_run`

     (Optional, Boolean) When `true`, only checks for updates but does not execute them. Defaults to `false`. 
`timeout`

     (Optional, time) Period to wait for a response. If no response is received before the timeout expires, the request fails and returns an error. Defaults to `30s`. 

### 响应正文

`needs_update`

     (integer) The number of transforms that need to be upgraded. 
`no_action`

     (integer) The number of transforms that don't require upgrading. 
`updated`

     (integer) The number of transforms that have been upgraded. 

###Examples

要将旧版转换升级到最新配置格式，请执行以下 API 调用：

    
    
    response = client.transform.upgrade_transforms
    puts response
    
    
    POST _transform/_upgrade

升级所有转换后，您会收到一个摘要：

    
    
    {
      "needs_update": 0,
      "updated": 2,
      "no_action": 1
    }

[« Update transform API](update-transform.md) [Usage API »](usage-api.md)
