#!/bin/bash

# === SYSTEM INFORMATION === #
echo "🔍 System Information"
uname -a
uptime
df -h
free -m
whoami
w
echo ""

# === FILE & DIRECTORY MANAGEMENT === #
echo "📂 File and Directory Operations"
mkdir -p /tmp/mydir
touch /tmp/mydir/file{1..5}.txt
ls -lah /tmp/mydir
rm -rf /tmp/mydir/file3.txt
cp -r /tmp/mydir /tmp/mydir_backup
mv /tmp/mydir_backup /tmp/newdir
echo ""

# === TEXT PROCESSING === #
echo "📝 Text Processing"
awk '{print $2, $1}' <<< "Hello World"
sed 's/World/Linux/' <<< "Hello World"
cut -d: -f1 /etc/passwd
grep "root" /etc/passwd
echo ""

# === USER & PERMISSIONS === #
echo "👤 User & Permissions Management"
id
groups
chmod 755 /tmp/newdir
chown $USER:$USER /tmp/newdir
useradd -m testuser
passwd testuser
usermod -aG sudo testuser
echo ""

# === PROCESS MANAGEMENT === #
echo "⚙️ Process Management"
ps aux | head -10
kill -9 <PID>
pkill -f "firefox"
nohup sleep 100 &
jobs
bg %1
fg %1
echo ""

# === NETWORKING === #
echo "🌐 Networking Commands"
ip a
ping -c 4 google.com
curl -I https://www.google.com
wget https://example.com/file.zip
netstat -tulnp | head -10
traceroute google.com
echo ""

# === SSH & REMOTE CONNECTIONS === #
echo "🔑 SSH & Remote Commands"
ssh user@remote-server "uptime"
scp file.txt user@remote:/tmp/
rsync -avz file.txt user@remote:/tmp/
ssh-keygen -t rsa -b 4096
ssh-copy-id user@remote
echo ""

# === DOCKER & CONTAINERS === #
echo "🐳 Docker & Container Management"
docker ps
docker images
docker run -d -p 8080:80 nginx
docker stop <container_id>
docker rm <container_id>
docker exec -it <container_id> bash
docker logs <container_id>
echo ""

# === SYSTEM AUDITING & SECURITY === #
echo "🛡️ Security & System Auditing"
ufw status
iptables -L -v -n
fail2ban-client status sshd
echo ""

# === DISK & STORAGE === #
echo "💾 Disk & Storage Management"
lsblk
mount | column -t
df -Th
du -sh /var/log
echo ""

# === BACKUPS & ARCHIVING === #
echo "📦 Backups & Archiving"
tar -czf backup.tar.gz /tmp/newdir
tar -xzf backup.tar.gz -C /tmp
zip -r backup.zip /tmp/newdir
unzip backup.zip -d /tmp
echo ""

# === AUTOMATION & SCHEDULING === #
echo "⏳ Automation & Scheduling"
echo "0 2 * * * /path/to/script.sh" | crontab -
crontab -l
echo ""

# === TROUBLESHOOTING & LOGS === #
echo "🐞 Debugging & Logs"
set -x
trap "echo 'Script interrupted!'" SIGINT SIGTERM
logger "Test log entry"
tail -f /var/log/syslog
dmesg | tail
set +x
echo ""

# === VIRTUALIZATION (VMs) === #
echo "🖥️ Virtual Machines (VMs)"
virsh list --all
virsh start myvm
virsh shutdown myvm
echo ""

# === SHUTDOWN & REBOOT === #
echo "🔌 Shutdown & Reboot"
shutdown -h now
reboot
echo "✔️ All system commands executed successfully!"
echo ""

# =====================================
# === SCRIPTING EXAMPLES (LOGIC) ===
# =====================================

echo "📝 Bash Scripting Logic Examples"

# === IF-ELSE EXAMPLE === #
echo "🔄 If-Else Example"
read -p "Enter a number: " num
if ((num > 10)); then
    echo "The number is greater than 10"
elif ((num == 10)); then
    echo "The number is exactly 10"
else
    echo "The number is less than 10"
fi
echo ""

# === FOR LOOP EXAMPLE === #
echo "🔁 For Loop Example"
for i in {1..5}; do
    echo "Iteration $i"
done
echo ""

# === WHILE LOOP EXAMPLE === #
echo "🔄 While Loop Example"
count=1
while [[ $count -le 5 ]]; do
    echo "Loop iteration $count"
    ((count++))
done
echo ""

# === FUNCTION EXAMPLE === #
echo "🔧 Function Example"
greet_user() {
    echo "Hello, $1!"
}
greet_user "Alice"
greet_user "Bob"
echo ""

# === CASE STATEMENT EXAMPLE === #
echo "🎭 Case Statement Example"
read -p "Enter a fruit (apple, banana, orange): " fruit
case "$fruit" in
    apple) echo "You chose apple!" ;;
    banana) echo "You chose banana!" ;;
    orange) echo "You chose orange!" ;;
    *) echo "Unknown fruit!" ;;
esac
echo ""

# === FILE CHECK EXAMPLE === #
echo "📂 File Check Example"
read -p "Enter file name: " filename
if [[ -f "$filename" ]]; then
    echo "The file '$filename' exists!"
else
    echo "File not found!"
fi
echo ""

# === EXIT STATUS HANDLING === #
echo "🔍 Exit Status Handling Example"
ls /nonexistent_directory
if [[ $? -eq 0 ]]; then
    echo "Command succeeded"
else
    echo "Command failed"
fi
echo ""

# === SLEEP & WAIT EXAMPLE === #
echo "⏳ Sleep & Wait Example"
sleep 2
echo "Waited for 2 seconds"
echo ""

# === REDIRECTION EXAMPLE === #
echo "📑 Output Redirection Example"
echo "Hello, world!" > output.txt
cat output.txt
echo ""

# === ENVIRONMENT VARIABLES EXAMPLE === #
echo "🌍 Environment Variables Example"
export MY_VAR="Hello"
echo "MY_VAR is set to: $MY_VAR"
echo ""

# === BACKGROUND & PARALLEL PROCESSING EXAMPLE === #
echo "🔧 Background Process Example"
(sleep 5 && echo "Background Task Done!") &
echo "Main script continues..."
wait  # Wait for background task to complete
echo ""

# === ARRAY EXAMPLE === #
echo "📦 Array Example"
my_array=("Linux" "Bash" "Shell" "Scripting")
for item in "${my_array[@]}"; do
    echo "Item: $item"
done
echo ""

# === RANDOM NUMBER GENERATION === #
echo "🎲 Random Number Example"
random_number=$((RANDOM % 100 + 1))
echo "Generated random number: $random_number"
echo ""

echo "🎉 All Bash scripting logic examples executed successfully!"
