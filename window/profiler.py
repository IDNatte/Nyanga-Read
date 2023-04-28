from memory_profiler import profile
from app import main
import cProfile


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()
    profiler.dump_stats("app_benchmark.prof")
