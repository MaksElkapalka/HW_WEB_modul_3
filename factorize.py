from multiprocessing import Pool, current_process, cpu_count


def factorize(*numbers):
    for number in numbers:
        results = []
        for num in range(1, number + 1):
            if number % num == 0:
                results.append(num)
    return results


def callback(result):
    print(f"Result in callback: {result}")


if __name__ == "__main__":

    print(f"Count CPU: {cpu_count()}")
    num_list = [128, 255, 99999, 10651060]
    with Pool(cpu_count()) as p:
        p.map_async(
            factorize,
            num_list,
            callback=callback,
        )
        p.close()
        p.join()

    print(f"End {current_process().name}")
