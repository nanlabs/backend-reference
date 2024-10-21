import argparse


def start():
    parser = argparse.ArgumentParser(
        description="Just an example", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
    parser.add_argument("-e", "--exclude", action="store_true", help="something to exclude")
    args = parser.parse_args()
    config = vars(args)
    print(config)


__name__ == "__main__" and start()
