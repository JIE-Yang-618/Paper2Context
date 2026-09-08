from paper2context.cli import main

def test_doctor(capsys):
    assert main(['doctor'])==0
    assert 'local-only' in capsys.readouterr().out

def test_inspect_cli(sample_pdf,capsys):
    assert main(['inspect',str(sample_pdf)])==0
    assert 'Pages: 4' in capsys.readouterr().out

def test_shorthand_convert(sample_pdf,tmp_path,monkeypatch,capsys):
    monkeypatch.chdir(tmp_path)
    assert main([str(sample_pdf)])==0
    assert 'Output:' in capsys.readouterr().out

def test_read_only_command_has_no_output_side_effect(sample_pdf,tmp_path,monkeypatch,capsys):
    monkeypatch.chdir(tmp_path)
    assert main(['metadata',str(sample_pdf)])==0
    assert not (sample_pdf.parent/(sample_pdf.stem+'_context')).exists()
