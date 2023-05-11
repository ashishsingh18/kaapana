from time import time
import json
import networkx as nx
from os.path import join, dirname, basename, exists, isfile, isdir


class BuildUtils:
    container_images_available = None
    container_images_unused = None
    charts_available = None
    charts_unused = None
    base_images_used = None
    logger = None
    kaapana_dir = None
    default_registry = None
    platform_filter = None
    external_source_dirs = None
    issues_list = None
    exit_on_error = True
    enable_build_kit = None
    create_offline_installation = None
    skip_push_no_changes = None
    push_to_microk8s = None

    @staticmethod
    def add_container_images_available(container_images_available):
        BuildUtils.container_images_available = container_images_available

        BuildUtils.container_images_unused = {}
        for image_av in BuildUtils.container_images_available:
            BuildUtils.container_images_unused[image_av.tag] = image_av

    @staticmethod
    def add_charts_available(charts_available):
        BuildUtils.charts_available = charts_available

        BuildUtils.charts_unused = {}
        for chart_av in BuildUtils.charts_available:
            BuildUtils.charts_unused[chart_av.chart_id] = chart_av

        for chart_object in BuildUtils.charts_available:
            chart_object.check_dependencies()

    @staticmethod
    def init(kaapana_dir, build_dir, external_source_dirs, platform_filter, default_registry, http_proxy, logger, exit_on_error, enable_build_kit,
             create_offline_installation, skip_push_no_changes, push_to_microk8s):

        BuildUtils.logger = logger
        BuildUtils.kaapana_dir = kaapana_dir
        BuildUtils.build_dir = build_dir
        BuildUtils.platform_filter = platform_filter
        BuildUtils.default_registry = default_registry
        BuildUtils.http_proxy = http_proxy
        BuildUtils.external_source_dirs = external_source_dirs
        BuildUtils.exit_on_error = exit_on_error
        BuildUtils.issues_list = []

        BuildUtils.base_images_used = []
        BuildUtils.enable_build_kit = enable_build_kit
        BuildUtils.create_offline_installation = create_offline_installation
        BuildUtils.skip_push_no_changes = skip_push_no_changes
        BuildUtils.push_to_microk8s = push_to_microk8s

    @staticmethod
    def get_timestamp():
        return str(int(time() * 1000))

    @staticmethod
    def get_build_order(build_graph):
        graph_bottom_up = list(reversed(list(nx.topological_sort(build_graph))))

        build_order = []
        for entry in graph_bottom_up:
            if "root" in entry.lower():
                continue

            name = entry.split(":")[1]
            version = entry.split(":")[2]
            entry_id = f"{name}:{version}"

            if "chart:" in entry:
                if entry_id in BuildUtils.charts_unused:
                    del BuildUtils.charts_unused[entry_id]
                else:
                    print(f"{entry_id} not found!")
                continue
            elif "base-image:" in entry:
                if entry_id in BuildUtils.container_images_unused:
                    del BuildUtils.container_images_unused[entry_id]
            elif "container:" in entry:
                if entry_id in BuildUtils.container_images_unused:
                    del BuildUtils.container_images_unused[entry_id]

            if "local-only" in name or BuildUtils.default_registry in name:
                build_order.append(entry_id)

        return build_order

    @staticmethod
    def make_log(output):
        std_out = output.stdout.split("\n")[-100:]
        log = {}
        len_std = len(std_out)
        for i in range(0, len_std):
            log[i] = std_out[i]
        std_err = output.stderr.split("\n")
        for err in std_err:
            if err != "":
                len_std += 1
                log[len_std] = f"ERROR: {err}"
        return log

    @staticmethod
    def generate_issue(component, name, level, msg, path="", output=None):
        log = ""
        if output != None:
            log = BuildUtils.make_log(output)
            BuildUtils.logger.error("LOG:")
            BuildUtils.logger.error(log)

        issue = {
            "component": component,
            "name": name,
            "filepath": path,
            "level": level,
            "msg": msg,
            "log": log,
            "timestamp": BuildUtils.get_timestamp(),
        }
        BuildUtils.issues_list.append(issue)
        BuildUtils.logger.warning(json.dumps(issue, indent=4, sort_keys=False))

        if BuildUtils.exit_on_error or level == "FATAL":
            exit(1)

    @staticmethod
    def generate_component_usage_info():
        unused_containers_json_path = join(BuildUtils.build_dir, "build_containers_unused.json")
        BuildUtils.logger.debug("")
        BuildUtils.logger.debug("Collect unused containers:")
        BuildUtils.logger.debug("")
        unused_container = []
        for container_id, container in BuildUtils.container_images_unused.items():
            BuildUtils.logger.debug(f"{container.tag}")
            unused_container.append(container.get_dict())
        with open(unused_containers_json_path, 'w') as fp:
            json.dump(unused_container, fp, indent=4)

        base_images_json_path = join(BuildUtils.build_dir, "build_base_images.json")
        base_images = []
        BuildUtils.logger.debug("")
        BuildUtils.logger.debug("Collect base-images:")
        BuildUtils.logger.debug("")
        for base_image in BuildUtils.base_images_used:
            BuildUtils.logger.debug(f"{base_image.tag}")
            base_images.append(base_image.get_dict())
        with open(base_images_json_path, 'w') as fp:
            json.dump(base_images, fp, indent=4)

        all_containers_json_path = join(BuildUtils.build_dir, "build_containers_all.json")
        BuildUtils.logger.debug("")
        BuildUtils.logger.debug("Collect all containers present:")
        BuildUtils.logger.debug("")
        all_container = []
        for container in BuildUtils.container_images_available:
            BuildUtils.logger.debug(f"{container.tag}")
            all_container.append(container.get_dict())

        with open(all_containers_json_path, 'w') as fp:
            json.dump(all_container, fp, indent=4)

        all_charts_json_path = join(BuildUtils.build_dir, "build_charts_all.json")
        BuildUtils.logger.debug("")
        BuildUtils.logger.debug("Collect all charts present:")
        BuildUtils.logger.debug("")
        all_charts = []
        for chart in BuildUtils.charts_available:
            BuildUtils.logger.debug(f"{chart.chart_id}")
            all_charts.append(chart.get_dict())

        with open(all_charts_json_path, 'w') as fp:
            json.dump(all_charts, fp, indent=4)

        unused_charts_json_path = join(BuildUtils.build_dir, "build_charts_unused.json")
        BuildUtils.logger.debug("")
        BuildUtils.logger.debug("Collect all charts present:")
        BuildUtils.logger.debug("")
        unused_charts = []
        for chart_id, chart in BuildUtils.charts_unused.items():
            BuildUtils.logger.debug(f"{chart.chart_id}")
            unused_charts.append(chart.get_dict())

        with open(unused_charts_json_path, 'w') as fp:
            json.dump(unused_charts, fp, indent=4)


if __name__ == '__main__':
    print("Please use the 'start_build.py' script to launch the build-process.")
    exit(1)
