@echo off
setlocal

REM ========================
REM Configuration
REM ========================
set MOUNT_DIR=C:\Mounts\OneDrive
set MOUNT_DRIVE=O:
set CACHE_DIR=%SYSTEMDRIVE%\rclone_cache

set VFS_CACHE_MAX_SIZE=48G
set VFS_READ_CHUNK_SIZE=256M
set VFS_READ_CHUNK_SIZE_LIMIT=2G
set POLL_INTERVAL=10s

REM ========================
REM Prepare directories
REM ========================
if not exist "%MOUNT_DIR%" mkdir "%MOUNT_DIR%"
if not exist "%CACHE_DIR%" mkdir "%CACHE_DIR%"

REM Map drive letter
subst %MOUNT_DRIVE% "%MOUNT_DIR%"

REM ========================
REM Mount OneDrive
REM ========================
rclone mount onedrive: "%MOUNT_DRIVE%\" ^
  --vfs-cache-mode full ^
  --vfs-cache-max-size %VFS_CACHE_MAX_SIZE% ^
  --vfs-cache-max-age 24h ^
  --vfs-read-chunk-size %VFS_READ_CHUNK_SIZE% ^
  --vfs-read-chunk-size-limit %VFS_READ_CHUNK_SIZE_LIMIT% ^
  --cache-dir "%CACHE_DIR%" ^
  --dir-cache-time 24h ^
  --poll-interval %POLL_INTERVAL% ^
  --network-mode ^
  --links ^
  --log-level INFO ^
  --fast-list

endlocal
