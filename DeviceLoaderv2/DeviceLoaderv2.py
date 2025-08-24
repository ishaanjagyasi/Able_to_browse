from _Framework.ControlSurface import ControlSurface
import Live


class DeviceLoader(ControlSurface):
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self.log_message("DeviceLoader: Starting initialization...")

        try:
            self.browser = self.application().browser
            self.song = self.application().get_document()
            self.device_cache = {}

            self.log_message("DeviceLoader: Connected to Live API successfully")

            # Build cache safely
            self.build_device_cache()

            self.log_message(
                "DeviceLoader: Initialization complete! Cache has %d items"
                % len(self.device_cache)
            )

        except Exception as e:
            self.log_message("DeviceLoader: Initialization error: %s" % str(e))

    def build_device_cache(self):
        """Build cache safely"""
        try:
            self.device_cache = {}
            self.log_message("DeviceLoader: Building device cache...")

            # Only do basic categories first
            basic_categories = [
                ("instruments", self.browser.instruments),
                ("audio_effects", self.browser.audio_effects),
                ("midi_effects", self.browser.midi_effects),
                ("drums", self.browser.drums),
                ("sounds", self.browser.sounds),
            ]

            for category_name, category in basic_categories:
                try:
                    if category:
                        self.log_message("DeviceLoader: Scanning %s..." % category_name)
                        self._index_browser_items(category, category_name, [])
                        self.log_message(
                            "DeviceLoader: %s done, cache now has %d items"
                            % (category_name, len(self.device_cache))
                        )
                    else:
                        self.log_message(
                            "DeviceLoader: %s is None, skipping" % category_name
                        )
                except Exception as e:
                    self.log_message(
                        "DeviceLoader: Error scanning %s: %s" % (category_name, str(e))
                    )

            # SAFE EXTENSIONS - Add more browser sections
            extended_categories = [
                ("packs", "packs"),
                ("user_library", "user_library"),
                ("legacy_library", "legacy_library"),
                ("plugins", "plugins"),
                ("vst_plugins", "vst_plugins"),
                ("au_plugins", "au_plugins"),
            ]

            for attr_name, category_name in extended_categories:
                try:
                    if hasattr(self.browser, attr_name):
                        browser_obj = getattr(self.browser, attr_name)
                        if browser_obj:
                            self.log_message("DeviceLoader: Scanning %s..." % attr_name)
                            self._index_browser_items(browser_obj, category_name, [])
                            self.log_message(
                                "DeviceLoader: %s done, cache now has %d items"
                                % (attr_name, len(self.device_cache))
                            )
                except Exception as e:
                    self.log_message(
                        "DeviceLoader: Error scanning %s: %s" % (attr_name, str(e))
                    )

            # Try hotswap
            try:
                if (
                    hasattr(self.browser, "hotswap_target")
                    and self.browser.hotswap_target
                ):
                    if hasattr(self.browser.hotswap_target, "item"):
                        self.log_message("DeviceLoader: Scanning hotswap...")
                        self._index_browser_items(
                            self.browser.hotswap_target.item, "hotswap", []
                        )
                        self.log_message(
                            "DeviceLoader: hotswap done, cache now has %d items"
                            % len(self.device_cache)
                        )
            except Exception as e:
                self.log_message("DeviceLoader: Error scanning hotswap: %s" % str(e))

            self.log_message(
                "DeviceLoader: Cache build complete with %d items"
                % len(self.device_cache)
            )

        except Exception as e:
            self.log_message("DeviceLoader: Cache build failed: %s" % str(e))

    def _index_browser_items(self, item, category, path):
        """Recursively index browser items"""
        try:
            if not item:
                return

            current_path = path + [str(item.name)]

            # Check if loadable
            try:
                if hasattr(item, "is_loadable") and item.is_loadable:
                    item_name = str(item.name).lower()

                    self.device_cache[item_name] = {
                        "item": item,
                        "name": str(item.name),
                        "category": category,
                        "path": current_path,
                    }

                    # Add word-based search
                    words = item_name.replace("-", " ").replace("_", " ").split()
                    for word in words:
                        if len(word) > 2 and word not in self.device_cache:
                            self.device_cache[word] = {
                                "item": item,
                                "name": str(item.name),
                                "category": category,
                                "path": current_path,
                            }
            except:
                pass

            # Process children
            try:
                if hasattr(item, "children") and item.children:
                    for child in item.children:
                        self._index_browser_items(child, category, current_path)
            except:
                pass

        except Exception as e:
            # Skip problematic items
            pass

    def search_device(self, query):
        """Search for device"""
        query = str(query).lower().strip()

        # Exact match
        if query in self.device_cache:
            return self.device_cache[query]

        # Partial matches
        matches = []
        for key, item_data in self.device_cache.items():
            if query in key:
                matches.append((len(key), key, item_data))

        # Sort by length (shorter matches first)
        matches.sort()

        return matches[0][2] if matches else None

    def load_device(self, device_name):
        """Load device onto selected track"""
        try:
            self.log_message("DeviceLoader: Loading device: %s" % device_name)

            device_data = self.search_device(device_name)

            if not device_data:
                return "ERROR: Device '%s' not found" % device_name

            selected_track = self.song.view.selected_track
            if not selected_track:
                return "ERROR: No track selected"

            # Load the device
            browser_item = device_data["item"]
            self.browser.load_item(browser_item)

            success_msg = "SUCCESS: Loaded '%s'" % device_data["name"]
            self.log_message("DeviceLoader: %s" % success_msg)
            return success_msg

        except Exception as e:
            error_msg = "ERROR: %s" % str(e)
            self.log_message("DeviceLoader: %s" % error_msg)
            return error_msg

    def test_device_loading(self, device_name="Operator"):
        """Test method for Max for Live"""
        try:
            self.log_message(
                "DeviceLoader: test_device_loading called with: %s" % device_name
            )
            self.log_message(
                "DeviceLoader: Cache has %d items" % len(self.device_cache)
            )

            if len(self.device_cache) == 0:
                self.log_message("DeviceLoader: Cache empty, rebuilding...")
                self.build_device_cache()

            result = self.load_device(device_name)
            self.log_message("DeviceLoader: Result: %s" % result)
            return result

        except Exception as e:
            error_msg = "DeviceLoader: Test error: %s" % str(e)
            self.log_message(error_msg)
            return error_msg

    def disconnect(self):
        """Cleanup"""
        self.log_message("DeviceLoader: Disconnecting...")
        ControlSurface.disconnect(self)
