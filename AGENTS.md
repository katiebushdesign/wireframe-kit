# HTML wireframe project

**Kit:** [`.wireframe-kit/`](.wireframe-kit/) — copy workflow, blocks, skills, scripts.

**New wireframe / onboard:** load skill **`create-wireframe`** (or `/create-wireframe`) — intake questions, then execute.

**Agents — read first:** [`.wireframe-kit/AI-INSTRUCTIONS.md`](.wireframe-kit/AI-INSTRUCTIONS.md) · [copy doc access if URL blocked](.wireframe-kit/copy-doc-access.md)

```bash
make link-skills       # once after clone
make parse-copy        # copy doc → JSON
make sync              # nav + footer (when multi-page shell exists)
make validate-blocks   # block classes in css/style.css
make serve             # local preview (onboard runs this automatically)
make setup-github      # SLUG=212-visual — katiebushdesign/{clientname}-wireframes + Pages
```

Configure: `.wireframe-kit/config/client.yaml`, `site-map.yaml`. Do not commit unless asked.
