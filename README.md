# bb_tools
 This repo cotains small script to solve small problems that I face in bugbounty

## gql_base64.py
This tool extracts base64 encoded strings from a Burp Suite XML export and decode them. Useful for extracting graphql base64 encoded IDs

### Usage
```bash
python gql_base64.py burp_export.xml
```

## sot.py
This tool filters a list of endpoints, removing duplicates that differ only by numeric IDs. It normalizes paths by replacing numeric segments with `{id}` and outputs only the first unique path encountered.

### Usage
```bash
cat endpoints.txt | sot
# or
python3 gql_base64.py burp_export.xml | sot
```
