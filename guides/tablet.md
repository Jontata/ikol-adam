# The following file details the setup of the tablet.

- Install termux from web.

- Initialize enviornment:

```(bash)
pkg update && pkg upgrade -y
pkg install curl jq wget openssh
pkg install termux-api  # Provides Termux APIs like notifications
```

- Write script.

```(bash)
#!/data/data/com.termux/files/usr/bin/bash

# GitHub Variables
GITHUB_REPO="your-repo"  # Replace with your repo
GITHUB_API="https://api.github.com/repos/$GITHUB_REPO/releases/latest"
APK_DIR="$HOME/Downloads"
APK_FILE="$APK_DIR/latest-app.apk"

# Create Downloads Directory
mkdir -p "$APK_DIR"

# Fetch the Latest Release URL
echo "Fetching latest APK URL..."
DOWNLOAD_URL=$(curl -s $GITHUB_API | jq -r '.assets[] | select(.name | endswith(".apk")) | .browser_download_url')

if [ -z "$DOWNLOAD_URL" ]; then
    echo "Error: Could not find APK file in the latest release."
    exit 1
fi

# Download the APK
echo "Downloading APK..."
wget -O "$APK_FILE" "$DOWNLOAD_URL"

# Trigger the APK Installation
echo "Starting APK installation..."
am start --user 0 -a android.intent.action.VIEW -d "file://$APK_FILE" -t "application/vnd.android.package-archive"

# Send a Notification
termux-notification --title "APK Installer" --content "New APK downloaded. Follow prompts to install."
```

- Save script in home directory.

Make it executable `chmod +x install_apk.sh`

Test if it works `./install_apk.sh`

- Automate with Cron (Termux:Tasker or Termux:Boot)

Install termux-cron: `pkg install cronie`

Ensure termux’s storage permission is enabled: `termux-setup-storage`

Start the cron service: `crond`

Edit cron jobs: `crontab -e`

Add a job to run script: `0 * * * * bash $HOME/install_apk.sh`

The script triggers the APK installation using the ``am`` command, which works if you enable “Install unknown apps” for Termux in Android settings.
