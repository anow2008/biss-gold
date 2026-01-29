#!/bin/sh
# =========================================
# Install script for BissPro Plugin
# =========================================

PLUGIN_NAME="BissPro"
PLUGIN_SRC="./$PLUGIN_NAME"
PLUGIN_DEST="/usr/lib/enigma2/python/Plugins/Extensions/$PLUGIN_NAME"

echo "Starting installation of $PLUGIN_NAME..."

# 1. Create destination directory
if [ ! -d "$PLUGIN_DEST" ]; then
    echo "Creating plugin directory..."
    mkdir -p "$PLUGIN_DEST"
fi

# 2. Copy plugin files
echo "Copying plugin files..."
cp -r "$PLUGIN_SRC/"* "$PLUGIN_DEST/"

# 3. Set permissions
echo "Setting permissions..."
find "$PLUGIN_DEST" -type d -exec chmod 755 {} \;
find "$PLUGIN_DEST" -type f -exec chmod 644 {} \;

# Make sure Python scripts are executable
find "$PLUGIN_DEST" -name "*.py" -exec chmod 755 {} \;

# 4. Ensure icons folder is readable
if [ -d "$PLUGIN_DEST/icons" ]; then
    chmod -R 755 "$PLUGIN_DEST/icons"
fi

echo "Installation completed."
echo "You can now restart your Enigma2 GUI or run the plugin from Extensions menu."

exit 0
