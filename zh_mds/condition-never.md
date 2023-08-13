

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher conditions](condition.md)

[« Watcher always condition](condition-always.md) [Watcher compare condition
»](condition-compare.md)

## 观察者永不条件

使用"从不"条件可在触发监视时跳过执行监视操作。处理监视输入，将记录添加到监视历史记录，并结束监视执行。此条件通常用于测试。

### 使用永不条件

没有要为"从不"条件指定的属性。要使用它，请指定条件类型并将其与空对象关联：

    
    
    "condition" : {
      "never" : {}
    }

[« Watcher always condition](condition-always.md) [Watcher compare condition
»](condition-compare.md)
