from click.testing import CliRunner
from main import hello


def test_hello_help():
    runner = CliRunner()
    result = runner.invoke(hello, ["--help"])
    assert result.exit_code == 0
    assert "Show this message and exit." in result.output

    result_h = runner.invoke(hello, ["-h"])
    assert result_h.exit_code == 0
    assert "Show this message and exit." in result_h.output


def test_hello_version():
    runner = CliRunner()
    result = runner.invoke(hello, ["--version"])
    assert result.exit_code == 0
    assert "1.0.0" in result.output

    result_v = runner.invoke(hello, ["-v"])
    assert result_v.exit_code == 0
    assert "1.0.0" in result_v.output


def test_hello_output():
    runner = CliRunner()
    result = runner.invoke(hello, ["--name", "World"])
    assert result.exit_code == 0
    assert "Hello World" in result.output
