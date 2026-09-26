from ora_plan import parse_plan

def test_parse_common_plan():
    text="""| Id | Operation          | Name      | Rows | Cost |
|  0 | SELECT STATEMENT   |           | 10   | 12   |
|* 1 | TABLE ACCESS FULL  | CUSTOMERS | 10   | 12   |"""
    steps=parse_plan(text)
    assert len(steps)==2
    assert steps[1].name=="CUSTOMERS"
    assert "scanning" in steps[1].meaning.lower()
