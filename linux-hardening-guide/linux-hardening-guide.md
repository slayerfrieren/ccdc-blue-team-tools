# Linux Hardening Guide

## 1. User Account Hardening

### 1.1. Disable Unused or Suspicious Accounts

List all user accounts and identify unnecessary ones:
```
cat /etc/passwd | awk -F: '{ print $1, $3, $7 }'
```

Lock suspicious or unnecessary accounts:
```
sudo usermod -L <username>
```

Delete unnecessary accounts:
```
sudo userdel -r <username>
```

Be sure to take note of any accounts that are necessary for the system to function. Also be sure to take invenyory of current accounts to monitor for any new accounts that are created.

### 1.2. Restrict Root Account Access

Disable root login over SSH: Edit /etc/ssh/sshd_config:
```
PermitRootLogin no
```

Restart SSH:
```
sudo systemctl restart sshd
```

Enforce the use of sudo for privileged tasks: Ensure only trusted users are in the sudo group:
```
sudo cat /etc/group | grep sudo
```

### 1.3. Enforce Strong Password Policies

Set password complexity and expiration rules in /etc/login.defs:
```
PASS_MAX_DAYS   90
PASS_MIN_DAYS   7
PASS_WARN_AGE   14
```

Use chage to enforce password expiration for existing users:
```
sudo chage -M 90 -m 7 -W 14 <username>
```
Install PAM (Pluggable Authentication Module) for password complexity:
```
sudo apt-get install libpam-pwquality
```

Edit /etc/security/pwquality.conf:
```
minlen = 12
dcredit = -1
ucredit = -1
ocredit = -1
lcredit = -1
```
### 1.4. Prevent New User Creation

Red Team might attempt to create new users if they gain access. Prevent this by restricting access to useradd and passwd commands.

Remove write permissions for unprivileged users:
```
sudo chmod o-x /usr/sbin/useradd /usr/bin/passwd
```

## 2. Lock Down SSH Access

### 2.1. Restrict SSH to Trusted IPs

Add trusted IP ranges to /etc/hosts.allow:
```
sshd: 192.168.1.0/24
```
Block all other IPs in /etc/hosts.deny:
```
sshd: ALL
```

### 2.2. Change Default SSH Port

Modify the SSH port in /etc/ssh/sshd_config:
```
Port 2222
```
Restart SSH:
```
sudo systemctl restart sshd
```
### 2.3. Use Key-Based Authentication

Generate SSH keys:
```
ssh-keygen -t rsa
```
Copy the public key to the server:
```
ssh-copy-id user@<server_ip>
```
Disable password-based login in /etc/ssh/sshd_config:
```
PasswordAuthentication no
```
Restart SSH:
```
sudo systemctl restart sshd
```

## 3. Restrict System Access

### 3.1. Monitor Active Sessions

View currently logged-in users:
```
who
```
Kill suspicious sessions:
```
sudo pkill -u <username>
```
### 3.2. Prevent Concurrent Logins

Limit the number of simultaneous logins for each user: Edit /etc/security/limits.conf:
```
* hard maxlogins 1
```

### 3.3. Disable TTY Access

Prevent interactive logins for non-admin users by assigning /usr/sbin/nologin as their shell:
```
sudo usermod -s /usr/sbin/nologin <username>
```

## 4. File and Directory Hardening

### 4.1. Check Permissions of Sensitive Files

Ensure critical system files are owned by root and have proper permissions:
```
sudo chmod 600 /etc/shadow
sudo chmod 644 /etc/passwd
```
### 4.2. Restrict Write Access

Prevent unauthorized users from writing to /etc:
```
sudo chmod -R go-w /etc
```
### 4.3. Monitor File Integrity

Install AIDE to detect unauthorized changes:
```
sudo apt-get install aide
sudo aideinit
```
Verify system integrity periodically:
```
sudo aide --check
```

## 5. Disable Unnecessary Services

### 5.1. List Active Services

Check running services:
```
sudo systemctl list-units --type=service --state=running
```
### 5.2. Disable Unnecessary Services

Stop and disable unnecessary services:
```
sudo systemctl stop <service_name>
sudo systemctl disable <service_name>
```
For example:

```
sudo systemctl stop bluetooth
sudo systemctl disable cups
```

## 6. Monitor and Block Suspicious Activity

### 6.1. Configure Fail2Ban

Install Fail2Ban to block repeated failed login attempts:
```
sudo apt-get install fail2ban
```
Create a custom jail for SSH in /etc/fail2ban/jail.local:
```
[sshd]
enabled = true
port = 2222
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```
Restart Fail2Ban:
```
sudo systemctl restart fail2ban
```
### 6.2. Block Suspicious IPs

Manually block IPs attempting malicious actions:
```
sudo iptables -A INPUT -s <malicious_ip> -j DROP
```

## 7. Audit System Logs

### 7.1. Enable System Logging

Ensure rsyslog is running:
```
sudo systemctl enable rsyslog
sudo systemctl start rsyslog
```
### 7.2. Review Logs Regularly

Monitor critical logs for suspicious activity:

Authentication logs:
```
sudo tail -f /var/log/auth.log
```
System logs:
```
sudo tail -f /var/log/syslog
```

## 8. Network Hardening

### 8.1. Configure Firewall

Set up iptables to allow only necessary traffic:

```
sudo iptables -A INPUT -p tcp --dport 2222 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
sudo iptables -A INPUT -j DROP
```
Save the rules:
```
sudo iptables-save > /etc/iptables/rules.v4
```
### 8.2. Disable IPv6

Edit /etc/sysctl.conf:
```
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
```
Apply changes:
```
sudo sysctl -p
```

## 9. Incident Response

### 9.1. Track Red Team Attempts

Use tools like tcpdump or Splunk to capture suspicious activity.

### 9.2. Isolate Compromised Accounts

Lock the account and analyze logs:
```
sudo usermod -L <username>
sudo grep <username> /var/log/auth.log
```