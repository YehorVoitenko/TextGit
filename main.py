import asyncio
from typing import Any

import aiofiles


async def get_hashed_object_with_indexes_from_text(file_path=None) -> list:
    result = []
    async with aiofiles.open(file_path, "r") as file:
        count = 0
        async for line in file:
            result.append((count, hash(line)))
            count += 1
    return result


async def get_hashed_object_with_indexes_from_string(input_object: Any):
    return hash(input_object)


async def main():
    original_text_hashed_values, changed_text_hashed_values = await asyncio.gather(
        get_hashed_object_with_indexes_from_text(file_path="txt_files/original_text"),
        get_hashed_object_with_indexes_from_text(file_path="txt_files/changed_text"),
    )

    text_differance = [
        line
        for line in changed_text_hashed_values
        if line not in set(original_text_hashed_values)
    ]

    await get_text_differences(text_differance)


async def text_differance_generator(text_differance: list):
    for i in text_differance:
        yield i


async def get_text_differences(text_differance: list):
    gen = text_differance_generator(text_differance)
    async for line in gen:
        line_index = line[0]
        async with aiofiles.open("txt_files/changed_text", "r") as file:
            lines = await file.readlines()
            line_file_value_changed_text = lines[line_index]

        async with aiofiles.open("txt_files/original_text", "r") as file:
            try:
                lines = await file.readlines()
                line_file_value_original_text = lines[line_index]

            except IndexError:
                line_file_value_original_text = ""
        print(
            line_index + 1,
            "|",
            compare_strings_by_word(
                line_file_value_original_text, line_file_value_changed_text
            ),
        )


def compare_strings_by_word(old_sting, new_sting):
    result = []

    old_sting_splitted = old_sting.split()
    new_sting_splitted = new_sting.split()

    max_len_sting = old_sting_splitted
    min_len_sting = new_sting_splitted

    if len(old_sting_splitted) < len(new_sting_splitted):
        max_len_sting = new_sting_splitted
        min_len_sting = old_sting_splitted

    for word in max_len_sting:
        try:
            if word not in min_len_sting or min_len_sting.index(
                word
            ) != max_len_sting.index(word):
                result.append((word, min_len_sting[max_len_sting.index(word)]))
        except IndexError:
            result.append((word, ""))
    return result


if __name__ == "__main__":
    asyncio.run(main())
