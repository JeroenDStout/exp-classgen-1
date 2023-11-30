init_directory(classgen)

# Define the Version project
init_project(classgen "support")

# Sources static
setup_project_source(classgen "core"
  script:
    classgen_grammar.g4
)

# Antlr files
set(antlr_generated_files)
antlr_py_build_single(${abs_can_script}/classgen_grammar.g4 "antlr" antlr_generated_files)
setup_project_source_specific(classgen "lang" "generated;script" ${antlr_generated_files})
 
# Target
configure_project_script(classgen)