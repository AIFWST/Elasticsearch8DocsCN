

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[EQL
search](eql.md)

[« EQL function reference](eql-function-ref.md) [Example: Detect threats
with EQL »](eql-ex-threat-detection.md)

## EQL 管道引用

Elasticsearch 支持以下 EQL 管道。

###'头'

最多返回指定数量的事件或序列，从最早的匹配项开始。工作原理类似于 Unix 头命令)。

**Example**

以下 EQL 查询最多返回三个最早的 powershell 命令。

    
    
    process where process.name == "powershell.exe"
    | head 3

**Syntax**

    
    
    head <max>

**Parameters**

`<max>`

     (Required, integer) Maximum number of matching events or sequences to return. 

###'尾巴'

最多返回指定数量的事件或序列，从最近的匹配项开始。工作原理类似于 Unix tailcommand)。

**Example**

以下 EQL 查询最多返回五个最新的"svchost.exe"进程。

    
    
    process where process.name == "svchost.exe"
    | tail 5

**Syntax**

    
    
    tail <max>

**Parameters**

`<max>`

     (Required, integer) Maximum number of matching events or sequences to return. 

[« EQL function reference](eql-function-ref.md) [Example: Detect threats
with EQL »](eql-ex-threat-detection.md)
