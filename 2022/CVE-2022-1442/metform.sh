#!/bin/bash

# Check if base URL provided
if [ -z "$1" ]; then
    echo "Base URL not provided. Usage: ./script.sh BASE_URL"
    exit 1
fi

# Set base URL from command-line argument
base_url=$1

# Step 1: Send CURL request to /wp-json/metform/v1/forms/templates/0
response=$(curl -qsk -X GET "$base_url/wp-json/metform/v1/forms/templates/0" -i)

# Step 2: Extract option value from the response using sed
option_values=$(echo "$response" | gsed -n 's/.*<option value="\([0-9]\+\)".*/\1/p')

# Step 3 :send CURL request to /wp-json/metform/v1/forms/get/optionvalue
response=$(curl -sqk -X GET "$base_url/wp-json/metform/v1/forms/get/$option_values")
if echo "$response" | grep -q "mf_mailchimp"; then
    curl -sqk -X GET "$base_url/wp-json/metform/v1/forms/get/$option_values" | jq
fi

