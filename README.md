# Wiki
Static site using GitHub Pages with Jekyll, see [Dockerfile](Dockerfile)

## Update Docs with Wiki
```pwsh
remove-Item -Force -Recurse ./docs/
git clone https://github.com/oleksis/youtube-dl-gui.wiki.git docs
```
## Preview website
Using `docker-compose`

```bash
docker-compose up --build --force-recreate
```
