

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Troubleshooting](troubleshooting.md)

[« Troubleshooting transforms](transform-troubleshooting.md)
[Troubleshooting searches »](troubleshooting-searches.md)

## 疑难解答观察程序

### 尝试添加监视时出现动态映射错误

如果您在尝试添加 awatch 时收到"_Dynamic映射Disabled_"错误，请验证".watches"索引的索引映射是否可用。您可以通过提交以下请求来执行此操作：

    
    
    response = client.indices.get_mapping(
      index: '.watches'
    )
    puts response
    
    
    GET .watches/_mapping

如果缺少索引映射，请按照以下步骤还原正确的映射：

1. 停止 Elasticsearch 节点。  2. 将"xpack.watcher.index.rest.direct_access：true"添加到"elasticsearch.yml"。  3. 重新启动 Elasticsearch 节点。  4. 删除 '.watches' 索引： response = client.index.delete( index： '.watches' ) 放置响应 删除 .watches

5. 禁用对".watches"索引的直接访问：

    1. Stop the Elasticsearch node. 
    2. Remove `xpack.watcher.index.rest.direct_access : true` from `elasticsearch.yml`. 
    3. Restart the Elasticsearch node. 

### 无法发送电子邮件

如果您在 Watcher 尝试发送电子邮件时收到身份验证错误，指示您需要从网络浏览器继续登录过程，则需要将 Gmail 配置为允许安全性较低的应用访问您的帐号。

如果为电子邮件帐户启用了双重验证，则必须生成并使用应用特定密码才能从 Watcher 发送电子邮件。有关详细信息，请参阅：

* Gmail：使用应用专用密码登录 * Outlook.com：应用专用密码和两步验证

### 观察程序无响应

请记住，没有内置的脚本验证添加到 awatch。有缺陷或故意恶意的脚本可能会对观察程序性能产生负面影响。例如，如果在短时间内添加多个具有错误脚本条件的监视，则 Watcher 可能会暂时无法处理监视，直到错误的监视超时。

[« Troubleshooting transforms](transform-troubleshooting.md)
[Troubleshooting searches »](troubleshooting-searches.md)
