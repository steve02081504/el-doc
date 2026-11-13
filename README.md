# EL 语言参考

EL 的语言、标准库和工具链参考站，附入门教程与实战指南。使用 MkDocs Material 构建，通过 GitHub Pages 发布。

- 在线阅读：[EL 语言参考](https://steve02081504.github.io/el-doc/)
- 本地预览：安装 `requirements.txt` 中的依赖后运行 `mkdocs serve`。
- 构建检查：`mkdocs build --strict`。
- 写作约定：[AUTHORING.md](AUTHORING.md)。

## 结构

| 入口 | 内容与维护位置 |
| --- | --- |
| 参考首页 | `docs/index.md`，按主题直达语言与库参考 |
| 语言参考 | `docs/reference/language/`，语法、语义、限制与规范出处 |
| 标准库参考 | `docs/stdlib/api/`，从源码注释生成的分类、模块、符号索引及 API 页 |
| 工具链参考 | `docs/toolchain.md` 与实现边界说明 |
| 教程与指南 | `docs/tutorials/index.md`；原有 `beginner/`、`language/`、`stdlib/` 和 `practice/` 页面保留 URL |

参考页按查询主题组织，不要求按章节顺序阅读。教程集中在导航中的一个分区，继续保留学习路线和练习。

## 从源码生成标准库参考

在本仓库运行，显式指定 EL 检出：

```text
python scripts/stdlib_docs.py --el-root /path/to/el
python scripts/stdlib_docs.py --el-root /path/to/el --check
python -m unittest discover -s tests -v
mkdocs build --strict
```

提取器读取 `src/stdlib/**/*.el` 中的功能性注释，输出 Markdown 与 `api.json`。API 页、默认环境、分类页、模块索引和符号索引均从同一模型生成；`hooks/api_navigation.py` 将分类和模块自动加入导航。格式、覆盖统计与提取边界见[文档注释与生成](docs/stdlib/documentation-comments.md)。生成快照随本仓库提交，站点构建不要求另行检出 EL。

语言参考描述规范合同，API 注释描述对应源码。示例未运行验证；站点构建不证明语言能力或示例执行通过。

## 站点功能与发布

`hooks/el_lexer.py` 注册 EL 代码高亮；`hooks/random_pages.py` 与 `docs/assets/random-page.js` 提供随机页面；`docs/assets/learning.js` 提供本机阅读记录与进度组件，教程可按需使用。样式位于 `docs/stylesheets/extra.css`。

`hooks/code_links.py` 使用生成的声明模型，把 EL 代码块中的标准环境名字、可确定的导入和成员链接到参考条目，关键词链接到语言参考。构建结束时检查链接页面和锚点；局部遮盖与未知接收者不按同名猜测。

推送到 `master` 后，`.github/workflows/deploy.yml` 检查站点与提取器，再发布到 GitHub Pages。
