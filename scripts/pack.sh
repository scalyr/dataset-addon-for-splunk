#!/usr/bin/env bash

SHORT=i:,v:,o:,r:,h
LONG=input:,version:,output:,release:,help
OPTS=$(getopt -a -n pack --options $SHORT --longoptions $LONG -- "$@")

eval set -- "$OPTS"

while :
do
  case "$1" in
    -i | --input )
      input="$2"
      shift 2
      ;;
    -v | --version )
      version="$2"
      shift 2
      ;;
    -o | --output )
      output="$2"
      shift 2
      ;;
    -r | --release )
      release="$2"
      shift 2
      ;;
    -h | --help)
      "This is a pack script"
      exit 2
      ;;
    --)
      shift;
      break
      ;;
    *)
      echo "Unexpected option: $1"
      ;;
  esac
done

echo "Input: ${input}";
echo "Version: ${version}";
echo "Output: ${output}";
echo "Release: ${release}";
echo;

if [ ! -d "${input}" ]; then
  echo "Input directory - ${input} - does not exist.";
  exit 1;
fi;

if [ -z "${version}" ]; then
  echo "Version has to be specified.";
  exit 1;
fi;

echo "Validate package - ${input}" && \
slim validate "${input}" && \
splunk-appinspect inspect "${input}" --included-tags splunk_appinspect && \
echo "Generate package - ${version}" && \
ucc-gen --source "${input}" --ta-version "${version}" && \
jq '.' globalConfig.json > globalConfig.new.json && \
mv globalConfig.new.json globalConfig.json && \
echo "Construct tarball" && \
slim package "${output}/${input}" -o "${release}" && \
echo "Validate released tarball" && \
slim validate "${release}/${input}-${version}.tar.gz"
