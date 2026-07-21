from .code_tools import read_file, list_directory
from .file_tools import list_files, grep_file
from .security_tools import security_scan


def make_search_codebase_tool(rag_tool):
    def search_codebase(query):
        return rag_tool.search_codebase(query)

    return search_codebase


TOOL_REGISTRY = {
    "read_file": {
        "function": read_file,
        "description": "Read the contents of a file",
        "args": {
            "path": "file path"
        }
    },
    "list_directory": {
        "function": list_directory,
        "description": "List the files contained in a directory",
        "args": {
            "path": "folder to analyze, default='.'"
        }
    },
    "list_files": {
        "function": list_files,
        "description": "List all files in the project",
        "args": {
            "path": "optional folder, default='.'"
        }
    },
    "grep_file": {
        "function": grep_file,
        "description": "Search for a word inside the project files",
        "args": {
            "keyword": "word to search for"
        }
    },
    "security_scan": {
        "function": security_scan,
        "description": "Runs an automated scan of the project for vulnerability patterns",
        "args": {
            "path": "Folder to analyze"
        }
    },
    "search_codebase": {
        "function": None,
        "description": "Semantically search the most relevant code in the repository using the RAG.",
        "args": {
            "query": "Description of what you are looking for"
        }
    },
}


def get_tool_specs(tool_names, extra_tools=None, rag_tool=None):
    specs = {}
    for name in tool_names:
        if name not in TOOL_REGISTRY:
            continue

        spec = dict(TOOL_REGISTRY[name])
        if name == "search_codebase" and rag_tool is not None:
            spec["function"] = make_search_codebase_tool(rag_tool)

        specs[name] = spec

    if extra_tools:
        for name, spec in extra_tools.items():
            specs[name] = spec

    return specs
