import headerparser

def split_dependencies(dependencies_string): 
    dependencies = []
    for y in dependencies_string.replace(" ","").split(','):
        dependencies.append(y)
    if len(dependencies) > 1:
        return dependencies
    else:
        return [dependencies_string.replace(" ","")]

parser = headerparser.HeaderParser()
parser.add_field("Package", required=True)
parser.add_field("Architecture", required=True)
parser.add_field("Version", required=True)
parser.add_field("Depends", "Pre-Depends" , default = [], multiple=True, type = lambda x: split_dependencies(x))
parser.add_field("Recommends", default=[])
parser.add_field("Suggests", "Enhances" ,default=[], multiple=True, type = lambda x: split_dependencies(x))
parser.add_field("Conflicts", "Breaks", "Replaces", default=[], multiple=True, type = lambda x: split_dependencies(x))
parser.add_field("Provides", default=[], type = lambda x: split_dependencies(x))
parser.add_field("Section")
parser.add_field("Size")
parser.add_field("Filename")
parser.add_field("MD5sum")
parser.add_field("SHA256")
parser.add_additional(enable = True)
# parser.add_field("Pre-Depends", default=[])
# parser.add_field("Replaces", default=[])
# parser.add_field("Enhances", default=[])
# parser.add_field("Breaks", default=[])