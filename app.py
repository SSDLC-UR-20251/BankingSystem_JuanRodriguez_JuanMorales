import python
from Stmt s, string kind
private import semmle.python.types.Builtins
from CallNode call, ControlFlowNode func

where major_version() = 2 and call.getFunction() = func and func.pointsTo(Value::named("apply"))
select call, "Call to the obsolete builtin function 'apply'."

where
  s instanceof Return and kind = "return" and exists(Try t | t.getFinalbody().contains(s))
  or
  s instanceof Break and
  kind = "break" and
  exists(Try t | t.getFinalbody().contains(s) |
    not exists(For loop | loop.contains(s) and t.getFinalbody().contains(loop)) and
    not exists(While loop | loop.contains(s) and t.getFinalbody().contains(loop))
  )
select s, "'" + kind + "' in a finally block will swallow any exceptions raised."
