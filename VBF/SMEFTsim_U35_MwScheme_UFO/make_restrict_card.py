import itertools
from parameters import *

coeffs = [par.name for par in all_parameters if par.name[0]=="c"]
print(coeffs)
texnames = {par.name:par.texname for par in all_parameters if par.name[0]=="c"}
print(texnames)

def write_wc_restrict(input_restrict_file):

    import re
    re_wilson = re.compile("[ ](c.*)[ ]")
    for coeff in coeffs:
        with open(input_restrict_file,'rt') as fp: 
            outfile = input_restrict_file.split('.dat')
            tempfile = open(outfile[0]+"_"+coeff+".dat",'wt')

            for line in fp:
                m_val = re_wilson.search(line)
	        if m_val and str(m_val.group(1)) == coeff:
                   tempfile.write(line.replace('0.','1.0'))
	        else: tempfile.write(line)

#    for coeff1,coeff2 in coeff_pairs:
#        with open(input_restrict_file,'rt') as fp: 
#            outfile = input_restrict_file.split('.dat')
#            tempfile = open(outfile[0]+"_"+coeff1+"_"+coeff2+".dat",'wt')

#            for line in fp:
#                m_val = re_wilson.search(line)
#	        if m_val and str(m_val.group(1)) == coeff1:
#                   tempfile.write(line.replace('0.','1.0'))
#	        elif m_val and str(m_val.group(1)) == coeff2:
#                   tempfile.write(line.replace('0.','1.0'))
#	        else: tempfile.write(line)

#write_wc_restrict("restrict_massless.dat")
