from aiogram import Dispatcher


def register_module(
    dp: Dispatcher,
    modules,
) -> None:
    root = sorted([m for m in modules if m.is_root], key=lambda m: m.root)
    children = sorted(
        [m for m in modules if not m.is_root], key=lambda m: m.module_depth
    )
    children = sorted(
        children,
        key=lambda m: m.parent,
    )

    root_map = {}

    for mod in root:
        dp.include_router(router=mod.router.router)
        root_map[mod.root] = mod.router.router
        print("\n[Auto] Root router inculde into dp: {}".format(mod.router.router))
    for mod in children:
        parent_router = root_map.get(mod.parent)
        if not parent_router:
            continue
        parent_router.include_router(mod.router.router)
        print(
            f"\n[Auto] Child router inculded into {parent_router}: {mod.router.router}"
        )
