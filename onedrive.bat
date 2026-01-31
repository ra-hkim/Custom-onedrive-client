@echo off
REM =============================================
REM OneDrive Mount Script for Projects/Backups
REM =============================================
REM Change drive letter if needed (O:)

echo Mounting OneDrive...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "rclone mount onedrive: O: --vfs-cache-mode full --vfs-cache-max-size 48G --vfs-cache-max-age 24h --vfs-read-chunk-size 256M --vfs-read-chunk-size-limit 2G --dir-cache-time 24h --poll-interval 10s --network-mode --allow-other --log-level INFO --fast-list --links"

pause
