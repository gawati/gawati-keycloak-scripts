# Gawati KeyCloak management scripts

## Generate a realm from a model Realm

First you will need to create a model realm in Key Cloak. 

 * Create the Realm; 
 * Create Roles; 
 * Create Groups ; 
 * Create Clients; 
 * Create Group Role Mappings

Finally export the model Realm from `Manage -> Export`. Remember to check the `Export Groups`, `Export Clients`, `Export Roles`. 

You can use this JSON file as a template to create new Realms. 

run ( you will need to run `npm install` first) :

```bash
node index.js --new_realm_name=Ethiopia --input_realm=.\exported_from_keycloak.json --output_file=.\ethiopia.json
```

The above will generate a realm for `Ethiopia`, which can be imported back. 

## Bugs

The bugs for the realm generation script are being currently tracked here : https://github.com/gawati/gawati-portal-ui/issues/44


