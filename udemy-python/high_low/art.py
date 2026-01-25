logo = """
 _   _ _____ 
| | | |_   _|
| |_| | | |  
|  _  | | | 
| | | |_| |_
|_| |_|_____|

 _      ____  
| |    / __ \\ 
| |   | |  | |
| |   | |  | | 
| |___| |__| | 
|______\\____/

"""

vs = """
 _    
| |   
| |__ 
| '_ \\
| | | |
|_| |_|

 _    
| |   
| |   
| |   
| |___
|_____|
"""
# #region agent log
import json
newline = '\n'
with open('/Users/rebeccaclarke/Documents/Financial/Gigs/devops_software_engineering/conceptprojects/.cursor/debug.log', 'a') as f: f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"A","location":"art.py:32","message":"vs string definition","data":{"vs_length":len(vs),"vs_repr":repr(vs),"vs_starts_with_newline":vs.startswith(newline),"vs_first_chars":repr(vs[:20])},"timestamp":1733456789000})+'\n')
# #endregion