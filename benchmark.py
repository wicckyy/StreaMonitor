import timeit
import random

class MockVideoData:
    def __init__(self, filename, filesize):
        self.filename = filename
        self.filesize = filesize

class MockBot:
    def __init__(self, num_videos):
        self.video_files = [MockVideoData(f"video_{i}.mp4", random.randint(1000, 100000)) for i in range(num_videos)]
        self.video_files_total_size = sum(v.filesize for v in self.video_files)

def old_way(streamer):
    videos = {}
    for video in streamer.video_files:
        videos[video.filename] = video
    return videos

def new_way(streamer):
    videos = {video.filename: video for video in streamer.video_files}
    return videos

if __name__ == "__main__":
    for size in [10, 50, 100, 500, 1000]:
        streamer = MockBot(size)

        old_time = timeit.timeit("old_way(streamer)", globals=globals(), number=10000)
        new_time = timeit.timeit("new_way(streamer)", globals=globals(), number=10000)

        print(f"Size: {size}")
        print(f"  Old way: {old_time:.5f}s")
        print(f"  New way: {new_time:.5f}s")
        print(f"  Improvement: {((old_time - new_time) / old_time) * 100:.2f}%\n")
