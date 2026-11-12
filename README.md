# EL 语言教程

面向新使用者的 EL 教学文档，用 MkDocs Material 构建，通过 GitHub Pages 发布。

- 在线阅读：<https://steve02081504.github.io/el-doc/>
- 本地预览：`pip install -r requirements.txt`，然后 `mkdocs serve`
- 构建检查：`mkdocs build --strict`
- 写作约定见 [AUTHORING.md](AUTHORING.md)：页面骨架、组件手册、排版规则与写作时要用的心理学原则。

## 站点结构

站点提供零基础动手路线和按主题查阅的进阶章节，导航与文件对应：

- `docs/index.md`：落地页。三条入口 + 学习地图 + 读法分流。
- `docs/roadmap.md`：学习地图。五个阶段、时间估算、每站自检清单、卡点排查。
- `docs/getting-started.md`：从保存文件、打开终端到运行与排错。
- `docs/beginner/`：零花钱、预算判断、阅读记录、采购函数与文具采购小助手；完整例子逐步过渡到独立任务。
- `docs/tour.md`：已有编程经验时使用的速览。
- `docs/language/index.md`、`docs/stdlib/index.md`：章节入口，讲清本章怎么读、哪些可以跳。
- 其余页面按 `language/`、`stdlib/`、`practice/`、`appendix/` 分目录，导航在 `mkdocs.yml`。

## 站点特性

- `hooks/api_navigation.py` 将生成的 API 模块页自动加入侧边栏，新增模块无需手改导航。
- `el`／`eol`／`repl` 代码块的高亮由 `hooks/el_lexer.py` 注册。
- 页尾「随便翻一页」按钮由 `hooks/random_pages.py` 生成页面清单，前端脚本在 `docs/assets/random-page.js`。
- 阅读进度条与首页的「继续上次」卡片由 `docs/assets/learning.js` 实现，数据只存在浏览器 `localStorage`，不上报。
- 可折叠的「先猜」、检查点清单与章节卡片样式在 `docs/stylesheets/extra.css`；Markdown 用法见 AUTHORING.md。

## 从 EL 源码生成标准库参考

`python scripts/stdlib_docs.py --el-root /path/to/el` 读取标准库的 `///` 功能性注释，生成 `docs/stdlib/api/` 下的 Markdown 与可供 CLI/GUI 消费的 JSON。生成快照随本仓库提交，站点构建不需要额外检出 EL。

注释格式、使用边界和未来 EL 子命令的职责见 [文档注释与生成](docs/stdlib/documentation-comments.md)。生成后用 `--check` 检查快照，用 `python -m unittest discover -s tests -v` 验证提取器，再运行 `mkdocs build --strict`。

## 发布

推送到 `master` 后，`.github/workflows/deploy.yml` 会构建并发布到 GitHub Pages。
