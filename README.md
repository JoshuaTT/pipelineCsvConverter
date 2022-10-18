# Pipeline CSV Converter

This small python tool converts Harding Pipeline CSV files to Echo compliant CSV files.

The tool expects a json file mapping subjects to departments and another file mapping instructor names to emails. These should be at ./subjToDept.json and ./nameToEmail.json respectively. Both in reference to the location of the convertPipelineToEcho.py.


usage: convertPipelineToEcho.py [-h] [-i INPUTPATH] [-o OUTPUTPATH] [-d] [-e SECONDINPUT]
                                [-t TERM]
<br>
options:<br>
  -h, --help      show this help message and exit<br>
  -i INPUTPATH    Path to input csv file.<br>
  -o OUTPUTPATH   Path to output converted file to.<br>
  -d              Only use this flag if you need to regenerate subjToDept.json<br>
  -e SECONDINPUT  Takes a second path to try and determine name/email mapping. Pass
                  formatted file to i argument.<br>
  -t TERM         The term for the converted file. (e.g. Fall 2022)<br>
