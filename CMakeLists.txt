#
# Initial set-up
#

cmake_minimum_required(VERSION 3.15)

project(classgen)
include(cmake/project.cmake)
include(cmake/publish.cmake)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)

# Languages
include(cmake/cxx.cmake)
include(cmake/python.cmake)

# Support
include(cmake/artefacts.cmake)
include(cmake/sources.cmake)

# Subprojects
add_subdirectory(src/version)

# Publication
finalise_publish()