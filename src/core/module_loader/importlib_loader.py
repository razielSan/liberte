import importlib
from collections import defaultdict
import pkgutil

from core.response.modules_loader import ModuleInfo


def get_root_and_parent(module_name: str, root_package: str):
    relative = module_name.replace(root_package + ".", "")
    parts = relative.split(".childes.")

    root = parts[0].split(".")[
        0
    ]  # отсекаем название файла если роутер корневой - test.router
    parent = root if len(parts) > 1 else None
    return root, parent


def load_modules(root_package: str):
    package = importlib.import_module(root_package)
    modules = defaultdict(dict)
    for module_info in pkgutil.walk_packages(
        path=package.__path__, prefix=package.__name__ + "."
    ):
        module_name = module_info.name
        if not module_name.endswith("settings") and not module_name.endswith("router"):
            continue
        root, parent = get_root_and_parent(
            module_name=module_name, root_package=root_package
        )

        # data = importlib.import_module(module_info.name)
        package_name, file_type = module_name.rsplit(".", 1)
        mod = importlib.import_module(module_name)
        modules[package_name][file_type] = mod
        modules[package_name]["root"] = root
        modules[package_name]["parent"] = parent
        modules[package_name]["package"] = package_name
    array_modules = []
    for package, data in modules.items():
        if "router" not in data or "settings" not in data:
            continue  # дополнительная проверка

        array_modules.append(
            ModuleInfo(
                package=data.get("package"),
                root=data.get("root"),
                parent=data.get("parent"),
                router=data.get("router"),
                settings=data.get("settings"),
            )
        )
    return array_modules
