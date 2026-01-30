#!/bin/bash
cd /root/clawd
echo "--- Pulling changes from GitHub ---"
git pull
echo "--- Restarting Clawdbot ---"
systemctl --user restart clawdbot-gateway.service
echo "--- Done! ---"
