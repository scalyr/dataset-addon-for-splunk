#!/usr/bin/env bash

SDLAPP_VERSION_CURRENT=`jq -r '.meta.version' globalConfig.json`
echo "current version: $SDLAPP_VERSION_CURRENT"

SDLAPP_VERSION_NEW=`awk -vFS=. -vOFS=. '{$NF++;print}' <<<"$SDLAPP_VERSION_CURRENT"`
echo "new version: $SDLAPP_VERSION_NEW"

# update version
jq ".meta.version=\""$SDLAPP_VERSION_NEW"\"" globalConfig.json | sponge globalConfig.json
jq ".info.id.version=\""$SDLAPP_VERSION_NEW"\"" TA_dataset/app.manifest | sponge TA_dataset/app.manifest

crudini --set TA_dataset/default/app.conf launcher version $SDLAPP_VERSION_NEW
crudini --set TA_dataset/default/app.conf id version $SDLAPP_VERSION_NEW
