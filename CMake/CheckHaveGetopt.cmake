# Check if getopt is present:
INCLUDE (${CMAKE_ROOT}/Modules/CheckIncludeFile.cmake)
SET(DONT_HAVE_GETOPT 1)
ADD_DEFINITIONS(-DDONT_HAVE_GETOPT)

