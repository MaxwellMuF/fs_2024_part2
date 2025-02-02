from pylint.pyreverse.main import Run

# with open("data_pipeline_berlin.py", "w") as f:
#     f.write(file_content)

# Run pyreverse to generate a UML diagram
args = ["-o", "png", "-p", "UserClasses", "domain/src/berlin_data_process/data_pipeline_berlin.py"]
Run(args)

# Use pantuml in bash instead
"""pyreverse -o plantuml -p UserClasses domain/src/berlin_data_process/data_pipeline_berlin.py > classes.puml
"""