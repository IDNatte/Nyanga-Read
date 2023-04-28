from app import server_main
import cProfile
import webview


def test():
    webview.create_window(
        "Nyanga Read",
        "http://localhost:5000",
        width=1280,
        height=700,
        min_size=(1280, 800),
    )

    webview.start(
        user_agent="pywebview-client/1.0 pywebview-ui/3.0.0",
        private_mode=False,
        debug=True,
    )


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    server_main()
    test()

    profiler.disable()
    profiler.dump_stats("app_benchmark.prof")
