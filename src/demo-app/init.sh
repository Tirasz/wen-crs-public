#!/bin/sh

# Check if the environment variables are set
if [ -z "$ELASTIC_CLIENT" ] || [ -z "$DUMMY_CLIENT" ]; then
    echo "Please set the environment variables ELASTIC_CLIENT and DUMMY_CLIENT"
    echo $ELASTIC_CLIENT
    echo $DUMMY_CLIENT
    exit 1
fi

# Define the fixed file path
FILE_PATH="/app/src/environments/environment.prod.ts"

# Check if the file exists
if [ ! -f "$FILE_PATH" ]; then
    echo "Environment file not found: $FILE_PATH"
    exit 1
fi

# Replace the strings in the file
sed -i "s|\$ENV\.ELASTIC_CLIENT|$ELASTIC_CLIENT|g" "$FILE_PATH"
sed -i "s|\$ENV\.DUMMY_CLIENT|$DUMMY_CLIENT|g" "$FILE_PATH"

echo "Strings replaced successfully in $FILE_PATH"
