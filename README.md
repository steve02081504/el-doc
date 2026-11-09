# EL 语言教程

面向新使用者的 EL 教学文档，用 MkDocs Material 构建，通过 GitHub Pages 发布。

- 在线阅读：<https://steve02081504.github.io/el-doc/>
- 本地预览：`pip install -r requirements.txt`，然后 `mkdocs serve`
- 构建检查：`mkdocs build --strict`
- 写作约定见 [AUTHORING.md](AUTHORING.md)：页面骨架、组件手册、排版规则与写作时要用的心理学原则。

## 站点结构

站点按“先跑起来，再懂原理，最后做出东西”组织，导航与文件对应：

- `docs/index.md`：落地页。三条入口 + 学习地图 + 读法分流。
- `docs/roadmap.md`：学习地图。五个阶段、时间估算、每站自检清单、卡点排查。
- `docs/getting-started.md`、`docs/tour.md`：起步的两页。
- `docs/language/index.md`、`docs/stdlib/index.md`：章节入口，讲清本章怎么读、哪些可以跳。
- 其余页面按 `language/`、`stdlib/`、`practice/`、`appendix/` 分目录，导航在 `mkdocs.yml`。

## 站点特性

- `el`／`eol`／`repl` 代码块的高亮由 `hooks/el_lexer.py` 注册。
- 页尾「随便翻一页」按钮由 `hooks/random_pages.py` 生成页面清单，前端脚本在 `docs/assets/random-page.js`。
- 阅读进度条与首页的「继续上次」卡片由 `docs/assets/learning.js` 实现，数据只存在浏览器 `localStorage`，不上报。
- 可折叠的「先猜」、检查点清单与章节卡片样式在 `docs/stylesheets/extra.css`；Markdown 用法见 AUTHORING.md。

## 发布

推送到 `master` 后，`.github/workflows/deploy.yml` 会构建并发布到 GitHub Pages。
