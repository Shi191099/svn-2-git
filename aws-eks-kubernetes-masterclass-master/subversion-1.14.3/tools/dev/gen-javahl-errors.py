#!/usr/bin/env python
#
# gen-javahl-errors.py: Generate a Java class containing an enum for the
#                       C error codes
#
# ====================================================================
#    Licensed to the Apache Software Foundation (ASF) under one
#    or more contributor license agreements.  See the NOTICE file
#    distributed with this work for additional information
#    regarding copyright ownership.  The ASF licenses this file
#    to you under the Apache License, Version 2.0 (the
#    "License"); you may not use this file except in compliance
#    with the License.  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing,
#    software distributed under the License is distributed on an
#    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#    KIND, either express or implied.  See the License for the
#    specific language governing permissions and limitations
#    under the License.
# ====================================================================
#

import sys, os

try:
  from svn import core
except ImportError as e:
  sys.stderr.write("ERROR: Unable to import Subversion's Python bindings: '%s'\n" \
                   "Hint: Set your PYTHONPATH environment variable, or adjust your " \
                   "PYTHONSTARTUP\nfile to point to your Subversion install " \
                   "location's svn-python directory.\n" % e)
  sys.stderr.flush()
  sys.exit(1)

def get_errors():
  errs = {}
  for key in vars(core):
    if key.find('SVN_ERR_') == 0:
      try:
        val = int(vars(core)[key])
        errs[val] = key
      except:
        pass
  return errs

def gen_javahl_class(error_codes, output_filename):
  jfile = open(output_filename, 'w')
  jfile.write(
"""/** ErrorCodes.java - This file is autogenerated by gen-javahl-errors.py
 */

package org.tigris.subversion.javahl;

/**
 * Provide mappings from error codes generated by the C runtime to meaningful
 * Java values.  For a better description of each error, please see
 * svn_error_codes.h in the C source.
 */
public class ErrorCodes
{
""")

  keys = sorted(error_codes.keys())

  for key in keys:
    # Format the code name to be more Java-esque
    code_name = error_codes[key][8:].replace('_', ' ').title().replace(' ', '')
    code_name = code_name[0].lower() + code_name[1:]

    jfile.write("    public static final int %s = %d;\n" % (code_name, key))

  jfile.write("}\n")
  jfile.close()

if __name__ == "__main__":
  if len(sys.argv) > 1:
    output_filename = sys.argv[1]
  else:
    output_filename = os.path.join('..', '..', 'subversion', 'bindings',
                                   'javahl', 'src', 'org', 'tigris',
                                   'subversion', 'javahl', 'ErrorCodes.java')

  gen_javahl_class(get_errors(), output_filename)
