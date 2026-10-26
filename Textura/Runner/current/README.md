# Runner

Runner owns the portable command entry, local orchestration and maintenance checks. Read [COMMAND.md](COMMAND.md) for actual command forms. The Python entry requires Python 3.11 or newer; the PowerShell launcher can discover the locally bundled runtime or use `TEXTURA_PYTHON`. No packages are installed by these commands.

Inputs come from explicit arguments and Configuration. Output is JSON on standard output; failures return a nonzero exit code and a JSON error on standard error. `validate` returns 1 for integrity findings; input/operation errors normally return 2. Parser usage errors also return 2. Successful execution is not proof of factual correctness.

All records are written by the owning handler, inside that component's `current/records/`. Source files and drafts are copied rather than modified. Maintenance snapshots stay in the affected component's `history/`. Runner does not own another component's data or create a global version archive.

This is a single-author, sequential local workflow. Do not run competing mutations against the same installation. Filesystem permissions are the host's responsibility; privacy labels guide agents and are not encryption or an operating-system access barrier. No command invokes a model, purchases a service, publishes content or writes to Bibliotheca Magna.

`--root` selects a data installation for testing or an explicitly selected workspace. Implementation modules always load from the launcher's installation. The root must already exist and contain Configuration. Use absolute source paths when running outside the installation.
