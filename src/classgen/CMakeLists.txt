init_directory(classgen)

# Define the Version project
init_project(classgen "support")

# Sources static
setup_project_source(classgen "core"
  src:
    dummy.cpp
)

# Target
configure_project_static_lib(classgen)
configure_cxx_target(classgen)