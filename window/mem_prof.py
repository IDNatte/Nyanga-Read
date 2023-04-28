from memory_profiler import profile
from app import main


@profile
def test():
    main()
