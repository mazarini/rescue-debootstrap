from rescue_debootstrap.util.env_util import load_env, print_env


def main() -> None:
    env = load_env()
    print_env(env)
    if env.isDebug():
        print(env)


if __name__ == "__main__":
    main()
