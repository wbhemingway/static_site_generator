from copy_static import copy_static


def main():
    src = "/home/willi/workspace/github.com/wbhemingway/static_site_generator/static"
    dst = "/home/willi/workspace/github.com/wbhemingway/static_site_generator/public"
    copy_static(src, dst)


if __name__ == "__main__":
    main()
