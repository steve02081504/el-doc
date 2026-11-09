# EL 语言教程

面向新使用者的 EL 教学文档，使用 MkDocs Material 构建，通过 GitHub Pages 发布。

- 在线阅读：<https://steve02081504.github.io/el-doc/>
- 本地预览：`pip install -r requirements.txt`，然后 `mkdocs serve`
- 构建检查：`mkdocs build --strict`
- 写作约定见 [AUTHORING.md](AUTHORING.md)

网站内容在 `docs/`，导航在 `mkdocs.yml`，EL 代码高亮由 `hooks/el_lexer.py` 注册。

## 发布

推送到 `main` 后，`.github/workflows/deploy.yml` 会构建并发布到 GitHub Pages。
