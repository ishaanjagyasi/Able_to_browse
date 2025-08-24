def create_instance(c_instance):
    c_instance.log_message("DeviceLoader: create_instance called!")
    try:
        # Method 1: Direct import
        from .DeviceLoaderv2 import DeviceLoader

        c_instance.log_message("DeviceLoader: Method 1 success - Direct import worked!")
        return DeviceLoader(c_instance)
    except:
        try:
            # Method 2: Module import then class access
            import DeviceLoaderv2 as module

            c_instance.log_message(
                "DeviceLoader: Method 2 - Trying to access class from module"
            )
            DeviceLoaderClass = getattr(module, "DeviceLoader", None)
            if DeviceLoaderClass:
                c_instance.log_message(
                    "DeviceLoader: Method 2 success - Found class via getattr!"
                )
                return DeviceLoaderClass(c_instance)
            else:
                c_instance.log_message(
                    "DeviceLoader: Method 2 failed - Class not found via getattr"
                )
        except Exception as e:
            c_instance.log_message("DeviceLoader: Method 2 exception: %s" % str(e))

        try:
            # Method 3: Explicit path import
            import sys
            import os

            current_dir = os.path.dirname(__file__)
            sys.path.insert(0, current_dir)
            exec("from DeviceLoaderv2 import DeviceLoader as LoaderClass")
            c_instance.log_message(
                "DeviceLoader: Method 3 success - Exec import worked!"
            )
            return LoaderClass(c_instance)
        except Exception as e:
            c_instance.log_message("DeviceLoader: Method 3 exception: %s" % str(e))

    c_instance.log_message("DeviceLoader: All methods failed!")
    return None
