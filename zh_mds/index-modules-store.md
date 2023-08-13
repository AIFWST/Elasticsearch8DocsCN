

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Index
modules](index-modules.md)

[« Slow Log](index-modules-slowlog.md) [Preloading data into the file system
cache »](preload-data-to-file-system-cache.md)

##Store

存储模块允许您控制如何在磁盘上存储和访问索引数据。

这是一个低级设置。某些存储实现的并发性较差或禁用堆内存使用情况的优化。我们建议坚持默认值。

### 文件系统存储类型

有不同的文件系统实现或_storage types_。默认情况下，Elasticsearch 将根据操作环境选择最佳实现。

还可以通过在"config/elasticsearch.yml"文件中配置存储类型来为所有索引显式设置存储类型：

    
    
    index.store.type: hybridfs

这是一个 _static_ 设置，可以在索引创建时基于每个索引进行设置：

    
    
    response = client.indices.create(
      index: 'my-index-000001',
      body: {
        settings: {
          "index.store.type": 'hybridfs'
        }
      }
    )
    puts response
    
    
    PUT /my-index-000001
    {
      "settings": {
        "index.store.type": "hybridfs"
      }
    }

这是仅限专家的设置，将来可能会被删除。

以下部分列出了支持的所有不同存储类型。

`fs`

     Default file system implementation. This will pick the best implementation depending on the operating environment, which is currently `hybridfs` on all supported systems but is subject to change. 
`simplefs`

     deprecated::[7.15,"simplefs is deprecated and will be removed in 8.0. Use niofs or other file systems instead. Elasticsearch 7.15 or later uses niofs for the simplefs store type as it offers superior or equivalent performance to simplefs."] 

简单 FS 类型是使用随机访问文件的文件系统存储(映射到 Lucene 'SimpleFsDirectory')的简单实现。此实现的并发性能较差(多个线程将成为瓶颈)，并且禁用了堆内存使用的一些优化。

`niofs`

     The NIO FS type stores the shard index on the file system (maps to Lucene `NIOFSDirectory`) using NIO. It allows multiple threads to read from the same file concurrently. It is not recommended on Windows because of a bug in the SUN Java implementation and disables some optimizations for heap memory usage. 
`mmapfs`

     The MMap FS type stores the shard index on the file system (maps to Lucene `MMapDirectory`) by mapping a file into memory (mmap). Memory mapping uses up a portion of the virtual memory address space in your process equal to the size of the file being mapped. Before using this class, be sure you have allowed plenty of [virtual address space](vm-max-map-count.html "Virtual memory"). 
`hybridfs`

     The `hybridfs` type is a hybrid of `niofs` and `mmapfs`, which chooses the best file system type for each type of file based on the read access pattern. Currently only the Lucene term dictionary, norms and doc values files are memory mapped. All other files are opened using Lucene `NIOFSDirectory`. Similarly to `mmapfs` be sure you have allowed plenty of [virtual address space](vm-max-map-count.html "Virtual memory"). 

您可以通过设置"node.store.allow_mmap"来限制"mmapfs"和相关"hybridfs"商店类型的使用。这是一个布尔设置，指示是否允许内存映射。默认值是允许它。此设置很有用，例如，如果您所处的环境无法控制创建大量内存映射的能力，因此您需要禁用使用内存映射的功能。

[« Slow Log](index-modules-slowlog.md) [Preloading data into the file system
cache »](preload-data-to-file-system-cache.md)
