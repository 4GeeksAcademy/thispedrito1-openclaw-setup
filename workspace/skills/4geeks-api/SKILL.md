# 4Geeks API Wrapper

Skill base para interactuar con la API de BreatheCode (4Geeks Academy).

## Configuración

Requiere `4GEEKS_TOKEN` en `/root/.openclaw/.env`.

## Script

**Ruta:** `scripts/4geeks_api.sh`

Wrapper genérico para cualquier endpoint de la API.

```bash
./4geeks_api.sh <method> <endpoint> [body]
```

### Ejemplos

```bash
# Obtener perfil
./4geeks_api.sh GET auth/user/me

# Obtener certificados
./4geeks_api.sh GET certificate/me

# POST a un endpoint
./4geeks_api.sh POST algún/endpoint '{"key":"value"}'
```

## Variables de Entorno

| Variable | Default | Descripción |
|----------|---------|-------------|
| `FG_TOKEN` | — | Token API (sobrescribe `.env`) |
| `FOURGEEKS_API_URL` | `https://breathecode.herokuapp.com/v1` | URL base |
