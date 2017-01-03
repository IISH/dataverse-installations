#from django.template.defaultfilters import filesizeformat
"""
Human readable file size

source: http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
"""

unit_prefixes1 = ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']
unit_prefixes2 = ['','K','M','G','T','P','E','Z']


def sizeof_fmt(num, suffix='B'):
    #return filesizeformat(num)
    for unit in unit_prefixes2:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)
