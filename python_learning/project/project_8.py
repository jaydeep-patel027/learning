import asyncio, threading, time
from multiprocessing import Pool

# ----- 1. ASYNCIO: many network checks, one program -----
# Work type: waiting. We chose asyncio because pinging websites spends most of
# the time waiting for network replies, allowing one program to switch between
# all 20 checks at each 'await'.
async def check_site(url):
    await asyncio.sleep(1)                  # wait for the reply
    return url, "UP"

async def check_all(urls):
    return await asyncio.gather(*(check_site(u) for u in urls))

async def check_all_one_by_one(urls):
    return [await check_site(u) for u in urls]


# ----- 2. THREADING: many downloads, workers wait for files -----
# Work type: waiting. We chose threading because each worker spends most of its
# time waiting for the 1-second download to finish, so multiple threads can wait
# at the same time.
def download(name, results):
    time.sleep(1)                           # pretend to download a file (1 second)
    results.append(name)

def download_all(names):
    results = []
    threads = [threading.Thread(target=download, args=(n, results)) for n in names]
    for t in threads: t.start()             # start all 10 workers first
    for t in threads: t.join()              # wait for all 10 to finish
    return results

def download_all_one_by_one(names):
    results = []
    for n in names:
        download(n, results)
    return results


# ----- 3. MULTIPROCESSING: heavy work on several cores -----
# Work type: calculating. We chose multiprocessing because resizing images is
# heavy CPU calculation, and Pool runs the work across separate processor cores
# at the same time.
def resize(image):
    return sum(i * i for i in range(10_000_000))   # heavy CPU work


if __name__ == "__main__":
    # Prepare data according to Section 7 (20 sites, 10 downloads, 8 images)
    urls = [f"site{i}.com" for i in range(1, 21)]
    files = [f"img{i}.png" for i in range(1, 11)]
    images = [f"p{i}" for i in range(1, 9)]

    # --- 1. Test Asyncio (20 sites) ---
    t0 = time.perf_counter()
    asyncio.run(check_all_one_by_one(urls))
    print(f"Asyncio Sequential (20 sites): {time.perf_counter() - t0:.2f}s")

    t0 = time.perf_counter()
    site_results = asyncio.run(check_all(urls))
    print(f"Asyncio Concurrent (20 sites): {time.perf_counter() - t0:.2f}s")
    print("Site results:", site_results)
    print("-" * 50)

    # --- 2. Test Threading (10 downloads) ---
    t0 = time.perf_counter()
    download_all_one_by_one(files)
    print(f"Threading Sequential (10 files): {time.perf_counter() - t0:.2f}s")

    t0 = time.perf_counter()
    dl_results = download_all(files)
    print(f"Threading Concurrent (10 files): {time.perf_counter() - t0:.2f}s")
    print("Downloaded:", dl_results)
    print("-" * 50)

    # --- 3. Test Multiprocessing (8 images) ---
    t0 = time.perf_counter()
    seq_resized = [resize(img) for img in images]
    print(f"Multiprocessing Sequential (8 images): {time.perf_counter() - t0:.2f}s")

    t0 = time.perf_counter()
    with Pool(4) as pool:
        mp_resized = pool.map(resize, images)
    print(f"Multiprocessing Pool(4) (8 images): {time.perf_counter() - t0:.2f}s")
    print("Resized results:", mp_resized)
    
    
    
    
