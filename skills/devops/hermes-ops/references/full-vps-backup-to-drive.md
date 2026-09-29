# Full VPS backup to Google Drive

Use this recipe when a hosting subscription is ending, before destructive maintenance, or when a restorable off-host copy of the whole VPS is required. This complements, rather than replaces, application-level Git backups.

## 1. Preflight

Measure the root filesystem and confirm the destination has more free space than the source's used bytes:

```bash
df -hT /
du -xhd1 / | sort -h
rclone about drive-hermes: --json
```

Inventory mounted filesystems, running containers, Docker volumes, and database services. A file-level backup cannot reconstruct provider boot metadata by itself, so preserve `/boot` and `/boot/efi` explicitly and keep any provider snapshot available until the restore test passes.

## 2. Repository and recovery key

Use an encrypted Restic repository through rclone:

```bash
export RESTIC_REPOSITORY='rclone:drive-hermes:VPS-Backups/<host>/restic'
export RESTIC_PASSWORD_FILE='/root/.config/restic/<host>-password'
restic init
restic cat config >/dev/null
```

Generate a strong password into a mode-`0600` file without printing it. Create a recovery note containing the repository path, password, and restore commands. Copy that note to a separate Drive recovery directory and verify it with `rclone lsl` before the long transfer. The note is sensitive; never paste its contents into logs or chat.

## 3. Snapshot live databases first

A raw copy of a live SQLite database and its WAL can be inconsistent. Discover candidate `.db`, `.sqlite`, and `.sqlite3` files under persistent application and Docker-volume paths, then:

1. Read only the first 16 bytes.
2. Process the file only if the header equals `b'SQLite format 3\x00'`.
3. Open the source read-only and use Python's `sqlite3.Connection.backup()` into a staging directory.
4. Run `PRAGMA integrity_check` on the staged copy.
5. Record `ok`, `skipped`, and `failed` separately; only true failures stop the backup.

Do not infer database type from the filename. Docker and other tools may have files named `metadata.db` that are not SQLite; treating every `.db` as SQLite produces a false failure before upload starts.

## 4. Save reconstruction inventory

Store these in the staging directory that Restic will include:

- `hostnamectl`
- `dpkg-query -W` (or the platform's package inventory)
- `systemctl list-unit-files`
- root crontab
- `docker ps -a --no-trunc`
- `docker volume ls`
- `docker inspect` for all containers
- logical database snapshots and their manifest

This inventory is not a substitute for the filesystem snapshot; it accelerates disaster recovery when service definitions or package versions must be reconstructed.

## 5. Run the filesystem backup

Back up all persistent filesystems explicitly:

```bash
restic backup / /boot /boot/efi \
  --one-file-system \
  --exclude-file=/root/.config/restic/<host>-excludes.txt \
  --tag hostinger-full --host <host>
```

Exclude `/dev`, `/proc`, `/sys`, `/run`, removable/mounted destinations, Docker overlay `merged` mountpoints, and Restic's local cache. Do not exclude application data, Docker volumes, credentials, or user caches merely to make the first backup smaller when the request is a full migration backup.

Run a multi-hour transfer as a notified background process with a durable log and status file. A started PID is progress, not success. If it exits nonzero, read the full log and fix the failing gate before restarting; Restic deduplicates already-uploaded blobs.

## 6. Verify before canceling the host

Require all of the following:

```bash
restic snapshots
restic check --read-data-subset=5%
restic restore latest --target /tmp/restore-test \
  --include /etc/hostname \
  --include /root/.hermes/config.yaml
cmp /etc/hostname /tmp/restore-test/etc/hostname
cmp /root/.hermes/config.yaml /tmp/restore-test/root/.hermes/config.yaml
```

For the highest assurance, use `restic check --read-data` when time and bandwidth permit. Read back the final status file, snapshot ID, repository path, verification result, and recovery-note location. Tell the user not to cancel the old VPS until the snapshot, integrity check, and test restore all pass.
