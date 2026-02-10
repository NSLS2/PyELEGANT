import importlib
import os

remote_name = os.environ.get("PYELEGANT_REMOTE", "")

if remote_name != "":
    try:
        remote = importlib.import_module(f".{remote_name}", "pyelegant")
    except ImportError as e:
        remote = None
        import_error = str(e)
else:
    remote = None
    import_error = None

if remote is None:
    print("\n## pyelegant:WARNING ##")
    if remote_name == "":
        print(
            "$PYELEGANT_REMOTE not set. All ELEGANT commands will only be run locally."
        )
    elif import_error and any(
        dep in import_error for dep in ["mpi4py", "dill", "qtpy"]
    ):
        print(f"Cannot load remote module '{remote_name}': {import_error}")
        print(
            "Missing parallel dependencies. Install with: pip install -e '.[parallel]' or use pixi environment 'all' or 'parallel'"
        )
        print("All ELEGANT commands will only be run locally.")
    elif import_error:
        print(f"Cannot load remote module '{remote_name}': {import_error}")
        print("All ELEGANT commands will only be run locally.")
    else:
        print(
            f"Invalid $PYELEGANT_REMOTE: '{remote_name}'. All ELEGANT commands will only be run locally."
        )
