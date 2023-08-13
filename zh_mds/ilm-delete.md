

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Data
management](data-management.md) ›[Index lifecycle actions](ilm-actions.md)

[« Allocate](ilm-allocate.md) [Force merge »](ilm-forcemerge.md)

##Delete

允许的阶段：删除。

永久删除索引。

###Options

`delete_searchable_snapshot`

     (Optional, Boolean) Deletes the searchable snapshot created in a previous phase. Defaults to `true`. This option is applicable when the [searchable snapshot](ilm-searchable-snapshot.html "Searchable snapshot") action is used in any previous phase. 

###Example

    
    
    response = client.ilm.put_lifecycle(
      policy: 'my_policy',
      body: {
        policy: {
          phases: {
            delete: {
              actions: {
                delete: {}
              }
            }
          }
        }
      }
    )
    puts response
    
    
    PUT _ilm/policy/my_policy
    {
      "policy": {
        "phases": {
          "delete": {
            "actions": {
              "delete" : { }
            }
          }
        }
      }
    }

[« Allocate](ilm-allocate.md) [Force merge »](ilm-forcemerge.md)
