import permasigner.__main__
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--codesign', action='store_true',
                        help="uses codesign instead of ldid")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="shows some debug info, only useful for testing")
    parser.add_argument('-u', '--url', type=str,
                        help="the direct URL of the IPA to be signed")
    parser.add_argument('-p', '--path', type=str,
                        help="the direct local path of the IPA to be signed")
    parser.add_argument('-i', '--install', action='store_true',
                        help="installs the application to your device")
    parser.add_argument('-n', '--noinstall',
                        action='store_true', help="skips the install prompt")
    parser.add_argument('-o', '--output', type=str,
                        help="specify output file")
    parser.add_argument('-b', '--bundleid', type=str,
                        help="specify new bundle id")
    parser.add_argument('-N', '--name', type=str,
                        help="specify new app name")
    parser.add_argument('-m', '--minver', type=str,
                        help="specify new minimum app version (14.0 recommended)")
    args = parser.parse_args()

    permasigner.__main__.main(args)
