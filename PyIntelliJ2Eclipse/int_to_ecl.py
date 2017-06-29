import fnmatch
import json
import os
import ordereddict
import sys
import xmltodict
from xmljson import badgerfish as bf
from lxml.html import Element, tostring
from progressbar import ProgressBar, Bar, Percentage, ETA

output_dict = {
    "classpath": []
}


def addSrcType(intellij_dict):
    for src in intellij_dict['module']['component']['content'].get('sourceFolder', {}):
        src_tmp = {
        "classpathentry":{
            "@kind": "src",

        }}
        if type(src)==ordereddict:
            src_tmp['classpathentry']['@path'] = src['@url'].replace('file://$MODULE_DIR$', '')
            output_dict['classpath'].append(src_tmp)

def addCombinedRules(intellij_dict):
    for order_entry in intellij_dict['module']['component']['orderEntry']:
        if order_entry['@type'] != 'module':
            continue
        src_tmp = {
        "classpathentry": {
            "@kind": "src",
            "@path": None,
            "@combineaccessrules": "false"
         }
        }
        src_tmp['classpathentry']['@path'] = '/' + order_entry['@module-name']
        output_dict['classpath'].append(src_tmp)


def addConType(intellij_dict):
    for order_entry in intellij_dict['module']['component']['orderEntry']:
        if order_entry['@type'] != 'library':
            continue
        src_tmp = {
        "classpathentry": {
            "@kind": "con",
            "@path": None
        }
        }
        src_tmp['classpathentry']['@path'] = "org.eclipse.jdt.USER_LIBRARY/" + order_entry['@name']
        output_dict['classpath'].append(src_tmp)


def main():
    absolute_folder = sys.argv[1]
    pattern = '*.iml'
    fileList = []
    # Walk through directory
    for dName, sdName, fList in os.walk(absolute_folder):
        for fileName in fList:
            if fnmatch.fnmatch(fileName, pattern): # Match search string
                fileList.append(os.path.join(dName, fileName))
    pbar = ProgressBar(widgets=['Processing :', Percentage(), ' ', Bar(), ' ', ETA()], maxval=len(fileList)).start()
    fcount = 0
    for fileName in fileList:
        eclipse_file_path = os.path.dirname(fileName)+'/.classpath'
        with open(fileName, 'r') as f:
            intellij_data = f.read()
        if not intellij_data:
            pass
        intellij_dict = xmltodict.parse(intellij_data)
        fcount = fcount + 1
        # print(intellij_dict)
        addSrcType(intellij_dict)
        addCombinedRules(intellij_dict)
        addConType(intellij_dict)
        # print json.dumps(intellij_dict)
        result = bf.etree(output_dict, root=Element('classpath'))

        #print tostring(result)
        with open(eclipse_file_path, 'w') as f:
            data = tostring(result, doctype='<?xml version="1.0" encoding="UTF-8"?>')
            data = data.replace('<classpath>','')
            data = data.replace('</classpath>', '')
            data = data.replace('<?xml version="1.0" encoding="UTF-8"?>', '<?xml version="1.0" encoding="UTF-8"?><classpath>')
            data = data +'</classpath>'
            f.write(data)
        # Add .project file
        project_path = os.path.dirname(fileName)+'/.project'
        xml_data = """<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
    <name>%s</name>
    <comment/>
    <projects/>
    <buildSpec>
	<buildCommand>
		<name>org.eclipse.jdt.core.javabuilder</name>
		<arguments/>
	</buildCommand>
    </buildSpec>
    <natures>
	<nature>org.eclipse.jdt.core.javanature</nature>
    </natures>
</projectDescription>"""
        root_name = os.path.splitext(os.path.basename(fileName))[0]
        xml_data = xml_data%(root_name)
        with open(project_path, 'w') as f:
            f.write(xml_data)
            pbar.update(fcount)
    pbar.finish()

if __name__ == '__main__':
    main()
