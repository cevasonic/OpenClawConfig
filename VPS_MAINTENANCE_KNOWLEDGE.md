# OpenClaw VPS Operations & Knowledge Base (AI Handover)

> [!IMPORTANT]
> This document is designed for AI Agents (Antigravity, Claude Code, etc.) to quickly understand the VPS environment and operations for OpenClaw. **DO NOT perform trial-and-error commands; use the established scripts and paths documented here.**

## 1. VPS Connection Details
- **Host:** `180.93.137.94`
- **User:** `root`
- **SSH Port:** `22`
- **SSH Config:** A Host entry `openclaw-vps` exists in `~/.ssh/config`.
- **SSH Key:** `id_ed25519_vps` is available in `~/.ssh/`.
- **Password:** Refer to `deploy_auth.exp` or `run_ssh.exp` in this repo for the plaintext password.

## 2. Key Directories & Files
- **OpenClaw Home:** `/opt/openclaw`
- **Configuration & Data:** `/opt/openclaw/.openclaw/`
- **Main Config File:** `/opt/openclaw/.openclaw/openclaw.json`
- **Environment Variables:** `/opt/openclaw/.env`
- **Executable:** `openclaw-gateway` (running as a systemd service or background process).

## 3. Service Management
- **Check Status:** `systemctl status openclaw-gateway.service`
- **Restart Service:** `systemctl restart openclaw-gateway.service`
- **View Logs:** `journalctl -u openclaw-gateway.service -f` or `tail -f /opt/openclaw/openclaw.log`

## 4. Maintenance & Cleanup (Pre-tested)
The following tasks have been tested and verified as **SAFE** to run:
- **System cleanup:** `apt-get clean`, `journalctl --vacuum-time=3d`, `npm cache clean --force`.
- **OpenClaw specific cleanup:**
  - Delete old Playwright browsers: `rm -rf /opt/openclaw/.cache/ms-playwright/*`.
  - Delete Go module cache: `rm -rf /opt/openclaw/go/pkg/mod/*`.
  - Delete old config backups: `rm -f /opt/openclaw/.openclaw/*.bak.*`, `rm -f /opt/openclaw/.openclaw/*.clobbered.*`.

## 5. Automation Scripts (Recommended)
Use the following pre-built Node.js scripts in the `scripts/` directory to perform tasks quickly:
- `node scripts/vps_status.js`: Provides a full report of disk usage, junk status, and service status.
- `node scripts/vps_cleanup.js`: Performs all safe cleanup tasks automatically.

## 7. Lessons Learned & Troubleshooting

### SSH Interaction on Windows Agent
- **Issue:** Standard `ssh` commands and `expect` scripts often hang or fail with "unexpected user interaction type" errors in the AI agent's terminal environment (PowerShell/CMD). This is due to TTY and password prompt handling issues.
- **Solution:** Use **Node.js with the `ssh2` library**. It is 100% reliable for programmatic SSH tasks, handles passwords gracefully, and provides clean output without terminal interaction bugs.
- **Dependency:** Always ensure `npm install ssh2` is run in the project root before executing the management scripts.

### Node.js Execution Policy
- **Issue:** `npm` might fail to run if PowerShell execution policies are restricted.
- **Solution:** Use `npm.cmd` instead of `npm` to bypass PowerShell-specific script execution restrictions.

### Playwright Cache Persistence
- **Issue:** Application might take longer to start after a full cleanup.
- **Fact:** Deleting `.cache/ms-playwright` is safe but forces the app to re-download browsers on the first run. This is expected behavior and not a bug.

## 6. Important Notes for AI Agents
- **Environment:** Windows local environment, Linux remote VPS.
- **Tools:** Use `node` with `ssh2` library for reliable remote execution if `expect` or `ssh` interaction fails in the agent terminal.
- **Safety:** NEVER delete `/opt/openclaw/.openclaw/plugin-runtime-deps` as it breaks plugin functionality.
