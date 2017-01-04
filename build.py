from conan.packager import ConanMultiPackager
import platform


if __name__ == "__main__":
    builder = ConanMultiPackager()

    builder.add_common_builds(shared_option_name="curl-cpp:shared", pure_c=False)

    accepted_builds = []
    if platform.system() == "Linux" or platform.system() == "Darwin":
        for build in builder.builds:
            if build[0]["arch"] != "x86":
                accepted_builds.append([build[0], build[1]])
        builder.builds = accepted_builds

    builder.run()
