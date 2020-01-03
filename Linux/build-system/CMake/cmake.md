### basic build command

- mkdir -p build && cd build && cmake .. 
- make -j4 **or** cmake --build .(# CMake 3.15+ only)
- make install 
- **Note**: Upper, lower, and mixed case commands are supported by CMake
- **Note**: Remember `INTERFACE` means things that consumers require but the producer doesn’t. It's related to the transitivity of dependence 
- **Note** that an unquoted value in CMake is the same as a quoted one if there are no spaces in it
- paths may contain a space at any time and should always be quoted when they are a variable (never write `${MY_PATH}`, always should be `"${MY_PATH}"`)
- **Debugging**: cmake3.15 -S .. -B build --trace-source=CMakeLists.txt

### basic command

1. **project**: Sets the name of the project, and stores it in the variable [`PROJECT_NAME`](https://cmake.org/cmake/help/latest/variable/PROJECT_NAME.html#variable:PROJECT_NAME).

   example: `project(Tutorial VERSION 1.2.3.4) `

2. **set**: Set a normal, cache, or environment variable to a given value.

   example: `set(CMAKE_CXX_STANDARD 11)`

3. **configure_file**: Copy a file to another location and modify its contents.

   example: `configure_file(TutorialConfig.h.in TutorialConfig.h)`

   **Note**: The generated file TutorialConfig.h will be in ${PROJECT_BINARY_DIR}

4. **add_executable**: Add an executable to the project using the specified source files.

   example: `add_executable(Tutorial tutorial.cxx)`

5. **target_include_directories**: Add include directories to a target.

   example: `target_include_directories(Tutorial PUBLIC "${PROJECT_BINARY_DIR}")`

6. **cmake_minimum_required**: Sets the minimum required version of cmake for a project.

   example: `cmake_minimum_required(VERSION 3.10)`

   ---

7. **aux_source_directory**: Find all source files in a directory. Collects the names of all the source files in the specified directory and stores the list in the `<variable>` provided.

   example: `aux_source_directory(src/main/cpp/src/ face)` 

8. **option**: Provide an option that the user can optionally select.

   example: `option(USE_MYMATH "Use tutorial provided math implementation" ON)`

9. **message**: Display a message to the user.

   example: `message(STATUS "Can't detect runtime and/or arch") `

10. **add_subdirectory**: Adds a subdirectory to the build.

   example: `add_subdirectory(MathFunctions)`

11. **list**: List operations.

    example: `list(APPEND EXTRA_LIBS MathFunctions)`

    **Note**:

    A list in cmake is a `;` separated group of strings. To create a list the set command can be used. For example, `set(var a b c d e)` creates a list with `a;b;c;d;e`, and `set(var "a b c d e")` creates a string or a list with one item in it. (Note macro arguments are not variables, and therefore cannot be used in LIST commands.)

12. **target_link_libraries**: Specify libraries or flags to use when linking a given target and/or its dependents.

    example: `target_link_libraries(Tutorial PUBLIC ${EXTRA_LIBS})`

13. **add_library**: Adds a library target called <name> to be built from the source files listed in the command invocation. (The source files can be omitted here if they are added later using target_sources().)

    example: `add_library(MathFunctions mysqrt.cxx)  `, default generate XXXX.a or XXXX.so 

---

12. **install**: This command generates installation rules for a project. Rules specified by calls to this command within a source directory are executed in order during installation.

    example: 

    ```cmake
    install(TARGETS Tutorial DESTINATION bin)
    install(FILES MathFunctions.h DESTINATION include)
    # install rules
    # EXPORT: This option associates the installed target files with an export called <export-name>. It must appear before any target options. To actually install the export file itself, call install(EXPORT), documented below.
    install(TARGETS MathFunctions tutorial_compiler_flags
            DESTINATION lib
            EXPORT MathFunctionsTargets)
    # install the configuration targets
    # The EXPORT form generates and installs a CMake file containing code to import targets from the installation tree into another project. 
    install(EXPORT MathFunctionsTargets
      FILE MathFunctionsTargets.cmake
      DESTINATION lib/cmake/MathFunctions
    )
    ```

13. **CMAKE_INSTALL_PREFIX**: If `make install` is invoked or `INSTALL` is built, this directory is prepended onto all install directories. 

    example: `cmake -DCMAKE_INSTALL_PREFIX=./tmp ..` && `make -j4` && `make install`

14. **enable_testing**: Enables testing for this directory and below. This command should be in the source directory root because ctest expects to find a test file in the build directory root.

    example: `enable_testing()`

15. **add_test**: Adds a test called `<name>`. The test name may not contain spaces, quotes, or other characters special in CMake syntax.

    example: `add_test(NAME Usage COMMAND Tutorial)`

16. **set_tests_properties**: Sets a property for the tests. If the test is not found, CMake will report an error. 

    example: `set_tests_properties(Usage
      PROPERTIES PASS_REGULAR_EXPRESSION "Usage:.*number"
      )`

17. **PASS_REGULAR_EXPRESSION**: The output must match this regular expression for the test to pass. If set, the test output will be checked against the specified regular expressions and at least one of the regular expressions has to match, otherwise the test will fail.

18. **function**: Defines a function named `<name>` that takes arguments named `<arg1>`, … The `<commands` in the function definition are recorded; they are not executed until the function is invoked.

    example: 

    ```cmake
    # define a function to simplify adding tests
    function(do_test target arg result)
      add_test(NAME Comp${arg} COMMAND ${target} ${arg})
      set_tests_properties(Comp${arg}
        PROPERTIES PASS_REGULAR_EXPRESSION ${result}
        )
    endfunction(do_test)
    ```

19. `ctest -N` and `ctest -VV`

    ---

20. **include**: Loads and runs CMake code from the file given. Variable reads and writes access the scope of the caller (dynamic scoping). 

    example: 

    ```cmake
    include(CheckSymbolExists)
    # CMAKE_REQUIRED_LIBRARIES = list of libraries to link
    set(CMAKE_REQUIRED_LIBRARIES "m")
    check_symbol_exists(log "math.h" HAVE_LOG)
    check_symbol_exists(exp "math.h" HAVE_EXP)
    ```

21. **target_compile_definitions**: Specifies compile definitions to use when compiling a given `<target>`

    example:   `target_compile_definitions(MathFunctions PRIVATE "HAVE_LOG" "HAVE_EXP")`

22. **target_compile_features**: Specifies compiler features required when compiling a given target. If the feature is not listed in the [`CMAKE_C_COMPILE_FEATURES`](https://cmake.org/cmake/help/latest/variable/CMAKE_C_COMPILE_FEATURES.html#variable:CMAKE_C_COMPILE_FEATURES) variable or [`CMAKE_CXX_COMPILE_FEATURES`](https://cmake.org/cmake/help/latest/variable/CMAKE_CXX_COMPILE_FEATURES.html#variable:CMAKE_CXX_COMPILE_FEATURES) variable, then an error will be reported by CMake. 

    **target_compile_options**: Adds options to the [`COMPILE_OPTIONS`](https://cmake.org/cmake/help/latest/prop_tgt/COMPILE_OPTIONS.html#prop_tgt:COMPILE_OPTIONS) or [`INTERFACE_COMPILE_OPTIONS`](https://cmake.org/cmake/help/latest/prop_tgt/INTERFACE_COMPILE_OPTIONS.html#prop_tgt:INTERFACE_COMPILE_OPTIONS) target properties. 

    example: 

    ```cmake
    add_library(tutorial_compiler_flags INTERFACE)
    target_compile_features(tutorial_compiler_flags INTERFACE cxx_std_11)
    
    # add compiler warning flags just when building this project via
    # the BUILD_INTERFACE genex
    set(gcc_like_cxx "$<COMPILE_LANG_AND_ID:CXX,ARMClang,AppleClang,Clang,GNU>")
    set(msvc_cxx "$<COMPILE_LANG_AND_ID:CXX,MSVC>")
    target_compile_options(tutorial_compiler_flags INTERFACE
      "$<${gcc_like_cxx}:$<BUILD_INTERFACE:-Wall;-Wextra;-Wshadow;-Wformat=2;-Wunused>>"
      "$<${msvc_cxx}:$<BUILD_INTERFACE:-W3>>"
    )
    
    # In this case, will be compiled with -DClimbingStats_FROM_BUILD_LOCATION.
    add_library(ClimbingStats climbingstats.cpp)
    target_compile_definitions(ClimbingStats INTERFACE
      $<BUILD_INTERFACE:ClimbingStats_FROM_BUILD_LOCATION>
      $<INSTALL_INTERFACE:ClimbingStats_FROM_INSTALLED_LOCATION>
    )
    ```

23. **add_custom_command**: Add a custom build rule to the generated build system.

    example: 

    ```cmake
    add_custom_command(
      OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/Table.h
      # Specify the command-line(s) to execute at build time.
      COMMAND MakeTable ${CMAKE_CURRENT_BINARY_DIR}/Table.h 
      # Specify files on which the command depends.
      DEPENDS MakeTable
      )
    ```

24. **InstallRequiredSystemLibraries**: Include this module to search for compiler-provided system runtime libraries and add install rules for them. Some optional variables may be set prior to including the module to adjust behavior:

    example:

    ```cmake
    include(InstallRequiredSystemLibraries)
    set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/License.txt")
    set(CPACK_PACKAGE_VERSION_MAJOR "${Tutorial_VERSION_MAJOR}")
    set(CPACK_PACKAGE_VERSION_MINOR "${Tutorial_VERSION_MINOR}")
    include(CPack)
    ```

25. To create a source distribution you would type(from the binary directory run):

    ```cmake
    cpack --config CPackSourceConfig.cmake
    ```

26. **set_target_properties**: Targets can have properties that affect how they are built.

    example: 

    ```cmake
    option(BUILD_SHARED_LIBS "Build using shared libraries" ON)
    # state that SqrtLibrary need PIC when the default is shared libraries
    set_target_properties(SqrtLibrary PROPERTIES
                            POSITION_INDEPENDENT_CODE ${BUILD_SHARED_LIBS}
                            )
    ```

27. [**Generator expressions**](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html#output-related-expressions): Generator expressions are evaluated during build system generation to produce information specific to each build configuration.

28. **configure_package_config_file**: `configure_package_config_file()` should be used instead of the plain [`configure_file()`](https://cmake.org/cmake/help/latest/command/configure_file.html#command:configure_file) command when creating the `<PackageName>Config.cmake` or `<PackageName>-config.cmake` file for installing a project or library. It helps making the resulting package relocatable by avoiding hardcoded paths in the installed `Config.cmake` file.

    **write_basic_package_version_file**: Writes a file for use as `<PackageName>ConfigVersion.cmake` file to `<filename>`. See the documentation of [find_package()](https://cmake.org/cmake/help/latest/command/find_package.html#command:find_package) for details on this.

    ```cmake
    include(CMakePackageConfigHelpers)
    # generate the config file that is includes the exports
    configure_package_config_file(${CMAKE_CURRENT_SOURCE_DIR}/Config.cmake.in
      "${CMAKE_CURRENT_BINARY_DIR}/MathFunctionsConfig.cmake"
      INSTALL_DESTINATION "lib/cmake/example"
      NO_SET_AND_CHECK_MACRO
      NO_CHECK_REQUIRED_COMPONENTS_MACRO
      )
    # generate the version file for the config file
    write_basic_package_version_file(
      "${CMAKE_CURRENT_BINARY_DIR}/MathFunctionsConfigVersion.cmake"
      VERSION "${Tutorial_VERSION_MAJOR}.${Tutorial_VERSION_MINOR}"
      COMPATIBILITY AnyNewerVersion
    )
    ```

29. **export**: Export targets from the build tree for use by outside projects. Creates a file `<filename>` that may be included by outside projects to import targets from the current project’s build tree. This is useful during **cross-compiling** to build utility executables that can run on the host platform in one project and then import them into another project being compiled for the target platform. 

    example: 

    ```cmake
    # generate the export targets for the build tree
    # needs to be after the install(TARGETS ) command
    export(EXPORT MathFunctionsTargets
      FILE "${CMAKE_CURRENT_BINARY_DIR}/MathFunctionsTargets.cmake"
    )
    ```

30. **set_property**: Sets one property on zero or more objects of a scope.

    ```cmake
    # setup the version numbering
    set_property(TARGET MathFunctions PROPERTY VERSION "1.0.0")
    set_property(TARGET MathFunctions PROPERTY SOVERSION "1")
    ```

31. **get_filename_component**: Get a specific component of a full filename.

    example: 

    ```cmake
    get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)
    ```

32. **mark_as_advanced**: An advanced variable will not be displayed in any of the cmake GUIs unless the `show advanced` option is on.

33. **find_library**: This command is used to find a library. A cache entry named by `` is created to store the result of this command.

    example:

    ```cmake
    # Searches for a specified prebuilt library and stores the path as a
    # variable. Because CMake includes system libraries in the search path by
    # default, you only need to specify the name of the public NDK library
    # you want to add. CMake verifies that the library exists before
    # completing its build.
    find_library( # Sets the name of the path variable.
            log-lib
            # Specifies the name of the NDK library that
            # you want CMake to locate.
            NAMES log)
    ```

34. **[find_package](https://cmake.org/cmake/help/latest/command/find_package.html#id1)**: Find an external project, and load its settings.

    example: 

    ```cmake
    function(find_external_dependency name)
      set(${name}_ROOT ""  CACHE PATH "Root directory to find ${name}")
      mark_as_advanced(${name}_DIR)
      find_package(${name} PATHS ${${name}_ROOT} REQUIRED)
    endfunction()
    
    project(Consumer)
    find_external_dependency(MathFunctions)
    ```

    ```cmake
    # find_package some typical error
    CMake Error at CMakeLists.txt:12 (find_package):
      Could not find a package configuration file provided by "MathFunctions"
      with any of the following names:
    
        MathFunctionsConfig.cmake
        mathfunctions-config.cmake
    
      Add the installation prefix of "MathFunctions" to CMAKE_PREFIX_PATH or set
      "MathFunctions_DIR" to a directory containing one of the above files.  If
      "MathFunctions" provides a separate development package or SDK, be sure it
      has been installed.
    ```

35. **find_package** vs **find_library**

    ```cmake
    Imagine you want to use zlib in your project, you need to find the header file zlib.h, and the library libz.so (on Linux). You can use the low-level cmake commands find_path and find_library to find them, or you can use find_package(ZLIB). The later command will try to find out all what is necessary to use zlib. It can be extra macro definitions, or dependencies.
    
    find_package: when the CMake command find_package(SomeThing) is called, as says the documentation, there are two possibility: the module mode (that searches for a file FindSomeThing.cmake), or the config mode (that searches for a file named SomeThingConfig.cmake).
    ```

36. ##### Reference: 

    1. https://cmake.org/cmake/help/latest/guide/tutorial/index.html
    2. https://gitlab.kitware.com/cmake/cmake/tree/master/Help/guide/tutorial
    3. https://cliutils.gitlab.io/modern-cmake/ 

