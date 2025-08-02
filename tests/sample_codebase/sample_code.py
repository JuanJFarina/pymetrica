class SomeAsyncContext:
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass


async def process_items(items):
    result = []
    async with SomeAsyncContext() as ctx:
        async for item in items:
            if item > 0 and item % 2 == 0:
                result.append(item)
            elif item < 0 or item == 0:
                result.append(-item)
            else:
                result.append(item * 2)
    return result


def compute(x):
    match x:
        case 0:
            return "zero"
        case 1 | 2:
            return "one or two"
        case _:
            return "other"


def main():
    try:
        data = [i for i in range(5) if i % 2 == 0]
        gen = (i * i for i in range(3))
        s = {i for i in range(3)}
        d = {i: str(i) for i in range(2)}

        val = True if len(data) > 2 else False

        count = 0
        while count < 3:
            assert count != 2
            count += 1

    except ValueError:
        print("ValueError!")
    except Exception as e:
        print("Other error:", e)


squares = [n * n for n in range(5) if n > 2]
