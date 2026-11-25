import project_paths as paths
from tasks.generate import generate_task_file
from tasks.tatsuoka import tatsuoka_expressions, write_tatsuoka_items


def main():
    generate_task_file(
        paths.GENERATED_TASKS,
        count_per_type=1000,
        seed=0,
        excluded_expressions=tatsuoka_expressions(),
    )
    write_tatsuoka_items(paths.TATSUOKA_ITEMS, sample_size=50000)
    print(f"Wrote {paths.TATSUOKA_ITEMS}")


if __name__ == "__main__":
    main()
