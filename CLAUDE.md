# Claude Code — Reglas para este proyecto

## REGLA CRÍTICA: Sincronización VPS ↔ Local

**Antes de cualquier deploy, debes seguir UNA de estas dos rutas. No mezclarlas.**

---

### Ruta A — Modifico workflows específicos

1. **Bajar del VPS SOLO los workflows que voy a modificar**
2. Editar esos archivos localmente
3. Hacer commit + push a git
4. **Subir al VPS SOLO esos mismos workflows** (no el deploy masivo)

```bash
# Subir un solo workflow al VPS sin tocar los demás:
scp workflows/MI_WORKFLOW.json root@46.202.159.18:/tmp/restore_wf.json
ssh root@... "docker run --rm ... n8n import:workflow --input=/tmp/workflow.json"
```

---

### Ruta B — Deploy completo (todos los workflows)

1. **Bajar TODOS los workflows del VPS primero** → guardar todos en `workflows/`
2. Editar los que necesito
3. Hacer commit + push a git
4. Ejecutar `deploy_to_vps.exp` (que sube todos)

```bash
# Exportar todos del VPS y guardar localmente:
expect export_current_vps.exp > /tmp/vps_export_raw.txt
python3 -c "... guardar TODOS los workflows del JSON en workflows/"
```

---

### Por qué es crítico

El script `deploy_to_vps.exp` sube **TODOS** los archivos de `workflows/*.json`.
Si algún workflow fue modificado directamente en la UI de n8n en el VPS (sin pasar por git),
su versión más nueva solo existe en el VPS. Si subes sin bajar antes, la pierdes.

**Nunca asumir que local == VPS. Siempre verificar antes de sobrescribir.**

---

## Workflows principales de este proyecto

| Archivo | Nombre en n8n | Tag |
|---|---|---|
| `3SujNhDcvxSyDmdAiUb7d.json` | 1-Content Factory-Web & LinkedIn | CreaContenido |
| `SwitchboardRouterV1.json` | 2-Telegram Router (The Switchboard) | CreaContenido |
| `LTtD6izOWBatig-7qv8IA.json` | 3-The Reactor | CreaContenido |
| `HhEbv3PhcA2XgDtN.json` | 4-LinkedIn Publisher (Worker) | CreaContenido |

## VPS

- Host: `46.202.159.18`
- Usuario: `root`
- Directorio proyecto: `/root/wordpress`
- Contenedor n8n: filtrar con `docker ps -q --filter 'ancestor=n8nio/n8n'`
