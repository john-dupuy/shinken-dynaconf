def load(obj, env=None, silent=True, key=None, filename=None):
    """
    Reads and loads in to "obj" a single key or all keys from source
    :param obj: the settings instance
    :param env: settings current env (upper case) default='DEVELOPMENT'
    :param silent: if errors should raise
    :param key: if defined load a single key, else load all from `env`
    :param filename: Custom filename to load (useful for tests)
    :return: None
    """
    # Load data from your custom data source (file, database, memory etc)
    # use `obj.set(key, value)` or `obj.update(dict)` to load data
    # use `obj.logger.debug` to log your loader activities
    # use `obj.find_file('filename.ext')` to find the file in search tree
    # Return nothing

    # This loader reads shinken .cfg files
    data = dict()
    found_file = obj.find_file(filename or "settings.cfg")
    if not found_file:
        obj.logger.debug(f"Cannot find {filename} or settings.cfg")

    # first get the object type (assumes objects in file are all of same type
    object_type = None
    with open(found_file) as settings_file:
        for line in settings_file.readlines():
            if line.startswith("#") or line.startswith("}"):
                continue
            if line.startswith("define"):
                # get the object type (host, contact, etc.)
                object_type = line.split()[1].strip()
                if object_type.endswith("{"):
                    object_type = object_type.rstrip("{")
                # pluralize the base key
                object_type = f"{object_type}s"
                data[object_type] = dict()
                break

    # now read the data
    if object_type:
        with open(found_file) as settings_file:
            object_num = -1
            for line in settings_file.readlines():
                if line.startswith("#") or line.startswith("}"):
                    continue
                if line.startswith("define"):
                    object_num += 1
                    data[object_type][f"{object_type}{object_num}"] = dict()
                    continue
                if line.split():
                    line_key, line_value = line.split(None, 1)
                    data[object_type][f"{object_type}{object_num}"][line_key] = line_value.strip()

    if key:
        value = data.get(key.lower())
        obj.logger.debug("CFG loader: %s:%s", key, value)
    else:
        obj.logger.debug("CFG loader: loading: {0}".format(data))
        obj.update(data)

    obj._loaded_files.append(found_file)
