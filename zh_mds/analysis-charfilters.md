

[Elastic Docs](/guide/) ›[Elasticsearch Guide [8.9]](index.md) ›[Text
analysis](analysis.md)

[« Word delimiter graph token filter](analysis-word-delimiter-graph-
tokenfilter.md) [HTML strip character filter »](analysis-htmlstrip-
charfilter.md)

## 字符筛选器参考

_Character filters_用于在将字符流传递到分词器之前对其进行预处理。

字符筛选器以字符流的形式接收原始文本，并可以通过添加、删除或更改字符来转换流。例如，字符过滤器可用于将印度教-阿拉伯数字 (٠١٢٣٤٥٦٧٨٩) 转换为阿拉伯-拉丁等效数字 (0123456789)，或<b>从流中删除 HTML 元素(如"')。

Elasticsearch有许多内置的字符过滤器，可用于构建自定义分析器。

HTML 条形字符过滤器

     The `html_strip` character filter strips out HTML elements like `<b>` and decodes HTML entities like `&amp;`. 
[Mapping Character Filter](analysis-mapping-charfilter.html "Mapping character
filter")

     The `mapping` character filter replaces any occurrences of the specified strings with the specified replacements. 
[Pattern Replace Character Filter](analysis-pattern-replace-charfilter.html
"Pattern replace character filter")

     The `pattern_replace` character filter replaces any characters matching a regular expression with the specified replacement. 

[« Word delimiter graph token filter](analysis-word-delimiter-graph-
tokenfilter.md) [HTML strip character filter »](analysis-htmlstrip-
charfilter.md)
