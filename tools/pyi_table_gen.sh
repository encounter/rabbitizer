#!/bin/bash

# SPDX-FileCopyrightText: © 2023 Decompollaborate
# SPDX-License-Identifier: MIT

set -e

INPUT_FILE=$1
OUTPUT_FILE=$2

echo "#!/usr/bin/env python3" > ${OUTPUT_FILE}
echo >> ${OUTPUT_FILE}
echo "# SPDX-FileCopyrightText: © 2022-2023 Decompollaborate" >> ${OUTPUT_FILE}
echo "# SPDX-License-Identifier: MIT" >> ${OUTPUT_FILE}
echo >> ${OUTPUT_FILE}
echo "# Automatically generated. DO NOT MODIFY" >> ${OUTPUT_FILE}

echo >> ${OUTPUT_FILE}

cpp -P -I include -I ../include ${INPUT_FILE} >> ${OUTPUT_FILE}
