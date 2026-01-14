# Local n8n Setup & Hostinger Migration

Este repositorio contiene la configuración para ejecutar **n8n** en local utilizando Docker, junto con los datos migrados desde el servidor de Hostinger.

## 🚀 Instalación y Uso

### Prerrequisitos
- Docker Desktop instalado y corriendo.

### Comandos Básicos

1.  **Iniciar n8n**:
    ```bash
    docker-compose up -d
    ```
2.  **Detener n8n**:
    ```bash
    docker-compose down
    ```
3.  **Ver Logs**:
    ```bash
    docker-compose logs -f
    ```

Accede a n8n en: [http://localhost:5678](http://localhost:5678)
Tus credenciales son las mismas que en Hostinger (se migró la base de datos de usuarios).

---

## 🔄 Proceso de Migración (Referencia)

Para traer los datos desde Hostinger, realizamos los siguientes pasos (ya ejecutados):
1.  Conexión SSH al servidor (`46.202.159.18`).
2.  Localización del volumen de Docker: `/var/lib/docker/volumes/n8n_data/_data`.
3.  Descarga segura de la base de datos `database.sqlite` y carpetas de configuración a `./n8n_data` local.

> **Nota**: Si necesitas re-sincronizar los datos en el futuro (borrando lo local), deberás repetir la descarga vía SCP.

---

## 🛠 Guía de Trabajo: Local vs Producción (Git Flow)

Me preguntabas: *¿Vale la pena usar Git? ¿Cómo trabajo ahora?*

**Respuesta CORTA:** Sí, absolutamente vale la pena. Es la diferencia entre "jugar" y "hacer ingeniería de software". Evita romper tus automatizaciones en producción.

### El Nuevo Flujo de Trabajo (SDLC)

Dado que la función nativa "Source Control" es de pago (Enterprise), usaremos la estrategia de **"Exportación por Script"**.

He creado un script automático `git-backup.sh` para facilitarte la vida.

#### Paso 1: Trabaja en Local
1.  Abre n8n en `localhost:5678`.
2.  Crea, edita y prueba tus workflows tranquilamente.

#### Paso 2: Guardar (Snapshot)
Cuando termines una sesión de trabajo:
1.  Abre tu terminal en esta carpeta.
2.  Ejecuta:
    ```bash
    ./git-backup.sh
    ```
    *Esto exportará todos tus workflows a la carpeta `/workflows` en formato JSON y creará un commit en Git automáticamente.*

### 🔐 Gestión de Credenciales (Importante)
Por seguridad, **las credenciales (API Keys, Contraseñas) NO se guardan en Git**.

Esto significa que cuando creas una nueva credencial en Local (ej: `Google Search Key`), **tienes que replicarla manualmente en el VPS**.

1.  Crea la credencial en Local y úsala en tus nodos.
2.  Despliega los cambios al VPS (con los scripts de abajo).
3.  Entra a tu n8n en Producción (`tudominio.com:5678`).
4.  Ve a `Credentials` > `New` y crea la misma credencial con los mismos datos.

> **Consejo**: Usa siempre el sistema de "Credentials" de n8n. **Nunca escribas claves directamente en los nodos** o en archivos `.env` inseguros.

#### Paso 3: Desplegar en Producción (VPS)
1.  Conéctate a tu VPS via SSH.
2.  Ve a tu carpeta de n8n.
3.  Ejecuta el script de restauración (que se bajará con git pull):
    ```bash
    ./restore_workflows.sh
    ```
    *Este script hace el `git pull` y el `docker import` por ti automáticamente.*

### Resumen
1.  **Local**: Creas el workflow.
2.  **Local**: `./git-backup.sh` (Guarda y sube a Git).
3.  **VPS**: `./restore_workflows.sh` (Baja y aplica los cambios).
