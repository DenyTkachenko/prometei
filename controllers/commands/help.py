def help(commands_dict):
    print("Available commands:\n")
    for cmd, info in commands_dict.items():
        print(f"Command: {cmd}")
        print(f"  Description: {info.get('description', 'No description')}")
        
        args_required = info.get("args_required", {})
        args_optional = info.get("args_optional", {})
        
        if args_required:
            print("  Required arguments:")
            for arg, validator in args_required.items():
                validator_name = validator.__name__ if callable(validator) else str(validator)
                print(f"    - {arg} (validator: {validator_name})")
        else:
            print("  Required arguments: None")
        
        if args_optional:
            print("  Optional arguments:")
            for arg, validator in args_optional.items():
                validator_name = validator.__name__ if callable(validator) else str(validator)
                print(f"    - {arg} (validator: {validator_name})")
        else:
            print("  Optional arguments: None")
        
        print("-" * 40)
