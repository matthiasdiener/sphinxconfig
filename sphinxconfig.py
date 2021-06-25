from os.path import dirname as _dirname, basename as _basename

html_theme = "furo"
html_show_sourcelink = True

project = _basename(_dirname(_dirname(__file__)))

autoclass_content = "class"

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True


def linkcode_resolve(domain, info, linkcode_url=None):
    import os
    import sys
    import inspect
    import pkg_resources

    if domain != "py" or not info["module"]:
        return None

    modname = info["module"]
    topmodulename = modname.split(".")[0]
    fullname = info["fullname"]

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split("."):
        try:
            obj = getattr(obj, part)
        except Exception:
            return None

    try:
        modpath = pkg_resources.require(topmodulename)[0].location
        filepath = os.path.relpath(inspect.getsourcefile(obj), modpath)
        if filepath is None:
            return
    except Exception:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except OSError:
        return None
    else:
        linestart, linestop = lineno, lineno + len(source) - 1

    if linkcode_url is None:
        linkcode_url = (
            f"https://github.com/inducer/{project}/blob/"
            + "main"
            + "/{filepath}#L{linestart}-L{linestop}"
        )

    return linkcode_url.format(
        filepath=filepath, linestart=linestart, linestop=linestop
    )


extensions = [
        "sphinx.ext.autodoc",
        "sphinx.ext.intersphinx",
        "sphinx.ext.linkcode",
        "sphinx.ext.doctest",
        "sphinx.ext.mathjax",
        "sphinx_copybutton",
        ]

__all__ = ("html_theme", "html_show_sourcelink",
        "project", "autoclass_content",
        "copybutton_prompt_text",
        "copybutton_prompt_is_regexp",
        "linkcode_resolve",
        "extensions")
