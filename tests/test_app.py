from markdown_code_runner import MARKERS, md_comment, process_markdown


def test_process_markdown():
    def assert_process(input_lines, expected_output):
        output = process_markdown(input_lines)
        assert output == expected_output, f"Expected {expected_output}, got {output}"

    # Test case 1: Single code block
    input_lines = [
        "Some text",
        MARKERS["start_code"],
        md_comment("print('Hello, world!')"),
        MARKERS["end_code"],
        MARKERS["start_output"],
        "This content will be replaced",
        MARKERS["end_output"],
        "More text",
    ]
    expected_output = [
        "Some text",
        MARKERS["start_code"],
        md_comment("print('Hello, world!')"),
        MARKERS["end_code"],
        MARKERS["start_output"],
        MARKERS["warning"],
        "Hello, world!",
        "",
        MARKERS["end_output"],
        "More text",
    ]
    assert_process(input_lines, expected_output)

    # Test case 2: Two code blocks
    input_lines = [
        "Some text",
        MARKERS["start_code"],
        md_comment("print('Hello, world!')"),
        MARKERS["end_code"],
        MARKERS["start_output"],
        "This content will be replaced",
        MARKERS["end_output"],
        "More text",
        MARKERS["start_code"],
        md_comment("print('Hello again!')"),
        MARKERS["end_code"],
        MARKERS["start_output"],
        "This content will also be replaced",
        MARKERS["end_output"],
    ]
    expected_output = [
        "Some text",
        MARKERS["start_code"],
        md_comment("print('Hello, world!')"),
        MARKERS["end_code"],
        MARKERS["start_output"],
        MARKERS["warning"],
        "Hello, world!",
        "",
        MARKERS["end_output"],
        "More text",
        MARKERS["start_code"],
        md_comment("print('Hello again!')"),
        MARKERS["end_code"],
        MARKERS["start_output"],
        MARKERS["warning"],
        "Hello again!",
        "",
        MARKERS["end_output"],
    ]
    assert_process(input_lines, expected_output)

    # Test case 3: No code blocks
    input_lines = [
        "Some text",
        "More text",
    ]
    expected_output = [
        "Some text",
        "More text",
    ]
    assert_process(input_lines, expected_output)
