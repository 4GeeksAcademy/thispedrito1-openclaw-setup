# 2026-06-26: Skill documentation pattern establecido

## Convención definitiva para skills

Cada skill debe seguir esta estructura:

```
skills/<nombre>/
  SKILL.md         ← documentación de uso (OBLIGATORIO)
  scripts/         ← ejecutables
  skill_log.md     ← log interno técnico (opcional, pero recomendado)

workspace/SKILL_LOG.md  ← bitácora GLOBAL de todas las skills (OBLIGATORIO)
```

### Reglas
1. **Toda skill nueva** debe tener su propio `SKILL.md` en su directorio
2. **Toda skill nueva** debe documentarse en el `SKILL_LOG.md` raíz con: origen (qué conversación la originó), decisiones técnicas, endpoints descubiertos, lecciones aprendidas
3. **skill_log.md** interno es opcional pero recomendado para logs técnicos detallados

## Skills existentes

| Skill | Directorio | Scripts |
|-------|-----------|---------|
| `4geeks` | `skills/4geeks/` | `4geeks_api.sh`, `4geeks_projects.sh` |

## Archivos relevantes
- `workspace/SKILL_LOG.md` — bitácora global
- `workspace/skills/4geeks-api/SKILL.md` — doc API wrapper
- `workspace/skills/4geeks-projects/SKILL.md` — doc proyectos con estado
- `workspace/skills/4geeks-pending/SKILL.md` — doc trabajo pendiente
- Cada skill tiene su propio `scripts/` con ejecutables
- `workspace/SKILL_LOG.md` — bitácora global con todas las skills documentadas
