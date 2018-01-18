#!/usr/bin/env bash
# Generate security documentation for the GSA PSHC discovery application.

SCRIPT_DIR="$(cd "$(dirname "$([ `readlink "$0"` ] && echo "`readlink "$0"`" || echo "$0")")"; pwd -P)"
cd "$SCRIPT_DIR/.."

CONTROL_PDF_FILE="${1}"
EXPORT_DIR="opencontrols/export"

# Remove old security documentation
rm -Rf opencontrols

echo "> Fetching compliance definition dependencies into opencontrols directory"
compliance-masonry get

echo "> Generating security documentation"
compliance-masonry docs gitbook --markdowns compliance/gitbook/markdown --exports "$EXPORT_DIR" LATO

if [ ! -z "$CONTROL_PDF_FILE" ]
then
  echo "> Generating PDF document from security documentation"
  gitbook pdf "$EXPORT_DIR" "$CONTROL_PDF_FILE"
fi