

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md)
›[Watcher](xpack-alerting.md) ›[Watcher conditions](condition.md)

[« Watcher conditions](condition.md) [Watcher never condition »](condition-
never.md)

## 观察程序始终条件

使用"始终"条件在触发监视时执行监视操作，除非它们受到限制。

"始终"条件使您能够按固定计划执行监视操作，例如，_"每周五中午，emailtosys.admin@example.com 发送状态报告"。_

### 使用 always条件

如果从监视中省略条件定义，则这是默认值。

没有要为"始终"条件指定的属性。要显式使用此条件，请指定条件类型并将其与空对象关联：

    
    
    "condition" : {
      "always" : {}
    }

[« Watcher conditions](condition.md) [Watcher never condition »](condition-
never.md)
