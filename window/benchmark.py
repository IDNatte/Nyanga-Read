from app import server_main
import cProfile
import webview
import timeit


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
        debug=True,
    )


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    server_exec_bench = timeit.timeit(stmt=server_main, number=1)
    window_exec_bench = timeit.timeit(stmt=test, number=1)

    profiler.disable()
    profiler.dump_stats("app_benchmark.prof")

    print(
        f"server exec time : {round(server_exec_bench, 3)} \nwindow exec time : {round(window_exec_bench, 3)}"
    )
