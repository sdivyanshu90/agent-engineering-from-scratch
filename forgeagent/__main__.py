"""Minimal offline ForgeAgent entry point; live providers are injected by callers."""
import argparse


def main(argv=None):
    parser=argparse.ArgumentParser(description="ForgeAgent coding-agent library entry point")
    parser.add_argument("--about",action="store_true",help="print the safety and provider-injection contract")
    args=parser.parse_args(argv)
    if args.about:
        print("ForgeAgent requires an injected provider and Workspace. Patch approval is human-only; tests fail closed without an injected backend.")
        return 0
    parser.print_help()
    return 0


if __name__=="__main__":
    raise SystemExit(main())
